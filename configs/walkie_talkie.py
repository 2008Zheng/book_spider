"""
户外对讲机品类 · 站点配置
目标：户外/骑行/安防对讲机，圈层小众、溢价高
示例站点：Garmin、Baofeng、Motorola 公开页
"""

from config import SiteConfig

# Garmin 户外通讯（高端）
WALKIE_GARMIN = SiteConfig(
    name="garmin_communicator",
    base_url="https://www.garmin.com",
    page_url_template="/en-US/c/outdoor-recreation/communicators/?page={page}",
    total_pages=2,
    first_page_is_root=False,
    delay=3.5,
    output_file="data/walkie_garmin.csv",
    model_fields=["sku", "title", "price", "currency", "scene_tag", "rating"]
)

# Baofeng（平价入门，UV-5R 等）
WALKIE_BAOFENG = SiteConfig(
    name="baofeng_radio",
    base_url="https://baofengradio.com",
    page_url_template="/collections/all?page={page}",
    total_pages=2,
    first_page_is_root=False,
    delay=3.0,
    output_file="data/walkie_baofeng.csv",
    model_fields=["sku", "title", "price", "currency", "scene_tag", "rating"]
)

SCENE_TAGS = {
    "hiking": "徒步登山",
    "cycling": "骑行公路",
    "camping": "露营篝火",
    "hunting": "狩猎隐蔽",
    "emergency": "应急安防",
    "frs": "民用短距",
    "gmrs": "户外中距",
    "ham": "业余无线电",
}
