I Need to Dynamically Design the Processing Flow
=====================================================================

We can encapsulate the construction process of a data source within a function and return the generated data source
as the function's result.

For example, the following code demonstrates how to use a function to construct a rough dataset for a waifu:

.. literalinclude:: dynamic_def_1.py
    :language: python
    :linenos:

You can obtain different datasets by adjusting the function's parameters, like this:

.. literalinclude:: dynamic_use_1.py
    :language: python
    :linenos:

This will give you a dataset like the one shown below:

.. image:: dynamic_use_1.jpeg
    :align: center

Similarly, you can directly integrate data exporting into the function, like this:

.. literalinclude:: dynamic_def_2.py
    :language: python
    :linenos:


