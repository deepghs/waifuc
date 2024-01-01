from waifuc.action import NoMonochromeAction, ClassFilterAction, TaggingAction
from waifuc.source import DanbooruSource


def get_waifu_dataset(her_name: str, drop_monochrome_images: bool = True,
                      solo_only: bool = True, illustration_only: bool = False,
                      no_character_tag: bool = True, n_images: int = 50):
    """
    Get a waifu dataset source based on specified criteria.

    :param her_name: Name of the waifu character.
    :type her_name: str
    :param drop_monochrome_images: Whether to exclude monochrome images.
    :type drop_monochrome_images: bool
    :param solo_only: Whether to include only solo images.
    :type solo_only: bool
    :param illustration_only: Whether to include only images classified as illustrations.
    :type illustration_only: bool
    :param no_character_tag: Whether to exclude images with character tags.
    :type no_character_tag: bool
    :param n_images: Number of images you need. 'None' means you need all the images.
    :type n_images: int
    :return: Waifu dataset source with specified criteria.
    :rtype: DanbooruSource
    """
    if solo_only:
        # Use the solo tag, only solo images will be included
        source = DanbooruSource([her_name, 'solo'])
    else:
        # Don't use the solo tag, include all images
        source = DanbooruSource([her_name])

    if drop_monochrome_images:
        # Drop monochrome images
        source = source.attach(NoMonochromeAction())
    if illustration_only:
        # Only use illustration images
        source = source.attach(ClassFilterAction(['illustration']))

    if no_character_tag:
        # Drop the character tags
        source = source.attach(TaggingAction(character_threshold=1.01))
    else:
        # Keep all the tags
        source = source.attach(TaggingAction())

    if n_images is not None:
        source = source[:n_images]
    return source
