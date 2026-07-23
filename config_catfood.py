from config import SiteConfig

CATFOOD_SITE_A = SiteConfig(
    name="chewy_catfood",
    base_url="https://www.chewy.com",
    page_url_template="/b/cat-food?page={page}",
    total_pages=5,
    delay=3.0,
    output_file="data/catfood.csv",
    model_fields=["sku", "title", "price", "rating"]
)
