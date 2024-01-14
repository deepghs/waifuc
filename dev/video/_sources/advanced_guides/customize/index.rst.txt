How to Customize In Waifuc?
=============================================

.. note::
    To enhance your reading experience in this chapter,
    it's recommended to go through the :ref:`waifuc-workflow` section
    and grasp the basic concepts of waifuc's workflow.

Framework Approach
---------------------------------------

Let's continue with the example of the donut shop. Although our donut production pipeline is already mature,
situations like the following may still arise:

- **During Donut Frying:**
    - Some customers prefer donuts made with whole wheat flour for a rougher texture but healthier option.
    - Some customers insist on donuts fried with a specific brand of olive oil.
- **During Donut Decoration:**
    - Some customers enjoy spicy-flavored icing.
    - Others want to use icing to create specific text or symbols to convey a special meaning.
- **During Donut Packaging:**
    - A small company has placed an order for a batch of donuts and wants its company logo and graphics printed on the packaging bags.

Such requirements are quite diverse and share a common characteristic:

- They are **not highly repeatable**. They either belong to relatively niche demands or pertain to special requirements for a specific batch of donuts. In either case, it is clearly not suitable for the official production line to be established permanently.
- **However, they do exist**. This is evident, as no valid demand should be ignored.

As a result, as the owner of a donut shop, you obviously cannot handle these demands all by yourself.
Therefore, you will upgrade your industry and open up the entire process—allowing customers to make donuts
in their own kitchens according to their taste preferences.

Clearly, waifuc has also taken into account the existence of diverse and specialized requirements.
From the very beginning, **waifuc's design is modular**. This means that users can not only customize
data processing workflows but also **create their own data sources, actions, and exporters to meet different dataset creation needs**.
The following sections will provide detailed explanations of this feature.


Custom Sources
--------------------------------------

Basic Data Sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In waifuc, all data sources inherit from the ``BaseDataSource`` class.
The core definition of this class is as follows (for the definition of ``ImageItem``,
see :ref:`waifuc-not-in-disk`:

.. autoclass:: waifuc.source.base.BaseDataSource
    :noindex:

.. code-include:: :class:`waifuc.source.base.BaseDataSource`
    :language: python
    :link-at-bottom:
    :link-to-documentation:

Pretty simple structure, isn't it? When you are building your own data source,
all you need to do is inherit from the ``BaseDataSource`` class and implement ``_iter``.
For example, in the following example, we use the `Pillow library <https://pillow.readthedocs.io/en/stable/>`_ to
randomly generate solid-color images of different sizes and save them to a specified path:

.. literalinclude:: example_random_color.py
    :language: python
    :linenos:

The resulting images look like this:

.. image:: example_random_color.png
    :align: center

It's worth noting that we not only saved the images but also saved associated metadata with the images.
For example, when we open one of the JSON files, the information inside will look something like this:

.. literalinclude:: example_random_color_item.json
    :language: json
    :linenos:

This is the metadata we specified in the code.

Web Data Sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In practical usage of waifuc, we often need to fetch data from the internet, which is quite common.
To address this need, waifuc provides a base class for web data sources called ``WebDataSource``.
Its basic structure is defined as follows:

.. autoclass:: waifuc.source.web.WebDataSource
    :noindex:

.. code-include:: :class:`waifuc.source.web.WebDataSource`
    :language: python
    :link-at-bottom:
    :link-to-documentation:


It indirectly inherits from the ``BaseDataSource`` class and implements the ``_iter`` method.
In the ``_iter_data`` method, you need to continuously iterate and provide resource IDs, image URLs,
and metadata. The downloading and output as ``ImageItem`` are automatically handled in the ``_iter`` method.

With this structure in place, you can easily implement web grabing for custom websites and use it as a
data source in waifuc. For example, you can grab images from the Huggingface repository (in this case,
we are using the `deepghs/game_character_skins <https://huggingface.co/datasets/deepghs/game_character_skins>`_
repository containing character skin data for various popular mobile games):

.. literalinclude:: example_huggingface_def.py
    :language: python
    :linenos:

After defining the above code, you can easily obtain images of my lovely waifu, Amiya's skin:

.. literalinclude:: example_huggingface_use.py
    :language: python
    :linenos:

The result looks like this:

.. image:: example_huggingface.png
    :align: center

Similarly, you can integrate your existing web grabing scripts for a specific website into waifuc,
making them usable as a data source for creating high-quality datasets.


About Metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you look closely, you may have noticed something - in the first example, the files are named ``untitled_xxx.png``,
which appears to be an automatically generated default filename. However, in the second example,
the filenames are different. To explain this, we need to provide some necessary explanations about the concept
of "metadata."

In the process of automating the handling of actual datasets, images often do not contain all the necessary information.
Therefore, we have designed the concept of ``ImageItem``, which binds images together with their associated metadata.
This approach facilitates richer image operations in subsequent processing steps and allows us to avoid unnecessary
redundant calculations using metadata.

Some fields in the metadata have special meanings, for example:

- The ``filename`` field, which is what caused the difference between the two examples you mentioned. **By writing the filename into this field, you can determine the filename to be used when saving the image**. Moreover, this field also supports filenames with relative paths, which will create subdirectories and save images accordingly. This feature allows you to generate datasets with complex nested directory structures automatically.
- The ``tags`` field, which stores the tags applied to the image by a tagger. It is a mapping structure where keys and values represent tag text and tag confidence, respectively. **When using TextualInversionExporter, the tag information stored in this field will be saved in `txt` format**, generating the format required for LoRA training.

By making good use of metadata, you can efficiently achieve complex data processing tasks in waifuc
in a straightforward manner.


Custom Actions
------------------------------

Apart from data sources, you can also create your own custom actions.

Base Action Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In waifuc, all action classes inherit from the ``BaseAction`` class, which is defined as follows:

.. autoclass:: waifuc.action.base.BaseAction
    :noindex:

.. code-include:: :class:`waifuc.action.base.BaseAction`
    :language: python
    :link-at-bottom:
    :link-to-documentation:

The ``iter`` method is the core feature of an action. It receives an individual data item and yields one or more
data items in an iterative manner (although yielding nothing is also allowed). By inheriting from
the ``BaseAction`` class and implementing the ``iter`` method, you can build your custom actions.

For example, if you want to randomly select some images from a data source and, for the selected images,
randomly select some of them to apply a mirror rotation, you can also add metadata that reflects random values
on the names of the final saved images. You can achieve this by creating a ``MyRandomAction`` like this:

.. literalinclude:: example_random_def.py
    :language: python
    :linenos:

Once defined, you can use it like this:

.. literalinclude:: example_random_use.py
    :language: python
    :linenos:

Running this code will produce images like the one below:

.. note::
    Since this action involves randomness, the results may not be exactly the same each time it's run;
    this image is for reference

.. image:: example_random.png
    :align: center

.. note::
    You might wonder what the ``reset`` method is for. Well, as the name suggests, **some actions may have states**.
    For example, the ``FirstNSelectAction`` code shown below:

    .. autoclass:: waifuc.action.count.FirstNSelectAction
        :noindex:

    .. code-include:: :class:`waifuc.action.count.FirstNSelectAction`
        :language: python
        :link-at-bottom:
        :link-to-documentation:

    The purpose of this action is to keep only the first ``n`` data items received. When ``n`` data items have passed
    through this action, it stops accepting new data items. To achieve this functionality, we need to initialize some
    stateful fields in the constructor. Therefore, **in some cases (such as deep copies of action objects), we need to**
    **reset the object to its initial state**. So, for actions that include states, it's essential to implement
    the ``reset`` method for resetting the action object.


Filter Action Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In waifuc, filtering is a common paradigm during the workflow setup. Filtering is characterized by:

- Taking one data item as input each time.
- Producing zero or one data item as output each time, and the output data item remains unchanged.
- Stateless, meaning the result is consistent whenever the same data item is input.

To facilitate such operations, we provide the ``FilterAction`` base class. When you inherit from this class,
you can quickly implement filtering actions. Here's its code definition:

.. autoclass:: waifuc.action.base.FilterAction
    :noindex:

.. code-include:: :class:`waifuc.action.base.FilterAction`
    :language: python
    :link-at-bottom:
    :link-to-documentation:

When inheriting this class, you only need to implement the ``check`` method. In this method,
you evaluate the input data item and return a Boolean value indicating whether to keep the data item.

For example, if you want to obtain images of the sexy babe waifu Texas and only keep comic-style images,
you can create a ``ComicOnlyAction`` like this:

.. literalinclude:: example_filter_def.py
    :language: python
    :linenos:

Then you can use it like this:

.. literalinclude:: example_filter_use.py
    :language: python
    :linenos:

Process Action Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to filtering actions, there is another common type of action called processing actions.
These actions have the following basic properties:

- Taking one data item as input each time.
- Producing strictly one data item as output each time.
- Stateless, meaning the result is consistent whenever the same data item is input.

Processing actions can be used to process input data items and directly output them. For this purpose,
we provide the ``ProcessAction`` base class. Here's its code definition:

.. autoclass:: waifuc.action.base.ProcessAction
    :noindex:

.. code-include:: :class:`waifuc.action.base.ProcessAction`
    :language: python
    :link-at-bottom:
    :link-to-documentation:

When your processing action class inherits from ``ProcessAction``,
you only need to implement the ``process`` method. In this method, you perform the processing of the input
data item and return the processed item as the method's result.

For example, if you want to obtain images of the sexy babe waifu Texas and only keep the head area to
create a dataset for an AI model that recognizes heads, you can create a ``CutHeadAction`` like this:

.. literalinclude:: example_process_def.py
    :language: python
    :linenos:

Then you can use it like this:

.. literalinclude:: example_process_use_1.py
    :language: python
    :linenos:

.. image:: example_process_1.png
    :align: center

The resulting images might initially seem not to be so good,
but they can be improved by using the ``FilterSimilarAction`` in combination, like this:

.. literalinclude:: example_process_use_2.py
    :language: python
    :linenos:

Congratulations, you now have a dataset of Texas with her head, and she is so fluffy you might want to give her a kiss!

.. image:: example_process_2.png
    :align: center


Custom Exporters
-------------------------------------

Clearly, **data exporters can also be customized**. Let's take a look at the code definition of ``BaseExporter``:

.. autoclass:: waifuc.export.base.BaseExporter
    :noindex:

.. code-include:: :class:`waifuc.export.base.BaseExporter`
    :language: python
    :link-at-bottom:
    :link-to-documentation:

By reading the code, it's evident that there are four methods to implement:

- ``pre_export``, which is executed before the actual export process and is typically used for initialization.
- ``export_item``, which is executed when a data item to be exported is obtained and is generally used for data writing operations.
- ``post_export``, which is executed after all data items have been exported and is generally used for resource cleanup and post-processing operations.
- ``reset``, similar to action classes, initializes the state of the data exporter object.

For example, if you don't want to save LoRA datasets in the format of image + txt but prefer image + csv
(a tabular data format for storing image filenames and their tags), you can do the following:

.. literalinclude:: example_export_def.py
    :language: python
    :linenos:

Then you can use it like this:

.. literalinclude:: example_export_use.py
    :language: python
    :linenos:

The resulting files will be as shown below:

.. image:: example_export.png
    :align: center

The contents of the ``tags.csv`` file will be as follows:

.. image:: example_export_csv.png
    :align: center

With this, we have covered the customization of all three core components of waifuc.
If you want to further understand the internal mechanisms, you can consider reading the source code.
**We look forward to waifuc users unleashing their imagination to develop their own data sources, actions,**
**and data exporters. We welcome anyone to contribute their development results as pull requests or release**
**them as independent PyPI packages to help more people.**
This is exactly what the DeepGHS team hoped to see when designing waifuc as a framework.


