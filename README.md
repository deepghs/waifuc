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
import os

from waifuc.action import AlignMaxSizeAction, NoMonochromeAction, FilterSimilarAction,
    TaggingAction, PaddingAlignAction, PersonSplitAction, FaceCountAction, FirstNSelectAction,
    CCIPAction, ModeConvertAction, ClassFilterAction, FileOrderAction
from waifuc.export import TextualInversionExporter
from waifuc.source import SankakuSource, PostOrder, PixivSearchSource, DanbooruSource,
    ZerochanSource, AnimePicturesSource

if __name__ == '__main__':
    s1 = PixivSearchSource('スルト(アークナイツ)', sort='popular_desc', no_ai=True,
                           refresh_token=os.environ['PIXIV_REFRESH_TOKEN'])
    s2 = DanbooruSource(['surtr_(arknights)'], username='username', api_key='api_key')
    s3 = SankakuSource(
        ['surtr_(arknights)', '-ai-created'],
        order=PostOrder.QUALITY,
        # rating=Rating.SAFE,
        username='username', password='password',
    )
    s4 = ZerochanSource('Surtr (Arknights)', strict=True)
    s5 = AnimePicturesSource(['surtr (arknights)'])

    # grab from zerochan and anime pictures first
    # and when up to 70, grab from pixiv, danbooru and sankaku
    s = (s4 | s5).attach(FaceCountAction(1))[:70] + (s1 | s2 | s3)

    s.attach(
        ModeConvertAction('RGB', 'white'),
        NoMonochromeAction(),  # no monochrome, greyscale or sketch
        ClassFilterAction(['illustration', 'bangumi']),  # no comic or 3d
        # RatingFilterAction(['safe', 'r15']),
        FilterSimilarAction('all'),  # filter similar images
        FaceCountAction(count=1),  # 1 face per image
        PersonSplitAction(),  # cut for each person
        FaceCountAction(count=1),
        FileOrderAction(),  # Rename files in order
        CCIPAction(min_val_count=15),  # CCIP, filter the character you may not wanna see in dataset
        AlignMaxSizeAction(800),
        TaggingAction(force=True),  # tagging with wd14 v2
        PaddingAlignAction((512, 512)),  # align to 512x512
        # RandomFilenameAction(),
        FilterSimilarAction('all'),  # filter again
        FirstNSelectAction(200),  # first 200 images
        # MirrorAction(),  # mirror then for augmentation
        # RandomFilenameAction(),  # random rename files
    ).export_item(TextualInversionExporter('surtr_dataset'))  # save to surtr_dataset directory

```
