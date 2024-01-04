Extracting Character Images from Videos
================================================================

(Chinese Doc：\ https://deepghs.github.io/waifuc/main/tutorials-CN/crawl_videos/index.html )

Install Additional Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

waifuc also provides a method to extract images from videos. Before running, you need to install additional dependencies, including the ``pyav`` library, for video processing:

.. code:: shell

    pip install git+https://github.com/deepghs/waifuc.git@main#egg=waifuc[video]


Extract Images from Video Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In waifuc, you can use ``VideoSource`` to process video files, extract frames, and save them as images. Here is an example:

.. literalinclude:: video_simple.py
    :language: python
    :linenos:

The saved images look like this:

.. image:: video_simple.png
    :align: center


Extract Images from a Folder Containing Videos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In many cases, you may want to process an entire series of downloaded anime videos stored in the same folder. You can directly extract frames from a folder containing videos, as shown in the following code:

.. literalinclude:: video_dir.py
    :language: python
    :linenos:

This code will iterate through all video files in the ``/data/videos`` path, extract frames, and save them to the ``/data/dstdataset`` folder.


Extract Character Images from a Folder Containing Videos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To extract character images from a video folder, you just need to add the ``PersonSplitAction`` to the code, as shown below:

.. literalinclude:: video_split.py
    :language: python
    :linenos:

The code above extracts frames from videos and saves portraits obtained from those frames, as shown below:

.. image:: video_split.png
    :align: center

However, it seems that some images are not suitable for training. Therefore, in actual anime videos, you can add more actions to obtain a higher quality training dataset. For example, the following code:

.. literalinclude:: video_split_better.py
    :language: python
    :linenos:

This will result in the following dataset:

.. image:: video_split_better.png
    :align: center

