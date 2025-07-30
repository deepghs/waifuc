# comfy_interrupt_action.py
from typing import Iterator

# 导入 ComfyUI 的模型管理模块
# 这是一个可选依赖，只有在 ComfyUI 环境下运行时才需要
try:
    import comfy.model_management
    is_comfy_env = True
except (ImportError, ModuleNotFoundError):
    is_comfy_env = False

from waifuc.action import ProcessAction
from waifuc.model import ImageItem


class ComfyInterruptAction(ProcessAction):
    """
    An action designed to be used within a ComfyUI environment.
    It checks for user interruption requests before processing each item.

    This action should be placed at the beginning of the waifuc pipeline.
    If a user cancels the execution in ComfyUI, this action will raise
    an exception that ComfyUI's execution manager can catch, immediately
    and cleanly stopping the entire workflow.

    Usage:
    ------
    >>> from waifuc.source import DanbooruSource
    >>> from your_project.actions import ComfyInterruptAction # Assuming you place this file correctly
    ...
    >>> source = DanbooruSource(['your_tags'])
    >>> pipeline = source.attach(
    ...     ComfyInterruptAction(),  # <-- Place it here, at the very beginning
    ...     # ... other actions
    ... )

    """

    def __init__(self):
        """
        Initializes the ComfyInterruptAction.
        It checks if the action is running within a ComfyUI environment.
        """
        if not is_comfy_env:
            # 可以在这里选择是抛出警告还是静默失败
            # For now, we allow it to be created, but it will do nothing
            # if not in a ComfyUI environment.
            pass

    def process(self, item: ImageItem) -> ImageItem:
        """
        Process a single ImageItem.

        If running in a ComfyUI environment, this method calls
        `comfy.model_management.throw_exception_if_processing_interrupted()`.
        Otherwise, it does nothing and simply passes the item through.

        :param item: The ImageItem to process.
        :type item: ImageItem
        :return: The same ImageItem, passed through.
        :rtype: ImageItem
        """
        if is_comfy_env:
            comfy.model_management.throw_exception_if_processing_interrupted()
        
        return item