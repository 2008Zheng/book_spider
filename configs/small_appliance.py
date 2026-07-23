"""
小家电品类 · 站点配置
目标：便携咖啡机 / 空气炸锅 / 迷你风扇 等跨境 DTC 公开页
示例站点：Cosori（空气炸锅）、Outin（便携咖啡机）、各品牌独立站
"""

from config import SiteConfig

# 示例：Cosori 美国站（公开商品列表页）
SMALL_APPLIANCE_COSORI = SiteConfig(
    name="cosori_airfryer",
    base_url="https://cosori.com",
    page_url_template="/collections/air-fryers?page={page}",
    total_pages=3,
    first_page_is_root=False,
    delay=3.0,
    output_file="data/small_appliance_cosori.csv",
    model_fields=["sku", "title", "price", "currency", "scene_tag", "rating"]
)

# 示例：Outin 便携咖啡机
SMALL_APPLIANCE_OUTIN = SiteConfig(
    name="outin_coffee",
    base_url="https://outin.com",
    page_url_template="/collections/portable-espresso-makers?page={page}",
    total_pages=2,
    first_page_is_root=False,
    delay=3.0,
    output_file="data/small_appliance_outin.csv",
    model_fields=["sku", "title", "price", "currency", "scene_tag", "rating"]
)

# 场景标签映射（用于溢价分析）
SCENE_TAGS = {
    "portable": "便携出行",
    "mini": "迷你桌面",
    "pro": "专业厨房",
    "smart": "智能物联",
    "travel": "旅行户外",
    "home": "家用基础",
}
