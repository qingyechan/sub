import base64
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch

SPEC = importlib.util.spec_from_file_location("subscription", Path(__file__).resolve().parents[1] / "scripts/main.py")
app = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(app)


class SubscriptionTests(unittest.TestCase):
    def test_nested_base64_subscription(self):
        link = "trojan://pass@example.com:443#node"
        encoded = link.encode()
        for _ in range(3):
            encoded = base64.b64encode(encoded)
        self.assertEqual(app.extract_nodes_from_text(encoded.decode()), {link})

    def test_missing_core_cleans_temporary_config(self):
        paths = []
        def fail_start(command, **kwargs):
            paths.append(Path(command[2]))
            self.assertTrue(paths[-1].exists())
            raise OSError("missing core")
        with patch.object(app.subprocess, "Popen", side_effect=fail_start):
            result = app.test_single_node_mihomo(("trojan://pass@example.com:443", "example.com", 443, "trojan"))
            self.assertIsNone(result)
        self.assertFalse(paths[0].exists())

    def test_probe_rejects_redirect_or_error_page(self):
        for status in (200, 301, 302, 500):
            session = MagicMock()
            session.get.return_value.__enter__.return_value.status_code = status
            self.assertIsNone(app.probe_https(session))

    def test_probe_requires_both_targets(self):
        session = MagicMock()
        contexts = []
        for status in (204, 500):
            context = MagicMock()
            context.__enter__.return_value.status_code = status
            context.__enter__.return_value.content = b""
            contexts.append(context)
        session.get.side_effect = contexts
        self.assertIsNone(app.probe_https(session))
        self.assertEqual(session.get.call_count, 2)

    def test_probe_accepts_two_empty_204_responses(self):
        session = MagicMock()
        session.get.return_value.__enter__.return_value.status_code = 204
        session.get.return_value.__enter__.return_value.content = b""
        self.assertIsNotNone(app.probe_https(session))
        self.assertEqual(session.get.call_count, 2)

    def test_quality_selection_caps_exit_country_and_duplicates(self):
        def node(i, ip, country, delay):
            return {"link": str(i), "delay": delay, "exit_ip": ip, "country": country,
                    "clash_proxy": {"type": "ss", "server": str(i), "name": str(i)}}
        nodes = [node(i, "1.2.3.4", "US", 100 + i) for i in range(10)]
        nodes += [node(20 + i, f"2.3.4.{i}", "HK", 200 + i) for i in range(30)]
        nodes += [node(100, "8.8.8.8", "TW", app.MAX_DELAY_MS + 1)]
        nodes += [dict(nodes[0], link="alias")]
        chosen = app.select_quality_nodes(nodes)
        self.assertEqual(len([n for n in chosen if n["exit_ip"] == "1.2.3.4"]), app.MAX_PER_EXIT)
        self.assertEqual(len([n for n in chosen if n["country"] == "HK"]), app.MAX_PER_COUNTRY)
        self.assertNotIn("100", [n["link"] for n in chosen])

    def test_unsupported_transport_is_not_silently_exported_as_tcp(self):
        self.assertIsNone(app.convert_to_clash_dict("vless://id@example.com:443?type=grpc", "node"))

    def test_client_groups_actively_probe_and_offer_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.yaml"
            app.export_clash_yaml([{"name": "node", "type": "ss"}], path)
            config = app.yaml.safe_load(path.read_text(encoding="utf-8"))
        groups = {g["name"]: g for g in config["proxy-groups"]}
        self.assertIn("FALLBACK", groups["PROXIES"]["proxies"])
        self.assertFalse(groups["AUTO"]["lazy"])
        self.assertEqual(groups["AUTO"]["expected-status"], 204)

    def test_trojan_password_sni_and_websocket(self):
        proxy = app.convert_to_clash_dict("trojan://a%40b@example.com:443?type=ws&path=%2Ftest%3Fed%3D2048&sni=edge.example#node", "test")
        self.assertEqual(proxy["password"], "a@b")
        self.assertEqual(proxy["sni"], "edge.example")
        self.assertEqual(proxy["ws-opts"]["path"], "/test?ed=2048")

    def test_ipv6_reality_retains_flow_and_short_id(self):
        proxy = app.convert_to_clash_dict("vless://123@[2606:4700::1]:443?security=reality&pbk=key&sid=abcd&flow=xtls-rprx-vision&sni=edge.example", "node")
        self.assertEqual(proxy["server"], "2606:4700::1")
        result = app.convert_clash_to_singbox(proxy)
        self.assertEqual(result["flow"], "xtls-rprx-vision")
        self.assertEqual(result["tls"]["reality"]["short_id"], "abcd")

    def test_singbox_groups_reference_real_outbounds(self):
        vmess = {"add": "example.com", "port": 443, "id": "test", "net": "ws", "path": "/ws", "tls": "tls"}
        links = ["trojan://pass@example.com:443", "vless://id@example.com:443", "vmess://" + base64.b64encode(json.dumps(vmess).encode()).decode(), "ss://" + base64.b64encode(b"aes-128-gcm:pass").decode() + "@example.com:443"]
        proxies = [app.convert_to_clash_dict(link, f"node{i}") for i, link in enumerate(links)]
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "singbox.json"
            app.export_singbox_json(proxies, target)
            config = json.loads(target.read_text(encoding="utf-8"))
        tags = {outbound["tag"] for outbound in config["outbounds"]}
        for outbound in config["outbounds"]:
            self.assertTrue(set(outbound.get("outbounds", [])) <= tags)
        self.assertEqual(len([o for o in config["outbounds"] if "server" in o]), 4)
        self.assertNotIn("version", config)

    def test_empty_result_does_not_touch_existing_files(self):
        with patch.object(app, "ensure_directories") as ensure:
            with self.assertRaises(RuntimeError):
                app.export_subscriptions([])
            ensure.assert_not_called()

    def test_residential_rejects_cloud_and_ipv6_cdn(self):
        self.assertFalse(app.is_verified_residential_offline("1.2.3.4", "cloud hosting", 3462))
        self.assertFalse(app.is_verified_residential_offline("2606:4700::1", "broadband", 3462))
        self.assertFalse(app.is_verified_residential_offline("1.2.3.4", "home user broadband", 123456))

    def test_link_names_are_uri_encoded(self):
        renamed = app.rename_node_link("trojan://pass@example.com:443#old", "中国香港 01")
        self.assertNotIn(" ", renamed)
        self.assertTrue(renamed.endswith("%E4%B8%AD%E5%9B%BD%E9%A6%99%E6%B8%AF%2001"))


if __name__ == "__main__":
    unittest.main()
