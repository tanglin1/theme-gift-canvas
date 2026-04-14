#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Xiaohongshu Content Generator
Generate complete Xiaohongshu notes: title + content + image prompts
"""

import random

TITLE_TEMPLATES = {
    "nianhui": [
        "Company year-end party gifts! Employees satisfied, leaders impressed",
        "What to choose for year-end gifts? These are practical and thoughtful",
        "HR must see! Year-end gift procurement guide",
        "Year-end gift list at 100 yuan per person! Great value",
        "Year-end raffle gifts recommendation, staff loves them"
    ],
    "birthday": [
        "Friend's birthday gift! Reaction was amazing",
        "How to choose birthday gifts? This list helps",
        "Birthday gift for bestie/boyfriend! Beautiful and practical",
        "Birthday gifts no雷区! This list is fool-proof",
        "Friend cried when receiving this birthday gift"
    ]
}

CONTENT_TEMPLATES = {
    "emotional": [
        "Every time I was afraid of雷区 when giving gifts, until I found this!",
        "After long consideration, I chose it - not disappointed!",
        "This gift moved my partner so much",
        "After long research, finally chose a satisfying gift",
        "This gift hits the heart, must share with everyone"
    ],
    "practical": [
        "This gift is super practical, used every day!",
        "Practical gifts are best, used for half a year still great",
        "Don't give those just looks, this is真正香",
        "Gave this to friend, everyone says very practical",
        "Self-use or gift both great, practical party satisfied"
    ]
}

TAGS = {
    "nianhui": ["#yearendgifts", "#companyparty", "#employeegifts", "#HRmustsee"],
    "birthday": ["#birthdaygift", "#bestiegift", "#boyfriendgift", "#giftrecommendations"]
}

def generate_title(theme):
    templates = TITLE_TEMPLATES.get(theme, TITLE_TEMPLATES["nianhui"])
    return random.choice(templates)

def generate_content(theme, gifts, style="emotional"):
    style_templates = CONTENT_TEMPLATES.get(style, CONTENT_TEMPLATES["emotional"])
    intro = random.choice(style_templates)
    
    content_parts = [intro, ""]
    content_parts.append(f"Recommended gifts for {theme}:")
    content_parts.append("")
    
    for i, gift in enumerate(gifts[:5], 1):
        name = gift.get("name", f"Gift {i}")
        price = gift.get("price", "TBD")
        reason = gift.get("reason", "Practical and nice")
        
        content_parts.append(f"{i}. *{name}*")
        content_parts.append(f"   Price: {price}")
        content_parts.append(f"   Reason: {reason}")
        content_parts.append("")
    
    return "\n".join(content_parts)

def generate_tags(theme):
    return TAGS.get(theme, TAGS["nianhui"])

def generate_full_post(theme, gifts, style="emotional"):
    return {
        "title": generate_title(theme),
        "content": generate_content(theme, gifts, style),
        "tags": generate_tags(theme)
    }

if __name__ == "__main__":
    sample_gifts = [
        {"name": "Wireless Earbuds", "price": "$50", "reason": "Practical tech"},
        {"name": "Flower Bouquet", "price": "$30", "reason": "Romantic"},
        {"name": "Skincare Set", "price": "$80", "reason": "High-end"}
    ]
    
    post = generate_full_post("nianhui", sample_gifts, "emotional")
    
    print("=== Xiaohongshu Post ===")
    print(f"\n[Title]\n{post['title']}")
    print(f"\n[Content]\n{post['content']}")
    print(f"\n[Tags]\n{', '.join(post['tags'])}")