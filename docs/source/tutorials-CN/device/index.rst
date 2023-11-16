我不想让Waifuc占用GPU
======================================

如何让waifuc不再占用GPU？
--------------------------------------------------

waifuc中\ **许多Action都基于对应的onnx模型**\ ，因此，\ **当waifuc检测到环境中包含可用的CUDA时，将会优先使用GPU**\ 进行模型相关运算以提高运行效率

(onnx是一种通用的AI模型格式，详见：\ https://en.wikipedia.org/wiki/Open_Neural_Network_Exchange )

但在部分情况下，我们不希望waifuc占用GPU

例如训练LoRA时正好占用了所有显存、在运行a1111的stable diffusion webui的同时又需要通过waifuc处理图像等等

那么，\ **可以通过如下命令设置**\ ``ONNX_MODE``\ **环境变量为CPU**\ ：

    .. code:: shell

        # linux
        export ONNX_MODE=cpu

        # windows, cmd
        set ONNX_MODE=cpu

waifuc对硬件的最低要求？
----------------------------------------

按照上述演示，显然，\ **waifuc在没有GPU的环境下一样可以正常工作**\ ，且运行效率完全在可接受的范围内

根据我们已经做过的测试，\ **waifuc可以在只提供2个CPU内核和6G内存，且没有GPU的云端运行环境下正常工作**\ ，例如Github Action和Huggingface Space等

正因这些较低配置却完全免费的运行环境与waifuc在低配置硬件上的适应能力，DeepGHS得以不花一分钱地完成了上千个二次元老婆的数据集爬取与处理工作

因此，\ **waifuc实际可以被认为在现有的几乎所有的台式电脑或者笔记本电脑上均可正常运行**
