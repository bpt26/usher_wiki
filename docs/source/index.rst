***************
UShER Wiki
***************

Welcome to the manual for UShER package, that includes SARS-CoV-2 Phylogenetics tools UShER, matUtils, matOptimize, RIPPLES, strain_phylogenetics, and others. Please see the table of contents below or on the sidebar, or `click here <https://usher-wiki.readthedocs.io/en/latest/QuickStart.html>`_ for a quick tutorial on getting started.

.. toctree::
   :hidden:
   
   QuickStart.rst
   Installation.rst
   UShER.rst
   matUtils.rst
   matOptimize.rst
   ripples.rst
   bte.rst
   tutorials.rst

.. _UShER:


UShER
=================

.. image:: usher_logo.png
    :width: 500px
    :align: center

UShER is a program for rapid, accurate placement of samples to existing phylogenies. Information on installation, usage, and features can be found `here <https://usher-wiki.readthedocs.io/en/latest/UShER.html>`__. Our manuscript about UShER can be found `here <https://www.nature.com/articles/s41588-021-00862-7>`_.


.. _matUtils:


matUtils
============

matUtils is a toolkit for querying, interpreting and manipulating the mutation-annotated trees (MATs). Information on its usage can be found `here <https://usher-wiki.readthedocs.io/en/latest/matUtils.html>`__.



matOptimize
============

matOptimize is a program to rapidly and effectively optimize a mutation-annotated tree (MAT) for parsimony using subtree pruning and regrafting (SPR) moves within a user-defined radius. Information on its usage can be found `here <https://usher-wiki.readthedocs.io/en/latest/matOptimize.html>`__.


RIPPLES
============

RIPPLES is a program that uses a phylogenomic technique to rapidly and sensitively detect recombinant nodes and their ancestors in a mutation-annotated tree (MAT). Information on its usage can be found `here <https://usher-wiki.readthedocs.io/en/latest/ripples.html>`__.


BTE
============

BTE is a separately packaged Cython API that wraps the highly optimized library underlying these other tools, exposing them for use in Python. Information about its usage can be found `here <https://usher-wiki.readthedocs.io/en/latest/bte.html>`__ and at its `repository <https://github.com/jmcbroome/BTE>`_.