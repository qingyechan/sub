# 🚀 免费节点自动测活订阅池 (含真实家宽/住宅IP甄选)

安卓 FlClash 用户请先阅读 [导入方法及“未知网络错误”排查](docs/flclash.md)。代码更新不会自动解决订阅域名在本地网络中的访问问题。

移动网络实测池（用户反馈可连通，共 39 个，非长期可用或带宽保证）：[Raw 订阅](https://raw.githubusercontent.com/qingyechan/sub/main/output/clash-mobile.yaml) · [备用 CDN](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/clash-mobile.yaml)。原始连接参数及名称固定保留，不受 GitHub 测速排序或完整池编号变化影响。

> 👤 **定制规范命名**: 所有订阅节点均重命名为 `国旗 地区 序号 (家宽) - xiaohe`  
> ⚡ **可用性说明**：默认 Clash 完整池包含当前 GitHub 测活配置和历史备用配置；历史节点未重新测活，全部需要在手机网络测试。GitHub 延迟排序不能代表移动网络表现。

---

最近成功生成时间：2026-10-22 03:40:00 UTC。默认完整池保留更多候选；最多 80 个的精选结果仅作可选配置，不再覆盖完整池。

FlClash：[完整池](https://raw.githubusercontent.com/qingyechan/sub/main/output/clash.yaml) · [当前 CI 测活池](https://raw.githubusercontent.com/qingyechan/sub/main/output/clash-tested.yaml) · [历史备用](https://raw.githubusercontent.com/qingyechan/sub/main/output/clash-history.yaml) · [可选精选池](https://raw.githubusercontent.com/qingyechan/sub/main/output/clash-fast.yaml)。历史备用不代表目前可用，精选文件可能在无复测结果时缺失。

## 📌 全部节点总订阅链接

| <div style="min-width:180px;">客户端 / 格式类型</div> | <div style="min-width:80px;">节点总数</div> | 备用 CDN 订阅直链 (可达性依网络而定) | 官方原生 Raw 直链 (开启代理) |
| :--- | :---: | :--- | :--- |
| 🚀 **Clash 完整池 (含历史备用)** | `1406` | [🚀 备用 CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/clash.yaml?v=1792640398) | [🌐 官方 Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/clash.yaml) |
| ⚡ **V2RayN (Base64 格式)** | `1008` | [⚡ 备用 CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/v2ray.txt?v=1792640398) | [🌐 官方 Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/v2ray.txt) |
| 📦 **sing-box (JSON 格式)** | `1008` | [📦 备用 CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/singbox.json?v=1792640398) | [🌐 官方 Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/singbox.json) |

---

## 🏠 按照家宽分类节点订阅 (住宅 IP 专区)
> 根据代理出口 IP、MaxMind ASN 与运营商白名单推断住宅属性，并排除已知机房与 Cloudflare 网段。该分类是启发式结果，无法证明 IP 一定为住宅宽带，也不代表信誉或解锁能力。

| 家宽地区 | 节点数 | V2RayN 专属订阅 | Clash 专属订阅 | sing-box 专属订阅 |
| :--- | :---: | :---: | :---: | :---: |
| 🇹🇼 中国台湾 (Taiwan) | 3 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/residential-by-country/TW.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/residential-by-country/TW.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/residential-by-country/clash-TW.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/residential-by-country/clash-TW.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/residential-by-country/singbox-TW.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/residential-by-country/singbox-TW.json) |

---

## 🗺️ 按照国家分类节点订阅 (非家宽/数据中心节点)

| 地区/国家 | 节点数 | V2RayN 专属订阅 | Clash 专属订阅 | sing-box 专属订阅 |
| :--- | :---: | :---: | :---: | :---: |
| 🇺🇸 美国 (United States) | 458 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/US.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/US.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-US.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-US.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-US.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-US.json) |
| 🇳🇱 荷兰 (Netherlands) | 163 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/NL.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/NL.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-NL.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-NL.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-NL.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-NL.json) |
| 🇯🇵 日本 (Japan) | 122 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/JP.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/JP.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-JP.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-JP.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-JP.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-JP.json) |
| 🇸🇬 新加坡 (Singapore) | 57 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/SG.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/SG.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-SG.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-SG.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-SG.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-SG.json) |
| 🇩🇪 德国 (Germany) | 43 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/DE.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/DE.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-DE.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-DE.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-DE.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-DE.json) |
| 🇰🇷 韩国 (South Korea) | 22 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/KR.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/KR.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-KR.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-KR.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-KR.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-KR.json) |
| 🇫🇷 法国 (France) | 21 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/FR.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/FR.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-FR.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-FR.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-FR.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-FR.json) |
| 🇭🇰 中国香港 (Hong Kong) | 15 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/HK.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/HK.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-HK.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-HK.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-HK.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-HK.json) |
| 🇬🇧 英国 (United Kingdom) | 14 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/GB.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/GB.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-GB.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-GB.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-GB.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-GB.json) |
| 🇨🇦 加拿大 (Canada) | 13 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/CA.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/CA.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-CA.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-CA.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-CA.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-CA.json) |
| 🇮🇹 意大利 (Italy) | 13 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/IT.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/IT.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-IT.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-IT.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-IT.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-IT.json) |
| 🇮🇳 印度 (India) | 10 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/IN.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/IN.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-IN.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-IN.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-IN.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-IN.json) |
| 🇵🇱 PL | 9 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/PL.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/PL.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-PL.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-PL.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-PL.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-PL.json) |
| 🇹🇼 中国台湾 (Taiwan) | 5 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/TW.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/TW.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-TW.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-TW.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-TW.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-TW.json) |
| 🇨🇿 CZ | 3 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/CZ.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/CZ.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-CZ.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-CZ.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-CZ.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-CZ.json) |
| 🇸🇪 SE | 3 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/SE.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/SE.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-SE.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-SE.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-SE.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-SE.json) |
| 🇹🇭 TH | 3 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/TH.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/TH.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-TH.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-TH.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-TH.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-TH.json) |
| 🇷🇴 RO | 3 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/RO.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/RO.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-RO.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-RO.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-RO.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-RO.json) |
| 🇨🇾 CY | 3 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/CY.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/CY.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-CY.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-CY.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-CY.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-CY.json) |
| 🇨🇭 CH | 3 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/CH.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/CH.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-CH.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-CH.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-CH.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-CH.json) |
| 🇦🇺 澳大利亚 (Australia) | 3 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/AU.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/AU.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-AU.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-AU.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-AU.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-AU.json) |
| 🇮🇱 IL | 3 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/IL.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/IL.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-IL.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-IL.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-IL.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-IL.json) |
| 🇦🇪 阿联酋 (UAE) | 2 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/AE.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/AE.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-AE.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-AE.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-AE.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-AE.json) |
| 🇿🇦 ZA | 2 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/ZA.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/ZA.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-ZA.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-ZA.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-ZA.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-ZA.json) |
| 🇱🇻 LV | 2 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/LV.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/LV.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-LV.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-LV.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-LV.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-LV.json) |
| 🇷🇺 俄罗斯 (Russia) | 2 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/RU.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/RU.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-RU.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-RU.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-RU.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-RU.json) |
| 🇫🇮 FI | 2 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/FI.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/FI.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-FI.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-FI.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-FI.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-FI.json) |
| 🇦🇹 AT | 1 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/AT.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/AT.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-AT.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-AT.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-AT.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-AT.json) |
| 🇮🇶 IQ | 1 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/IQ.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/IQ.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-IQ.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-IQ.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-IQ.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-IQ.json) |
| 🇪🇸 西班牙 (Spain) | 1 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/ES.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/ES.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-ES.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-ES.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-ES.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-ES.json) |
| 🇨🇳 CN | 1 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/CN.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/CN.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-CN.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-CN.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-CN.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-CN.json) |
| 🇪🇪 EE | 1 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/EE.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/EE.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-EE.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-EE.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-EE.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-EE.json) |
| 🇮🇪 IE | 1 | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/IE.txt?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/IE.txt) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/clash-IE.yaml?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/clash-IE.yaml) | [CDN 直链](https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/by-country/singbox-IE.json?v=1792640398) · [Raw 直链](https://raw.githubusercontent.com/qingyechan/sub/main/output/by-country/singbox-IE.json) |

---

## 🔒 私有仓库（Private）无感免翻订阅方案 (基于 Cloudflare Workers)

> 如果你希望将本 GitHub 仓库设置为 **Private (私有仓库)** 保护节点资产，外部客户端无法直接拉取原生 Raw 或公共 CDN 链接，可以通过以下 Cloudflare Worker 搭建轻量级私密网关反代：

### 1. 获取 GitHub 永久个人令牌 (PAT)
1. 进入 GitHub -> **Settings** -> **Developer Settings** -> **Personal access tokens (classic)**。
2. 点击 **Generate new token (classic)**，勾选 `repo` 权限，有效期设为 `No expiration`（永不过期）。
3. 复制保存生成的以 `ghp_` 开头的 Token。

### 2. 部署 Cloudflare Worker
登录 Cloudflare Dashboard，创建一个新的 Worker，复制以下脚本粘贴并部署：

```javascript
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
```

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

[![Star History Chart](https://api.star-history.com/svg?repos=qingyechan/sub&type=Date)](https://star-history.com/#qingyechan/sub&Date)

---

## 🛠️ 项目使用说明
1. **自动更新机制**：GitHub Actions 每小时全自动运行并刷新上述全部订阅与数据。
2. **多客户端兼容**：
   - **Clash / Clash Verge / Mihomo Party**：直接复制上方表格中的 **Clash 专属订阅** 链接。
   - **v2rayN / v2rayNG**：直接复制上方表格中的 **V2RayN 专属订阅** 链接。
   - **sing-box**：直接使用上方 **sing-box 专属订阅** 链接。
