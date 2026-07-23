# 🕷️ Book Spider - 通用电商爬虫框架

一个基于 Python 的**工程化通用爬虫框架**，支持多站点、多页并发采集，内置数据清洗与可视化分析模块。

---

## 📊 项目成果

| 数据集 | 采集量 | 说明 |
|---|---|---|
| 图书数据（books.csv） | 960 条 | 书名、价格、评分（books.toscrape.com） |
| 名言数据（quotes.csv） | 100 条 | 名言、作者、标签（quotes.toscrape.com） |

### 📈 数据分析报告

![analysis_report](data/analysis_report.png)

<details>
<summary>📊 点击查看详细统计</summary>

**图书数据概览**：
- 总采集：960 条
- 有效价格：20 条（受限于目标网站 JS 动态渲染，详见下方说明）
- 评分分布：1-5 星均匀分布

**名言数据概览**：
- 总采集：100 条
- 最高频作者：Albert Einstein（10 次）
- 最高频标签：love（14 次）

</details>

---

## 🛠️ 技术栈

| 技术 | 用途 |
|---|---|
| Python 3.x | 核心语言 |
| Requests | HTTP 请求 |
| BeautifulSoup4 | HTML 解析 |
| Pandas | 数据清洗与分析 |
| Matplotlib | 数据可视化 |
| Logging | 日志系统 |

---
## 🐛 踩坑记录（价格数据排查）

**现象**：初版爬取 960 条图书数据，价格字段全为 £0.00。

**假设**：目标网站采用 JavaScript 动态渲染价格，计划引入 Selenium。

**验证**：
- 使用 `requests` 直接抓取第 2、3 页 HTML，状态码 200
- 确认价格文本 `£xx.xx` 存在于响应体中
- 定位根因：
  1. 分页 URL 路径错误（`/page-N.html` → `/catalogue/page-N.html`）
  2. 价格解析未处理 UTF-8 / Latin-1 编码乱码（`Â£`）

**修复**：
- 修正 `page_url_template`
- 在 `fetch()` 中设置 `response.encoding = "utf-8"`
- 清洗价格字符串后再 `float()`

**结果**：价格覆盖率从 **2% → 100%**，无需浏览器自动化。

> **经验**：遇到数据缺失，先抓包验证假设，而非直接上重武器（Selenium）。
---
## 📁 项目结构
