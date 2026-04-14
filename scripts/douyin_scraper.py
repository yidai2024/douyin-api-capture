#!/usr/bin/env python3
"""
Douyin.com API 接口抓取脚本
使用 Playwright 拦截网络请求
"""

from playwright.sync_api import sync_playwright
import json
import time
from datetime import datetime
from urllib.parse import urlparse
import re

def capture_douyin_apis():
    """抓取 douyin.com 的所有 API 接口"""
    
    all_apis = []
    seen_urls = set()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-CN'
        )
        
        page = context.new_page()
        
        def handle_request(request):
            url = request.url
            method = request.method
            
            # Skip static assets
            skip_extensions = ['.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg', 
                             '.woff', '.woff2', '.ttf', '.ico', '.webp', '.mp4', '.m3u8']
            if any(url.lower().endswith(ext) for ext in skip_extensions):
                return
            
            # Skip data URLs
            if url.startswith('data:') or url.startswith('blob:'):
                return
            
            # Skip analytics/tracking pixel images
            parsed = urlparse(url)
            if parsed.path.endswith('.gif') or parsed.path.endswith('.png'):
                if any(x in url for x in ['analytics', 'tracking', 'pixel', 'beacon', 'collect']):
                    pass  # Keep these, they're interesting
                else:
                    return
            
            if url not in seen_urls:
                seen_urls.add(url)
                
                api_info = {
                    'url': url,
                    'method': method,
                    'domain': parsed.netloc,
                    'path': parsed.path,
                    'timestamp': datetime.now().isoformat(),
                    'headers': dict(request.headers),
                    'post_data': None
                }
                
                # Capture POST data
                if method in ['POST', 'PUT', 'PATCH']:
                    try:
                        post_data = request.post_data
                        if post_data:
                            api_info['post_data'] = post_data[:2000]  # Limit size
                    except:
                        pass
                
                all_apis.append(api_info)
        
        def handle_response(response):
            url = response.url
            # Update API info with response status
            for api in all_apis:
                if api['url'] == url:
                    api['status_code'] = response.status
                    api['content_type'] = response.headers.get('content-type', '')
                    break
        
        # Attach handlers
        page.on('request', handle_request)
        page.on('response', handle_response)
        
        # Pages to visit
        pages_to_visit = [
            ('https://www.douyin.com/', '首页'),
            ('https://www.douyin.com/discover', '发现页'),
            ('https://www.douyin.com/search', '搜索页'),
            ('https://www.douyin.com/hot', '热点页'),
            ('https://www.douyin.com/channel', '频道页'),
        ]
        
        for url, name in pages_to_visit:
            print(f"\n{'='*60}")
            print(f"正在访问: {name} ({url})")
            print(f"{'='*60}")
            
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=30000)
                time.sleep(3)  # Wait for dynamic content
                
                # Scroll to trigger lazy loading
                for _ in range(3):
                    page.evaluate('window.scrollBy(0, 500)')
                    time.sleep(1)
                
                # Take screenshot
                screenshot_name = f"douyin_{name.replace('/', '_')}.png"
                page.screenshot(path=f"/root/{screenshot_name}")
                print(f"截图已保存: {screenshot_name}")
                
            except Exception as e:
                print(f"访问失败: {e}")
        
        # Try to interact with search
        print(f"\n{'='*60}")
        print("尝试搜索功能")
        print(f"{'='*60}")
        
        try:
            page.goto('https://www.douyin.com/', wait_until='domcontentloaded', timeout=30000)
            time.sleep(2)
            
            # Look for search input
            search_selectors = [
                'input[placeholder*="搜索"]',
                'input[type="search"]',
                '#search-input',
                '.search-input input',
                'input[aria-label*="搜索"]'
            ]
            
            for selector in search_selectors:
                try:
                    search_input = page.locator(selector).first
                    if search_input.is_visible(timeout=2000):
                        search_input.fill('热门')
                        time.sleep(1)
                        search_input.press('Enter')
                        time.sleep(3)
                        page.screenshot(path="/root/douyin_search_result.png")
                        print("搜索完成，截图已保存")
                        break
                except:
                    continue
        except Exception as e:
            print(f"搜索交互失败: {e}")
        
        browser.close()
    
    return all_apis


def analyze_apis(apis):
    """分析抓取到的 API"""
    
    # Categorize by domain
    by_domain = {}
    for api in apis:
        domain = api['domain']
        if domain not in by_domain:
            by_domain[domain] = []
        by_domain[domain].append(api)
    
    # Categorize by type
    douyin_core = []
    third_party = []
    cdn_resources = []
    
    for api in apis:
        domain = api['domain']
        if 'douyin.com' in domain or 'bytedance' in domain or 'byteimg' in domain:
            douyin_core.append(api)
        elif any(x in domain for x in ['baidu', 'google', 'facebook', 'clarity', 'sentry']):
            third_party.append(api)
        else:
            cdn_resources.append(api)
    
    return {
        'by_domain': by_domain,
        'douyin_core': douyin_core,
        'third_party': third_party,
        'cdn_resources': cdn_resources,
        'total': len(apis)
    }


if __name__ == '__main__':
    print("开始抓取 douyin.com API 接口...")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    apis = capture_douyin_apis()
    
    print(f"\n{'='*60}")
    print(f"抓取完成! 共发现 {len(apis)} 个请求")
    print(f"{'='*60}")
    
    # Save raw data
    with open('/root/douyin_raw_apis.json', 'w', encoding='utf-8') as f:
        json.dump(apis, f, ensure_ascii=False, indent=2)
    print(f"原始数据已保存: douyin_raw_apis.json")
    
    # Analyze
    analysis = analyze_apis(apis)
    
    with open('/root/douyin_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2, default=str)
    print(f"分析结果已保存: douyin_analysis.json")
    
    # Print summary
    print(f"\n域名统计:")
    for domain, items in sorted(analysis['by_domain'].items(), key=lambda x: -len(x[1])):
        print(f"  {domain}: {len(items)} 个请求")
    
    print(f"\n分类统计:")
    print(f"  抖音核心 API: {len(analysis['douyin_core'])} 个")
    print(f"  第三方服务: {len(analysis['third_party'])} 个")
    print(f"  CDN 资源: {len(analysis['cdn_resources'])} 个")
