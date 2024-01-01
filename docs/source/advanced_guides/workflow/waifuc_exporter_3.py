# NOTE: you already have a source that can provide image items
from waifuc.export import TextualInversionExporter

# save to /my/lora/dataset with images and TXTs
# which is ready for LoRA Training
source.exporter(TextualInversionExporter('/my/lora/dataset'))
