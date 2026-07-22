import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False


# ============ 图书数据分析 ============
print("=" * 50)
print("   📊 图书数据分析报告")
print("=" * 50)

df = pd.read_csv("data/books.csv")
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df_valid = df[df["price"] > 0]

print(f"\n📌 总采集数量: {len(df)} 条（有效价格: {len(df_valid)} 条）")
print(f"📌 平均价格: £{df_valid['price'].mean():.2f}")
print(f"📌 最高价格: £{df_valid['price'].max():.2f}")
print(f"📌 最低价格: £{df_valid['price'].min():.2f}")
print(f"📌 价格中位数: £{df_valid['price'].median():.2f}")

# 评分分布
print("\n⭐ 评分分布:")
rating_counts = df["rating"].value_counts().sort_index()
for rating, count in rating_counts.items():
    bar = "█" * count
    print(f"  {rating:.0f} 星: {count:>4} 本  {bar}")

# 价格区间（仅对有价格的）
if len(df_valid) > 0:
    bins = [0, 20, 30, 40, 50, 60, 100]
    labels_price = ["£0-20", "£20-30", "£30-40", "£40-50", "£50-60", "£60+"]
    df_valid["price_range"] = pd.cut(df_valid["price"], bins=bins, labels=labels_price)
    price_dist = df_valid["price_range"].value_counts().sort_index()
    print("\n💰 价格区间分布:")
    for label, count in price_dist.items():
        bar = "█" * count
        print(f"  {label:<8}: {count:>4} 本  {bar}")
else:
    print("\n💰 价格区间分布: 无有效价格数据")
    price_dist = pd.Series({"无数据": 0})

# 最贵 / 最便宜（仅对有价格的）
if len(df_valid) > 0:
    print("\n📖 最贵的 5 本书:")
    top5 = df_valid.nlargest(5, "price")[["title", "price", "rating"]]
    for _, row in top5.iterrows():
        print(f"  {row['title']:.<50} £{row['price']:>6.2f}  ⭐{row['rating']:.0f}")

    print("\n📖 最便宜的 5 本书:")
    bottom5 = df_valid.nsmallest(5, "price")[["title", "price", "rating"]]
    for _, row in bottom5.iterrows():
        print(f"  {row['title']:.<50} £{row['price']:>6.2f}  ⭐{row['rating']:.0f}")
else:
    print("\n📖 最贵 / 最便宜: 无有效价格数据")

# 各评分平均价格
print("\n⭐ 各评分平均价格:")
if len(df_valid) > 0:
    avg_price_by_rating = df_valid.groupby("rating")["price"].mean().round(2)
    for rating, avg in avg_price_by_rating.items():
        print(f"  {rating:.0f} 星: 均价 £{avg:.2f}")
else:
    print("  无有效价格数据")


# ============ 名言数据分析 ============
print("\n" + "=" * 50)
print("   💬 名言数据分析报告")
print("=" * 50)

df_q = pd.read_csv("data/quotes.csv")
print(f"\n📌 总采集数量: {len(df_q)} 条")

# 作者出现次数 Top 10
print("\n👤 作者出现次数 Top 10:")
author_counts = df_q["author"].value_counts().head(10)
for author, count in author_counts.items():
    bar = "█" * count
    print(f"  {author:<25} {count:>3} 条  {bar}")

# 标签出现次数 Top 15
print("\n🏷 标签出现次数 Top 15:")
all_tags = []
for tags_str in df_q["tags"].dropna():
    all_tags.extend([t.strip() for t in tags_str.split(",")])
tag_counts = pd.Series(all_tags).value_counts().head(15)
for tag, count in tag_counts.items():
    bar = "█" * count
    print(f"  {tag:<20} {count:>3} 次  {bar}")


# ============ 画图 ============
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("📊 图书数据采集分析报告", fontsize=16, fontweight="bold")

# 图1: 评分分布
ax1 = axes[0, 0]
colors = ["#ff6b6b", "#feca57", "#48dbfb", "#ff9ff3", "#54a0ff"]
bars = ax1.bar(rating_counts.index.astype(str), rating_counts.values, color=colors[:len(rating_counts)])
ax1.set_title("⭐ 评分分布", fontsize=13, fontweight="bold")
ax1.set_xlabel("评分")
ax1.set_ylabel("数量")
for bar, count in zip(bars, rating_counts.values):
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
             str(count), ha="center", va="bottom", fontweight="bold")

# 图2: 价格分布直方图
ax2 = axes[0, 1]
ax2.hist(df["price"], bins=20, color="#54a0ff", edgecolor="white", alpha=0.85)
ax2.axvline(df["price"].mean(), color="red", linestyle="--", linewidth=2, label=f"均价 £{df['price'].mean():.2f}")
ax2.set_title("💰 价格分布", fontsize=13, fontweight="bold")
ax2.set_xlabel("价格 (£)")
ax2.set_ylabel("数量")
ax2.legend()

# 图3: 价格区间饼图（仅在有数据时画）
ax3 = axes[1, 0]
pie_data = price_dist.values
pie_labels = [str(x) for x in price_dist.index]

if pie_data.sum() > 0:
    explode = [0.05] * len(pie_data)
    ax3.pie(pie_data, labels=pie_labels, autopct="%1.1f%%",
            colors=["#ff6b6b", "#feca57", "#48dbfb", "#ff9ff3", "#54a0ff", "#5f27cd"],
            explode=explode, startangle=90)
    ax3.set_title("💰 价格区间占比", fontsize=13, fontweight="bold")
else:
    ax3.text(0.5, 0.5, "价格数据不可用\n（网站 JS 动态渲染）",
             ha="center", va="center", fontsize=12, color="gray")
    ax3.set_title("💰 价格区间占比（无数据）", fontsize=13, fontweight="bold")

# 图4: 名言标签 Top 10
ax4 = axes[1, 1]
top_tags = tag_counts.head(10)
y_pos = range(len(top_tags))
ax4.barh(list(reversed(y_pos)), list(reversed(top_tags.values)), color="#ff6b6b", edgecolor="white")
ax4.set_yticks(y_pos)
ax4.set_yticklabels(reversed(top_tags.index))
ax4.set_title("🏷 名言标签 Top 10", fontsize=13, fontweight="bold")
ax4.set_xlabel("出现次数")

plt.tight_layout()
plt.savefig("data/analysis_report.png", dpi=150, bbox_inches="tight")
print("\n📊 图表已保存到: data/analysis_report.png")

plt.show()
