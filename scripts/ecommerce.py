#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
电商SKU图生成器 - E-commerce SKU Image Generator
生成淘宝/京东/拼多多等平台的商品主图和详情页配图
"""

# 平台规格
PLATFORM_SPECS = {
    "taobao": {
        "name": "淘宝/天猫",
        "main_image": (800, 800),
        "detail_images": [(750, 1000), (750, 1000), (750, 1000)],
        "color_scheme": "warm",  # 暖色调
        "aspect_ratios": ["1:1", "3:4", "4:3"]
    },
    "jd": {
        "name": "京东",
        "main_image": (800, 800),
        "detail_images": [(800, 1000), (800, 1000)],
        "color_scheme": "blue",  # 蓝色系
        "aspect_ratios": ["1:1", "3:4"]
    },
    "pdd": {
        "name": "拼多多",
        "main_image": (600, 600),
        "detail_images": [(600, 800), (600, 800)],
        "color_scheme": "vibrant",  # 鲜艳
        "aspect_ratios": ["1:1"]
    },
    "dy": {
        "name": "抖音电商",
        "main_image": (1080, 1080),
        "detail_images": [(1080, 1920), (1080, 1440)],
        "color_scheme": "trendy",  # 潮流
        "aspect_ratios": ["1:1", "9:16", "3:4"]
    }
}

# 主图模板
MAIN_IMAGE_TEMPLATES = {
    "product_center": {
        "description": "产品居中，左右留白",
        "layout": "center",
        "product_size": 0.7  # 产品占比70%
    },
    "product_full": {
        "description": "产品充满画面",
        "layout": "full",
        "product_size": 0.95
    },
    "product_lifestyle": {
        "description": "产品+场景图",
        "layout": "lifestyle",
        "product_size": 0.5
    },
    "comparison": {
        "description": "对比图（Before/After）",
        "layout": "side_by_side",
        "product_size": 0.4
    }
}

# 详情页模板
DETAIL_IMAGE_TEMPLATES = {
    "feature_list": {
        "description": "功能特点列表",
        "sections": ["卖点1", "卖点2", "卖点3", "卖点4"]
    },
    "scenario_show": {
        "description": "场景展示",
        "sections": ["使用场景1", "使用场景2", "细节图"]
    },
    "comparison": {
        "description": "对比图",
        "sections": ["自家产品", "竞品对比", "优势标注"]
    },
    "story": {
        "description": "品牌故事",
        "sections": ["品牌理念", "产品故事", "用户评价"]
    }
}


def generate_main_image_prompt(product_info: dict, platform: str = "taobao", 
                               template: str = "product_center") -> str:
    """
    生成商品主图的Prompt
    
    Args:
        product_info: 产品信息字典
        platform: 平台 (taobao/jd/pdd/dy)
        template: 主图模板
    Returns:
        str: 图像生成Prompt
    """
    spec = PLATFORM_SPECS.get(platform, PLATFORM_SPECS["taobao"])
    width, height = spec["main_image"]
    
    product_name = product_info.get("name", "产品")
    product_desc = product_info.get("description", "")
    key_features = product_info.get("features", [])
    color_scheme = product_info.get("colors", spec["color_scheme"])
    
    # 颜色方案
    color_map = {
        "warm": "warm beige #F5F0E8, soft gold #E8D5B7, coral accents #FF8A80",
        "blue": "cool white #F5F7FA, ocean blue #1E88E5, silver #CFD8DC",
        "vibrant": "bright white #FFFFFF, vivid orange #FF7043, teal #26A69A",
        "trendy": "gradient purple-pink #E91E63 to #9C27B0, gold #FFD700, white #FFFFFF"
    }
    
    colors = color_map.get(color_scheme, color_map["warm"])
    
    # 构建Prompt
    prompt = f"""Create a professional e-commerce product image for {spec['name']} ({width}x{height}px).

=== PRODUCT INFO ===
Product Name: {product_name}
Product Description: {product_desc}
Key Features: {', '.join(key_features[:3])}

=== PLATFORM REQUIREMENTS ===
Platform: {spec['name']}
Recommended Size: {width}x{height}px
Aspect Ratio: 1:1

=== STYLE REQUIREMENTS ===
- Clean, professional e-commerce product photography style
- {colors}
- {MAIN_IMAGE_TEMPLATES[template]['description']}
- Product should occupy approximately {int(MAIN_IMAGE_TEMPLATES[template]['product_size']*100)}% of the image
- Include subtle shadow under product for depth
- White or light gradient background
- No text overlays on main image (for platform requirements)
- High contrast, sharp details
- Professional lighting with soft highlights

=== LAYOUT ===
- Product centered in frame
- Even margins on all sides
- Clean minimalist aesthetic suitable for {spec['name']} platform

=== QUALITY STANDARDS ===
- Commercial product photography quality
- Suitable for platform requirements
- High resolution with clear details
- Professional lighting and color accuracy
"""
    
    return prompt


def generate_detail_image_prompt(product_info: dict, platform: str = "taobao",
                                  template: str = "feature_list") -> str:
    """
    生成详情页配图的Prompt
    
    Args:
        product_info: 产品信息字典
        platform: 平台
        template: 详情页模板
    Returns:
        str: 图像生成Prompt
    """
    spec = PLATFORM_SPECS.get(platform, PLATFORM_SPECS["taobao"])
    width, height = spec["detail_images"][0]
    
    product_name = product_info.get("name", "产品")
    features = product_info.get("features", [])
    
    # 获取模板配置
    template_config = DETAIL_IMAGE_TEMPLATES.get(template, DETAIL_IMAGE_TEMPLATES["feature_list"])
    
    # 构建卖点列表
    feature_sections = ""
    for i, section in enumerate(template_config["sections"]):
        feature_sections += f"\n- Section {i+1}: {section}"
    
    prompt = f"""Create a detailed product feature image for {spec['name']} ({width}x{height}px).

=== PRODUCT INFO ===
Product Name: {product_name}
Key Features: {', '.join(features[:5])}

=== TEMPLATE TYPE ===
Template: {template_config['description']}
Sections to include: {feature_sections}

=== STYLE REQUIREMENTS ===
- Modern e-commerce detail page design
- Clean layout with clear visual hierarchy
- Color scheme: consistent with product branding
- Chinese text for Chinese e-commerce platforms
- Iconography for feature highlights
- Professional, trustworthy aesthetic
- Suitable for mobile and desktop viewing

=== LAYOUT STRUCTURE ===
- Clear section divisions
- Icon + text combinations for features
- Adequate white space for readability
- Brand logo placement (corner)
- Consistent typography hierarchy

=== TECHNICAL REQUIREMENTS ===
- Resolution: {width}x{height}px
- File format: JPG/PNG
- Mobile-optimized layout
- Fast loading consideration
"""
    
    return prompt


def generate_multi_platform_prompt(product_info: dict) -> dict:
    """
    生成多平台适配的Prompt套件
    
    Args:
        product_info: 产品信息字典
    Returns:
        dict: 各平台的Prompt字典
    """
    result = {}
    
    for platform, spec in PLATFORM_SPECS.items():
        result[platform] = {
            "platform_name": spec["name"],
            "main_image": generate_main_image_prompt(product_info, platform),
            "detail_images": [
                generate_detail_image_prompt(product_info, platform, template) 
                for template in DETAIL_IMAGE_TEMPLATES.keys()
            ]
        }
    
    return result


# 示例用法
if __name__ == "__main__":
    # 示例产品信息
    sample_product = {
        "name": "智能保温杯",
        "description": "316不锈钢真空保温，可显示温度，24小时保温",
        "features": ["316不锈钢", "智能测温", "24小时保温", "防滑设计", "一键显示温度"],
        "colors": "blue"
    }
    
    # 生成淘宝主图Prompt
    print("=== 淘宝主图Prompt ===")
    print(generate_main_image_prompt(sample_product, "taobao"))
    
    print("\n=== 京东详情页Prompt ===")
    print(generate_detail_image_prompt(sample_product, "jd"))
    
    print("\n=== 多平台Prompt套件 ===")
    multi = generate_multi_platform_prompt(sample_product)
    for platform, data in multi.items():
        print(f"\n{platform}: {data['platform_name']}")