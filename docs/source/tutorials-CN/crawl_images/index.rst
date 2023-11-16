我想从网站上爬取一些数据
========================

如何从网站爬取数据？
--------------------

实际上，\ **waifuc能爬取的网站远远不止Danbooru一个**

不过在正式开始之前，Narugo要介绍他的另一位老婆，可爱的小兔娘\ **阿米娅**\ ``amiya``\ ，同样来自\ **明日方舟**\ ``Arknights``

以下为Narugo发癫内容：你问我为什么有这么多老婆？众所周知，二次元爱好者的老婆有无限多个，她们都是我的天使\ **😍**

    .. image:: amiya.png
        :align: center

Zerochan
~~~~~~~~

`Zerochan <https://zerochan.net/>`__\ 是一个包含图像平均质量较高的网站，我们可以使用极为简单的方式进行爬取

**当我们不需要大批量的获取图像，而只需要50张图像时**\ ，可以使用以下代码实现：

    .. literalinclude:: zerochan_simple_50.py
        :language: python
        :linenos:

请注意，\ **此处使用**\ ``SaveExporter``\ **导出，而非之前的**\ ``TextureInversionExporter``\ **导出**\ ，关于它的作用将在本篇后续部分进行介绍

上述爬取到的图像数据将被导出到\ **指定的**\ ``./data/amiya_zerochan``\ **本地路径**\ 下，结果如下：

    .. image:: zerochan_simple_50.png
        :align: center

然而，我们会发现一个问题：

Zerochan上有较多的member-only的图像，我们需要登录后才能获取它们

为此我们可以\ **使用自己的用户名**\ ``username``\ 和\ **密码**\ ``password``\ 进行鉴权，以获得更多、更优质的图像，代码如下：

    .. literalinclude:: zerochan_login_50.py
        :language: python
        :linenos:

再次运行，果然我们成功获取到了不少的member-only图像：

    .. image:: zerochan_login_50.png
        :align: center

不过我们又发现，这些图像很多分辨率并不高，边长超过1000像素的不多

这是因为\ **Zerochan会默认选用**\ ``large``\ **尺寸的图像**\ ，以提高下载速度

如果需要更大尺寸的图像，可以将\ **尺寸选择**\ ``select``\ 设置为\ ``full``\ ，就像这样：

    .. literalinclude:: zerochan_login_50_full.py
        :language: python
        :linenos:

再再次运行后，得到的将全都是全尺寸的图像

然而，依然还存在一个问题：高质量图片中很多都是官方画作，而阿米娅作为游戏的女主角，更是常作为C位出现在多人图中

**我们实际上只需要仅包含她自己的图像**\ ，这当然是没问题，只需要将\ **严格搜索模式**\ ``strict``\ 设置为\ ``True``\ 即可：

    .. literalinclude:: zerochan_login_50_full_strict.py
        :language: python
        :linenos:

再再再次运行，我们最终得到了来自Zerochan的高质量、全尺寸且均为阿米娅单人的图像，如下所示：

    .. image:: zerochan_login_50_full_strict.png
        :align: center

Danbooru
~~~~~~~~

理所当然，\ `Danbooru <https://danbooru.donmai.us/>`__\也是可以轻松被waifuc爬取的，使用十分简单：

    .. literalinclude:: danbooru_50.py
        :language: python
        :linenos:

以及，\ **在Danbooru及其类似网站可通过添加**\ ``solo``\ **关键词来直接筛选单人图像**\ ，以节省操作步骤，就像这样：

    .. literalinclude:: danbooru_50_solo.py
        :language: python
        :linenos:

Pixiv
~~~~~

waifuc\ **支持对**\ `Pixiv <https://www.pixiv.net/>`__\ **的多种爬取方式：关键词检索、用户检索以及各种排行榜爬取**

我们可以使用\ ``PixivSearchSource``\ 数据源来进行关键词检索方式的图像数据爬取，如下所示：

    .. literalinclude:: pixiv_50.py
        :language: python
        :linenos:

我们也可以使用\ ``PixivUserSource``\ 数据源来进行检索方式的图像数据爬取，如下所示：

    .. literalinclude:: pixiv_50_user.py
        :language: python
        :linenos:

我们还可以使用\ ``PixivRankingSource``\ 数据源来进行可选择的排行榜的图像数据爬取，如下所示：

    .. literalinclude:: pixiv_50_ranking.py
        :language: python
        :linenos:

Anime-Pictures
~~~~~~~~~~~~~~

`Anime-Pictures <https://anime-pictures.net/posts?search_tag=amiya+%28arknights%29&lang=en&page=0>`__\的图像数量不多，但是质量普遍很高

因此waifuc也同样支持对它的爬取，如下所示：

    .. literalinclude:: anime_pictures_50.py
        :language: python
        :linenos:

Sankaku
~~~~~~~

`Sankaku <https://chan.sankakucomplex.com/>`__\的图像数量庞大且种类很多

waifuc同样支持了它，如下所示：

    .. literalinclude:: sankaku_50.py
        :language: python
        :linenos:

Gelbooru
~~~~~~~~

`Gelbooru <https://gelbooru.com/>`__\与Danbooru的内容很相似，但在一些特定内容上有更多图像

waifuc同样它支持的爬取，如下所示：

    .. literalinclude:: gelbooru_50.py
        :language: python
        :linenos:

Duitang
~~~~~~~

`Duitang <https://www.duitang.com/>`__\是一个来自中国的网站，因其建站时间较长，也包含不少优质的图像

应中国用户的请求，Narugo为waifuc添加了针对堆糖(duitang)的支持，如下所示：

    .. literalinclude:: duitang_50.py
        :language: python
        :linenos:

其余受支持的图像站
~~~~~~~~~~~~~~~~~~

除了上述的这些外，waifuc还支持了大量其他的图像站。\ **所有受支持图像站**\ 如下所示：

-  `ATFBooruSource <https://booru.allthefallen.moe/>`__
-  `AnimePicturesSource <https://anime-pictures.net/>`__
-  `DanbooruSource <https://danbooru.donmai.us/>`__
-  `DerpibooruSource <https://derpibooru.org/>`__
-  `DuitangSource <https://www.duitang.com/>`__
-  `E621Source <https://e621.net/>`__
-  `E926Source <https://e926.net/>`__
-  `FurbooruSource <https://furbooru.com/>`__
-  `GelbooruSource <https://gelbooru.com/>`__
-  `Huashi6Source <https://www.huashi6.com/>`__
-  `HypnoHubSource <https://hypnohub.net/>`__
-  `KonachanNetSource <https://konachan.net/>`__
-  `KonachanSource <https://konachan.com/>`__
-  `LolibooruSource <https://lolibooru.moe/>`__
-  `PahealSource <https://rule34.paheal.net/>`__
-  `PixivRankingSource <https://pixiv.net/>`__
-  `PixivSearchSource <https://pixiv.net/>`__
-  `PixivUserSource <https://pixiv.net/>`__
-  `Rule34Source <https://rule34.xxx/>`__
-  `SafebooruOrgSource <https://safebooru.org/>`__
-  `SafebooruSource <https://safebooru.donmai.us/>`__
-  `SankakuSource <https://chan.sankakucomplex.com/>`__
-  `TBIBSource <https://tbib.org/>`__
-  `WallHavenSource <https://wallhaven.cc/>`__
-  `XbooruSource <https://xbooru.com/>`__
-  `YandeSource <https://yande.re/>`__
-  `ZerochanSource <https://www.zerochan.net/>`__

(关于上述\ ``Source``\ 的更多信息和使用细节，详见waifuc源代码)

我想从多个网站上爬取数据
------------------------

在一些情况中，我们希望从多个网站获取图像数据

比如下面的情况中，我们需要从Danbooru上获取30张图像，再从zerochan上获取30张图像

为满足此类需求，waifuc提供了\ ``Source``\ 间的串并联操作，可以通过串联\ ``+``\ 和并联\ ``|``\ 将多个数据源进行集成

例如在上面的需求中，我们可以将Danbooru数据源和Zerochan数据源进行串联，形成新的数据源，如下所示：

    .. literalinclude:: source_concat.py
        :language: python
        :linenos:

上述代码将先从Danbooru爬取30张图像，再从Zerochan爬取30张图像

这样，我们可以得到如下的数据集：

    .. image:: source_concat.png
        :align: center

除此之外，在部分情况下，我们可能并不会提前设计好从各个数据源爬取多少图像，而是希望能尽量多地从不同数据源爬取，并最终得到一个需要的总数量。在这种情况下，我们可以使用并联操作，如下所示：

    .. literalinclude:: source_union.py
        :language: python
        :linenos:

在这一次爬取中，将从两个站中随机选择进行爬取，直至爬取到60张图像为止

因此实际上最终获得的数据集并不确定，以下数据集仅供参考：

.. image:: source_union.png
    :align: center

所有的\ ``Source``\ 间也可以进行复杂的嵌套运算，以构建一个复杂的数据源：

    .. literalinclude:: source_complex.py
        :language: python
        :linenos:

此处就构建了一个复杂的数据源
``s = s_zerochan[:50] + (s_db | s_pixiv)[:50]``\ ，具体功能为：

-  先从Zerochan上爬取50张图像
-  再从Danbooru和Pixiv上随机爬取，共计50张图像

因此这个数据源最终将爬取以Zerochan为主的100张图像

``Source``\ 的串并联操作还可以在\ ``attach``\ 方法之后进行，即进行预处理后，再进行串并联

例如：

    .. literalinclude:: source_complex_attach.py
        :language: python
        :linenos:

上述代码的效果是：

-  从Zerochan和Danbooru两个网站上爬取图像
-  Zerochan的图像需要进行去背景处理，而Danbooru上的不需要
-  两个数据源总计爬取60张图像

得到的结果如下所示，可以看到，zerochan的图像都进行了去背景处理：

.. image:: source_complex_attach.png
    :align: center

通过以上演示可以了解，串并联是\ ``Source``\ 的一项重要特性，合理利用将让配置多样化且极富灵活性

为什么会有这么多json文件？
--------------------------

如果你坚持读到了这里，你应该会注意到示例图中的一个问题

上述所有使用\ ``SaveExporter``\ 进行保存的数据集，每个图像文件都有与其同名的json文件

你一定会感到好奇，这些json文件是做什么用的？我该如何关闭它们的生成？

该部分将对此一一作出解答

首先，我们打开一个其中的json文件\ ``.danbooru_6814120_meta.json``\ ，并查看里面的内容：

    .. collapse:: A Sample Meta-Information JSON

        .. literalinclude:: meta_json.json
            :language: json
            :linenos:

内容比较长，\ **简单来说，这是一个存储图像文件元数据**\ ``meta-information``\ **文件**

它包含了以下的信息：

-  来自danbooru网站的图像信息，即图像的tag、尺寸、ID、上传时间等
-  图像的url信息，即图像是从哪里被下载的
-  图像的命名信息，即图像将被保存为什么文件名
-  图像的tag信息，即当生成训练用的数据集时，其tag将包含哪些

这些信息在一些处理环节中，将发挥其应有的作用

例如tag信息，生成该信息需要从网站进行爬取，或者使用tagger进行打标，而该信息将在产生LoRA训练数据集时进行写入

因此在waifuc中，默认对json文件进行保存，并且可以使用\ ``SaveExporter``\ 进行保存

为了充分利用这些元数据，我们\ **可以使用**\ ``LocalSource``\ **将包含json文件的本地数据集通过**\ ``SaveExporter``\ **再次加载**\ ：

    .. literalinclude:: local.py
        :language: python
        :linenos:

以上代码可以将包含元数据的本地数据集再次载入，并按照LoRA训练数据集的格式进行再次保存，即只保留存储标注信息的txt文件

处理后的数据集如下所示：

    .. image:: local_to_dataset.png
        :align: center

.. note:: 值得注意的是:

    - \ ``LocalSource``\ **对所有本地的数据集都可进行加载，并不一定需要元数据**

    - 若没有json文件，得到的图像数据将不包含初始元数据，这意味着tag等信息必须重新生成

    - \ ``LocalSource``\ **作为一种**\ ``Source``\ **，也可以进行串并联操作，因此你可以同时使用来自网络和本地的图像构建数据集**

当你确定只需要图像，不需要任何元数据时，设置参数\ ``no_meta``\为\ ``True``\来实现这一点：

    .. literalinclude:: save_no_meta.py
        :language: python
        :linenos:

这样的代码将不会保存任何json文件，将只爬取50张图像，如下所示：

    .. image:: save_no_meta.png
        :align: center

我不想将图像保存到硬盘上，如何直接使用它们？
--------------------------------------------

你可能不希望将图像文件缓存到硬盘上，而是直接在内存中处理以节省时间

    .. literalinclude:: iterate_usage.py
        :language: python
        :linenos:

没错，\ **所有**\ ``Source``\ **都是可以作为List进行遍历操作的**

而其中的item，其类型定义如下：

    .. literalinclude:: item_definition.py
        :language: python
        :linenos:

不难发现，每一个item的结构十分简单，包含一个\ ``PIL.Image``\ 结构的图像对象和一个用于存储元信息的\ ``meta``\项。

获取到item项后，你将可以自行使用其图像对象和元数据定制所需要的操作。
