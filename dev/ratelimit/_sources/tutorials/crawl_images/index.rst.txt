Crawling Some Images From Websites
=================================================

(Chinese Doc：\ https://deepghs.github.io/waifuc/main/tutorials-CN/crawl_images/index.html )

How to Crawl Data From Websites?
----------------------------------------------

In fact, **waifuc can crawl from many websites, not just Danbooru**. But before we get started, allow me to formally introduce my another waifu, Amiya, a cute bunny girl. (You may ask why I have so many waifus. Well, as you know, anime lovers have an infinite number of waifus; they are all my honey and angels **😍**)

.. image:: amiya.png
    :align: center

Zerochan
~~~~~~~~~~~~~~~~~~~~~~

`Zerochan <https://zerochan.net/>`_ is a website with many high-quality images. We can crawl from it in a straightforward way. Considering we only need 50 images due to the large quantity, the following code achieves this:

.. literalinclude:: zerochan_simple_50.py
    :language: python
    :linenos:

Please note that we use ``SaveExporter`` here instead of the previous ``TextureInversionExporter``. Its function will be explained in the following sections. The data crawled here will be stored locally in the ``/data/amiya_zerochan`` directory, as shown below:

.. image:: zerochan_simple_50.png
    :align: center

However, we've noticed an issue—Zerochan has many member-only images, requiring login to access. To address this, we can use our username and password for authentication to obtain more and higher-quality images:

.. literalinclude:: zerochan_login_50.py
    :language: python
    :linenos:

Indeed, we successfully obtained many member-only images, as shown below:

.. image:: zerochan_login_50.png
    :align: center

However, many of these images have relatively low resolutions, with few exceeding 1000 pixels in either dimension. This is because Zerochan defaults to using the ``large`` size to speed up downloads. If you need larger images, you can modify the size selection like this:

.. literalinclude:: zerochan_login_50_full.py
    :language: python
    :linenos:

After crawling, all the images will be in full size.

However, there's still an issue—many high-quality images are official promotional art, and since Amiya is a main character, she often appears in group art. **We actually need images that only feature her**. No problem, just set the search mode to `strict`:

.. literalinclude:: zerochan_login_50_full_strict.py
    :language: python
    :linenos:

Now we have high-quality images of Amiya alone from Zerochan, as shown below:

.. image:: zerochan_login_50_full_strict.png
    :align: center


Danbooru
~~~~~~~~~~~~~~~~~~~~~~~~~

Clearly, `Danbooru <https://danbooru.donmai.us/>`_ can also be crawled easily:

.. literalinclude:: danbooru_50.py
    :language: python
    :linenos:

Moreover, on Danbooru and many similar sites, you can directly collect solo images by adding the ``solo`` tag, like this:

.. literalinclude:: danbooru_50_solo.py
    :language: python
    :linenos:

Pixiv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

waifuc also supports crawling for `Pixiv <https://www.pixiv.net/>`_, including keyword searches, artist-specific crawls, and crawls based on rankings.

We can use ``PixivSearchSource`` to crawl images based on keywords, as shown below:

.. literalinclude:: pixiv_50.py
    :language: python
    :linenos:

We can also use ``PixivUserSource`` to crawl images from a specific artist, as shown below:

.. literalinclude:: pixiv_50_user.py
    :language: python
    :linenos:

We can use ``PixivRankingSource`` to crawl images from the ranking, as shown below:

.. literalinclude:: pixiv_50_ranking.py
    :language: python
    :linenos:


Anime-Pictures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Anime-Pictures <https://anime-pictures.net/>`_ is a site with fewer images, but generally high quality. waifuc also supports crawling from it, as shown below:

.. literalinclude:: anime_pictures_50.py
    :language: python
    :linenos:


Sankaku
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Sankaku <https://chan.sankakucomplex.com/>`_ is a site with a large number of images of various types, and waifuc also supports it, as shown below:

.. literalinclude:: sankaku_50.py
    :language: python
    :linenos:


Gelbooru
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

waifuc also supports crawling from `Gelbooru <https://gelbooru.com/>`_, as shown below:

.. literalinclude:: gelbooru_50.py
    :language: python
    :linenos:


Duitang
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In response to a request from a mysterious user on civitai, waifuc has added support for Duitang. `Duitang <https://www.duitang.com/>`_ is a Chinese website that contains many high-quality anime images. The crawling code is as follows:

.. literalinclude:: duitang_50.py
    :language: python
    :linenos:


Other Supported Sites
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the above-mentioned websites, we also support a large number of other image websites. All supported websites are listed below:

1. ATFBooruSource (Website: `https://booru.allthefallen.moe <https://booru.allthefallen.moe>`_)
2. AnimePicturesSource (Website: `https://anime-pictures.net <https://anime-pictures.net>`_)
3. DanbooruSource (Website: `https://danbooru.donmai.us <https://danbooru.donmai.us>`_)
4. DerpibooruSource (Website: `https://derpibooru.org <https://derpibooru.org>`_)
5. DuitangSource (Website: `https://www.duitang.com <https://www.duitang.com>`_)
6. E621Source (Website: `https://e621.net <https://e621.net>`_)
7. E926Source (Website: `https://e926.net <https://e926.net>`_)
8. FurbooruSource (Website: `https://furbooru.com <https://furbooru.com>`_)
9. GelbooruSource (Website: `https://gelbooru.com <https://gelbooru.com>`_)
10. Huashi6Source (Website: `https://www.huashi6.com <https://www.huashi6.com>`_)
11. HypnoHubSource (Website: `https://hypnohub.net <https://hypnohub.net>`_)
12. KonachanNetSource (Website: `https://konachan.net <https://konachan.net>`_)
13. KonachanSource (Website: `https://konachan.com <https://konachan.com>`_)
14. LolibooruSource (Website: `https://lolibooru.moe <https://lolibooru.moe>`_)
15. PahealSource (Website: `https://rule34.paheal.net <https://rule34.paheal.net>`_)
16. PixivRankingSource (Website: `https://pixiv.net <https://pixiv.net>`_)
17. PixivSearchSource (Website: `https://pixiv.net <https://pixiv.net>`_)
18. PixivUserSource (Website: `https://pixiv.net <https://pixiv.net>`_)
19. Rule34Source (Website: `https://rule34.xxx <https://rule34.xxx>`_)
20. SafebooruOrgSource (Website: `https://safebooru.org <https://safebooru.org>`_)
21. SafebooruSource (Website: `https://safebooru.donmai.us <https://safebooru.donmai.us>`_)
22. SankakuSource (Website: `https://chan.sankakucomplex.com <https://chan.sankakucomplex.com>`_)
23. TBIBSource (Website: `https://tbib.org <https://tbib.org>`_)
24. WallHavenSource (Website: `https://wallhaven.cc <https://wallhaven.cc>`_)
25. XbooruSource (Website: `https://xbooru.com <https://xbooru.com>`_)
26. YandeSource (Website: `https://yande.re <https://yande.re>`_)
27. ZerochanSource (Website: `https://www.zerochan.net <https://www.zerochan.net>`_)

For more information and details on using these data sources, refer to the official waifuc source code.


Crawling Data from Multiple Websites
----------------------------------------------------------

In reality, there are often cases where we want to retrieve image data from multiple websites. For example, we might need 30 images from Danbooru and another 30 from Zerochan.

To address this situation, ``waifuc`` provides concatenation and union operations for data sources. In simple terms, you can integrate multiple data sources using concatenation (``+``) and union (``|``). For example, to fulfill the mentioned requirement, we can concatenate the data sources of Danbooru and Zerochan, creating a new data source, as shown below:

.. literalinclude:: source_concat.py
    :language: python
    :linenos:

The code above first crawls 30 images from Danbooru and then another 30 from Zerochan. Consequently, we get a dataset like this:

.. image:: source_concat.png
    :align: center

Moreover, in some cases, we might not know in advance the number of images each data source contains. Instead, we may want to collect images from different sources as much as possible, with a specific total quantity in mind. In such cases, we can use the union operation, as shown below:

.. literalinclude:: source_union.py
    :language: python
    :linenos:

In this example, it randomly crawls one image at a time from either of the two websites until it collects 60 images. Thus, the final dataset is not fixed, and the following dataset is just an example:

.. image:: source_union.png
    :align: center

In fact, all waifuc data sources support such concatenation and union operations. You can even perform complex nested operations to construct a sophisticated data source:

.. literalinclude:: source_complex.py
    :language: python
    :linenos:

Here, a complex data source ``s = s_zerochan[:50] + (s_db | s_pixiv)[:50]`` is created, which effectively means:

1. First, crawl 50 images from Zerochan.
2. Then, randomly crawl a total of 50 images from Danbooru and Pixiv.

This results in obtaining a maximum of 100 images.

Moreover, concatenation and union operations can be performed after the attach syntax, meaning that you can preprocess the data source and then concatenate or union it. For example, in the following example:

.. literalinclude:: source_complex_attach.py
    :language: python
    :linenos:

The above code crawls images from both Zerochan and Danbooru, removes the background for images from Zerochan, and saves a total of 60 images. The results you get might look similar to the following, where images from Zerochan have their backgrounds removed:

.. image:: source_complex_attach.png
    :align: center

Concatenation and union are essential features of waifuc data sources, and using them wisely makes the configuration of data sources very flexible and versatile.


Why Are There So Many JSON Files?
--------------------------------------------

If you've read up to this point, you may have noticed something — all the datasets saved using ``SaveExporter`` have a corresponding JSON file with the same name as each image. You must be curious about the purpose of these JSON files, and this section will provide an explanation.

Firstly, let's open the file ``.danbooru_6814120_meta.json`` and take a look at its content. The JSON data looks something like this:

.. collapse:: A Sample Meta-Information JSON

    .. literalinclude:: meta_json.json
        :language: json
        :linenos:

In essence, **this is a data file used to store metadata about the images**. In this metadata file, it contains the following information:

1. Information about the image from the Danbooru website, including tags, dimensions, ID, upload time, etc.
2. URL information about the image, i.e., where the image was downloaded from.
3. Naming information for the image, i.e., what filename the image will be saved as.
4. Tag information for the image, i.e., what tags will be included when generating a training dataset.

These pieces of information play their respective roles in various processing steps. For example, tag information requires crawling from the website or using a tagger for labeling, and this information will be written during the generation of the LoRA training dataset. Therefore, in waifuc, they are maintained and can be saved using ``SaveExporter``.

To make the most of this information, **you can reload the dataset saved to your local machine using `LocalSource`**. You can achieve this using the following code:

.. literalinclude:: local.py
    :language: python
    :linenos:

The code above reloads the dataset containing metadata that was previously saved and re-saves it in the format of the LoRA training dataset. The resulting files will look like the following:

.. image:: local_to_dataset.png
    :align: center

Of course, it's worth noting that ``LocalSource`` can be used not only for paths containing metadata files but also for paths containing only images. However, it will not include the initial metadata in the pipeline, meaning that information such as tags will need to be regenerated.

Additionally, like other data sources, **`LocalSource` also supports concatenation and union operations**. Leveraging this feature, you can use data from both the internet and local sources to build a dataset.

When you are sure that you only need images and don't need any metadata for the next loading, you can use the ``no_meta`` parameter of `SaveExporter` to achieve this:

.. literalinclude:: save_no_meta.py
    :language: python
    :linenos:

This code will not save any metadata files, and you will precisely get 50 images, as shown below:

.. image:: save_no_meta.png
    :align: center


.. _waifuc-not-in-disk:

I Don't Want to Save Images to Disk, How Can I Use Them Directly?
-------------------------------------------------------------------------------

In another scenario, you might not want to save image files to the hard disk but rather use them directly in memory to save time. waifuc also supports this usage, as shown below:

.. literalinclude:: iterate_usage.py
    :language: python
    :linenos:

Yes, data sources (including those that have used the ``attach`` method) can be iterated over. The type of each item is defined as follows:

.. literalinclude:: item_definition.py
    :language: python
    :linenos:

As you can see, the structure of each item is straightforward, containing an ``image`` object of type ``PIL.Image`` and a ``meta`` item for storing metadata.

Once you have the item, you can customize the operations you need using its image object and metadata.

