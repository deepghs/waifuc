from waifuc.export import TextualInversionExporter


def get_waifu_dataset(her_name: str, save_dir: str, drop_monochrome_images: bool = True,
                      solo_only: bool = True, illustration_only: bool = False,
                      no_character_tag: bool = True, n_images: int = 50):
    # -----------------------------
    # Create your source here ...
    # -----------------------------

    source.export(TextualInversionExporter(save_dir))
