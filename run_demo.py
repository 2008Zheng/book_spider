"""
run_demo.py · 一键演示
===================
1) 生成 4 品类模拟数据
2) 跑场景溢价分析（出图 + JSON 报告）
3) 生成 4 份 HTML 周报

真实环境只需把 mock_xxx() 替换为：parser 输出 + SQLite 读取
"""

"""
run_demo.py · 一键演示（自动打开 HTML 周报 · 稳定版）
"""

import sys
import os
from pathlib import Path

# ---------- 路径锁定 ----------
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
    BASE_DIR = Path(os.path.dirname(sys.executable))
else:
    BASE_DIR = Path(__file__).parent

def open_html(path: Path):
    """用系统默认程序打开 HTML（Windows 最稳方案）"""
    if not path.exists():
        print(f"  ⚠️ 文件不存在：{path}")
        return
    abs_path = str(path.resolve())
    print(f"  🔗 尝试打开：{abs_path}")

    # 方案 1：os.startfile（Windows 原生，最稳）
    try:
        os.startfile(abs_path)
        print(f"  ✅ os.startfile 成功")
        return
    except Exception as e:
        print(f"  ⚠️ os.startfile 失败：{e}")

    # 方案 2：webbrowser 兜底
    try:
        import webbrowser
        webbrowser.open(path.resolve().as_uri())
        print(f"  ✅ webbrowser 成功")
    except Exception as e:
        print(f"  ❌ 自动打开失败：{e}")

def main():
    print("=" * 60)
    print("  PriceLens · 4 品类场景溢价分析 · 一键演示")
    print("=" * 60)

    # Step 1: 分析
    print("\n▶ Step 1/3: 场景溢价分析")
    if getattr(sys, 'frozen', False):
        import analyze_scene
        analyze_scene.main()
    else:
        import subprocess
        subprocess.run([sys.executable, "analyze_scene.py", "--category", "all"], check=True)

    # Step 2: 周报
    print("\n▶ Step 2/3: 生成周报")
    if getattr(sys, 'frozen', False):
        import gen_weekly_report
        gen_weekly_report.main()
    else:
        import subprocess
        subprocess.run([sys.executable, "gen_weekly_report.py", "--category", "all"], check=True)

    # Step 3: 打开浏览器
    print("\n▶ Step 3/3: 打开周报")
    for cat in ["sun_protect", "small_appliance", "camera_gear", "walkie_talkie"]:
        html = BASE_DIR / "data" / "reports" / cat / f"{cat}_weekly_report.html"
        open_html(html)

    print("\n" + "=" * 60)
    print("  ✅ 全部完成！浏览器应已弹出 4 份周报")
    print("=" * 60)

    if getattr(sys, 'frozen', False):
        input("\n按回车键退出...")

if __name__ == "__main__":
    main()
