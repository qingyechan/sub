# FlClash 使用与导入排查

本项目给 FlClash 提供完整的 Clash/Mihomo YAML 配置。源码 ZIP、v2ray.txt 和 singbox.json 不用于此导入步骤。

## 安卓导入

1. 在 FlClash 的配置页面点击添加，通过 URL 导入以下一个地址。
2. 选中配置，在代理页面运行延迟测试，选择 PROXIES 中的 AUTO 或一个可用节点。
3. 启动连接，并按安卓提示允许 VPN。

GitHub 原始订阅：

```text
https://raw.githubusercontent.com/qingyechan/sub/main/output/clash.yaml
```

CDN 备用订阅：

```text
https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/clash.yaml
```

两种地址均受所在网络影响，不能保证直连。发布后工作流会请求刷新主要订阅的 CDN 缓存；CDN 刷新失败或尚未传播时，内容仍可能晚于 GitHub。如果仍看到旧节点数量，可以临时用 Raw 链接或下载最新 YAML 文件导入。
如果 Fork 到自己的仓库，请将地址中的 qingyechan/sub 换成自己的仓库名。

## 添加配置时出现“未知网络错误”

该提示本身不能确定原因，也不能据此认定节点全部失效。按下面步骤区分下载和解析问题：

1. 在同一台手机的浏览器里打开订阅地址。应显示或下载 YAML 文本，不能使用 GitHub 的 blob 网页地址。
2. 如果打不开，切换 Wi-Fi / 移动数据，或尝试上面的另一个订阅入口。
3. 如果能下载，将文件保存为 clash.yaml，在 FlClash 选择本地文件导入。
4. 本地导入成功而 URL 失败时，优先检查应用的下载路径、网络设置及日志。浏览器和应用可能采用不同的网络设置。
5. 本地导入也失败时，记录 FlClash 版本和具体日志，检查内核兼容或 YAML 内容。

本地文件导入不会自动拉取仓库更新。网络恢复后应换回 URL 订阅。
延迟测试只代表测试目标的连接情况；GitHub Actions 测活成功也不保证手机所在网络能够连接节点。

## 项目更新

合并代码修复后，在 GitHub Actions 手动运行 Update Subscriptions。只有运行成功且新输出提交后，FlClash 才能获取新配置；原来的订阅 URL 不变。

默认在 PROXIES 中选择 AUTO：每 120 秒在手机网络上主动测速；FALLBACK 组可按顺序选择可用节点。单个节点超时仍会显示在列表里，但自动组会根据自己的测试结果选择可用节点。

输出上限 80 个节点、每个出口 IP 最多 2 个、每个地区最多 20 个。服务端要求两个独立 HTTPS 204 目标通过、单次耗时不超过 3000ms、获得真实公网出口 IP，并在发布前复测。使用的 Mihomo 配置与最终导出一致，不能完整转换的传输不再默认为 TCP。

工作流改为每小时运行，GitHub 可能延迟调度。output/status.json 提供最近一次成功发布的时间和测活数量；工作流失败会保留旧输出，不能把旧文件当作刚刚测活的结果。

局域网流量直连，其余流量交给 PROXIES，尚未包含国内外分流规则。

如果首次没有任何代理且两个订阅地址均无法直连，当前仓库无法凭空提供一个可达的下载域名。可在能访问 GitHub 的设备下载 clash.yaml 传到手机；成功的 Actions 运行也提供 subscriptions 文件包。这不是让另一个代理充当日常中转。

FlClash 官方项目：https://github.com/chen08209/FlClash
