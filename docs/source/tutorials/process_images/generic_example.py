from waifuc.source import LocalSource

if __name__ == '__main__':
    # define "source" to cache the data clawed from source.
    source = LocalSource('/data/mydataset')
    source = source.attach(
        XXXAction()  # now source's output will be items processed by XXXAction
    )  # and then they'll be cached by new "source" that is different
