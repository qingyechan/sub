# FlClash 完整池与历史备用

GitHub 运行器与用户手机的网络不同，不能把运行器上低延迟的少量节点当作移动网络的最佳集合。

## 移动网络实测池

2026-10-22 用户反馈的 39 个可连通节点已按来源提交和国家/编号精确保存到 config/mobile-approved.yaml，生成独立文件 output/clash-mobile.yaml。记录包括美国 18、意大利 9、日本 4、俄罗斯 1、香港 2、英国 1、新加坡 2、澳大利亚 1、德国 1。

日常使用可在 FlClash 添加 `https://raw.githubusercontent.com/qingyechan/sub/main/output/clash-mobile.yaml`，或备用 CDN `https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/clash-mobile.yaml`。选中此配置后在 PROXIES 选择 AUTO，或直接选择原节点名。下载受阻时可用本地文件导入。

这份实测池固定保存原始代理参数及名称，不根据完整池序号再次匹配，不受境外 CI 测速淘汰，不自动加入未经用户反馈的新节点。状态见 output/mobile-status.json。用户反馈仅证明报告时的连通性，不代表下载速度、长期稳定或将来一定可用；失效后需依据新的手机实测结果更新审批文件。完整池和历史备用仍独立保留。

## 订阅

- 默认完整池：`https://raw.githubusercontent.com/qingyechan/sub/main/output/clash.yaml`
- 备用 CDN：`https://cdn.jsdelivr.net/gh/qingyechan/sub@main/output/clash.yaml`
- 历史备用：将上述地址的文件名改为 `clash-history.yaml`。
- 当前 CI 测活池：文件名 `clash-tested.yaml`。
- 可选精选池：文件名 `clash-fast.yaml`；没有通过复测的节点时，该文件可能缺失。

默认完整池合并当前 CI 测活节点和历史备用，只去掉完全重复的代理配置，不按运行器延迟或地区压缩到 80 个。每出口 2 个、每地区 20 个、总数 80 的限制只用于可选精选池。
历史备用由 2026-10-20 至 2026-10-21 修改前的四个快照恢复，带“历史备用”名称，未重新测活，不代表目前可用。来源及去重数量见 output/history-sources.json。
历史文件会在后续更新时保留，CI 失败不再成为删除这些备选项的依据。

## 安卓操作

1. 配置页面添加 URL，或者将下载的 YAML 保存到手机后通过文件导入。
2. 选中完整池配置，在 PROXIES 中进入 HISTORY，即可找到恢复的历史节点；可以搜索“美国”。
3. 测试时选择一个节点实际访问网页，记录名称、测速结果及日志。测速 URL 超时与所有网页都不能访问需要分开判断。
4. AUTO 使用 Google 的 204 目标，FALLBACK 使用 Cloudflare 的 204 目标，便于区分目标站差异。完整池扩大后改为按需测速，间隔 600 秒、超时 8000ms，避免每 120 秒主动测试上千节点。

CDN 可能保留旧缓存或未完成刷新。先确认配置节点数量与仓库 status.json 的 published 字段一致；历史恢复首次为 942 个，后续会变化。静态文件和固定提交链接不会自动更新。

## 下载失败

“未知网络错误”本身不能确定原因。在同一手机浏览器打开 URL，确认下载的是 YAML 文本，而不是 GitHub blob 网页。浏览器和应用可能有不同网络路径。
如果手机不能访问订阅域名，可从能访问 GitHub 的设备下载文件传到手机。代码修改不能保证移动网络直接访问 Raw 或 CDN。
本地文件导入后需要手动更新；域名恢复可用后再改为 URL 订阅。

FlClash 官方项目：https://github.com/chen08209/FlClash
