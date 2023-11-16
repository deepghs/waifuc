How to Prevent Waifuc from Using GPU
=====================================================

(Chinese Doc：\ https://deepghs.github.io/waifuc/main/tutorials-CN/device/index.html )

Preventing GPU Usage in Waifuc
---------------------------------------------

In reality, many actions in Waifuc are based on `ONNX <https://en.wikipedia.org/wiki/Open_Neural_Network_Exchange>`_ models. Therefore, **when waifuc detects the presence of available CUDA in the environment, it prioritizes using the GPU** for model-related computations to enhance efficiency.

However, in some cases, we may not want Waifuc to use the GPU (for example, when running a1111's stable diffusion webui while processing data). In such cases, **you can set the ONNX_MODE environment variable to force it to use the CPU for execution**.

.. code:: shell

    # Linux
    export ONNX_MODE=cpu

    # Windows, CMD
    set ONNX_MODE=cpu


Minimum Hardware Requirements for Waifuc
----------------------------------------------------

As demonstrated above, it's evident that **Waifuc can operate normally even without a GPU**, and its performance is completely acceptable.

Based on our tests, **Waifuc can run successfully in cloud environments with only 2 CPU cores and 6GB of memory, without a GPU**. Examples of such environments include GitHub Actions and Huggingface Space. The adaptability of Waifuc to lower hardware configurations in these free-running environments allowed us to complete the scraping of datasets for over a thousand anime waifus without spending a penny.

Therefore, **Waifuc can practically be considered to run smoothly on almost all desktops or laptops**.

