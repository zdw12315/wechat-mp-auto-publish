# -*- coding: utf-8 -*-
"""
微信公众号自动发布文章 - GitHub Actions 版本
"""

import os
import json
import random
import requests

print("=" * 50)
print("脚本开始执行")
print(f"当前目录: {os.getcwd()}")
print(f"文件列表: {os.listdir('.')}")
print("=" * 50)

# 从环境变量读取配置
APPID = os.environ.get('WECHAT_APPID')
APPSECRET = os.environ.get('WECHAT_APPSECRET')

print(f"APPID: {'已设置' if APPID else '未设置'}")
print(f"APPSECRET: {'已设置' if APPSECRET else '未设置'}")

if not APPID or not APPSECRET:
    print("错误：未设置环境变量")
    exit(1)

# 文章模板库（中老年爱转发类文章）
ARTICLE_TEMPLATES = [
    {
        "title": "人老了，最值钱的东西不是钱，而是这两样！看完恍然大悟",
        "content": """<p>人这一辈子，忙忙碌碌大半生，年轻时拼事业、攒钱、买房，以为这就是人生的全部。</p>
<p>等到头发花白、步履蹒跚的时候才明白：<strong>老了以后，最值钱的从来不是银行卡里的数字，而是两样东西。</strong></p>
<h3>第一样：健康的身体</h3>
<p>有多少人年轻时不注意，熬夜、喝酒、透支身体，等到老了，高血压、糖尿病、心脏病全找上门来。</p>
<p>躺在病床上才懂得，再多的钱，也换不回一副好身板。</p>
<h3>第二样：乐观的心态</h3>
<p>同样的年龄，为什么有的人精神矍铄、笑容满面，有的人却愁眉苦脸、怨天尤人？</p>
<p>区别就在心态。</p>
<p><strong>亲爱的朋友们，人生下半场，比的不是谁更有钱，而是谁更健康、谁更快乐。</strong></p>""",
        "digest": "人老了，健康和心态最值钱。"
    },
    {
        "title": "60岁后，这5个习惯要改掉，否则身体越来越差",
        "content": """<p>人到了60岁，身体开始走下坡路，这时候如果不注意保养，各种疾病就会找上门来。</p>
<p>今天给大家总结<strong>5个一定要改掉的习惯</strong>：</p>
<h3>第一个：久坐不动</h3><p>每坐1小时，起来活动5-10分钟。</p>
<h3>第二个：吃饭太快</h3><p>细嚼慢咽，每口饭咀嚼20-30次。</p>
<h3>第三个：熬夜</h3><p>晚上10点前睡觉，保证7-8小时睡眠。</p>
<h3>第四个：不喝水</h3><p>每天喝水1500-2000毫升。</p>
<h3>第五个：生气</h3><p>学会控制情绪，保持平和心态。</p>
<p><strong>朋友们，健康是最大的财富！</strong></p>""",
        "digest": "60岁后，这5个坏习惯一定要改掉！"
    }
]

def get_access_token():
    """获取微信access_token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}"
    try:
        response = requests.get(url, timeout=30)
        data = response.json()
        token = data.get('access_token')
        if token:
            print(f"获取access_token成功")
            return token
        else:
            print(f"获取access_token失败: {data}")
            return None
    except Exception as e:
        print(f"获取access_token异常: {e}")
        return None

def create_article(access_token, title, content, digest):
    """创建图文草稿"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    article = {
        "articles": [
            {
                "title": title,
                "author": "每日精选",
                "digest": digest,
                "content": content,
                "need_open_comment": 1,
                "only_fans_can_comment": 0
            }
        ]
    }
    try:
        response = requests.post(url, json=article, timeout=30)
        data = response.json()
        media_id = data.get('media_id')
        if media_id:
            print(f"创建草稿成功: {title}")
            return media_id
        else:
            print(f"创建草稿失败: {data}")
            return None
    except Exception as e:
        print(f"创建草稿异常: {e}")
        return None

def publish_article(access_token, media_id):
    """发布文章"""
    url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={access_token}"
    try:
        response = requests.post(url, json={"media_id": media_id}, timeout=30)
        data = response.json()
        if data.get('errcode') == 0:
            print("发布成功！")
            return True
        else:
            print(f"发布失败: {data}")
            return False
    except Exception as e:
        print(f"发布异常: {e}")
        return False

def main():
    """主函数"""
    print("=== 开始执行公众号自动发布 ===")
    
    # 获取access_token
    access_token = get_access_token()
    if not access_token:
        print("错误：无法获取access_token")
        return
    
    # 随机选择一篇文章
    template = random.choice(ARTICLE_TEMPLATES)
    print(f"选择文章: {template['title']}")
    
    # 创建草稿
    media_id = create_article(access_token, template['title'], template['content'], template['digest'])
    if not media_id:
        print("错误：创建草稿失败")
        return
    
    # 发布文章
    success = publish_article(access_token, media_id)
    if success:
        print(f"发布成功: {template['title']}")
    else:
        print(f"发布失败: {template['title']}")

if __name__ == "__main__":
    main()
