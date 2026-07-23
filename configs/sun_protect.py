"""
户外防晒用品品类 · 站点配置
目标：防晒衣/帽/喷雾/面罩，季节性极强，山系溢价明显
示例站点：迪卡侬、蕉下（公开页）、伯希和、Columbia
"""

from config import SiteConfig

# 迪卡侬防晒（高性价比基线）
SUN_DECATLON = SiteConfig(
    name="decathlon_sun",
    base_url="https://www.decathlon.com",
    page_url_template="/collections/sun-protection?page={page}",
    total_pages=3,
    first_page_is_root=False,
    delay=3.0,
    output_file="data/sun_decathlon.csv",
    model_fields=["sku", "title", "price", "currency", "scene_tag", "rating"]
)

# Columbia（户外中高端）
SUN_COLUMBIA = SiteConfig(
    name="columbia_sun",
    base_url="https://www.columbia.com",
    page_url_template="/c/outdoor-sun-protection/?page={page}",
    total_pages=2,
    first_page_is_root=False,
    delay=3.0,
    output_file="data/sun_columbia.csv",
    model_fields=["sku", "title", "price", "currency", "scene_tag", "rating"]
)

# 蕉下（山系溢价代表，独立站/天猫旗舰店公开页）
SUN_BENEUNDER = SiteConfig(
    name="beneunder_sun",
    base_url="https://www.beneunder.com",
    page_url_template="/collections/sun-protection?page={page}",
    total_pages=2,
    first_page_is_root=False,
    delay=3.0,
    output_file="data/sun_beneunder.csv",
    model_fields=["sku", "title", "price", "currency", "scene_tag", "rating"]
)

SCENE_TAGS = {
    "mountain": "山系户外",
    "hiking": "徒步登山",
    "fishing": "垂钓涉水",
    "running": "跑步运动",
    "daily": "日常通勤",
    "kids": "儿童防护",
    "uv": "UPF50+专业",
    "bucket": "渔夫帽款",
}
