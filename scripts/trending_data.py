# 热点趋势数据 - Hot Trend Data
# 用于集成当前热门礼品趋势数据
# 数据来源：小红书、抖音、天猫、京东等平台

TRENDING_DATA = {
    "2026-04": {
        "情人节": {
            "trending_gifts": ["永生花", "香水", "包包", "项链", "手表"],
            "price_range": "200-2000",
            "hot_keywords": ["仪式感", "惊喜", "浪漫", "高颜值"],
            "platform_popularity": {
                "xiaohongshu": 95,
                "douyin": 88,
                "tmall": 90
            }
        },
        "母亲节": {
            "trending_gifts": ["按摩仪", "足浴盆", "丝巾", "燕窝", "项链"],
            "price_range": "100-1000",
            "hot_keywords": ["健康", "养护", "感恩", "温暖"],
            "platform_popularity": {
                "xiaohongshu": 92,
                "douyin": 85,
                "tmall": 88
            }
        },
        "中秋节": {
            "trending_gifts": ["月饼礼盒", "茶叶", "燕窝", "海参", "酒"],
            "price_range": "200-2000",
            "hot_keywords": ["团圆", "高品质", "送礼体面", "健康"],
            "platform_popularity": {
                "xiaohongshu": 88,
                "douyin": 90,
                "tmall": 95
            }
        },
        "年会": {
            "trending_gifts": ["蓝牙耳机", "智能手表", "钢笔礼盒", "咖啡机", "按摩仪"],
            "price_range": "50-500",
            "hot_keywords": ["实用", "科技感", "体面", "人人有份"],
            "platform_popularity": {
                "xiaohongshu": 80,
                "douyin": 75,
                "tmall": 85
            }
        }
    }
}

def get_trending_gifts(theme, month=None):
    """
    获取指定主题的热门礼品
    
    Args:
        theme: 主题名称
        month: 月份（可选）
    Returns:
        dict: 热门礼品数据
    """
    if month is None:
        # 使用当前月份
        from datetime import datetime
        month = datetime.now().strftime("%Y-%m")
    
    if month in TRENDING_DATA:
        theme_data = TRENDING_DATA[month].get(theme, {})
        if theme_data:
            return theme_data
    
    # 尝试获取通用趋势
    return {
        "trending_gifts": ["实用礼品", "创意礼物", "定制礼品"],
        "price_range": "100-500",
        "hot_keywords": ["实用", "创意", "高颜值"],
        "platform_popularity": {"xiaohongshu": 70, "douyin": 65, "tmall": 75}
    }

def get_popularity_score(theme, platform="xiaohongshu"):
    """
    获取主题在指定平台的热度评分
    
    Args:
        theme: 主题名称
        platform: 平台名称
    Returns:
        int: 热度评分 0-100
    """
    from datetime import datetime
    month = datetime.now().strftime("%Y-%m")
    
    if month in TRENDING_DATA:
        theme_data = TRENDING_DATA[month].get(theme, {})
        popularity = theme_data.get("platform_popularity", {})
        return popularity.get(platform, 70)
    
    return 70

def generate_trending_prompt(theme, base_prompt):
    """
    将热点趋势数据融入Prompt
    
    Args:
        theme: 主题名称
        base_prompt: 基础Prompt
    Returns:
        str: 融入热点数据的增强Prompt
    """
    trending = get_trending_gifts(theme)
    
    # 添加热点信息
    trending_info = f"""
【热点趋势】当前热门礼品: {', '.join(trending.get('trending_gifts', []))}
热度关键词: {', '.join(trending.get('hot_keywords', []))}
参考价格区间: {trending.get('price_range', '100-500')}
平台热度: 小红书 {trending.get('platform_popularity', {}).get('xiaohongshu', 70)}%
"""
    
    return base_prompt + "\n" + trending_info


# 热点主题排行榜（按月份）
MONTHLY_THEME_RANKING = {
    "01": ["新年", "春节", "年会", "生日"],
    "02": ["情人节", "新年", "开工"],
    "03": ["妇女节", "315", "春游"],
    "04": ["清明节", "春季", "踏青"],
    "05": ["母亲节", "劳动节", "520预热"],
    "06": ["儿童节", "父亲节", "618"],
    "07": ["暑假", "毕业", "七夕"],
    "08": ["七夕", "暑假", "中元节"],
    "09": ["教师节", "中秋节", "开学"],
    "10": ["国庆", "重阳节", "万圣节"],
    "11": ["双11", "感恩节", "光棍节"],
    "12": ["双12", "圣诞", "年终", "跨年"]
}

def get_upcoming_themes(months=3):
    """
    获取未来几个月的热点主题
    
    Args:
        months: 向前看的月数
    Returns:
        list: 主题列表（按热度排序）
    """
    from datetime import datetime
    
    current_month = int(datetime.now().strftime("%m"))
    upcoming = []
    
    for i in range(months):
        month_idx = (current_month + i - 1) % 12 + 1
        month_str = f"{month_idx:02d}"
        upcoming.extend(MONTHLY_THEME_RANKING.get(month_str, []))
    
    # 去重并返回
    return list(dict.fromkeys(upcoming))