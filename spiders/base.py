import requests
import time
import logging
from abc import ABC, abstractmethod
from config import SiteConfig
from storage import save_to_csv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


class BaseSpider(ABC):
    """通用爬虫框架——所有站点爬虫继承此类"""

    def __init__(self, config: SiteConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        })
        self.results = []

    def build_url(self, page: int) -> str:
        """构造第 page 页的 URL"""
        if page == 1 and self.config.first_page_is_root:
            return self.config.base_url + "/"
        return self.config.base_url + self.config.page_url_template.format(page=page)

    def fetch(self, url: str) -> str:
        """请求网页，返回 HTML"""
        logger.info(f"正在请求: {url}")
        resp = self.session.get(url, timeout=10)
        resp.raise_for_status()
        resp.encoding = "utf-8"
        return resp.text

    @abstractmethod
    def parse(self, html: str) -> list[Dict]:
        """解析网页 → 返回结构化数据列表（由子类实现）"""
        pass

    @abstractmethod
    def create_model(self, item: Dict) -> object:
        """将字典转换为数据模型对象（由子类实现）"""
        pass

    def run(self):
        """主流程：循环翻页 → 解析 → 保存"""
        logger.info(f"开始爬取 [{self.config.name}]，共 {self.config.total_pages} 页")

        for page in range(1, self.config.total_pages + 1):
            url = self.build_url(page)

            try:
                html = self.fetch(url)
                items = self.parse(html)
                self.results.extend(items)
                logger.info(f"  → 第 {page} 页找到 {len(items)} 条，累计 {len(self.results)} 条")

                time.sleep(self.config.delay)

            except Exception as e:
                logger.error(f"第 {page} 页失败: {e}")
                continue

        # 转换为模型对象
        models = [self.create_model(item) for item in self.results]

        # 保存
        save_to_csv(models, self.config.output_file, self.config.model_fields)
        logger.info(f"🎉 全部完成！共采集 {len(models)} 条 → {self.config.output_file}")

