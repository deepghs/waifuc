Training a LoRA for My Waifu
======================================

Before we dive in, please note the following:

1. You should have Python installed and a basic understanding of Python. For Python tutorials, you can refer to `https://python.swaroopch.com/ <https://python.swaroopch.com/>`_.
2. **Complete the installation of the waifuc library.** Check out the installation guide `here <https://deepghs.github.io/waifuc/main/tutorials/installation/index.html>`_.

What Should I Do?
-------------------------------

1. First, get to know your waifu, especially her name and origin. For example, my waifu is the beautiful demon girl with red hair named Surtr from the mobile game Arknights.

    .. image:: surtr.png
        :align: center

2. **Find her on an image website and note the search keywords.** For Surtr, you can use the tag ``surtr_(arknights)`` on `Danbooru <https://danbooru.donmai.us/>`_ to find her images.

    .. image:: danbooru_surtr.png
        :align: center

3. Save the following code in a file named ``crawl.py``:

    .. literalinclude:: danbooru_surtr.py
        :language: python
        :linenos:

4. Run the following command to execute the code:

    .. code:: shell

        python crawl.py


5. After running the code, open the ``/data/surtr_dataset`` folder to find surtr's training dataset. It contains 200 images, each with a corresponding txt file for tags.

    .. image:: danbooru_crawled.png
        :align: center

6. Congratulations! You can now use the ``/data/surtr_dataset`` folder for LoRA training. 🎉

How Does the Code Work?
-------------------------------------

In the provided code, we've constructed a comprehensive pipeline using waifuc, encompassing three main components, which are also the primary modules of waifuc:

1. **Data Source (Source):** Responsible for loading data into the pipeline.

    - ``DanbooruSource``: Used to **crawl images from the Danbooru website and load them into the pipeline**. In this example, we perform image retrieval on Danbooru using the tag ``surtr_(arknights)``.

2. **Data Processing (Action):** Processes the loaded image data.

    - ``ModeConvertAction``: **Converts image formats**; in this example, it converts to the RGB format and adds a white background to transparent images.

    - ``NoMonochromeAction``: **Filters monochrome images** (greyscale, line art, monochrome comics, etc.).

    - ``ClassFilterAction``: Filters specified types of images; in this example, it **retains only `illustration` (illustrations) and `bangumi` (anime screenshots)**, while `comic` (comics) and `3D` (3D images like those from Koikatsu and MikuMikuDance) are filtered out.

    - ``FilterSimilarAction``: **Filters similar images** to prevent duplicate images from entering the dataset.

    - ``FaceCountAction``: **Filters images based on the number of faces**; in this example, it keeps only images with exactly one face and filters out images with no faces or multiple faces.

    - ``PersonSplitAction``: **Splits images to isolate individual characters** within the picture.

    - ``CCIPAction``: **Filters out irrelevant characters introduced into the pipeline**; in this example, images of characters other than Surtr are filtered out.

    - ``AlignMinSizeAction``: **Compresses oversized images**; in this example, it resizes images with a short side longer than 800 pixels to ensure the short side does not exceed 800 pixels.

    - ``TaggingAction``: **Applies tagging to images using wd14v2 tagger**; in this example, as the images are sourced from Danbooru, which already includes tag information, setting `force` to `True` instructs the tagger to reapply tags.

    - ``FirstNSelectAction``: **Retains only the first several images**; when the number of images reaching this step reaches the set quantity (200 in this example), the pipeline terminates further crawling and processing.

    - ``RandomFilenameAction``: **Randomly renames images** and uses ``.png`` as the file extension when saving.

3. **Data Export (Exporter):** Exports the processed data.

    - ``TextualInversionExporter``: Exports the processed data in the format of images and txt labels to the specified path (``/data/surtr_dataset`` in this case).

The overall process is illustrated below:

.. image:: sample_workflow.puml.svg
    :align: center

Building upon this foundation, you can:

1. **Replace the data source** to **crawl data from other websites**. We support various data sources for different websites, including Pixiv, Sankaku, Rule34, AnimePictures, Zerochan, Konachan, Duitang, Huashi6, and more.
2. If you have images in your **local folder**, you can use ``LocalSource`` to **load them into the pipeline** for processing.
3. **Add or remove Actions** to modify the data filtering and processing flow.
4. **Replace the Exporter** to save images in different formats to meet diverse data usage requirements.

The comprehensive workflow is presented above. This flexible and customizable structure allows you to adapt the pipeline to various scenarios.

Good News!
-------------------------------------

After reviewing the example, you may notice that the pipeline requires finding character tags on image websites before loading data into the pipeline. This process seems cumbersome, requiring manual user intervention.

The good news is, we've partially solved this problem! **You can now input the character's name directly (in Chinese, Japanese, or English), and the pipeline will automatically generate data sources from various websites for data crawling.**

To use this feature, install the additional dependency:

.. code:: shell

    pip install git+https://github.com/deepghs/waifuc.git@main#egg=waifuc[gchar]

This library, gchar, contains a pre-built character database with character tables for several mobile games and corresponding tags on various image websites. It currently supports limited games, including Genshin Impact, Arknights, Azur Lane, Blue Archive, Girls’ Front-Line, and more. All the supported games are listed `here <https://narugo1992.github.io/gchar/main/best_practice/supported/index.html>`_.

Replace ``s = DanbooruSource(['surtr_(arknights)'])`` with ``s = GcharAutoSource('surtr')`` in the code to automatically select the most suitable data source for your character. The full code looks like this:

.. literalinclude:: gchar_surtr.py
    :language: python
    :linenos:

Now you can enjoy automatic data source selection for data crawling. Happy training! 🚀
