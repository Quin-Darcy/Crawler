import crawler
import os


def main():
    root = crawler.Crawler()
    root.set_start()
    root.burrow()
    root.show()
    os.system('killall firefox')


if __name__ == '__main__':
    main()
