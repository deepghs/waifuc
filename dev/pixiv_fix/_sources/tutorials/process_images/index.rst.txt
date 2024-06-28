Process Crawled or Local Images and Data
=======================================================

(Chinese Doc：\ https://deepghs.github.io/waifuc/main/tutorials-CN/process_images/index.html )

For data that is about to be crawled or has already been crawled, further processing is often needed to make it suitable for LoRA training. This section will introduce such functionalities in waifuc.

**Important Note:**

.. note::

    1. When processing crawled data, all data sources support a caching mechanism. This means you can temporarily store data using a defined variable. For the sake of convenience, we will demonstrate using ``LocalSource`` to load local data. In reality, actions can be used with any data source.
    2. Waifuc provides a variety of preset actions. Due to space limitations, not all features will be demonstrated here. A comprehensive list of functions can be found in the documentation.


How to Process Data
-----------------------------

In waifuc, we use actions to process the data obtained, as shown in the examples earlier.

We can use the ``attach`` method of the data source to add an action to the data source, creating a new data source. Here's an example:

.. literalinclude:: generic_example.py
    :language: python
    :linenos:

However, it's important to note that every time the ``attach`` method is called, a **new data source** will be generated. It won't change the original data source. Therefore, **the following usage is incorrect**, and the action in the ``attach`` method will not be effectively added:

.. literalinclude:: generic_example_wrong.py
    :language: python
    :linenos:


Common Actions and Usage Examples
-----------------------------------------------

ModeConvertAction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ModeConvertAction`` is a very commonly used action. Since actual images often come in various formats such as grayscale, binary, RGB, RGBA, etc. (see: `Pillow Modes <https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes>`_), we need to convert the mode of the images to facilitate further processing by other actions. Here's how you can use it:

.. literalinclude:: mode_convert.py
    :language: python
    :linenos:

In this code, ``ModeConvertAction`` will convert all images to the RGB mode. For images with a transparent background (e.g., PNG images in RGBA format), it will fill the background with white.

Considering the requirements of many subsequent action stages for image mode and to avoid format incompatibility issues during data saving, it is recommended to add this action as the first action in most cases.


FirstNSelectAction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For data sources, we often want to keep only the first several data items. Furthermore, for web data sources, limiting the number of images fetched is essential to ensure the finiteness of the process. Therefore, we can use ``FirstNSelectAction`` to truncate the data stream, as shown below:

.. literalinclude:: firstn.py
    :language: python
    :linenos:

This code will retain only the first 100 images read from ``/data/mydataset`` and save them to ``/data/dstdataset``.

It's worth noting that there is a more concise way to use ``FirstNSelectAction``, as shown below:

.. literalinclude:: firstn_sugar.py
    :language: python
    :linenos:

Yes, this code is equivalent to the code using ``FirstNSelectAction``. This is a concise form frequently used in the earlier content.


NoMonochromeAction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When processing training data, monochrome images (as defined `here <https://danbooru.donmai.us/wiki_pages/monochrome?z=2>`_) often sneak in. In most cases, these images are not desirable because they can have a negative impact on the model's training. Therefore, we want to filter them out. In waifuc, this is very simple. For example, for the following images stored in ``/data/raw``:

.. image:: monochrome_raw.png
    :align: center

We can use the following code to filter out monochrome images:

.. literalinclude:: monochrome.py
    :language: python
    :linenos:

However, note that depending on the content of the images, this action may also filter out images with color that are too similar to monochrome images.

Non-monochrome images will be saved in the ``/data/dstdataset`` path, as shown below:

.. image:: monochrome_processed.png
    :align: center


ClassFilterAction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Similarly, when processing training data, there are often manga and 3D images mixed in. In most cases, we want to exclude them. This is also very easy for waifuc. For example, for the following image:

.. image:: class_raw.png
    :align: center

You can use the following code to filter out manga (images with comic frames) and 3D images:

.. literalinclude:: class.py
    :language: python
    :linenos:

The final saved images are accurately filtered out:

.. image:: class_processed.png
    :align: center


FilterSimilarAction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When fetching data, we often need to filter out identical or similar images. In waifuc, there is a ``FilterSimilarAction`` based on the `LPIPS model <https://github.com/richzhang/PerceptualSimilarity>`_ to filter similar images. For example, for the following 10 images:

.. image:: lpips_raw.png
    :align: center

You can use the following code to filter out similar images:

.. literalinclude:: lpips.py
    :language: python
    :linenos:

The final images obtained are as follows:

.. image:: lpips_processed.png
    :align: center

TaggingAction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To train a LoRA dataset, it is generally necessary to label the content of the images. The specific format is an image plus a text file with the same name. For example, for the following set of images:

.. image:: tagging_raw.png
    :align: center

You can use the following code to generate tags for them and export them using ``TextureInversionExporter``:

.. literalinclude:: tagging.py
    :language: python
    :linenos:

The resulting dataset looks like this:

.. image:: tagging_processed.png
    :align: center

.. note::

    1. ``TaggingAction`` itself does not directly export images in the image+txt data format. It only generates tag information for images and stores it in the image's metadata. The actual export in the format required for LoRA training occurs only when ``TextualInversionExporter`` is used for the final export.
    2. When fetching images from some websites (such as Danbooru), the images on the website already have tag information. In this case, if you **directly use `TaggingAction`**, it will skip images with pre-existing tag information, resulting in tag information in the final exported dataset coming entirely from the crawled website. If you want to regenerate tag information for each image, you need to use ``TagginngAction(force=True)`` for forced tagging, replacing the original tagging information with information generated by the tagger.

PersonSplitAction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When fetching images, you may encounter images with multiple people. In some cases, we may want to split the various characters in the image to facilitate further filtering. In such cases, you can use `PersonSplitAction`. For example, for the following image:

.. image:: person_split_raw.png
    :align: center

You can use the following code to split the image:

.. literalinclude:: person_split.py
    :language: python
    :linenos:

The final split and saved images look like this:

.. image:: person_split_processed.png
    :align: center


FaceCountAction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Waifuc can also filter based on the number of faces in an image. For example, for the following set of images:

.. image:: face_count_raw.png
    :align: center

You can use the following code to filter out images with only one face:

.. literalinclude:: face_count.py
    :language: python
    :linenos:

The resulting dataset looks like this, with photos containing multiple faces filtered out:

.. image:: face_count_processed.png
    :align: center


CCIPAction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When fetching data, there is often a situation where **irrelevant characters are mixed in**. Even for websites with clear character tags like Danbooru, there will still be a certain percentage of irrelevant characters. **This problem is often difficult to completely avoid through common tagging mechanisms**, but such impurities can have a significant negative impact on the quality of LoRA training.

To address this issue, waifuc provides ``CCIPAction``, which can automatically filter out irrelevant characters from the data source. For example, in the following code:

.. literalinclude:: ccip_simple.py
    :language: python
    :linenos:

The effect is shown in the image below. Seven irrelevant images are randomly removed from a total of 32 images:

.. image:: ccip_simple.jpeg
    :align: center

Moreover, when we stack ``PersonSplitAction`` and ``CCIPAction``, we can filter images that contain both single and multiple characters in the data source (which is actually very common). The code is as follows:

.. literalinclude:: ccip_complex.py
    :language: python
    :linenos:

The effect is shown in the image below:

.. image:: ccip_complex.jpeg
    :align: center

.. note::

    1. By default, **make sure the data source can provide at least 15 images**. The CCIP model needs a certain number of images for cross-validation to determine the main character in the data source. If an insufficient number of images is provided, all images will accumulate in the ``CCIPAction`` step, preventing them from entering subsequent actions.
    2. The effective prerequisite for ``CCIPAction`` is that the data set contains **exactly one main character** (i.e., the character the user wants to obtain data for), and the **proportion of this character in the data source should not be too low** (ideally not less than 60%). The CCIP model needs to use clustering algorithms to determine the main character in the data source to filter all images. If the data source does not satisfy this characteristic, ``CCIPAction`` will take a long time to determine the main character, resulting in image accumulation.


AlignMinSizeAction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When the data source contains images that are too large, but large-sized images are not needed during training, and storage space needs to be saved as much as possible, you can use ``AlignMinSizeAction`` to compress large-sized images. The code is as follows:

.. literalinclude:: align_min_size.py
    :language: python
    :linenos:

The above code scales images with a short side length greater than 800, maintaining the original aspect ratio, so that the short side length becomes 800. For images with a short side length not exceeding 800, no modifications are made.


RandomFilenameAction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In some cases, to keep the processed image data in a shuffled state, avoiding the sequential loading of images in the model training script, we need to shuffle the images. In waifuc, you can use the following code to randomly rename all the images:

.. literalinclude:: random_filename.py
    :language: python
    :linenos:


ThreeStageSplitAction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In some experiments related to LoRA character model training, it has been preliminarily proven that splitting the same portrait image again for model training can improve LoRA's generalization and enhance the fidelity of character details. Therefore, waifuc also supports such operations. For example, for the following set of images:

.. image:: 3stage_raw.png
    :align: center

You can use ``ThreeStageSplitAction`` to split the images into full body - upper body - head, as shown in the code below:

.. literalinclude:: 3stage.py
    :language: python
    :linenos:

The ``FilterSimilarAction`` can filter out highly similar sub-images that may appear after the split. It is recommended to add this action. The final processed dataset looks like this:

.. image:: 3stage_processed.png
    :align: center

Other Actions
----------------------------------

In fact, waifuc supports more than just the several actions mentioned above. You can find more actions in the `source code <https://github.com/deepghs/waifuc/blob/main/waifuc/action/__init__.py>`_.

Additionally, actions are customizable, meaning you can customize the actions you need and add them to the processing pipeline. Details about this will be explained in the subsequent content.

