*****
UShER Wiki
*****

Welcome to the manual for UShER, MAT Utils, and other related SARS-CoV-2 Phylogenetics tools.

Programs
========
* UShER_
* matUtils_
* RotTrees_

.. toctree::
   :hidden:

   index.rst
   Presentations.rst
   Publications.rst

.. _UShER:

UShER
=======
.. image:: usher_logo.png
    :width: 700px
    :align: center

UShER is a program for rapid, accurate placement of samples to existing phylogenies. It is available for downloading `here <https://github.com/yatisht/usher>`_ and is updated regularly. While not restricted to SARS-CoV-2 phylogenetic analyses, it has enabled real-time phylogenetic analyses and genomic contact tracing in that its placement is orders of magnitude faster and more memory-efficient than previous methods, and is being widely used by several SARS-CoV-2 research groups, including the `UCSC Genome Browser team <https://genome.ucsc.edu/cgi-bin/hgPhyloPlace>`_ and `Rob Lanfear's global phylogeny releases <https://github.com/roblanf/sarscov2phylo/releases>`_.

--------------
Installation
--------------



--------------
Methodology
--------------

--------------
Usage
--------------


.. _matUtils:

matUtils
=========

**r**\ e\ **s**\ tructured **t**\ ext.

matUtils is a set of tools to be used for analyses relating to **m**\ utation\  **a**\ nnotated\  **t**\ rees, such as the protobuf (.pb) files used in UShER. This toolkit is currently under development and will be publicized shortly.

.. _RotTrees:

RotTrees
==========

RotTrees enables quick inference of congruence of tanglegrams. This is particularly useful for SARS-CoV-2 phylogenomics due to multiple groups independently analyzing data-sets with many identical samples. Previous tanglegram visualization software relied on fewer rotations to minimize crossings over:

.. image:: tanglegrams_comparison.png
    :width: 700px
    :align: center

RotTrees produces a merged tree from two input trees that is maximally resolved and compatible with both input trees (refer to our manuscript referenced at the bottom for more details). 

.. image:: rotation.gif
    :width: 700px
    :align: center
