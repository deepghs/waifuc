from waifuc.export import TextualInversionExporter

get_waifu_dataset(
    'surtr_(arknights)',
    drop_monochrome_images=True,
    solo_only=True,
    no_character_tag=False,
    n_images=50,
).export(TextualInversionExporter('test_safety'))
