# waifuc

[![PyPI](https://img.shields.io/pypi/v/waifuc)](https://pypi.org/project/waifuc/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/waifuc)
![Loc](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/narugo1992/847b3edfcbae29b86b8b5d8b3dfb854f/raw/loc.json)
![Comments](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/narugo1992/847b3edfcbae29b86b8b5d8b3dfb854f/raw/comments.json)

[![Code Test](https://github.com/deepghs/waifuc/workflows/Code%20Test/badge.svg)](https://github.com/deepghs/waifuc/actions?query=workflow%3A%22Code+Test%22)
[![Package Release](https://github.com/deepghs/waifuc/workflows/Package%20Release/badge.svg)](https://github.com/deepghs/waifuc/actions?query=workflow%3A%22Package+Release%22)
[![codecov](https://codecov.io/gh/deepghs/waifuc/branch/main/graph/badge.svg?token=XJVDP4EFAT)](https://codecov.io/gh/deepghs/waifuc)

![GitHub Org's stars](https://img.shields.io/github/stars/deepghs)
[![GitHub stars](https://img.shields.io/github/stars/deepghs/waifuc)](https://github.com/deepghs/waifuc/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/deepghs/waifuc)](https://github.com/deepghs/waifuc/network)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/deepghs/waifuc)
[![GitHub issues](https://img.shields.io/github/issues/deepghs/waifuc)](https://github.com/deepghs/waifuc/issues)
[![GitHub pulls](https://img.shields.io/github/issues-pr/deepghs/waifuc)](https://github.com/deepghs/waifuc/pulls)
[![Contributors](https://img.shields.io/github/contributors/deepghs/waifuc)](https://github.com/deepghs/waifuc/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/deepghs/waifuc)](https://github.com/deepghs/waifuc/blob/master/LICENSE)

Efficient Train Data Collector for Anime Waifu.

**This project is still under development, official version will be released soon afterwards.**

If you need to use it immediately, just clone it and run `pip install .`.

## Installation

You can simply install it with `pip` command line from the official PyPI site.

```shell
pip install waifuc
```

If your operating environment includes a available GPU, you can use the following installation command to achieve higher
performance:

```shell
pip install waifuc[gpu]
```

For more information about installation, you can refer
to [Installation](https://deepghs.github.io/waifuc/main/tutorials/installation/index.html).

## An Example

Grab surtr (arknights)'s dataset

```python
from waifuc.action import NoMonochromeAction, FilterSimilarAction, \
    TaggingAction, PaddingAlignAction, PersonSplitAction, FaceCountAction, FirstNSelectAction, \
    CCIPAction, ModeConvertAction, ClassFilterAction, RandomFilenameAction, AlignMinSizeAction
from waifuc.export import TextualInversionExporter
from waifuc.source import GcharAutoSource

if __name__ == '__main__':
    # data source for surtr in arknights, images from many sites will be crawled
    # all supported games and sites can be found at
    # https://narugo1992.github.io/gchar/main/best_practice/supported/index.html#supported-games-and-sites
    # ATTENTION: GcharAutoSource required `pip install waifuc[gchar]`
    s = GcharAutoSource('surtr')

    # crawl images, process them, and then save them to directory with given format
    s.attach(
        # preprocess images with white background RGB
        ModeConvertAction('RGB', 'white'),

        # pre-filtering for images
        NoMonochromeAction(),  # no monochrome, greyscale or sketch
        ClassFilterAction(['illustration', 'bangumi']),  # no comic or 3d
        # RatingFilterAction(['safe', 'r15']),  # filter images with rating, like safe, r15, r18
        FilterSimilarAction('all'),  # filter duplicated images

        # human processing
        FaceCountAction(count=1),  # drop images with 0 or >1 faces
        PersonSplitAction(),  # crop for each person
        FaceCountAction(count=1),

        # CCIP, filter the character you may not want to see in dataset
        CCIPAction(min_val_count=15),

        # if min(height, weight) > 800, resize it to 800
        AlignMinSizeAction(800),

        # tagging with wd14 v2, if you don't need character tag, set character_threshold=1.01
        TaggingAction(force=True),

        PaddingAlignAction((512, 512)),  # align to 512x512
        FilterSimilarAction('all'),  # filter again
        FirstNSelectAction(200),  # first 200 images
        # MirrorAction(),  # mirror image for data augmentation
        RandomFilenameAction(ext='.png'),  # random rename files
    ).export(
        # save to surtr_dataset directory
        TextualInversionExporter('surtr_dataset')
    )

```

Usage of 3-stage-cropper:

```python
from waifuc.action import ThreeStageSplitAction
from waifuc.export import SaveExporter
from waifuc.source import LocalSource

source = LocalSource('/your/path/contains/images')
source.attach(
    ThreeStageSplitAction(),
).export(SaveExporter('/your/output/path'))

```