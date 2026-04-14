#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
批量生成礼品画布 - Batch Gift Canvas Generator
用于一次生成多个主题的礼品创意画布
"""

import os
import sys
import argparse
import time

# 设置环境变量
os.environ['DASHSCOPE_API_KEY'] = os.environ.get('DASHSCOPE_API_KEY', '')
os.environ['DASHSCOPE_BASE_URL'] = os.environ.get('DASHSCOPE_BASE_URL', 'https://dashscope.aliyuncs.com/api/v1/')

def generate_single_canvas(theme_info, output_dir):
    """
    生成单个礼品画布
    
    Args:
        theme_info: 主题信息字典
        output_dir: 输出目录
    Returns:
        bool: 是否成功
    """
    from scripts.image_generation_editing import generate
    
    # 构建Prompt
    prompt = build_prompt(theme_info)
    
    # 调用生成API
    result = generate(
        user_requirement=prompt,
        n=1,
        size="1024*1536"
    )
    
    if result.get("success"):
        # 保存图片
        image_url = result["content"][0].get("image", "")
        if image_url:
            filename = f"{theme_info['theme']}_gift_canvas.png"
            save_image(image_url, os.path.join(output_dir, filename))
            return True
    return False

def build_prompt(theme_info):
    """构建生成Prompt"""
    theme = theme_info.get("theme", "通用")
    budget = theme_info.get("budget", "50-500")
    recipients = theme_info.get("recipients", "同事")
    focus = theme_info.get("focus", "商务体面")
    
    prompt = f"""Create a high-density gift planning infographic for {theme} gift-giving. Theme colors: {theme_info.get('colors', 'blue + gold')}. Portrait 3:4 ratio.

MODULE 1 - 主题速览:
- 主题关键词: {theme}
- 预算区间: {budget}
- 送礼对象: {recipients}
- 侧重点: {focus}

MODULE 2 - 价格梯度地图:
- 入门款: [低价位推荐]
- 主流款: [中价位推荐]
- 品质款: [高价位推荐]
- 高端款: [顶配推荐]

MODULE 3 - 品类矩阵:
- 实用好物: [推荐]
- 文创美学: [推荐]
- 美食饮品: [推荐]
- 体验服务: [推荐]
- 定制专属: [推荐]

MODULE 4 - 对象匹配指南:
- [针对{recipients}的推荐]

MODULE 5 - 一句话选品逻辑:
- 最安全:
- 最用心:
- 最体面:

MODULE 6 - 避坑提醒:
- 避免:
- 误区:

Clean modern Chinese typography, gift box icons, price tags, professional style."""
    return prompt

def save_image(url, filepath):
    """保存图片"""
    import requests
    try:
        response = requests.get(url, timeout=30)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"图片已保存: {filepath}")
    except Exception as e:
        print(f"保存图片失败: {e}")

def batch_generate(theme_list, output_dir="."):
    """
    批量生成多个主题的礼品画布
    
    Args:
        theme_list: 主题列表，每个元素是一个字典
        output_dir: 输出目录
    Returns:
        dict: 生成结果统计
    """
    success_count = 0
    fail_count = 0
    results = []
    
    for i, theme_info in enumerate(theme_list):
        print(f"\n[{i+1}/{len(theme_list)}] 正在生成: {theme_info.get('theme', '未知主题')}")
        
        try:
            # 生成间隔，避免API限流
            if i > 0:
                time.sleep(5)
            
            success = generate_single_canvas(theme_info, output_dir)
            if success:
                success_count += 1
                results.append({"theme": theme_info.get("theme"), "status": "success"})
            else:
                fail_count += 1
                results.append({"theme": theme_info.get("theme"), "status": "failed"})
        except Exception as e:
            print(f"生成失败: {e}")
            fail_count += 1
            results.append({"theme": theme_info.get("theme"), "status": "error", "error": str(e)})
    
    return {
        "total": len(theme_list),
        "success": success_count,
        "failed": fail_count,
        "results": results
    }

def main():
    parser = argparse.ArgumentParser(description="批量生成礼品画布")
    parser.add_argument("--themes", type=str, help="主题列表，逗号分隔，如：情人节,母亲节,中秋节")
    parser.add_argument("--budget", type=str, default="50-500", help="预算区间")
    parser.add_argument("--recipients", type=str, default="同事", help="送礼对象")
    parser.add_argument("--output", type=str, default=".", help="输出目录")
    parser.add_argument("--file", type=str, help="主题列表JSON文件")
    
    args = parser.parse_args()
    
    theme_list = []
    
    # 从文件加载
    if args.file:
        import json
        with open(args.file, 'r', encoding='utf-8') as f:
            theme_list = json.load(f)
    # 从命令行参数解析
    elif args.themes:
        themes = args.themes.split(',')
        for theme in themes:
            theme_list.append({
                "theme": theme.strip(),
                "budget": args.budget,
                "recipients": args.recipients,
                "focus": "商务体面"
            })
    else:
        print("请提供主题列表或主题文件")
        return
    
    # 执行批量生成
    result = batch_generate(theme_list, args.output)
    
    print(f"\n批量生成完成!")
    print(f"总计: {result['total']}")
    print(f"成功: {result['success']}")
    print(f"失败: {result['failed']}")

if __name__ == "__main__":
    main()