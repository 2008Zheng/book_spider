"""
gen_weekly_report.py · 周报生成器（HTML 版）· 最终修复版
"""

import argparse
import base64
import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# ============================================================
# 字体（和 analyze_scene.py 统一）
# ============================================================
_FONT_PATH = r"C:\Windows\Fonts\simhei.ttf"
if not os.path.exists(_FONT_PATH):
    _FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"
fp = fm.FontProperties(fname=_FONT_PATH)
plt.rcParams["font.family"] = fp.get_name()
plt.rcParams["font.sans-serif"] = [fp.get_name(), "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ============================================================
# 工具函数
# ============================================================
def img_to_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()

def read_total_skus(summary_path: Path, category: str) -> int:
    if not summary_path.exists():
        return 0
    try:
        s = json.loads(summary_path.read_text(encoding="utf-8"))
        return int(s.get(category, {}).get("total_skus", 0))
    except (json.JSONDecodeError, ValueError):
        return 0

# ============================================================
# 调价告警（模拟）
# ============================================================
def mock_alerts(category: str, n_alerts: int = 5) -> pd.DataFrame:
    old = [199, 159, 89, 249, 129]
    new = [179, 159, 99, 219, 139]
    df = pd.DataFrame({
        "sku": [f"{category}_A{i}" for i in range(n_alerts)],
        "title": [f"竞品SKU-{i+1}" for i in range(n_alerts)],
        "old_price": old,
        "new_price": new,
    })
    df["change_pct"] = ((df["new_price"] / df["old_price"] - 1) * 100).round(1).astype(str) + "%"
    return df[["sku", "title", "old_price", "new_price", "change_pct"]]

# ============================================================
# HTML 模板
# ============================================================
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<title>{title}</title>
<style>
body {{ font-family:"Noto Sans CJK SC","Microsoft YaHei",sans-serif; max-width:880px; margin:24px auto; color:#222; line-height:1.6; }}
h1 {{ border-bottom:3px solid #ff6b35; padding-bottom:8px; }}
h2 {{ color:#1a73e8; margin-top:28px; border-left:4px solid #1a73e8; padding-left:10px; }}
.metric {{ display:inline-block; width:170px; margin:8px 12px; text-align:center; }}
.metric .v {{ font-size:26px; font-weight:bold; color:#ff6b35; }}
.metric .l {{ font-size:12px; color:#666; }}
table {{ border-collapse:collapse; width:100%; margin:12px 0; font-size:13px; }}
th {{ background:#1a73e8; color:#fff; padding:8px; text-align:left; }}
td {{ padding:6px 8px; border-bottom:1px solid #eee; }}
tr.up td {{ background:#fff5f0; }} tr.down td {{ background:#f0f9ff; }}
.alert-up {{ color:#d93025; font-weight:bold; }} .alert-down {{ color:#188038; font-weight:bold; }}
.tip {{ background:#fff8e1; border-left:4px solid #f9ab00; padding:10px 14px; margin:14px 0; border-radius:4px; }}
img {{ max-width:100%; border:1px solid #ddd; border-radius:6px; margin:8px 0; }}
.footer {{ color:#999; font-size:12px; margin-top:32px; border-top:1px solid #eee; padding-top:10px; }}
</style></head><body>

<h1>📊 {title}</h1>
<p style="color:#666;">数据周期：{week_start} ~ {week_end} ｜ 生成时间：{gen_time}</p>

<h2>一、核心指标</h2>
<div class="metric"><div class="v">{total_skus}</div><div class="l">监控SKU数</div></div>
<div class="metric"><div class="v">{baseline_avg}</div><div class="l">品类基线均价</div></div>
<div class="metric"><div class="v" style="color:#188038;">{top_premium_scene}</div><div class="l">最高溢价场景</div></div>
<div class="metric"><div class="v">{alert_count}</div><div class="l">本周调价事件</div></div>

<h2>二、场景均价对比</h2>
<img src="data:image/png;base64,{chart_bar}" alt="场景均价对比">

<h2>二·五、近 4 周价格趋势</h2>
<img src="data:image/png;base64,{chart_trend}" alt="4周趋势">

<h2>三、品牌×场景 热力图</h2>
<img src="data:image/png;base64,{chart_heatmap}" alt="热力图">

<h2>四、场景溢价率排名</h2>
<table><tr><th>场景</th><th>均价</th><th>溢价率</th></tr>{premium_rows}</table>

<h2>五、本周调价告警</h2>
{alert_table}

<h2>六、运营建议</h2>
<div class="tip"><b>💡 选品切入建议：</b>{suggestion}</div>

<div class="footer">
本报告由 PriceLens 价格雷达自动生成 ｜ 数据来源：各品牌独立站/平台公开商品页 ｜ 仅供甲方内部经营分析使用，不得转售原始数据
</div></body></html>"""

# ============================================================
# 渲染
# ============================================================
CATEGORY_LABELS = {
    "sun_protect": "户外防晒用品",
    "small_appliance": "小家电",
    "camera_gear": "摄影器材",
    "walkie_talkie": "户外对讲机",
}

SUGGESTIONS = {
    "sun_protect": "山系户外/UPF50+ 场景溢价最高，建议在 ¥169–199 区间切入山系防晒衣，避开迪卡侬 ¥79 基线，用「轻量+山系设计」做差异化。",
    "small_appliance": "Pro/Smart 场景均价显著高于家用基础款，便携咖啡机建议定价 ¥159–199（Outin 同级），强调旅行户外场景。",
    "camera_gear": "无线/Vlog 场景溢价明显，三脚架+补光灯套装建议以 ¥299 切入，对标 SmallRig，强调「无线+便携」组合价值。",
    "walkie_talkie": "徒步/狩猎场景溢价 17–19%，入门级 GMRS 对讲机建议 ¥199 起步，避开 Baofeng ¥39 低价带，主打「合规+易用」。",
}

def render_report(category: str, report_json: dict, chart_dir: Path) -> str:
    cat_label = CATEGORY_LABELS.get(category, category)
    suggestion = SUGGESTIONS.get(category, "建议结合场景溢价数据，选择空白价格带切入。")

    # ---- 柱状图 ----
    bar_b64 = img_to_base64(chart_dir / f"{category}_scene_price.png")
    # ---- 热力图 ----
    heat_b64 = img_to_base64(chart_dir / f"{category}_scene_heatmap.png")

    # ---- 趋势图（智能查找，只算一次） ----
    script_dir = Path(__file__).resolve().parent
    trend_b64 = ""
    candidates = [
        script_dir / "data" / "reports" / "trends" / f"{category}_trend_4w.png",
        chart_dir.parent / "trends" / f"{category}_trend_4w.png",
        chart_dir / "trends" / f"{category}_trend_4w.png",
    ]
    for p in candidates:
        if p.exists():
            trend_b64 = img_to_base64(p)
            print(f"  📈 已嵌入趋势图：{p.name}（{len(trend_b64)} 字符）")
            break
    if not trend_b64:
        print(f"  ⚠️ 未找到趋势图，尝试过 {len(candidates)} 个路径")

    # ---- 溢价表格 ----
    scenes = report_json.get("scenes", {})
    sorted_scenes = sorted(scenes.items(), key=lambda x: x[1].get("premium_rate", 0), reverse=True)
    rows_html = ""
    for scene, info in sorted_scenes:
        cls = "up" if info.get("premium_rate", 0) > 15 else ("down" if info.get("premium_rate", 0) < -5 else "")
        sign = "+" if info.get("premium_rate", 0) >= 0 else ""
        rows_html += f'<tr class="{cls}"><td>{scene}</td><td>{info.get("avg_price","-")}</td><td>{sign}{info.get("premium_rate","-")}%</td></tr>'

    # ---- 告警表 ----
    alerts = mock_alerts(category)
    alert_rows = ""
    for _, r in alerts.iterrows():
        direction = "up" if str(r["change_pct"]).startswith("+") else "down"
        cls = "alert-up" if direction == "up" else "alert-down"
        arrow = "🔺" if direction == "up" else "🔻"
        alert_rows += f'<tr class="{direction}"><td>{r["sku"]}</td><td>{r["title"]}</td><td>{r["old_price"]}</td><td>{r["new_price"]}</td><td class="{cls}">{arrow} {r["change_pct"]}</td></tr>'
    alert_table = f'<table><tr><th>SKU</th><th>商品</th><th>原价</th><th>现价</th><th>变动</th></tr>{alert_rows}</table>'

    # ---- 最高溢价 ----
    if sorted_scenes:
        top_scene_name, top_info = sorted_scenes[0]
        top_premium_str = f"{top_scene_name}（+{top_info.get('premium_rate',0)}%）"
    else:
        top_premium_str = "-"

    # ---- 日期 ----
    today = datetime.now()
    week_start = (today - timedelta(days=today.weekday())).strftime("%Y.%m.%d")
    week_end = (today + timedelta(days=4 - today.weekday())).strftime("%Y.%m.%d")

    total_skus = report_json.get("total_skus", 0)
    baseline_avg = report_json.get("baseline_avg", "-")

    # ---- 唯一一次 format ----
    html = HTML_TEMPLATE.format(
        title=f"PriceLens · {cat_label}竞品价格周报",
        week_start=week_start, week_end=week_end,
        gen_time=today.strftime("%Y-%m-%d %H:%M"),
        total_skus=total_skus,
        baseline_avg=baseline_avg,
        top_premium_scene=top_premium_str,
        alert_count=len(alerts),
        chart_bar=bar_b64,
        chart_heatmap=heat_b64,
        chart_trend=trend_b64,
        premium_rows=rows_html,
        alert_table=alert_table,
        suggestion=suggestion,
    )
    return html

# ============================================================
# 主流程
# ============================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", default="all")
    args = parser.parse_args()

    base = Path("data/reports")
    cats = ["sun_protect", "small_appliance", "camera_gear", "walkie_talkie"]
    target = cats if args.category == "all" else [args.category]

    summary_path = base / "summary.json"
    summary_data = {}
    if summary_path.exists():
        try:
            summary_data = json.loads(summary_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            summary_data = {}

    for cat in target:
        rj_path = base / cat / f"{cat}_premium_report.json"
        if not rj_path.exists():
            print(f"⚠️ 跳过 {cat}：未找到 {rj_path}")
            continue

        rj = json.loads(rj_path.read_text(encoding="utf-8"))
        rj["total_skus"] = summary_data.get(cat, {}).get("total_skus", 0)

        html = render_report(cat, rj, base / cat)
        out = base / cat / f"{cat}_weekly_report.html"
        out.write_text(html, encoding="utf-8")
        print(f"✅ 周报已生成：{out}")

    print("\n📬 使用方式：用浏览器打开 HTML → 另存为 PDF 发邮件")

if __name__ == "__main__":
    main()
