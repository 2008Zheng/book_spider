import sys
from spiders.books_spider import BooksSpider
from spiders.quotes_spider import QuotesSpider

def main():
    print("=" * 50)
    print("      通用爬虫框架 - 多站点采集器")
    print("=" * 50)
    print()
    print("请选择要运行的爬虫：")
    print("  [1] 图书爬虫（books.toscrape.com）→ 1000 条")
    print("  [2] 名言爬虫（quotes.toscrape.com）→ 100 条")
    print("  [3] 全部运行")
    print("  [q] 退出")
    print()

    choice = input("请输入选项: ").strip()

    if choice == "1":
        BooksSpider().run()
    elif choice == "2":
        QuotesSpider().run()
    elif choice == "3":
        print("\n>>> 先运行图书爬虫 >>>")
        BooksSpider().run()
        print("\n>>> 再运行名言爬虫 >>>")
        QuotesSpider().run()
        print("\n🎉🎉🎉 全部任务完成！")
    elif choice.lower() == "q":
        print("退出。")
        sys.exit(0)
    else:
        print("无效选项，请重新运行。")

if __name__ == "__main__":
    main()
