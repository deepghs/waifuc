我想给我老婆炼丹
================

在本教程开始之前，你需要完成如下内容：

1. 首先，\ **安装Python并掌握基本用法**

   (\ **Python3**\ 教程，外部链接详见：

   中文：\ https://www.runoob.com/python3/python3-tutorial.html

   英文：\ https://python.swaroopch.com/ )

2. 之后，\ **完成waifuc库安装**

   (本项目安装详见：\ https://deepghs.github.io/waifuc/main/tutorials-CN/installation/index.html )

我该怎么做？
----------------------

1. 第一步，找到你一见钟情的老婆，\ **记住她的名字和出处**

   比如，Narugo的老婆是下面这位红发的恶魔女孩

   **她叫史尔特尔**\ ``Surtr``\ ，\ **出处为明日方舟**\ ``Arknights``

    .. image:: surtr.png
        :align: center

2. **在图像站上，找到她对应的人物关键词**

   例如对于史尔特尔，可以在\ `Danbooru <https://danbooru.donmai.us/>`__\ 上找到她的关键词\ ``surtr_(arknights)``

    .. image:: danbooru_surtr.png
        :align: center

3. 接着，创建一个名为\ ``crawl.py``\ 的Python程序文件，将以下代码粘贴进去并保存：

    .. literalinclude:: danbooru_surtr.py
        :language: python
        :linenos:

4. 执行以下的命令来运行上一步的程序：

    .. code:: shell

        python crawl.py

5. 等待程序运行完毕，打开为其指定的\ ``./data/surtr_dataset``\ 文件夹，你将看到包含200图的史尔特尔数据集，且已经完成了标注，即与图像同名的txt文件

    .. image:: danbooru_crawled.png
        :align: center

6. 按照以上内容如法炮制，仅需稍作等待，我们便可以轻易地得到任何想要的角色数据集

上文提供的代码是如何运行的？
-------------------------------------

在上文中，我们使用waifuc搭建了一条图像从爬取到输出的完整流水线。流水线分为三个部分，同时也对应了waifuc的三个主要组件：

- 数据源组件\ ``Source``\，\ **加载图像数据加入流水线**

  在本例中使用：

  - ``DanbooruSource``\ ，\ **从Danbooru图像站爬取图像数据并加入流水线**

      在Danbooru上按照关键词 ``surtr_(arknights)`` 进行检索并爬取

- 图像操作组件\ ``Action``\ ，\ **对图像进行处理与筛选**

  在本例中使用：

  - ``ModeConvertAction``\ ，\ **对图像进行格式转换处理**

      本例中转换为RGB色彩格式，并对透明背景的图添加白色背景

  - ``NoMonochromeAction``\ ，\ **对图像进行单色图过滤**

      过滤掉黑白图、线稿、单色漫画等

  - ``ClassFilterAction``\ ，\ **对图像进行类型过滤**

      本例中只保留\ **插画**\ ``illustration``\ 和\ **番剧截图**\ ``bangumi``\ 两种图像
      **漫画**\ ``comic``\和\ **恋活、MMD等**\ ``3D``\ 图像将被过滤

  - ``FilterSimilarAction``\ ，\ **对图像进行相似过滤**

      过滤掉相似度高的图像

  - ``FaceCountAction``\ ，\ **对图像进行人像数量过滤**

      本例中只保留单一人像的图像，无人像或多人像的图像将被过滤

  - ``PersonSplitAction``\ ，\ **对图像进行人物拆分处理**

      将图像中的所有人物以单一人物为单位裁出为多个图像

  - ``CCIPAction``\ ，\ **对图像进行人物相关过滤**

      本例中将过滤掉非surtr角色的图像

  - ``AlignMinSizeAction``\ ，\ **对图像进行压缩处理**

      本例中将短边长度超过800像素的图像等比例缩放至短边为800像素

  - ``TaggingAction``\ ，\ **对图像使用wd14v2 tagger进行打标处理**

      本例中由于爬取的图像来自Danbooru，本身包含提示词信息，因此需要将\ ``force``\ 设置为\ ``True``\ 来让打标器重新打标

  - ``FirstNSelectAction``\ ，\ **对图像进行取前N个处理**

      当到达这一步的图像达到设置数量时，终止之前的所有操作

      本例中设置数量为200，满足时将停止继续对后续图像的爬取和操作

  - ``RandomFilenameAction``\ ，\ **对图像进行随机命名处理**

      本例中将图像进行随机重命名，并使用\ ``.png``\ 作为图像保存为图像文件时的扩展名

- 图像导出组件\ ``Exporter``\ ，\ **将图像以指定形式导出至目录**

   在本例中使用：

  - ``TextualInversionExporter``\ ，**将图像以图像文件+标注格式导出至目录**

      以图像文件+txt标注文件形式保存处理完毕的图像到指定路径

      本例中保存至\ ``./data/surtr_dataset``\ 路径

感谢Narugo保留的PlantUML源代码，汉化流程图如下：

    .. image:: sample_workflow.puml.svg
        :align: center

.. note:: 对以上内容的补充：

    - **可通过替换** \ ``Source``\ **中的其他数据源来从其他的网站爬取图像数据**

       - ``Source``\ 支持大部分图像站的数据源，包括\ **Pixiv、Sankaku、Rule34、AnimePictures、Zerochan、Konachan、堆糖（duitang）、触站（huashi6）**\ 等

    - **可通过**\ ``Source``\ **中的**\ ``LocalSource``\ **数据源加载本地目录来获取图像数据**

       - ``Source``\ 中的\ ``LocalSource``\ 数据源可用来加载指定的本地目录，以获取图像数据

    - **可通过增减、排序**\ ``Action``\ **中的操作根据具体需求来构建工作流程**

       - waifuc支持调用\ ``Source``\ 的\ ``attach``\ 方法，以增减、排序的模块化方式为图像添加\ ``Action``\ 中的操作，有相当高的自由度与灵活性

    - **可通过**\ ``Exporter``\ **中的其他导出来将图像以其他形式导出**

       - ``Exporter``\ 提供了数种导出，以适应不同情况的使用需求

好消息！
--------

上面的例子中，需要用户先从图像站上获取需要的关键词，才能进行检索——这简直太“繁琐”了！DeepGHS也觉得，这样太麻烦了，甚至还需要用户进行手动操作！

不过好消息是，DeepGHS团队已经一定程度上解决了这个问题——团队提供了一个\ **额外的、支持多语言输入的、可以直接使用角色名字的数据源**

.. note:: 让我介绍一下gchar：

    ``gchar``\为\ ``Source``\ 的扩展包，包含了\ **一个预置的角色数据库，对目前主流二游的所有角色支持：**

   - **中/日/英官方名称检索**
   - **神秘网友援助的别名/外号检索**

(具体支持列表详见：\ https://narugo1992.github.io/gchar/main/best_practice/supported/index.html#supported-games-and-sites )

这个包通过如下命令进行安装：

    .. code:: bash

        pip install git+https://github.com/deepghs/waifuc.git@main#egg=waifuc[gchar]



``gchar``\目前已经完全支持明日方舟\ ``Arknights``\ 的角色数据，史尔特尔的当然也包括在其中

因此，我们只需\ **从**\ ``Source``\ **中导入**\ ``GcharAutoSource``

并\ **将**\ ``s = DanbooruSource(['surtr_(arknights)'])``\ **替换为**\ ``s = GcharAutoSource('surtr')``\ **或**\ ``s = GcharAutoSource('史尔特尔')``\ 即可

当然，上面提到了，\ **角色的外号与别称也是被允许的，不过相较于官方名称来说，覆盖程度会较窄**

完整代码如下：

    .. literalinclude:: gchar_surtr.py
        :language: python
        :linenos: