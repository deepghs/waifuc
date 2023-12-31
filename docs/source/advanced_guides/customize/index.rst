How to Get Creative with Development
=============================================

.. note::
    To enhance your reading experience in this chapter,
    it's recommended to go through the "Understanding the waifuc Workflow" section
    and grasp the basic concepts of waifuc's workflow.

Framework Flexibility
---------------------------------------

Let's stick to the donut shop analogy. Even though our donut production pipeline is quite mature, scenarios like the following may still arise:

- **During Donut Frying**
    - Some customers prefer donuts made with whole wheat flour for a rougher texture but healthier choice.
    - Certain customers insist on donuts fried with a specific brand of olive oil.
- **During Processing**
    - Customers might be into spicy-flavored icing.
    - Some customers wish to have special symbols or text drawn with icing to represent a unique meaning.
- **During Packaging**
    - A company ordered a batch of donuts and wants their company logo and graphics on the packaging.

These kinds of demands share a common trait:

- **Low Replicability**: They either cater to relatively niche preferences or are specific to a particular batch of donuts. Neither case is suitable for the official establishment of a dedicated production line.
- **But They Do Exist**: This is evident; no valid demand should be disregarded.

As the donut shop owner, you decide to open up the entire process—allowing customers to make donuts in their own kitchens with their preferred flavors.

Clearly, waifuc anticipated diverse and unique requirements. Therefore, right from the beginning, **waifuc is designed to be framework-flexible**—this means users can not only customize the data processing pipeline but also **construct their own data sources, actions, and exporters to meet various dataset creation needs**. The following sections will provide a detailed overview of this feature.


