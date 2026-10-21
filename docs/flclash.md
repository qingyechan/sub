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

两种地址均受所在网络影响，不能保证直连。CDN 可能有缓存，更新可能晚于 GitHub。
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

当前生成规则为 MATCH,PROXIES，即所有匹配流量交给 PROXIES。它尚未包含国内外分流规则。

FlClash 官方项目：https://github.com/chen08209/FlClash
