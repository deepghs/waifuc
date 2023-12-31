What is CCIP, and What Makes It Tick?
==================================================

Given that `CCIPAction` plays a crucial role in tidying up character training datasets within waifuc,
many users have shown keen interest in it.
Therefore, we think it's worthwhile to dedicate a section to introduce CCIP and `CCIPAction`.

What is CCIP
------------------------------------

**CCIP, short for Contrastive Character Image Pretraining, is a contrastive learning model tailored for character feature training**.
It draws inspiration and its name from CLIP, falling under the umbrella of contrastive learning models just like CLIP.
However, while CLIP aligns images with text, CCIP aligns images of animated characters.
This concept and demand were originally proposed by narugo1992, and the technical route and solution were designed and implemented by 7eu7d7.
narugo1992 took charge of dataset collection, and 7eu7d7 provided the computational power for CCIP training and version iterations.

The CCIP model comprises two components:

1. Feature Extractor, responsible for extracting feature vectors of characters in images.
2. Feature Comparator, used for similarity calculations among the extracted feature vectors.

The currently widely-used CCIP model was trained on the `v1_pruned` version of the dataset
`Huggingface - deepghs/character_similarity <https://huggingface.co/datasets/deepghs/character_similarity>`_.
This dataset encompasses approximately 240,000 images from 3,982 different characters.

Through widespread use and testing, CCIP has indeed proven to deliver promising results.


.. image:: ccip_action_states.puml.svg
    :align: center



