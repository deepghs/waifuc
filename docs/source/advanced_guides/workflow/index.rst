.. _waifuc-workflow:

Understanding the Waifuc Workflow
=============================================================

Let's Whip Up Some Donuts
---------------------------------------------

Now, you might find this title a tad surprising, but hang tight! Picture this scenario:
you've got a charming little donut shop, and from time to time, customers with various taste preferences
swing by to buy some delectable donuts. So, what's on your to-do list?

The answer is pretty simple, broken down into three key tasks:

1. **Get Your Undecorated Donuts**: Before your official opening each day, getting your hands on some ready-to-fry donuts is undoubtedly your top priority. This typically involves coordinating with your ingredient supplier or prepping them yourself.

2. **Artisanal Crafting Services**: Before welcoming customers, you've got to pick the donuts, sift out any flawed ones, and keep track of losses. And then comes the wide array of customer requests: hollowed or intricately carved shapes, smearing icing, sprinkling toppings, and much more, making your day "eventful."

3. **Wrap Up the Tempting Delights**: When it's time to hand them over to customers, don't forget the elegant packaging and a cheerful message. Remember to wish them a delightful meal!

"Phew, that's quite a hassle!"😅

For waifuc, although the workflow matches these steps—corresponding to Data Source, Action, and Exporter—
it handles everything from acquiring the donuts to packaging and delivery within its realm.
In a nutshell, waifuc can transform you into the proud owner of an all-in-one donut vending machine.

.. note::
    To make upcoming reading more convenient, we've drawn some comparisons between concepts:

    - Donut Vending Production Line — Waifuc Workflow
    - Getting Undecorated Donuts — Source
    - Crafting Donuts — Action
    - Donut Packaging — Exporter

Source
-------------------------------

Before you whip up those delectable donuts, you need to get your hands on some pre-fried donuts.
Depending on your specific situation, you might have various options:

- Mix and make the dough on-site, then fry them into golden-brown donuts (undecorated donuts).
- Don't overlook the leftover donuts from closing time yesterday; the freezer's a lifesaver.
- Still not enough? Well, you could always "procure" some from your neighbor... 😏

.. image:: jerry_and_donuts.png
    :align: center

Regardless of the scenario, **all you need are the fried donuts**—how the donuts came to be?
Well, that's not really important.

If you've grasped the above process, congratulations — **you've also understood the concept of Source in waifuc**.
If we were to draw a parallel between this logic and the waifuc paradigm, it might look something like this:

.. note::
    Please note that the following code is not executable; it's for illustration and analogy purposes only

.. literalinclude:: donuts_source.py
    :language: python
    :linenos:

In a nutshell, you might **acquire images from various sources**, like scraping from Danbooru,
reading from your hard drive, or extracting frames from videos, and so on.
However, **they will all be output in a uniform format for downstream processing**.
For example, the following code illustrates different image data sources,
but they are used in the same way with no differences:

.. literalinclude:: waifuc_source.py
    :language: python
    :linenos:

So, no matter where your images come from, they all play nicely together! 😄


Actions
-----------------------------

Once you have enough undecorated donuts, the next step is the actual donut-making process.
Depending on various requirements, you might perform the following actions:

- **Filtering**:
    - Discard donuts that have gone bad overnight.
    - Get rid of donuts that were poorly made on the spot.
    - Toss out the neighbor's subpar donuts with no regrets.
- **Processing**:
    - Satisfy picky customers by carving suitable patterns on the donuts.
    - Spread the desired icing evenly over the donuts.
    - Sprinkle toppings like honey, sugar, nut sprinkles, jimmies, or other condiments as needed.
    - Special decorations might bring novelty during festivities.
    - If necessary, cut the donuts into bite-sized pieces for easy consumption.

After going through these steps, you'll have **finished donuts**.

If you understood the process above, congratulations — **you've also grasped the concept of Actions in waifuc**.
To draw a parallel with waifuc's paradigm, the following code snippets provide a similar analogy:

.. note::
    Please note that the code below is not meant to run, it's for illustrative purposes only.

- Producing some plain chocolate donuts

.. literalinclude:: donuts_action_1.py
    :language: python
    :linenos:

The final product should look like this (image sponsored by DALL-E):

.. image:: donut_choco.png
    :align: center

- Producing some strawberry-flavored donuts with sugar sprinkles

.. literalinclude:: donuts_action_2.py
    :language: python
    :linenos:

The final product will look something like this (image sponsored by DALL-E):

.. image:: donut_strawberry.png
    :align: center

In simple terms, in waifuc, after going through a series of actions (Action) such as filtering, processing,
and slicing for images, **you will get a collection of processed images that make up your training dataset**.
For example, in the following waifuc code, after crawling images, monochrome images will first be removed.
Following that, if an image is too large, it will be resized to a smaller size. Finally, each image will be tagged.
The resulting image data will go through these three processes sequentially.

.. literalinclude:: waifuc_action.py
    :language: python
    :linenos:

Order Matters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After seeing the above code, you might have a question – what is the relationship between the actions 
used in the ``attach`` function? Is their order important?

To answer this question, let's continue with the analogy of the donut shop. 
In the previous content, we tried to make strawberry-flavored donuts with sugar sprinkles. 
In the analogous code, we used ``IcingAction`` first and then ``JimmiesAction``, indicating that for donuts, 
we first apply icing and then sprinkle sugar candies.

But what if we reverse the order, first sprinkle sugar candies, and then apply icing – obviously, 
sugar candies will have a hard time sticking to the donut and will often end up in a mess. 
This means that ``JimmiesAction`` did not work as expected; afterward, we apply strawberry-flavored icing.

Here's the code:

.. literalinclude:: donuts_action_order.py
    :language: python
    :linenos:

So, the donut you will end up with will look like this (image provided by DALL-E, please ignore the strawberry
above because it seems to not quite understand what I meant):

.. image:: donut_strawberry_failed.png

In simple terms, the ``attach`` method represents the order of operations, and changing the order means
a significant change in the processing flow – we shouldn't understand the relationship between operations
in the ``attach`` method as a simple unordered stack. For example, **in the waifuc code example above,
if we move NoMonochromeAction to the end, the entire process will become – first, scaling and tagging,
and then filtering**. The consequence of this is that a large number of monochrome images will be tagged first
and then deleted, resulting in significantly slower program execution and unnecessary waste of computing resources.

.. literalinclude:: waifuc_action_order.py
    :language: python
    :linenos:


Semi-Finished Products?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Imagine a scenario where you are preparing to make a batch of donuts with sugar sprinkles,
and you have already applied the icing. However, you suddenly have to leave for a while due to an unexpected event.
In a situation like this, what should you do when you come back? It's similar to the following code,
so what should you do next?

.. literalinclude:: donuts_action_attach_1.py
    :language: python
    :linenos:

It's quite simple; you just need to heat it up a bit to melt the icing slightly and then sprinkle the sugar candies,
just like this:

.. literalinclude:: donuts_action_attach_2.py
    :language: python
    :linenos:

In reality, when the first ``attach`` is called, a new secondary data source (Secondary Source,
corresponding to the concept of Primary Source, such as the DanbooruSource at the beginning) has already been generated.
This data source is exactly the same as the others, except it produces donuts with the previous icing.
We just need to process this new data source as usual. In waifuc, this concept is similar.
For example, the following two code snippets are completely equivalent:

- Code 1 (using a single ``attach``):

.. literalinclude:: waifuc_action_attach_1.py
    :language: python
    :linenos:

- Code 2 (first using ``attach`` to generate a new source, then attaching operations to that source):

.. literalinclude:: waifuc_action_attach_2.py
    :language: python
    :linenos:

Exporter
---------------------------------

When we have finished making donuts, we need to deliver them to the customers.
Specifically, you may encounter the following scenarios:

- During tea time, hungry customers want to have hot donuts right away. You need to **put the freshly made donuts into paper bags** and **hand them over** to the customers.
- Customers want to buy a dozen donuts as a snack for late-night coding. You need to neatly **pack the donuts in a box** and help the customer wrap it for **carrying back home**.
- Customers who have heard about your donuts want to buy a whole cartload of them for a party. You need to **put the donuts in a fresh-keeping bag**, **load them into a van**, secure them with tie-down straps to prevent them from falling off during transport.

In any of these cases, what you need to do is deliver the finished donuts to the customers.
**You need to deliver in different forms according to the actual needs of the customers, but you don't care about how the donuts were made before or how the customers will use them.**

If you understand the above process, congratulations - **you have also understood the concept of Exporter in waifuc**.
If we compare this logic to the paradigm of waifuc, it should be something like the following code snippets

.. note::
    Please note that the following code cannot actually run, it is for analogy and illustration purposes.

- Hand over the donuts directly to the customer

.. literalinclude:: donuts_exporter_1.py
    :language: python
    :linenos:

- Package a dozen donuts and hand them over to the customer

.. literalinclude:: donuts_exporter_2.py
    :language: python
    :linenos:

- Load a large quantity of donuts into boxes and onto a pickup truck

.. literalinclude:: donuts_exporter_3.py
    :language: python
    :linenos:

With this, your donut shop is officially up and running. Congratulations! 🎉👏🎊

In simple terms, a Data Exporter retrieves data from the data source you provide
(it could be a native data source or a secondary data source) and exports the data in the desired format according
to a preset process. For example, in the following waifuc code, using different Data Exporters with the same
data source results in completely different data formats:

- Export in the format of images + JSON metadata

.. literalinclude:: waifuc_exporter_1.py
    :language: python
    :linenos:

- Export only images, without JSON metadata

.. literalinclude:: waifuc_exporter_2.py
    :language: python
    :linenos:

- Export in the format of images + TXT, which is suitable for training most neural network models

.. literalinclude:: waifuc_exporter_3.py
    :language: python
    :linenos:

With this, a complete waifuc image data processing workflow is set up.

