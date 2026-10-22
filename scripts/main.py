import os
import re
import sys
import json
import time
import uuid
import ipaddress
import gzip
import hashlib
import tempfile
import base64
import shutil
import socket
import urllib.request
import urllib.parse
import subprocess
import requests
import yaml
import maxminddb
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

SOURCE_URLS = [
    "https://wild-cloud-9893.heleimail.workers.dev",
    "https://github.com/Au1rxx/free-vpn-subscriptions/raw/main/output/by-country/v2ray-base64-TW.txt",
    "https://raw.githubusercontent.com/ShatakVPN/ConfigForge-V2Ray/main/configs/all.txt",
    "https://raw.githubusercontent.com/10ium/HiN-VPN/main/subscription/base64/mix",
    "https://raw.githubusercontent.com/10ium/telegram-configs-collector/main/protocols/hysteria",
    "https://raw.githubusercontent.com/10ium/telegram-configs-collector/main/security/tls",
    "https://github.com/Au1rxx/free-vpn-subscriptions/raw/main/output/v2ray-base64.txt",
    "https://raw.githubusercontent.com/freefq/free/master/v2",
    "https://open.heleimail.workers.dev/",
    "https://www.ermao.net/sub/v2ray/ermao.net",
]

OUTPUT_DIR = "output"
COUNTRY_DIR = os.path.join(OUTPUT_DIR, "by-country")
RESIDENTIAL_COUNTRY_DIR = os.path.join(OUTPUT_DIR, "residential-by-country")
MIHOMO_BIN = os.environ.get("MIHOMO_BIN", os.path.abspath("mihomo"))
PROBE_URLS = ("https://www.gstatic.com/generate_204", "https://cp.cloudflare.com/generate_204")
MAX_DELAY_MS = 6500
MAX_NODES = 80
MAX_PER_COUNTRY = 20
MAX_PER_EXIT = 2

def ensure_directories():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(COUNTRY_DIR, exist_ok=True)
    os.makedirs(RESIDENTIAL_COUNTRY_DIR, exist_ok=True)

# Cloudflare 官方全部 Anycast 网段（严禁进入家宽专区）
CLOUDFLARE_IP_NETWORKS = [
    ipaddress.ip_network("173.245.48.0/20"),
    ipaddress.ip_network("103.21.244.0/22"),
    ipaddress.ip_network("103.22.200.0/22"),
    ipaddress.ip_network("103.31.4.0/22"),
    ipaddress.ip_network("141.101.64.0/18"),
    ipaddress.ip_network("108.162.192.0/18"),
    ipaddress.ip_network("190.93.240.0/20"),
    ipaddress.ip_network("188.114.96.0/20"),
    ipaddress.ip_network("197.234.240.0/22"),
    ipaddress.ip_network("198.41.128.0/17"),
    ipaddress.ip_network("162.158.0.0/15"),
    ipaddress.ip_network("104.16.0.0/13"),
    ipaddress.ip_network("104.24.0.0/14"),
    ipaddress.ip_network("172.64.0.0/13"),
    ipaddress.ip_network("131.0.72.0/22"),
    ipaddress.ip_network("2400:cb00::/32"),
    ipaddress.ip_network("2606:4700::/32"),
    ipaddress.ip_network("2803:f800::/32"),
    ipaddress.ip_network("2405:b500::/32"),
    ipaddress.ip_network("2405:8100::/32"),
    ipaddress.ip_network("2a06:98c0::/29"),
    ipaddress.ip_network("2c0f:f248::/32"),
]

def is_cloudflare_cdn_ip(ip_str):
    try:
        ip_obj = ipaddress.ip_address(ip_str)
        for net in CLOUDFLARE_IP_NETWORKS:
            if ip_obj in net:
                return True
    except Exception:
        pass
    return False

# 常见机房与数据中心 ASN
DATACENTER_ASNS = {
    13335, 16509, 14618, 15169, 396982, 8075, 24940, 16276, 
    14061, 31898, 63949, 45102, 132203, 20473, 60068, 55081,
    197540, 51167, 8560, 42708, 201814, 49981, 212238, 46652,
    141995, 200019, 136907, 39351, 9009, 174, 3356, 1299, 2914,
    199180, 202051, 62240, 49304, 34665, 209242, 219337, 44477,
    200651, 202685, 210644, 205628, 51852, 204544, 397373
}

# 严格机房关键词
IDC_KEYWORDS = [
    "hosting", "datacenter", "data center", "cloud", "server", "vps",
    "dedicated", "compute", "colo", "digitalocean", "linode", "ovh",
    "hetzner", "choopa", "vultr", "alibaba", "tencent", "amazon", "aws",
    "google", "microsoft", "oracle", "fastly", "cloudflare", "akamai",
    "netgrid", "m247", "leaseweb", "contabo", "cogent", "zenlayer",
    "ucloud", "lagom", "ipvolume", "hostkey", "selectel", "quadranet",
    "buyvm", "play2go", "fzco"
]

# 核心民用宽带 ASN
TRUE_RESIDENTIAL_ASNS = {
    3462, 9924, 17709, 4780, 18049,
    9269, 3491, 4760, 9304, 17816,
    2516, 4713, 9605, 17511, 17676,
    9318, 4766,
    701, 702, 7922, 20115, 2856, 5089, 5607, 3320, 3209
}

RESIDENTIAL_WHITELIST_KEYWORDS = [
    "broadband", "dynamic", "pppoe", "cust", "dial", "user", "home",
    "residential", "ftth", "cable", "dsl", "consumer",
    "chunghwa", "hinet", "cht", "data communication business group",
    "taiwan fixed network", "kbro", "far eastone", "tfn",
    "hkbn", "hong kong broadband", "pccw", "hkt", "hgc", "smartone",
    "so-net", "kddi", "softbank", "ocn", "plala", "sk broadband", "korea telecom",
    "comcast", "charter", "at&t", "verizon", "spectrum", "cox", "vodafone",
    "deutsche telekom", "telekom", "orange", "bt-central", "virgin media"
]

COUNTRY_NAMES = {
    "HK": "中国香港 (Hong Kong)",
    "TW": "中国台湾 (Taiwan)",
    "JP": "日本 (Japan)",
    "SG": "新加坡 (Singapore)",
    "US": "美国 (United States)",
    "KR": "韩国 (South Korea)",
    "DE": "德国 (Germany)",
    "GB": "英国 (United Kingdom)",
    "CA": "加拿大 (Canada)",
    "FR": "法国 (France)",
    "NL": "荷兰 (Netherlands)",
    "RU": "俄罗斯 (Russia)",
    "IN": "印度 (India)",
    "AU": "澳大利亚 (Australia)",
    "IT": "意大利 (Italy)",
    "ES": "西班牙 (Spain)",
    "TR": "土耳其 (Turkey)",
    "AE": "阿联酋 (UAE)",
    "OTHER": "其他地区 (Other)",
}

VALID_SS_CIPHERS = {
    "aes-128-gcm", "aes-192-gcm", "aes-256-gcm",
    "chacha20-ietf-poly1305", "xchacha20-ietf-poly1305",
    "2022-blake3-aes-128-gcm", "2022-blake3-aes-256-gcm",
    "2022-blake3-chacha20-poly1305", "aes-128-ctr", "aes-192-ctr",
    "aes-256-ctr", "aes-128-cfb", "aes-192-cfb", "aes-256-cfb", "rc4-md5"
}

def get_country_flag(country_code):
    if not country_code or country_code.upper() in ["OTHER", "ZZ", "XX", "T1"]:
        return "🌐"
    try:
        cc = country_code.upper()
        if len(cc) == 2 and cc.isalpha():
            return chr(ord(cc[0]) + 127397) + chr(ord(cc[1]) + 127397)
    except Exception:
        pass
    return "🌐"

def safe_download(url, dest_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Accept': '*/*'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response, open(dest_path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

def setup_environment():
    print("[*] 正在准备离线数据库与 Mihomo 内核...")
    if not os.path.exists("Country.mmdb"):
        safe_download("https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-Country.mmdb", "Country.mmdb")
    if not os.path.exists("ASN.mmdb"):
        safe_download("https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb", "ASN.mmdb")
    
    if not os.path.exists(MIHOMO_BIN):
        if sys.platform != "linux":
            raise RuntimeError("Set MIHOMO_BIN to a local Mihomo executable, or run on GitHub Actions Ubuntu")
        archive = "mihomo.gz"
        safe_download("https://github.com/MetaCubeX/mihomo/releases/download/v1.19.32/mihomo-linux-amd64-compatible-v1.19.32.gz", archive)
        with open(archive, "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        if digest != "ba3ce607747a07f948fc35780e108a4a7c7f552a38b9bd4d115f313ebcb89c20":
            raise RuntimeError("Mihomo download checksum mismatch")
        with gzip.open(archive, "rb") as source, open(MIHOMO_BIN, "wb") as target:
            shutil.copyfileobj(source, target)
        os.chmod(MIHOMO_BIN, 0o755)
        os.remove(archive)

def extract_nodes_from_text(text):
    results = set()
    if not text:
        return results
    current = text.strip()
    for _ in range(3):
        try:
            padded = current + '=' * (-len(current) % 4)
            decoded = base64.b64decode(padded, altchars=b'-_', validate=True).decode('utf-8')
            text += "\n" + decoded
            current = decoded.strip()
        except Exception:
            break

    pattern = r'((?:vmess|vless|ss|trojan|hysteria2|hy2)://[^\s"\'<>]+)'
    for m in re.findall(pattern, text):
        clean = m.strip().rstrip(".,;\"')")
        results.add(clean)
    return results

def fetch_raw_nodes():
    nodes = set()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    print("[*] 正在抓取全部可用节点池...")
    for url in SOURCE_URLS:
        try:
            resp = requests.get(url, headers=headers, timeout=25)
            if resp.status_code == 200:
                extracted = extract_nodes_from_text(resp.text)
                nodes.update(extracted)
                print(f"[+] 抓取成功: {url} -> 获得 {len(extracted)} 个节点")
            else:
                print(f"[!] 响应异常 {url} -> HTTP {resp.status_code}")
        except Exception as e:
            print(f"[!] 拉取失败 {url}: {e}")
    print(f"[*] 初始抓取总量: {len(nodes)} 个")
    return sorted(nodes)

def parse_node_to_xray_outbound(node_str):
    try:
        if node_str.startswith("vless://"):
            parsed = urllib.parse.urlsplit(node_str)
            uuid_str, server, port = urllib.parse.unquote(parsed.username or ""), parsed.hostname, parsed.port
            if not uuid_str or not server or not port or not 1 <= port <= 65535:
                return None, None, None, "vless"
            params = dict(urllib.parse.parse_qsl(parsed.query, keep_blank_values=True))

            outbound = {
                "protocol": "vless",
                "settings": {
                    "vnext": [{
                        "address": server,
                        "port": port,
                        "users": [{"id": uuid_str, "encryption": params.get("encryption", "none")}]
                    }]
                },
                "streamSettings": {
                    "network": params.get("type", "tcp"),
                    "security": params.get("security", "none")
                }
            }
            if params.get("flow"):
                outbound["settings"]["vnext"][0]["users"][0]["flow"] = params["flow"]
            if params.get("security") == "reality":
                pbk = params.get("pbk", "")
                if not pbk:
                    return None, None, None, "vless"
                outbound["streamSettings"]["realitySettings"] = {
                    "serverName": params.get("sni", server),
                    "publicKey": pbk,
                    "shortId": params.get("sid", ""),
                    "fingerprint": params.get("fp", "chrome")
                }
            elif params.get("security") == "tls":
                outbound["streamSettings"]["tlsSettings"] = {
                    "serverName": params.get("sni", server),
                    "allowInsecure": True
                }
            if params.get("type") == "ws":
                outbound["streamSettings"]["wsSettings"] = {
                    "path": params.get("path", "/"),
                    "headers": {"Host": params.get("host", server)}
                }
            return outbound, server, port, "vless"

        elif node_str.startswith("vmess://"):
            b64 = node_str[8:]
            b64 += '=' * (-len(b64) % 4)
            data = json.loads(base64.b64decode(b64).decode('utf-8', errors='ignore'))
            server = str(data.get("add", "")).strip()
            port = int(data.get("port", 0))
            uuid_str = str(data.get("id", "")).strip()
            if not server or port <= 0:
                return None, None, None, "vmess"
            
            is_tls = data.get("tls") in ["tls", "1"]
            outbound = {
                "protocol": "vmess",
                "settings": {
                    "vnext": [{
                        "address": server,
                        "port": port,
                        "users": [{"id": uuid_str, "alterId": int(data.get("aid", 0)), "security": "auto"}]
                    }]
                },
                "streamSettings": {
                    "network": data.get("net", "tcp"),
                    "security": "tls" if is_tls else "none"
                }
            }
            if is_tls:
                outbound["streamSettings"]["tlsSettings"] = {
                    "serverName": str(data.get("host", server)).strip(),
                    "allowInsecure": True
                }
            if data.get("net") == "ws":
                outbound["streamSettings"]["wsSettings"] = {
                    "path": data.get("path", "/"),
                    "headers": {"Host": str(data.get("host", server)).strip()}
                }
            return outbound, server, port, "vmess"

        elif node_str.startswith("trojan://"):
            parsed = urllib.parse.urlsplit(node_str)
            password, server, port = urllib.parse.unquote(parsed.username or ""), parsed.hostname, parsed.port
            if not password or not server or not port or not 1 <= port <= 65535:
                return None, None, None, "trojan"
            params = dict(urllib.parse.parse_qsl(parsed.query, keep_blank_values=True))
            
            outbound = {
                "protocol": "trojan",
                "settings": {
                    "servers": [{"address": server, "port": port, "password": password}]
                },
                "streamSettings": {
                    "network": params.get("type", "tcp"),
                    "security": "tls",
                    "tlsSettings": {"serverName": params.get("sni", server), "allowInsecure": True}
                }
            }
            if params.get("type") == "ws":
                outbound["streamSettings"]["wsSettings"] = {
                    "path": params.get("path", "/"),
                    "headers": {"Host": params.get("host", server)}
                }
            return outbound, server, port, "trojan"

        elif node_str.startswith("ss://"):
            raw = node_str[5:].split("#")[0].strip()
            server, port, password, cipher = "", 0, "", ""
            
            if "@" in raw:
                user_info, host_info = raw.split("@", 1)
                user_info += '=' * (-len(user_info) % 4)
                try:
                    dec = base64.b64decode(user_info).decode('utf-8', errors='ignore')
                    if ":" in dec:
                        cipher, password = dec.split(":", 1)
                except Exception:
                    pass
                if ":" in host_info:
                    server, port_s = host_info.split("/")[0].split("?")[0].split(":", 1)
                    port = int(port_s)
            else:
                padded = raw + '=' * (-len(raw) % 4)
                try:
                    dec = base64.b64decode(padded).decode('utf-8', errors='ignore')
                    if "@" in dec:
                        u_info, h_info = dec.split("@", 1)
                        if ":" in u_info:
                            cipher, password = u_info.split(":", 1)
                        if ":" in h_info:
                            server, port_s = h_info.split("/")[0].split("?")[0].split(":", 1)
                            port = int(port_s)
                except Exception:
                    pass

            if server and port > 0:
                outbound = {
                    "protocol": "shadowsocks",
                    "settings": {
                        "servers": [{"address": server, "port": port, "method": cipher or "chacha20-ietf-poly1305", "password": password}]
                    }
                }
                return outbound, server, port, "ss"

        elif node_str.startswith("hy2://") or node_str.startswith("hysteria2://"):
            prefix = "hy2://" if node_str.startswith("hy2://") else "hysteria2://"
            raw = node_str[len(prefix):].split("#")[0]
            m = re.search(r"([^@]+)@([^:/?#]+):(\d+)", raw)
            if m:
                auth, server, port_s = m.groups()
                port = int(port_s)
                outbound = {
                    "protocol": "hysteria2",
                    "settings": {
                        "servers": [{"address": server, "port": port, "password": auth}]
                    }
                }
                return outbound, server, port, "hysteria2"
    except Exception:
        pass
    return None, None, None, "unknown"

def convert_to_clash_dict(node_str, name):
    try:
        outbound, server, port, proto = parse_node_to_xray_outbound(node_str)
        if not outbound:
            return None
        # Do not silently turn unsupported gRPC/HTTP/2/plugin links into TCP nodes.
        if outbound.get("streamSettings", {}).get("network", "tcp") not in {"tcp", "ws"}:
            return None
        if proto == "ss" and urllib.parse.parse_qs(urllib.parse.urlsplit(node_str).query).get("plugin"):
            return None
        if proto == "vless":
            user = outbound["settings"]["vnext"][0]["users"][0]
            stream = outbound["streamSettings"]
            proxy = {
                "name": name,
                "type": "vless",
                "server": server,
                "port": port,
                "uuid": user["id"],
                "udp": True,
                "tls": stream.get("security") in ["tls", "reality"],
                "skip-cert-verify": True
            }
            if stream.get("security") == "reality":
                r_set = stream.get("realitySettings", {})
                proxy["reality-opts"] = {"public-key": r_set.get("publicKey", ""), "short-id": r_set.get("shortId", "")}
                proxy["servername"] = r_set.get("serverName", server)
                proxy["client-fingerprint"] = r_set.get("fingerprint", "chrome")
            elif stream.get("security") == "tls":
                proxy["servername"] = stream.get("tlsSettings", {}).get("serverName", server)
            if user.get("flow"):
                proxy["flow"] = user["flow"]
            if stream.get("network") == "ws":
                proxy["network"] = "ws"
                proxy["ws-opts"] = stream.get("wsSettings", {})
            return proxy
        elif proto == "vmess":
            user = outbound["settings"]["vnext"][0]["users"][0]
            stream = outbound["streamSettings"]
            proxy = {
                "name": name,
                "type": "vmess",
                "server": server,
                "port": port,
                "uuid": user["id"],
                "alterId": user.get("alterId", 0),
                "cipher": "auto",
                "udp": True,
                "tls": stream.get("security") == "tls",
                "skip-cert-verify": True
            }
            if stream.get("security") == "tls":
                proxy["servername"] = stream.get("tlsSettings", {}).get("serverName", server)
            if stream.get("network") == "ws":
                proxy["network"] = "ws"
                proxy["ws-opts"] = stream.get("wsSettings", {})
            return proxy
        elif proto == "trojan":
            srv = outbound["settings"]["servers"][0]
            stream = outbound["streamSettings"]
            proxy = {
                "name": name,
                "type": "trojan",
                "server": server,
                "port": port,
                "password": srv["password"],
                "udp": True,
                "sni": stream.get("tlsSettings", {}).get("serverName", server),
                "skip-cert-verify": True
            }
            if stream.get("network") == "ws":
                proxy["network"] = "ws"
                proxy["ws-opts"] = stream.get("wsSettings", {})
            return proxy
        elif proto == "ss":
            srv = outbound["settings"]["servers"][0]
            return {
                "name": name,
                "type": "ss",
                "server": server,
                "port": port,
                "cipher": srv["method"],
                "password": srv["password"],
                "udp": True
            }
        elif proto == "hysteria2":
            srv = outbound["settings"]["servers"][0]
            return {
                "name": name,
                "type": "hysteria2",
                "server": server,
                "port": port,
                "password": srv["password"],
                "udp": True,
                "skip-cert-verify": True
            }
    except Exception:
        pass
    return None

def probe_https(session):
    """Require two independent HTTPS 204 responses; redirects/pages are failures."""
    delays = []
    for url in PROBE_URLS:
        started = time.monotonic()
        with session.get(url, timeout=(6, 6), allow_redirects=False, stream=True) as response:
            if response.status_code != 204 or response.content:
                return None
        delay = int((time.monotonic() - started) * 1000)
        if delay > MAX_DELAY_MS:
            return None
        delays.append(delay)
    return max(delays)


def test_single_node_mihomo(node_tuple):
    raw_node, server, port, proto = node_tuple
    proxy = convert_to_clash_dict(raw_node, "probe")
    if not proxy or proto == "hysteria2":
        return None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(("127.0.0.1", 0))
        local_port = listener.getsockname()[1]
    with tempfile.TemporaryDirectory(prefix="sub-probe-") as directory:
        cfg_path = os.path.join(directory, "config.json")
        # The very same converted proxy is measured and later exported to FlClash.
        config = {"mixed-port": local_port, "bind-address": "127.0.0.1", "allow-lan": False,
                  "log-level": "silent", "mode": "rule", "proxies": [proxy], "rules": ["MATCH,probe"]}
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False)
        proc = None
        try:
            proc = subprocess.Popen([MIHOMO_BIN, "-d", directory, "-f", cfg_path],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            deadline = time.monotonic() + 5
            while True:
                if proc.poll() is not None:
                    return None
                try:
                    with socket.create_connection(("127.0.0.1", local_port), timeout=0.1):
                        break
                except OSError:
                    if time.monotonic() >= deadline:
                        return None
                    time.sleep(0.05)
            with requests.Session() as session:
                # Prevent CI/local environment proxy variables from bypassing the node.
                session.trust_env = False
                endpoint = f"http://127.0.0.1:{local_port}"
                session.proxies = {"http": endpoint, "https": endpoint}
                delay = probe_https(session)
                if delay is None:
                    return None
                for url in ("https://api.ipify.org?format=json", "https://ip.seeip.org/json"):
                    try:
                        with session.get(url, timeout=(3, 3), allow_redirects=False) as response:
                            response.raise_for_status()
                            exit_ip = ipaddress.ip_address(response.json()["ip"])
                            if exit_ip.is_global:
                                return (raw_node, server, port, proto, str(exit_ip), delay, True)
                    except (requests.RequestException, ValueError, KeyError, TypeError):
                        continue
                # Never guess the exit IP from the ingress server after a failed IP check.
                return None
        except (OSError, requests.RequestException, ValueError):
            return None
        finally:
            if proc is not None:
                if proc.poll() is None:
                    proc.kill()
                proc.wait()


def run_real_delay_test_mihomo(candidates):
    print(f"[*] Mihomo multi-target HTTPS probe: {len(candidates)} candidates")
    alive = []
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = [executor.submit(test_single_node_mihomo, item) for item in candidates]
        for future in as_completed(futures):
            result = future.result()
            if result:
                alive.append(result)
    print(f"[+] Passed probe: {len(alive)}")
    return alive


def select_quality_nodes(nodes):
    """Keep latency-ranked, diverse exits instead of publishing thousands of aliases."""
    selected, seen_configs, exit_counts, country_counts = [], set(), {}, {}
    for item in sorted(nodes, key=lambda n: (n["delay"], n["link"])):
        if item["delay"] > MAX_DELAY_MS:
            continue
        proxy = dict(item["clash_proxy"])
        proxy.pop("name", None)
        key = json.dumps(proxy, sort_keys=True, ensure_ascii=False)
        ip, cc = item["exit_ip"], item["country"]
        if key in seen_configs or exit_counts.get(ip, 0) >= MAX_PER_EXIT or country_counts.get(cc, 0) >= MAX_PER_COUNTRY:
            continue
        seen_configs.add(key)
        exit_counts[ip] = exit_counts.get(ip, 0) + 1
        country_counts[cc] = country_counts.get(cc, 0) + 1
        selected.append(item)
        if len(selected) >= MAX_NODES:
            break
    return selected


def rename_node_link(raw_link, new_name):
    try:
        if raw_link.startswith("vmess://"):
            b64 = raw_link[8:]
            b64 += '=' * (-len(b64) % 4)
            data = json.loads(base64.b64decode(b64).decode('utf-8', errors='ignore'))
            data["ps"] = new_name
            new_b64 = base64.b64encode(json.dumps(data, ensure_ascii=False).encode('utf-8')).decode('utf-8')
            return f"vmess://{new_b64}"
        elif any(raw_link.startswith(p) for p in ["vless://", "trojan://", "ss://", "hy2://", "hysteria2://"]):
            base_part = raw_link.split("#")[0].strip()
            return f"{base_part}#{urllib.parse.quote(new_name, safe='')}"
    except Exception:
        pass
    return raw_link

def get_rdns_host(ip):
    try:
        host, _, _ = socket.gethostbyaddr(ip)
        return host.lower()
    except Exception:
        return ""

def is_verified_residential_offline(ip, org_str, asn):
    if asn in DATACENTER_ASNS or is_cloudflare_cdn_ip(ip):
        return False
    info = str(org_str).lower()
    for kw in IDC_KEYWORDS:
        if kw in info:
            return False
            
    # ASN only indicates the operator, not whether an individual address is residential.
    return asn in TRUE_RESIDENTIAL_ASNS

def classify_and_filter(alive_nodes):
    country_reader = maxminddb.open_database("Country.mmdb")
    asn_reader = maxminddb.open_database("ASN.mmdb")
    verified = []

    def classify_item(item):
        raw_node, server, port, proto, exit_ip, delay, is_confirmed_exit = item

        country_code = "OTHER"
        try:
            c = country_reader.get(exit_ip)
            if c and "country" in c:
                code = c["country"]["iso_code"]
                if code not in ["T1", "A1", "A2", "OTHER"]:
                    country_code = code.upper()
        except Exception:
            pass

        # 核心拦截：如果未拿到经代理穿透的真实出网 IP，或命中 Cloudflare CDN，一票否决家宽属性
        if not is_confirmed_exit or is_cloudflare_cdn_ip(exit_ip):
            is_residential = False
        else:
            is_residential = False
            try:
                a = asn_reader.get(exit_ip)
                asn = a.get("autonomous_system_number", 0) if a else 0
                org = str(a.get("autonomous_system_organization", "")).lower() if a else ""
                
                if asn not in DATACENTER_ASNS:
                    is_residential = is_verified_residential_offline(exit_ip, org, asn)
            except Exception:
                pass

        c_dict = convert_to_clash_dict(raw_node, "temp")
        if not c_dict:
            return None

        return {
            "link": raw_node,
            "clash_proxy": c_dict,
            "country": str(country_code).upper(),
            "is_residential": is_residential,
            "exit_ip": exit_ip,
            "port": port,
            "proto": proto,
            "delay": delay
        }

    print("[*] 正在解析真实出口国家并鉴定住宅属性...")
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(classify_item, item) for item in alive_nodes]
        for f in as_completed(futures):
            res = f.result()
            if res:
                verified.append(res)

    country_reader.close()
    asn_reader.close()

    # 关键防线：普通池保留不同配置，家宽专区强制单 IP 严格去重（杜绝 40 个重复高危 IP 刷屏）
    unique_all = []
    seen_all = set()
    seen_res_ips = set()

    for item in sorted(verified, key=lambda n: (n["delay"], n["link"])):
        link_core = item["link"].split("#")[0].strip()
        all_key = f"{item['proto']}://{item['exit_ip']}:{item['port']}_{hash(link_core)}"
        if all_key not in seen_all:
            seen_all.add(all_key)
            
            # 若标记为家宽，但该物理出口 IP 已存在，直接降级为普通节点，绝不重复生成
            if item["is_residential"]:
                if item["exit_ip"] in seen_res_ips:
                    item["is_residential"] = False
                else:
                    seen_res_ips.add(item["exit_ip"])
            unique_all.append(item)

    print(f"[*] 智能去重与家宽防刷完成，出库总节点: {len(unique_all)} 个，纯净独立家宽: {len(seen_res_ips)} 个")
    return unique_all

def merge_clash_proxies(current, historical):
    """Preserve historical alternatives without asserting they work on the user's network."""
    merged, seen, used_names = [], set(), set()
    for is_history, proxies in ((False, current), (True, historical)):
        for source in proxies:
            proxy = dict(source)
            identity = json.dumps({k: v for k, v in proxy.items() if k != "name"}, sort_keys=True)
            if identity in seen:
                continue
            seen.add(identity)
            name = str(proxy["name"])
            if is_history and not name.startswith("历史备用 "):
                name = f"历史备用 {len(merged) + 1:04d} | {name}"
            candidate = name
            suffix = 2
            while candidate in used_names:
                candidate = f"{name} ({suffix})"
                suffix += 1
            proxy["name"] = candidate
            used_names.add(candidate)
            merged.append(proxy)
    return merged


def load_historical_proxies():
    path = os.path.join(OUTPUT_DIR, "clash-history.yaml")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)["proxies"]


def export_clash_yaml(clash_proxies, filepath):
    names = [p["name"] for p in clash_proxies]
    history_names = [name for name in names if name.startswith("历史备用 ")]
    config = {
        "port": 7890,
        "socks-port": 7891,
        "allow-lan": False,
        "mode": "rule",
        "log-level": "info",
        "proxies": clash_proxies,
        "proxy-groups": [
            {"name": "PROXIES", "type": "select", "proxies": ["AUTO", "FALLBACK"] + (["HISTORY"] if history_names else []) + names},
            {"name": "AUTO", "type": "url-test", "url": "https://www.google.com/generate_204", "expected-status": 204,
             "interval": 600, "timeout": 8000, "tolerance": 100, "lazy": True, "proxies": names},
            {"name": "FALLBACK", "type": "fallback", "url": PROBE_URLS[1], "expected-status": 204,
             "interval": 600, "timeout": 8000, "lazy": True, "proxies": names}
        ] + ([{"name": "HISTORY", "type": "select", "proxies": history_names}] if history_names else []),
        "rules": ["IP-CIDR,127.0.0.0/8,DIRECT,no-resolve", "IP-CIDR,10.0.0.0/8,DIRECT,no-resolve",
                  "IP-CIDR,172.16.0.0/12,DIRECT,no-resolve", "IP-CIDR,192.168.0.0/16,DIRECT,no-resolve",
                  "IP-CIDR6,::1/128,DIRECT,no-resolve", "IP-CIDR6,fc00::/7,DIRECT,no-resolve", "MATCH,PROXIES"]
    }
    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

def convert_clash_to_singbox(proxy):
    protocol = proxy["type"]
    if protocol not in {"ss", "vmess", "vless", "trojan"}:
        raise ValueError(f"Unsupported sing-box protocol: {protocol}")
    result = {
        "type": "shadowsocks" if protocol == "ss" else protocol,
        "tag": proxy["name"], "server": proxy["server"], "server_port": proxy["port"]
    }
    if protocol == "ss":
        result.update(method=proxy["cipher"], password=proxy["password"])
    elif protocol == "trojan":
        result["password"] = proxy["password"]
    else:
        result["uuid"] = proxy["uuid"]
        if protocol == "vmess":
            result.update(security=proxy.get("cipher", "auto"), alter_id=proxy.get("alterId", 0))
        elif proxy.get("flow"):
            result["flow"] = proxy["flow"]
    if proxy.get("tls") or protocol == "trojan":
        tls = {
            "enabled": True,
            "server_name": proxy.get("servername", proxy.get("sni", proxy["server"])),
            "insecure": proxy.get("skip-cert-verify", False)
        }
        if proxy.get("reality-opts"):
            reality = proxy["reality-opts"]
            tls["reality"] = {"enabled": True, "public_key": reality["public-key"], "short_id": reality.get("short-id", "")}
            tls["utls"] = {"enabled": True, "fingerprint": proxy.get("client-fingerprint", "chrome")}
        result["tls"] = tls
    if proxy.get("network") == "ws":
        ws = proxy.get("ws-opts", {})
        result["transport"] = {"type": "ws", "path": ws.get("path", "/"), "headers": ws.get("headers", {})}
    return result


def export_singbox_json(clash_proxies, filepath):
    node_outbounds = [convert_clash_to_singbox(p) for p in clash_proxies]
    names = [p["name"] for p in clash_proxies]
    outbounds = [
        {"type": "selector", "tag": "select", "outbounds": ["auto"] + names},
        {"type": "urltest", "tag": "auto", "outbounds": names, "url": "https://www.google.com/generate_204"},
        {"type": "direct", "tag": "direct"}
    ] + node_outbounds
    config = {
        "inbounds": [{"type": "mixed", "tag": "mixed-in", "listen": "127.0.0.1", "listen_port": 7890}],
        "outbounds": outbounds,
        "route": {"final": "select"}
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def format_node_group(nodes_list, res_tag_force=False):
    formatted_links = []
    formatted_proxies = []
    
    for idx, item in enumerate(nodes_list, start=1):
        cc = item["country"]
        flag = get_country_flag(cc)
        c_name = COUNTRY_NAMES.get(cc, cc)
        
        is_res = item["is_residential"] or res_tag_force
        tag = " (家宽)" if is_res else ""
        node_name = f"{flag} {c_name} {idx:02d}{tag} - xiaohe"
        
        new_proxy = dict(item["clash_proxy"])
        new_proxy["name"] = node_name
        formatted_proxies.append(new_proxy)
        
        new_link = rename_node_link(item["link"], node_name)
        formatted_links.append(new_link)
        
    return formatted_links, formatted_proxies

def export_subscriptions(verified_nodes):
    if not verified_nodes:
        raise RuntimeError("No verified nodes; preserving existing subscriptions and README")
    ensure_directories()
    residential_nodes = [n for n in verified_nodes if n["is_residential"]]
    non_residential_nodes = [n for n in verified_nodes if not n["is_residential"]]

    # 1. 导出全量总订阅
    all_links, all_proxies = format_node_group(verified_nodes)
    with open(os.path.join(OUTPUT_DIR, "v2ray.txt"), "w", encoding="utf-8") as f:
        f.write(base64.b64encode("\n".join(all_links).encode()).decode())
    export_clash_yaml(all_proxies, os.path.join(OUTPUT_DIR, "clash-tested.yaml"))
    export_clash_yaml(merge_clash_proxies(all_proxies, load_historical_proxies()), os.path.join(OUTPUT_DIR, "clash.yaml"))
    export_singbox_json(all_proxies, os.path.join(OUTPUT_DIR, "singbox.json"))

    # 2. 导出家宽总订阅
    res_links, res_proxies = format_node_group(residential_nodes, res_tag_force=True)
    with open(os.path.join(OUTPUT_DIR, "residential.txt"), "w", encoding="utf-8") as f:
        f.write(base64.b64encode("\n".join(res_links).encode()).decode())
    if res_proxies:
        export_clash_yaml(res_proxies, os.path.join(OUTPUT_DIR, "residential-clash.yaml"))
        export_singbox_json(res_proxies, os.path.join(OUTPUT_DIR, "residential-singbox.json"))
    else:
        for f in ["residential-clash.yaml", "residential-singbox.json"]:
            p = os.path.join(OUTPUT_DIR, f)
            if os.path.exists(p): os.remove(p)

    # 3. 按国家分类【非家宽/机房】
    shutil.rmtree(COUNTRY_DIR, ignore_errors=True)
    os.makedirs(COUNTRY_DIR, exist_ok=True)
    by_cc = {}
    for n in non_residential_nodes:
        by_cc.setdefault(n["country"], []).append(n)

    for cc, n_list in by_cc.items():
        c_links, c_proxies = format_node_group(n_list)
        with open(os.path.join(COUNTRY_DIR, f"{cc}.txt"), "w", encoding="utf-8") as f:
            f.write(base64.b64encode("\n".join(c_links).encode()).decode())
        export_clash_yaml(c_proxies, os.path.join(COUNTRY_DIR, f"clash-{cc}.yaml"))
        export_singbox_json(c_proxies, os.path.join(COUNTRY_DIR, f"singbox-{cc}.json"))

    # 4. 按国家分类【真家宽】
    shutil.rmtree(RESIDENTIAL_COUNTRY_DIR, ignore_errors=True)
    os.makedirs(RESIDENTIAL_COUNTRY_DIR, exist_ok=True)
    res_by_cc = {}
    for n in residential_nodes:
        res_by_cc.setdefault(n["country"], []).append(n)

    for cc, n_list in res_by_cc.items():
        cr_links, cr_proxies = format_node_group(n_list, res_tag_force=True)
        with open(os.path.join(RESIDENTIAL_COUNTRY_DIR, f"{cc}.txt"), "w", encoding="utf-8") as f:
            f.write(base64.b64encode("\n".join(cr_links).encode()).decode())
        export_clash_yaml(cr_proxies, os.path.join(RESIDENTIAL_COUNTRY_DIR, f"clash-{cc}.yaml"))
        export_singbox_json(cr_proxies, os.path.join(RESIDENTIAL_COUNTRY_DIR, f"singbox-{cc}.json"))

    print(f"[*] 导出完毕！全量真活: {len(all_links)} | 家宽真活: {len(res_links)}")
    return len(all_links), len(res_links)

def update_readme():
    repo_name = os.environ.get("GITHUB_REPOSITORY", "qingyechan/sub").strip()
    cache_bust = int(time.time())
    
    def count_file(path):
        if not os.path.exists(path):
            return 0
        try:
            with open(path, "r", encoding="utf-8") as f:
                c = f.read().strip()
                if not c:
                    return 0
                decoded = base64.b64decode(c).decode("utf-8", errors="ignore")
                return len([line for line in decoded.splitlines() if line.strip()])
        except Exception:
            return 0

    total_count = count_file(os.path.join(OUTPUT_DIR, "v2ray.txt"))
    res_count = count_file(os.path.join(OUTPUT_DIR, "residential.txt"))
    clash_count = 0
    full_path = os.path.join(OUTPUT_DIR, "clash.yaml")
    if os.path.exists(full_path):
        with open(full_path, encoding="utf-8") as f:
            clash_count = len(yaml.safe_load(f)["proxies"])

    res_counts = {}
    if os.path.exists(RESIDENTIAL_COUNTRY_DIR):
        for fn in os.listdir(RESIDENTIAL_COUNTRY_DIR):
            if fn.endswith(".txt"):
                cc = fn[:-4]
                cnt = count_file(os.path.join(RESIDENTIAL_COUNTRY_DIR, fn))
                if cnt > 0:
                    res_counts[cc] = cnt

    normal_counts = {}
    if os.path.exists(COUNTRY_DIR):
        for fn in os.listdir(COUNTRY_DIR):
            if fn.endswith(".txt"):
                cc = fn[:-4]
                cnt = count_file(os.path.join(COUNTRY_DIR, fn))
                if cnt > 0:
                    normal_counts[cc] = cnt

    clash_cdn_url = f"https://cdn.jsdelivr.net/gh/{repo_name}@main/output/clash.yaml?v={cache_bust}"
    clash_raw_url = f"https://raw.githubusercontent.com/{repo_name}/main/output/clash.yaml"
    v2_cdn_url = f"https://cdn.jsdelivr.net/gh/{repo_name}@main/output/v2ray.txt?v={cache_bust}"
    v2_raw_url = f"https://raw.githubusercontent.com/{repo_name}/main/output/v2ray.txt"
    sb_cdn_url = f"https://cdn.jsdelivr.net/gh/{repo_name}@main/output/singbox.json?v={cache_bust}"
    sb_raw_url = f"https://raw.githubusercontent.com/{repo_name}/main/output/singbox.json"

    res_rows = []
    for cc in sorted(res_counts.keys(), key=lambda x: res_counts[x], reverse=True):
        flag = get_country_flag(cc)
        name = COUNTRY_NAMES.get(cc, cc)
        cnt = res_counts[cc]
        v2_cdn = f"https://cdn.jsdelivr.net/gh/{repo_name}@main/output/residential-by-country/{cc}.txt?v={cache_bust}"
        v2_raw = f"https://raw.githubusercontent.com/{repo_name}/main/output/residential-by-country/{cc}.txt"
        clash_cdn = f"https://cdn.jsdelivr.net/gh/{repo_name}@main/output/residential-by-country/clash-{cc}.yaml?v={cache_bust}"
        clash_raw = f"https://raw.githubusercontent.com/{repo_name}/main/output/residential-by-country/clash-{cc}.yaml"
        sb_cdn = f"https://cdn.jsdelivr.net/gh/{repo_name}@main/output/residential-by-country/singbox-{cc}.json?v={cache_bust}"
        sb_raw = f"https://raw.githubusercontent.com/{repo_name}/main/output/residential-by-country/singbox-{cc}.json"

        col_v2 = f"[CDN 直链]({v2_cdn}) · [Raw 直链]({v2_raw})"
        col_clash = f"[CDN 直链]({clash_cdn}) · [Raw 直链]({clash_raw})"
        col_sb = f"[CDN 直链]({sb_cdn}) · [Raw 直链]({sb_raw})"
        res_rows.append(f"| {flag} {name} | {cnt} | {col_v2} | {col_clash} | {col_sb} |")
    res_table_str = "\n".join(res_rows) if res_rows else "| 暂无可用家宽节点 | 0 | - | - | - |"

    normal_rows = []
    for cc in sorted(normal_counts.keys(), key=lambda x: normal_counts[x], reverse=True):
        flag = get_country_flag(cc)
        name = COUNTRY_NAMES.get(cc, cc)
        cnt = normal_counts[cc]
        v2_cdn = f"https://cdn.jsdelivr.net/gh/{repo_name}@main/output/by-country/{cc}.txt?v={cache_bust}"
        v2_raw = f"https://raw.githubusercontent.com/{repo_name}/main/output/by-country/{cc}.txt"
        clash_cdn = f"https://cdn.jsdelivr.net/gh/{repo_name}@main/output/by-country/clash-{cc}.yaml?v={cache_bust}"
        clash_raw = f"https://raw.githubusercontent.com/{repo_name}/main/output/by-country/clash-{cc}.yaml"
        sb_cdn = f"https://cdn.jsdelivr.net/gh/{repo_name}@main/output/by-country/singbox-{cc}.json?v={cache_bust}"
        sb_raw = f"https://raw.githubusercontent.com/{repo_name}/main/output/by-country/singbox-{cc}.json"

        col_v2 = f"[CDN 直链]({v2_cdn}) · [Raw 直链]({v2_raw})"
        col_clash = f"[CDN 直链]({clash_cdn}) · [Raw 直链]({clash_raw})"
        col_sb = f"[CDN 直链]({sb_cdn}) · [Raw 直链]({sb_raw})"
        normal_rows.append(f"| {flag} {name} | {cnt} | {col_v2} | {col_clash} | {col_sb} |")
    normal_table_str = "\n".join(normal_rows) if normal_rows else "| 暂无可用节点 | 0 | - | - | - |"

    worker_code = """```javascript
export default {
  async fetch(request) {
    const GITHUB_TOKEN = "ghp_你的GitHub永久访问令牌";
    const OWNER = "hezhanleiok";
    const REPO = "freesub";
    const BRANCH = "main";

    const url = new URL(request.url);
    const filePath = "output" + url.pathname;
    const ghUrl = "[https://raw.githubusercontent.com/](https://raw.githubusercontent.com/)" + OWNER + "/" + REPO + "/" + BRANCH + "/" + filePath;
    
    const res = await fetch(ghUrl, {
      headers: {
        "Authorization": "token " + GITHUB_TOKEN,
        "User-Agent": "Cloudflare-Worker"
      }
    });

    if (!res.ok) {
      return new Response("Not Found", { status: 404 });
    }

    return new Response(await res.text(), {
      headers: { 
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "no-cache" 
      }
    });
  }
}
```"""

    readme_content = f"""# 🚀 免费节点自动测活订阅池 (含真实家宽/住宅IP甄选)

安卓 FlClash 用户请先阅读 [导入方法及“未知网络错误”排查](docs/flclash.md)。代码更新不会自动解决订阅域名在本地网络中的访问问题。

> 👤 **定制规范命名**: 所有订阅节点均重命名为 `国旗 地区 序号 (家宽) - xiaohe`  
> ⚡ **可用性说明**：默认 Clash 完整池包含当前 GitHub 测活配置和历史备用配置；历史节点未重新测活，全部需要在手机网络测试。GitHub 延迟排序不能代表移动网络表现。

---

最近成功生成时间：{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}。默认完整池保留更多候选；最多 {MAX_NODES} 个的精选结果仅作可选配置，不再覆盖完整池。

FlClash：[完整池](https://raw.githubusercontent.com/{repo_name}/main/output/clash.yaml) · [当前 CI 测活池](https://raw.githubusercontent.com/{repo_name}/main/output/clash-tested.yaml) · [历史备用](https://raw.githubusercontent.com/{repo_name}/main/output/clash-history.yaml) · [可选精选池](https://raw.githubusercontent.com/{repo_name}/main/output/clash-fast.yaml)。历史备用不代表目前可用，精选文件可能在无复测结果时缺失。

## 📌 全部节点总订阅链接

| <div style="min-width:180px;">客户端 / 格式类型</div> | <div style="min-width:80px;">节点总数</div> | 备用 CDN 订阅直链 (可达性依网络而定) | 官方原生 Raw 直链 (开启代理) |
| :--- | :---: | :--- | :--- |
| 🚀 **Clash 完整池 (含历史备用)** | `{clash_count}` | [🚀 备用 CDN 直链]({clash_cdn_url}) | [🌐 官方 Raw 直链]({clash_raw_url}) |
| ⚡ **V2RayN (Base64 格式)** | `{total_count}` | [⚡ 备用 CDN 直链]({v2_cdn_url}) | [🌐 官方 Raw 直链]({v2_raw_url}) |
| 📦 **sing-box (JSON 格式)** | `{total_count}` | [📦 备用 CDN 直链]({sb_cdn_url}) | [🌐 官方 Raw 直链]({sb_raw_url}) |

---

## 🏠 按照家宽分类节点订阅 (住宅 IP 专区)
> 根据代理出口 IP、MaxMind ASN 与运营商白名单推断住宅属性，并排除已知机房与 Cloudflare 网段。该分类是启发式结果，无法证明 IP 一定为住宅宽带，也不代表信誉或解锁能力。

| 家宽地区 | 节点数 | V2RayN 专属订阅 | Clash 专属订阅 | sing-box 专属订阅 |
| :--- | :---: | :---: | :---: | :---: |
{res_table_str}

---

## 🗺️ 按照国家分类节点订阅 (非家宽/数据中心节点)

| 地区/国家 | 节点数 | V2RayN 专属订阅 | Clash 专属订阅 | sing-box 专属订阅 |
| :--- | :---: | :---: | :---: | :---: |
{normal_table_str}

---

## 🔒 私有仓库（Private）无感免翻订阅方案 (基于 Cloudflare Workers)

> 如果你希望将本 GitHub 仓库设置为 **Private (私有仓库)** 保护节点资产，外部客户端无法直接拉取原生 Raw 或公共 CDN 链接，可以通过以下 Cloudflare Worker 搭建轻量级私密网关反代：

### 1. 获取 GitHub 永久个人令牌 (PAT)
1. 进入 GitHub -> **Settings** -> **Developer Settings** -> **Personal access tokens (classic)**。
2. 点击 **Generate new token (classic)**，勾选 `repo` 权限，有效期设为 `No expiration`（永不过期）。
3. 复制保存生成的以 `ghp_` 开头的 Token。

### 2. 部署 Cloudflare Worker
登录 Cloudflare Dashboard，创建一个新的 Worker，复制以下脚本粘贴并部署：

{worker_code}

### 3. 私有订阅链接映射方式
部署后 Worker 会分配一个专属域名（例如 `my-sub.yourname.workers.dev`），你的客户端可以直接无感订阅：
* **总 V2RayN 订阅**: `https://你的域名.workers.dev/v2ray.txt`
* **总 Clash 订阅**: `https://你的域名.workers.dev/clash.yaml`
* **总 sing-box 订阅**: `https://你的域名.workers.dev/singbox.json`
* **台湾家宽 V2RayN**: `https://你的域名.workers.dev/residential-by-country/TW.txt`
* **香港家宽 Clash**: `https://你的域名.workers.dev/residential-by-country/clash-HK.yaml`
* **日本家宽 sing-box**: `https://你的域名.workers.dev/residential-by-country/singbox-JP.json`

---

## ⭐ 项目热度

[![Star History Chart](https://api.star-history.com/svg?repos={repo_name}&type=Date)](https://star-history.com/#{repo_name}&Date)

---

## 🛠️ 项目使用说明
1. **自动更新机制**：GitHub Actions 每小时全自动运行并刷新上述全部订阅与数据。
2. **多客户端兼容**：
   - **Clash / Clash Verge / Mihomo Party**：直接复制上方表格中的 **Clash 专属订阅** 链接。
   - **v2rayN / v2rayNG**：直接复制上方表格中的 **V2RayN 专属订阅** 链接。
   - **sing-box**：直接使用上方 **sing-box 专属订阅** 链接。
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"[+] README.md 实时动态表格更新完毕！真实总节点: {total_count}, 真实家宽: {res_count}")

if __name__ == "__main__":
    setup_environment()
    raw_nodes = fetch_raw_nodes()

    candidates = []
    seen_candidates = set()
    for raw in raw_nodes:
        outbound, server, port, proto = parse_node_to_xray_outbound(raw)
        proxy = convert_to_clash_dict(raw, "probe")
        if outbound and server and port and proto != "hysteria2" and proxy:
            key = json.dumps(proxy, sort_keys=True, ensure_ascii=False)
            if key not in seen_candidates:
                seen_candidates.add(key)
                candidates.append((raw, server, port, proto))

    print(f"[*] 格式合规候选节点数: {len(candidates)}")
    alive_nodes = run_real_delay_test_mihomo(candidates)
    verified = classify_and_filter(alive_nodes)
    shortlisted = select_quality_nodes(verified)
    print(f"[*] Rechecking {len(shortlisted)} optional shortlist nodes; preserving the full pool")
    recheck = [(n["link"], n["clash_proxy"]["server"], n["port"], n["proto"]) for n in shortlisted]
    shortlist = select_quality_nodes(classify_and_filter(run_real_delay_test_mihomo(recheck)))
    export_subscriptions(verified)
    shortlist_path = os.path.join(OUTPUT_DIR, "clash-fast.yaml")
    if shortlist:
        export_clash_yaml(format_node_group(shortlist)[1], shortlist_path)
    elif os.path.exists(shortlist_path):
        os.remove(shortlist_path)
    subprocess.run([MIHOMO_BIN, "-t", "-d", tempfile.gettempdir(), "-f", os.path.abspath(os.path.join(OUTPUT_DIR, "clash.yaml"))],
                   check=True, timeout=30)
    with open(os.path.join(OUTPUT_DIR, "status.json"), "w", encoding="utf-8") as f:
        with open(os.path.join(OUTPUT_DIR, "clash.yaml"), encoding="utf-8") as clash_file:
            full_proxies = yaml.safe_load(clash_file)["proxies"]
        json.dump({"generated_at": datetime.now(timezone.utc).isoformat(), "probe_location": "GitHub Actions",
                   "core": "Mihomo v1.19.32", "candidates": len(candidates), "first_pass": len(alive_nodes),
                   "published": len(full_proxies), "ci_tested": len(verified), "optional_shortlist": len(shortlist),
                   "historical_alternatives": sum(p["name"].startswith("历史备用 ") for p in full_proxies),
                   "https_targets": list(PROBE_URLS), "max_delay_ms": MAX_DELAY_MS,
                   "rechecked_before_publish": False, "shortlist_rechecked": True,
                   "local_network_availability_guaranteed": False}, f, indent=2)
    update_readme()
