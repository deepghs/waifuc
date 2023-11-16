from waifuc.source import DanbooruSource

if __name__ == '__main__':
    s = DanbooruSource(
        ['amiya_(arknights)', 'solo'],
        min_size=10000,
    )[:50]
    for item in s:
        print(item)
