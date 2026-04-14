# Douyin.com API 接口文档

> 抓取时间: 2026-04-14  
> 工具: Playwright (Headless Chrome)  
> 总请求量: 373 个  
> 核心 API: 42 个

---

## 目录

- [1. 核心业务 API](#1-核心业务-api)
- [2. 直播相关 API](#2-直播相关-api)
- [3. 登录认证 API](#3-登录认证-api)
- [4. 第三方服务 API](#4-第三方服务-api)
- [5. CDN 资源](#5-cdn-资源)
- [6. 请求参数说明](#6-请求参数说明)
- [7. 技术架构](#7-技术架构)

---

## 1. 核心业务 API

基础域名: `https://www.douyin.com` 和 `https://www-hj.douyin.com`

### 1.1 视频 Feed 流

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/aweme/v2/web/module/feed/` | 获取推荐视频 Feed 流 |

```
POST https://www.douyin.com/aweme/v2/web/module/feed/

参数:
  device_platform: webapp
  aid: 6383
  channel: channel_pc_web
  module_id: 3003101
  count: 20                    # 每次加载数量
  refresh_index: 1             # 刷新索引
  refer_type: 10
  pull_type: 0                 # 0=首次, 2=加载更多
  use_lite_type: 2
  pre_item_ids: <逗号分隔的已看视频ID>

Body (POST):
  encoded_pre_item_ids: <base64编码的已看视频ID>
```

---

### 1.2 视频详情

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/aweme/v1/web/aweme/detail/` | 获取单个视频详情 |
| POST | `/aweme/v1/web/multi/aweme/detail/` | 批量获取视频详情 |

```
GET https://www.douyin.com/aweme/v1/web/aweme/detail/
    ?device_platform=webapp
    &aid=6383
    &channel=channel_pc_web
    &aweme_id=<视频ID>
    &request_source=600
    &origin_type=quick_player
```

---

### 1.3 热搜与搜索

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/aweme/v1/web/hot/search/list/` | 获取热搜榜 |
| GET | `/aweme/v1/web/search/sug/` | 搜索建议/补全 |

```
GET https://www.douyin.com/aweme/v1/web/hot/search/list/
    ?device_platform=webapp
    &aid=6383
    &channel=channel_pc_web
    &detail_list=1
    &source=6
    &main_billboard_count=5

GET https://www-hj.douyin.com/aweme/v1/web/search/sug/
    ?device_platform=webapp
    &aid=6383
    &keyword=<搜索关键词>
    &source=aweme_video_web
```

---

### 1.4 用户相关

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/aweme/v1/web/query/user/` | 查询用户信息 |
| GET | `/aweme/v1/web/get/user/settings` | 获取用户设置 |
| POST | `/aweme/v1/web/set/user/settings` | 设置用户配置 |
| GET | `/aweme/v1/web/get/user/risklevel/` | 获取用户风控等级 |
| GET | `/aweme/v1/web/social/count` | 获取社交数据统计 |

```
GET https://www.douyin.com/aweme/v1/web/query/user/
    ?device_platform=webapp
    &aid=6383
    &publish_video_strategy_type=2

GET https://www.douyin.com/aweme/v1/web/social/count
    ?device_platform=webapp
    &aid=6383
    &source=6
```

---

### 1.5 通知与消息

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/aweme/v1/web/external/notification/` | 获取外部通知 |
| POST | `/aweme/v1/web/im/get/online_feedback/entrance/` | 获取在线反馈入口 |
| POST | `/aweme/v1/web/page/turn/offline` | 页面离线通知 |

```
GET https://www.douyin.com/aweme/v1/web/external/notification/
    ?device_platform=webapp
    &aid=6383
    &channel=channel_pc_web
    &os=2
    &client_type=1
    &scene=admin_pc_push
```

---

### 1.6 频道与资源

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/aweme/v1/web/channel/hotspot` | 获取频道热点 |
| GET | `/aweme/v1/web/solution/resource/list/` | 获取资源列表 |
| GET | `/aweme/v1/web/douyin/select/tab/course/catagory/tag/` | 获取课程分类标签 |

```
GET https://www.douyin.com/aweme/v1/web/channel/hotspot
    ?device_platform=webapp
    &aid=6383

GET https://www.douyin.com/aweme/v1/web/solution/resource/list/
    ?spot_keys=7359502129541449780_douyin_pc_tab
    &app_id=6383

GET https://www.douyin.com/aweme/v1/web/solution/resource/list/
    ?spot_keys=7359502129541449780_douyin_pc_banner
    &app_id=6383
```

---

### 1.7 A/B 测试与配置

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/service/2/abtest_config/` | 获取 A/B 测试配置 |
| POST | `/passport/ticket_guard/get_client_cert/` | 获取客户端证书 |
| POST | `/passport/user_info/get_sec_ts/` | 获取安全时间戳 |
| GET | `/passport/general/login_guiding_strategy/` | 获取登录引导策略 |

---

## 2. 直播相关 API

基础域名: `https://live.douyin.com`

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/webcast/room/info_by_scene/` | 获取直播间信息 |
| GET | `/webcast/setting/` | 获取直播设置 |
| GET | `/webcast/diamond/` | 获取钻石/礼物信息 |

```
GET https://live.douyin.com/webcast/room/info_by_scene/
    ?aid=6383
    &app_name=douyin_web
    &device_platform=web
    &room_id=<直播间ID>
    &scene=aweme_video_feed_pc

GET https://www.douyin.com/webcast/diamond/
    ?type=1
    &aid=1128
    &pc_entrance=1
    &entrance=4
```

---

## 3. 登录认证 API

基础域名: `https://login.douyin.com`

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/passport/web/get_qrcode/` | 获取登录二维码 |
| POST | `/passport/web/check_qrconnect/` | 检查二维码扫码状态 |
| POST | `/passport/web/challenge/` | 验证码挑战 |
| POST | `/ttwid/check/` | 检查 TTWID Token |

```
GET https://login.douyin.com/passport/web/get_qrcode/
    ?aid=6383
    &language=zh
    &is_new_login=1
    &need_logo=false

POST https://login.douyin.com/passport/web/check_qrconnect/
    ?aid=6383
    &token=<二维码token>

POST Body:
  need_logo=false
  is_frontier=true
  token=<token>
  is_new_login=1
  next=https://www.douyin.com
  need_short_url=true
```

---

## 4. 第三方服务 API

| 服务商 | URL | 用途 |
|--------|-----|------|
| 字节跳动监控 | `https://mon.zijieapi.com` | 数据上报 |
| 字节跳动 SDK | `https://mssdk.bytedance.com/web/common` | 设备指纹 |
| 字节跳动 SDK | `https://mssdk.bytedance.com/web/r/token` | Token 获取 |
| 字节跳动 MCS | `https://mcs.zijieapi.com` | 消息通信 |
| 字节跳动 VCS | `https://vcs.zijieapi.com` | 视频通话服务 |
| 字节跳动安全 | `https://security.zijieapi.com` | 安全服务 |
| 字节跳动隐私 | `https://privacy.zijieapi.com` | 隐私服务 |
| FeelGood | `https://api.feelgood.cn` | 用户反馈 |
| 字节跳动 APM | `https://lf3-short.ibytedapm.com` | 性能监控 |
| 字节跳动 TNC | `https://tnc0-aliec2.zijieapi.com/get_domains/v5/` | 域名配置 |

---

## 5. CDN 资源

| 域名 | 用途 |
|------|------|
| `p3-pc-sign.douyinpic.com` | 用户头像、视频封面 (120个请求) |
| `lf3-pendah.bytetos.com` | 静态资源、JS/CSS (77个请求) |
| `p9-pc-sign.douyinpic.com` | 图片资源 (9个请求) |
| `lf-douyin-pc-web.douyinstatic.com` | 前端静态资源 |
| `v26-web.douyinvod.com` | 视频流媒体 |
| `lf3-cdn-tos.bytegoofy.com` | CDN 资源 |
| `fonts.bytedance.com` | 字体文件 |
| `lf-ucenter-web.yhgfb-cn-static.com` | 用户中心资源 |
| `p-pc-weboff.byteimg.com` | 图片资源 |

---

## 6. 请求参数说明

### 6.1 通用参数

所有 API 都包含以下通用参数:

```
device_platform: webapp        # 设备平台
aid: 6383                      # 应用 ID
channel: channel_pc_web        # 渠道
update_version_code: 170400    # 版本号
version_code: 170400
version_name: 17.4.0
cookie_enabled: true
screen_width: 1920
screen_height: 1080
browser_language: zh-CN
browser_platform: Linux x86_64
browser_name: Chrome
browser_version: 120.0.0.0
browser_online: true
engine_name: Blink
engine_version: 120.0.0.0
os_name: Windows
os_version: 10
cpu_core_num: 8
device_memory: 8
platform: PC
downlink: 10
effective_type: 4g
round_trip_time: 0
```

### 6.2 认证参数

```
webid: <设备ID>                # Web 设备标识
uifid: <用户指纹>              # 用户唯一指纹
verifyFp: <验证指纹>           # 验证指纹
fp: <指纹>                     # 指纹
msToken: <Token>               # 消息 Token (动态)
a_bogus: <签名>                # 反爬虫签名 (动态)
```

### 6.3 反爬虫机制

抖音使用多种反爬虫技术:

1. **a_bogus 签名**: 每个请求都需要动态生成的签名参数
2. **msToken**: 消息 Token，需要从服务端获取
3. **verifyFp/fp**: 设备指纹，用于标识浏览器
4. **uifid**: 用户唯一指纹
5. **TNC 域名配置**: 动态域名解析配置

---

## 7. 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                    Douyin.com PC 前端                    │
│                  React + Webpack                         │
├─────────────────────────────────────────────────────────┤
│  www.douyin.com           │  live.douyin.com            │
│  (主站 API)               │  (直播 API)                 │
├─────────────────────────────────────────────────────────┤
│  login.douyin.com         │  www-hj.douyin.com          │
│  (登录认证)               │  (备用 API)                 │
├─────────────────────────────────────────────────────────┤
│  mssdk.bytedance.com      │  mon.zijieapi.com           │
│  (设备指纹 SDK)           │  (数据监控)                 │
├─────────────────────────────────────────────────────────┤
│  CDN: *.douyinpic.com     │  CDN: *.bytetos.com         │
│  (图片资源)               │  (静态资源)                 │
├─────────────────────────────────────────────────────────┤
│  v26-web.douyinvod.com    │  (视频流媒体)               │
└─────────────────────────────────────────────────────────┘
```

### 域名说明

| 域名 | 用途 | 请求量 |
|------|------|--------|
| `www.douyin.com` | 主站 | 77 |
| `www-hj.douyin.com` | 备用/灰度 | 6 |
| `live.douyin.com` | 直播 | 11 |
| `login.douyin.com` | 登录 | 9 |
| `p3-pc-sign.douyinpic.com` | 图片CDN | 120 |
| `lf3-pendah.bytetos.com` | 静态CDN | 77 |
| `mon.zijieapi.com` | 监控 | 9 |
| `mssdk.bytedance.com` | 设备SDK | 9 |

---

## 附录: 完整 API 端点列表

### www.douyin.com
```
GET  /aweme/v1/web/aweme/detail/
POST /aweme/v1/web/multi/aweme/detail/
POST /aweme/v2/web/module/feed/
GET  /aweme/v1/web/hot/search/list/
GET  /aweme/v1/web/search/sug/
GET  /aweme/v1/web/query/user/
GET  /aweme/v1/web/get/user/settings
POST /aweme/v1/web/set/user/settings
GET  /aweme/v1/web/get/user/risklevel/
GET  /aweme/v1/web/social/count
GET  /aweme/v1/web/external/notification/
POST /aweme/v1/web/im/get/online_feedback/entrance/
POST /aweme/v1/web/page/turn/offline
GET  /aweme/v1/web/channel/hotspot
GET  /aweme/v1/web/solution/resource/list/
GET  /aweme/v1/web/douyin/select/tab/course/catagory/tag/
POST /service/2/abtest_config/
POST /passport/ticket_guard/get_client_cert/
POST /passport/user_info/get_sec_ts
GET  /passport/general/login_guiding_strategy/
POST /ttwid/check/
GET  /webcast/diamond/
```

### live.douyin.com
```
GET  /webcast/room/info_by_scene/
GET  /webcast/setting/
```

### login.douyin.com
```
GET  /passport/web/get_qrcode/
POST /passport/web/check_qrconnect/
POST /passport/web/challenge/
POST /ttwid/check/
```

---

*文档由 Playwright 自动抓取生成*
