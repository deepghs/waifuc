我想从视频中获取角色图像
========================

安装额外依赖
------------

waifuc同样提供了从视频中获取图像的方法

在开始运行之前首先需要安装额外的依赖，其中包含\ ``pyav``\
库，以便对视频进行处理：

    .. code:: shell

       pip install git+https://github.com/deepghs/waifuc.git@main#egg=waifuc[video]

从视频文件中获取图像
--------------------

在waifuc中，可以使用\ ``VideoSource``\
对视频文件进行抽帧处理，并以图像的形式保存到给定的路径中，如下所示：

    .. literalinclude:: video_simple.py
        :language: python
        :linenos:

保存的图像如下所示：

    .. image:: video_simple.png
        :align: center

从包含视频的文件夹中获取图像
----------------------------

在此基础上，很多情况下，我们需要对下载好的一整部动漫系列视频进行处理，而他们常常被放在同一个文件夹中

为此我们可以直接从包含视频的文件夹中进行抽帧，如下所示：

    .. literalinclude:: video_dir.py
        :language: python
        :linenos:

该代码将对\ ``/data/videos``\ 路径下的全部视频文件进行逐一抽帧，并保存至\ ``/data/dstdataset``\ 文件夹

从包含视频的文件夹中获取角色图像
--------------------------------

在上述代码的基础上，我们只需要为其添加\ ``PersonSplitAction``\
即可从视频文件夹中截取人像图像，如下所示：

    .. literalinclude:: video_split.py
        :language: python
        :linenos:

上述代码从视频中抽帧，并从抽取的图像中截取人像保存下来，如下所示：

    .. image:: video_split.png
        :align: center

不过看起来似乎有一些图像并不适合用于训练。因此在实际的动漫视频中，可以通过添加更多的\ ``Action``\来获得更高质量的训练数据集。例如下面的代码：

    .. literalinclude:: video_split_better.py
        :language: python
        :linenos:

最终将得到如下的数据集

    .. image:: video_split_better.png
        :align: center