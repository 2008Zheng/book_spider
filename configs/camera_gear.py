"""
摄影器材品类 · 站点配置
目标：三脚架 / 补光灯 / 麦克风 / 滤镜
示例站点：SmallRig、Neewer、B&H 公开页
"""

from config import SiteConfig

# SmallRig 官方（配件为主）
CAMERA_SMALLRIG = SiteConfig(
    name="smallrig_tripod",
    base_url="https://smallrig.com",
    page_url_template="/collections/tripods-monopods?page={page}",
    total_pages=3,
    first_page_is_root=False,
    delay=3.0,
    output_file="data/camera_smallrig.csv",
    model_fields=["sku", "title", "price", "currency", "scene_tag", "rating"]
)

# Neewer（平价配件）
CAMERA_NEEWER = SiteConfig(
    name="neewer_light",
    base_url="https://neewer.com",
    page_url_template="/collections/led-video-lights?page={page}",
    total_pages=3,
    first_page_is_root=False,
    delay=3.0,
    output_file="data/camera_neewer.csv",
    model_fields=["sku", "title", "price", "currency", "scene_tag", "rating"]
)

# B&H 公开商品页（专业器材，价格高）
CAMERA_BH = SiteConfig(
    name="bh_photo_video",
    base_url="https://www.bhphotovideo.com",
    page_url_template="/c/search?q=tripod&page={page}",
    total_pages=2,
    first_page_is_root=False,
    delay=4.0,
    output_file="data/camera_bh.csv",
    model_fields=["sku", "title", "price", "currency", "scene_tag", "rating"]
)

SCENE_TAGS = {
    "studio": "棚拍专业",
    "vlog": "Vlog创作",
    "travel": "旅行轻便",
    "macro": "微距特写",
    "wireless": "无线自由",
    "ring": "环形美颜",
}
