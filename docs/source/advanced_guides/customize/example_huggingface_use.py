from waifuc.export import SaveExporter

s = HuggingfaceSource('deepghs/game_character_skins', 'arknights/R001')
s.export(SaveExporter('test_hf_amiya'))
