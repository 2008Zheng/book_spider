"""
storage_sqlite.py · SQLite 存储 + 历史趋势图
"""

import os
import sys
import json
import sqlite3
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# ---------- 字体（和 analyze_scene.py 保持一致） ----------
_FONT_PATH = r"C:\Windows\Fonts\simhei.ttf"
if not os.path.exists(_FONT_PATH):
    _FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"
fp = fm.FontProperties(fname=_FONT_PATH)
plt.rcParams["font.family"] = fp.get_name()
plt.rcParams["axes.unicode_minus"] = False

# ---------- 路径 ----------
if getattr(sys, 'frozen', False):
    BASE = Path(os.path.dirname(sys.executable))
else:
    BASE = Path(__file__).parent

DB_PATH = BASE / "data" / "pricelens.db"
CHART_DIR = BASE / "data" / "reports" / "trends"
CHART_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. 初始化数据库
# ============================================================
def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            week_start TEXT,
            category TEXT,
            site TEXT,
            scene_tag TEXT,
            sku TEXT,
            title TEXT,
            price REAL,
            currency TEXT,
            crawl_time TEXT
        )
    """)
    conn.commit()
    return conn

# ============================================================
# 2. 写入快照（真实环境用）
# ============================================================
def save_snapshot(category: str, items: list):
    conn = get_conn()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")

    for item in items:
        conn.execute("""
            INSERT INTO prices (week_start, category, site, scene_tag, sku, title, price, currency, crawl_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            week_start,
            category,
            item.get("site", ""),
            item.get("scene_tag", ""),
            item.get("sku", ""),
            item.get("title", "")[:100],
            item.get("price", 0.0),
            item.get("currency", "USD"),
            now
        ))
    conn.commit()
    conn.close()
    print(f"  💾 已写入数据库：{category}（{len(items)} 条）")

# ============================================================
# 3. 读取历史（最近 N 周）
# ============================================================
def load_history(category: str, weeks: int = 4):
    import pandas as pd
    conn = get_conn()
    since = (datetime.now() - timedelta(weeks=weeks)).strftime("%Y-%m-%d")
    df = pd.read_sql_query("""
        SELECT week_start, category, AVG(price) as avg_price
        FROM prices
        WHERE category = ? AND week_start >= ?
        GROUP BY week_start
        ORDER BY week_start
    """, conn, params=(category, since))
    conn.close()
    return df

# ============================================================
# 4. 画 4 周历史价格曲线
# ============================================================
def draw_trend_chart(category: str, label_cn: str, weeks: int = 4) -> Path:
    import pandas as pd
    df = load_history(category, weeks)

    fig, ax = plt.subplots(figsize=(9, 4.5))

    if len(df) > 0:
        ax.plot(df["week_start"], df["avg_price"],
                marker="o", linewidth=2.5, color="#1a73e8", markersize=8)
        last_row = df.iloc[-1]
        ax.annotate(f'{last_row["avg_price"]:.1f}',
                    xy=(last_row["week_start"], last_row["avg_price"]),
                    xytext=(0, 12), textcoords="offset points",
                    fontproperties=fp, fontsize=11, color="#d93025",
                    arrowprops=dict(arrowstyle="->", color="#d93025"))
        ax.set_ylabel("品类基线均价", fontproperties=fp)
    else:
        ax.text(0.5, 0.5, "暂无历史数据\n请先运行一次采集",
                ha="center", va="center", fontproperties=fp, fontsize=13,
                color="#999")

    ax.set_title(f"「{label_cn}」近 {weeks} 周价格趋势", fontproperties=fp, fontsize=14, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.xticks(rotation=20, fontproperties=fp)
    plt.tight_layout()

    out = CHART_DIR / f"{category}_trend_{weeks}w.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"  📈 趋势图已生成：{out.name}")
    return out

# ============================================================
# 5. 为 4 个品类画趋势图
# ============================================================
CATEGORY_LABELS = {
    "sun_protect": "户外防晒用品",
    "small_appliance": "小家电",
    "camera_gear": "摄影器材",
    "walkie_talkie": "户外对讲机",
}

def draw_all_trends(weeks: int = 4):
    paths = []
    for cat, label in CATEGORY_LABELS.items():
        p = draw_trend_chart(cat, label, weeks)
        paths.append(p)
    return paths

# ============================================================
# 6. 模拟 4 周历史数据（演示用 · 关键函数）
# ============================================================
def mock_4_weeks_history():
    """模拟插入过去 4 周的快照，便于演示趋势图"""
    conn = get_conn()
    today = datetime.now()

    mock_prices = {
        "sun_protect":     [168.0, 170.5, 171.6, 173.2],
        "small_appliance": [118.0, 119.5, 120.7, 122.1],
        "camera_gear":     [110.5, 111.8, 113.0, 114.5],
        "walkie_talkie":   [155.0, 156.3, 158.0, 159.4],
    }

    sites_map = {
        "sun_protect": ["beneunder", "decathlon", "columbia"],
        "small_appliance": ["cosori", "outin"],
        "camera_gear": ["smallrig", "neewer", "bh"],
        "walkie_talkie": ["garmin", "baofeng"],
    }

    for cat, prices in mock_prices.items():
        for i, price in enumerate(prices):
            week_start = (today - timedelta(weeks=3-i)).strftime("%Y-%m-%d")
            for s in sites_map[cat]:
                conn.execute("""
                    INSERT INTO prices (week_start, category, site, scene_tag, sku, title, price, currency, crawl_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    week_start, cat, s, "demo", f"{s}_demo",
                    f"{s} demo item", price + np.random.normal(0, 5),
                    "CNY" if "sun" in cat else "USD",
                    f"{week_start} 10:00"
                ))

    conn.commit()
    conn.close()
    print("  🎲 已插入 4 周模拟历史数据")

# ============================================================
# 7. 命令行入口（方便测试）
# ============================================================
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--weeks", type=int, default=4)
    parser.add_argument("--seed", action="store_true", help="插入模拟历史数据")
    args = parser.parse_args()

    if args.seed:
        mock_4_weeks_history()

    draw_all_trends(args.weeks)
    print(f"\n✅ 趋势图目录：{CHART_DIR}")
