# -*- coding: utf-8 -*-
"""
微信公众号自动发布文章 - GitHub Actions 版本
每天自动发布中老年爱转发类文章
"""

import os
import json
import random
import requests

# 从环境变量读取配置
APPID = os.environ.get('WECHAT_APPID')
APPSECRET = os.environ.get('WECHAT_APPSECRET')

# 文章模板库
ARTICLE_TEMPLATES = [
    {
        "title": "人老了，最值钱的东西不是钱，而是这两样！看完恍然大悟",
        "content": """<p>人这一辈子，忙忙碌碌大半生，年轻时拼事业、攒钱、买房，以为这就是人生的全部。</p>
<p>等到头发花白、步履蹒跚的时候才明白：<strong>老了以后，最值钱的从来不是银行卡里的数字，而是两样东西。</strong></p>
<h3>第一样：健康的身体</h3>
<p>有多少人年轻时不注意，熬夜、喝酒、透支身体，等到老了，高血压、糖尿病、心脏病全找上门来。</p>
<p>躺在病床上才懂得，再多的钱，也换不回一副好身板。</p>
<p>每天早上醒来，能自己穿衣服、能出门遛弯、能自己吃饭——这就是最大的福气。</p>
<h3>第二样：乐观的心态</h3>
<p>同样的年龄，为什么有的人精神矍铄、笑容满面，有的人却愁眉苦脸、怨天尤人？</p>
<p>区别就在心态。</p>
<p>人老了，该放下的要放下，该释怀的要释怀。子女的事少操心，钱够花就行，最重要的是<strong>自己开心</strong>。</p>
<p><strong>亲爱的朋友们，人生下半场，比的不是谁更有钱，而是谁更健康、谁更快乐。</strong></p>
<p><strong>愿每一位朋友都能健康长寿，开心每一天！</strong></p>""",
        "digest": "人老了，健康和心态最值钱。看完这篇文章，你会明白什么才是真正的财富。"
    },
    {
        "title": "60岁后，这5个习惯要改掉，否则身体越来越差",
        "content": """<p>人到了60岁，身体开始走下坡路，这时候如果不注意保养，各种疾病就会找上门来。</p>
<p>今天给大家总结<strong>5个一定要改掉的习惯</strong>：</p>
<h3>第一个：久坐不动</h3>
<p>久坐会导致血液循环不畅，容易形成血栓。<strong>建议：</strong>每坐1小时，起来活动5-10分钟。</p>
<h3>第二个：吃饭太快</h3>
<p>吃得太快会增加肠胃负担。<strong>建议：</strong>细嚼慢咽，每口饭咀嚼20-30次。</p>
<h3>第三个：熬夜</h3>
<p>熬夜会扰乱生物钟，降低免疫力。<strong>建议：</strong>晚上10点前睡觉，保证7-8小时睡眠。</p>
<h3>第四个：不喝水</h3>
<p>长期缺水会导致血液黏稠。<strong>建议：</strong>每天喝水1500-2000毫升。</p>
<h3>第五个：生气</h3>
<p>生气是最伤身体的情绪。<strong>建议：</strong>学会控制情绪，保持平和心态。</p>
<p><strong>朋友们，健康是最大的财富，养成好习惯，享受幸福的晚年生活！</strong></p>""",
        "digest": "60岁后，这5个坏习惯一定要改掉！久坐、吃饭快、熬夜、不喝水、生气，你中了几个？"
    },
    {
        "title": "人这一生，最珍贵的不是金钱，而是这三样东西",
        "content": """<p>人这一生，忙忙碌碌，追求的东西很多。</p>
<p>有人追求金钱，有人追求名利，有人追求地位。</p>
<p>但到了最后才发现，<strong>最珍贵的不是这些身外之物，而是三样东西。</strong></p>
<h3>第一：健康的身体</h3>
<p>身体是革命的本钱，没有健康，一切都是零。</p>
<h3>第二：真心的朋友</h3>
<p>人这一辈子，能遇到几个真心朋友，是莫大的幸运。</p>
<h3>第三：温暖的家庭</h3>
<p>家，是心灵的港湾，是疲惫时的依靠。</p>
<p><strong>朋友们，人生短暂，不要等到失去了才懂得珍惜。</strong></p>
<p><strong>珍惜健康，珍惜朋友，珍惜家人，这才是人生最大的财富！</strong></p>""",
        "digest": "人生最珍贵的不是金钱，而是健康、朋友和家庭。看完这篇文章，你会明白什么才是最重要的。"
    }
]

def get_access_token():
    """获取微信公众号 access_token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}"
    try:
        response = requests.get(url, timeout=30)
        data = response.json()
        if 'access_token' in data:
            print(f"获取access_token成功")
            return data['access_token']
        else:
            print(f"获取access_token失败: {data}")
            return None
    except Exception as e:
        print(f"获取access_token异常: {str(e)}")
        return None

def create_article(access_token, title, content, digest, author="每日精选"):
    """创建图文消息素材"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    
    article = {
        "articles": [
            {
                "title": title,
                "author": author,
                "digest": digest,
                "content": content,
                "content_source_url": "",
                "thumb_media_id": "",
                "need_open_comment": 1,
                "only_fans_can_comment": 0
            }
        ]
    }
    
    try:
        response = requests.post(url, json=article, timeout=30)
        result = response.json()
        print(f"创建草稿结果: {result}")
        return result.get('media_id')
    except Exception as e:
        print(f"创建草稿异常: {str(e)}")
        return None

def publish_article(access_token, media_id):
    """发布图文消息"""
    url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={access_token}"
    
    try:
        response = requests.post(url, json={"media_id": media_id}, timeout=30)
        result = response.json()
        print(f"发布结果: {result}")
        return result.get('errcode') == 0
    except Exception as e:
        print(f"发布异常: {str(e)}")
        return False

def main():
    print("=== 开始执行公众号自动发布 ===")
    
    if not APPID or not APPSECRET:
        print("错误：未设置 WECHAT_APPID 或 WECHAT_APPSECRET")
        return
    
    # 获取 access_token
    access_token = get_access_token()
    if not access_token:
        print("获取access_token失败，退出")
        return
    
    # 随机选择文章
    template = random.choice(ARTICLE_TEMPLATES)
    print(f"选择文章: {template['title']}")
    
    # 创建草稿
    media_id = create_article(
        access_token,
        template['title'],
        template['content'],
        template['digest']
    )
    
    if not media_id:
        print("创建草稿失败，退出")
        return
    
    print(f"创建草稿成功")
    
    # 发布文章
    success = publish_article(access_token, media_id)
    
    if success:
        print(f"=== 文章发布成功: {template['title']} ===")
    else:
        print("=== 文章发布失败 ===")

if __name__ == "__main__":
    main()
