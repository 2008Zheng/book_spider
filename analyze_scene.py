"""
analyze_scene.py · 场景溢价对比分析（交付级 · 中文不乱码）
=========================================================
输入：各品类 parser 输出的统一字段列表
输出：
  1) 场景均价对比柱状图
  2) 品牌×场景热力图
  3) 场景溢价率 JSON 报告
  4) 场景溢价率 CSV 摘要（Excel 友好）
  5) 汇总 summary.json（供周报使用）

用法：
  python analyze_scene.py --category sun_protect
  python analyze_scene.py --category all
"""

import argparse
import json
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# ✅ 强制指定 SimHei 字体文件（你系统里真实存在的路径）
FONT_PATH = r"C:\Windows\Fonts\simhei.ttf"
fp = fm.FontProperties(fname=FONT_PATH)

# ✅ 让 matplotlib 全局认识这个字体
plt.rcParams["font.family"] = fp.get_name()
plt.rcParams["font.sans-serif"] = [fp.get_name(), "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
import numpy as np
import pandas as pd

# ============================================================
# ✅ 全局中文字体（只设一次，Windows/macOS 通用）
# ============================================================
plt.rcParams["font.sans-serif"] = [
    "SimHei",               # Windows
    "Microsoft YaHei",      # Windows
    "Noto Sans CJK SC",     # Linux / Docker
    "PingFang SC",          # macOS
    "Arial Unicode MS"
]
plt.rcParams["axes.unicode_minus"] = False  # 负号正常

# ============================================================
# 1. 场景映射 & 排序规则
# ============================================================
SCENE_LABEL_CN = {
    "mountain": "山系户外", "daily": "日常通勤", "running": "跑步运动",
    "uv": "UPF50+专业", "fishing": "垂钓涉水", "bucket": "渔夫帽款", "kids": "儿童防护",
    "portable": "便携出行", "home": "家用基础", "pro": "专业厨房", "smart": "智能物联", "travel": "旅行户外",
    "studio": "棚拍专业", "vlog": "Vlog创作", "wireless": "无线自由", "ring": "环形美颜", "macro": "微距特写",
    "hiking": "徒步登山", "cycling": "骑行公路", "hunting": "狩猎隐蔽",
    "emergency": "应急安防", "ham": "业余无线电", "gmrs": "户外中距",
}

SCENE_ORDER = {
    "sun_protect": ["mountain", "uv", "fishing", "running", "daily", "bucket", "kids"],
    "small_appliance": ["pro", "smart", "portable", "travel", "home"],
    "camera_gear": ["studio", "wireless", "vlog", "macro", "ring", "travel"],
    "walkie_talkie": ["hiking", "hunting", "gmrs", "cycling", "ham", "emergency"],
}

# ============================================================
# 2. Mock 数据（真实环境替换为 parser 输出）
# ============================================================
def mock_sun_protect(n=120):
    rng = np.random.RandomState(42)
    sites = ["beneunder", "decathlon", "columbia"]
    scenes = SCENE_ORDER["sun_protect"]
    rows = []
    for i in range(n):
        site = rng.choice(sites, p=[0.4, 0.35, 0.25])
        scene = rng.choice(scenes)
        base = {"decathlon": 79, "columbia": 159, "beneunder": 199}[site]
        premium = 1.0 + (0.3 if scene in ("mountain", "uv") else 0)
        price = round(max(29, base * premium + rng.normal(0, 12)), 1)
        rows.append({
            "sku": f"{site}_{i}",
            "title": f"{site} {scene} sun protection",
            "price": price,
            "currency": "CNY",
            "scene_tag": scene,
            "rating": round(rng.uniform(3.5, 5.0), 1),
            "site": site
        })
    return rows

def mock_small_appliance(n=80):
    rng = np.random.RandomState(7)
    sites = ["cosori", "outin"]
    scenes = SCENE_ORDER["small_appliance"]
    rows = []
    for i in range(n):
        site = rng.choice(sites)
        scene = rng.choice(scenes)
        base = {"cosori": 89, "outin": 129}[site]
        premium = 1.0 + (0.25 if scene in ("pro", "smart") else 0)
        price = round(max(39, base * premium + rng.normal(0, 15)), 1)
        rows.append({
            "sku": f"{site}_{i}",
            "title": f"{site} {scene} appliance",
            "price": price,
            "currency": "USD",
            "scene_tag": scene,
            "rating": round(rng.uniform(3.8, 4.9), 1),
            "site": site
        })
    return rows

def mock_camera_gear(n=100):
    rng = np.random.RandomState(13)
    sites = ["smallrig", "neewer", "bh"]
    scenes = SCENE_ORDER["camera_gear"]
    rows = []
    for i in range(n):
        site = rng.choice(sites, p=[0.35, 0.35, 0.3])
        scene = rng.choice(scenes)
        base = {"smallrig": 79, "neewer": 39, "bh": 199}[site]
        premium = 1.0 + (0.4 if scene in ("wireless", "studio") else 0)
        price = round(max(15, base * premium + rng.normal(0, 18)), 1)
        rows.append({
            "sku": f"{site}_{i}",
            "title": f"{site} {scene} gear",
            "price": price,
            "currency": "USD",
            "scene_tag": scene,
            "rating": round(rng.uniform(3.6, 4.9), 1),
            "site": site
        })
    return rows

def mock_walkie_talkie(n=60):
    rng = np.random.RandomState(23)
    sites = ["garmin", "baofeng"]
    scenes = SCENE_ORDER["walkie_talkie"]
    rows = []
    for i in range(n):
        site = rng.choice(sites, p=[0.5, 0.5])
        scene = rng.choice(scenes)
        base = {"garmin": 249, "baofeng": 39}[site]
        premium = 1.0 + (0.3 if scene in ("ham", "hunting") else 0)
        price = round(max(19, base * premium + rng.normal(0, 20)), 1)
        rows.append({
            "sku": f"{site}_{i}",
            "title": f"{site} {scene} radio",
            "price": price,
            "currency": "USD",
            "scene_tag": scene,
            "rating": round(rng.uniform(3.5, 4.8), 1),
            "site": site
        })
    return rows

# ============================================================
# 3. 图表绘制
# ============================================================
def scene_premium_chart(df: pd.DataFrame, category: str, out_dir: Path):
    """场景均价对比柱状图（按品牌分组）"""
    g = df.groupby(["site", "scene_tag"])["price"].mean().unstack()
    g.columns = [SCENE_LABEL_CN.get(c, c) for c in g.columns]
    g = g.sort_index()

    ax = g.plot(kind="bar", figsize=(10, 5.5), edgecolor="white", linewidth=0.5)
    ax.set_title(f"「{category}」场景均价对比（按品牌）", fontsize=13, fontweight="bold")
    ax.set_ylabel("均价（本地货币）")
    ax.set_xlabel("")
    ax.legend(loc="upper right", fontsize=9)
    plt.xticks(rotation=0)
    plt.tight_layout()

    p = out_dir / f"{category}_scene_price.png"
    plt.savefig(p, dpi=150)
    plt.close()
    return p

def scene_premium_heatmap(df: pd.DataFrame, category: str, out_dir: Path):
    """品牌×场景热力图（列顺序固定）"""
    pivot = df.pivot_table(values="price", index="site", columns="scene_tag", aggfunc="mean")

    order = SCENE_ORDER.get(category, list(pivot.columns))
    pivot = pivot[order]
    pivot.columns = [SCENE_LABEL_CN.get(c, c) for c in pivot.columns]

    fig, ax = plt.subplots(figsize=(9, 4))
    im = ax.imshow(pivot.values, cmap="YlOrRd", aspect="auto")

    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, rotation=35, ha="right")
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)

    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            v = pivot.values[i, j]
            if not np.isnan(v):
                ax.text(j, i, f"{v:.0f}", ha="center", va="center",
                         color="white" if v > pivot.values.mean() else "black", fontsize=9)

    ax.set_title(f"「{category}」品牌×场景 均价热力图", fontsize=13, fontweight="bold")
    fig.colorbar(im, ax=ax, shrink=0.8, label="均价")
    plt.tight_layout()

    p = out_dir / f"{category}_scene_heatmap.png"
    plt.savefig(p, dpi=150)
    plt.close()
    return p

# ============================================================
# 4. 溢价率计算 & 报告输出
# ============================================================
def premium_rate_report(df: pd.DataFrame, category: str) -> dict:
    baseline = df["price"].mean()
    currency = df["currency"].iloc[0] if "currency" in df.columns else "UNKNOWN"

    grouped = df.groupby("scene_tag")["price"].mean()
    rates = {}
    for scene, avg in grouped.items():
        rate = (avg - baseline) / baseline * 100
        rates[SCENE_LABEL_CN.get(scene, scene)] = {
            "avg_price": round(avg, 1),
            "premium_rate": round(rate, 1)
        }

    return {
        "category": category,
        "baseline_avg": round(baseline, 1),
        "currency": currency,
        "total_skus": len(df),
        "scenes": dict(sorted(rates.items(), key=lambda x: -x[1]["premium_rate"]))
    }

def save_csv_summary(report: dict, category: str, out_dir: Path):
    df = pd.DataFrame([
        {
            "场景": scene,
            "均价": info["avg_price"],
            "溢价率(%)": info["premium_rate"]
        }
        for scene, info in report["scenes"].items()
    ])
    csv_path = out_dir / f"{category}_summary.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")  # Excel 不乱码
    return csv_path

# ============================================================
# 5. 主流程
# ============================================================
def analyze_category(category: str, items: list, out_dir: Path):
    df = pd.DataFrame(items)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 图表
    p1 = scene_premium_chart(df, category, out_dir)
    p2 = scene_premium_heatmap(df, category, out_dir)

    # 报告
    report = premium_rate_report(df, category)
    json_path = out_dir / f"{category}_premium_report.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # CSV
    csv_path = save_csv_summary(report, category, out_dir)

    print(f"\n✅ [{category}] 分析完成：")
    print(f"   - 样本量：{report['total_skus']} 条")
    print(f"   - 基线均价：{report['baseline_avg']} {report['currency']}")
    print(f"   - 图表：{p1.name}, {p2.name}")
    print(f"   - JSON报告：{json_path.name}")
    print(f"   - CSV摘要：{csv_path.name}")

    for k, v in report["scenes"].items():
        flag = "🔺" if v["premium_rate"] > 15 else ("➖" if abs(v["premium_rate"]) <= 10 else "🔻")
        print(f"     {flag} {k:10s} 均价 {v['avg_price']:>7}  溢价 {v['premium_rate']:>+6.1f}%")

    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", default="all",
                        choices=["sun_protect","small_appliance","camera_gear","walkie_talkie","all"])
    args = parser.parse_args()

    out = Path("data/reports")
    all_reports = {}

    data_map = {
        "sun_protect": ("sun_protect", mock_sun_protect(120)),
        "small_appliance": ("small_appliance", mock_small_appliance(80)),
        "camera_gear": ("camera_gear", mock_camera_gear(100)),
        "walkie_talkie": ("walkie_talkie", mock_walkie_talkie(60)),
    }

    if args.category == "all":
        for key, (cat, items) in data_map.items():
            all_reports[key] = analyze_category(cat, items, out / cat)
    else:
        cat, items = data_map[args.category]
        all_reports[args.category] = analyze_category(cat, items, out / args.category)

    summary_path = out / "summary.json"
    summary_path.write_text(json.dumps(all_reports, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n📦 汇总报告：{summary_path}")

if __name__ == "__main__":
    main()
