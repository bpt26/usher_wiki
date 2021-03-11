.. include:: includes.rst.txt

***************
Explanations and Tutorials
***************

This document contains detailed explanations and example workflows for Usher and matUtils.

.. _protobuf:
-----------
The Mutation Annotated Tree (MAT) Protocol Buffer (.pb)
-----------

Google's protocol buffer format is a highly optimized, flexible binary storage format, with APIs for many languages. 
We use a specially formatted protocol buffer to store a Mutation Annotated Tree object.

.. _extract:
-----------
matUtils extract Explanation
-----------

matUtils extract exists as a flexible prebuilt pipeline, which can quickly subset and convert an input MAT .pb file. 
Generally, its parameters can be grouped into three categories: 
1. Selection- these parameters define a subtree to use for further processing. If none are set, the whole input tree is used.
2. Conversion- these parameters are used to request subtree representations in the indicated formats.
3. Information- these parameters save information about the subtree which is not a direct representation of that subtree, such as mutations defining each clade in the subtree.

.. _annotate:
-----------
matUtils annotate Explanation
-----------

filler

.. _uncertainty:
-----------
matUtils uncertainty Explanation
-----------

matUtils uncertainty calculates two specific metrics for sample placement certainty.