***************
BTE
***************

-----------------
Overview
-----------------

BTE is a Cython API wrapper around the highly optimized phylogenetics library underlying the Pandemic Phylogenetics toolkit. 
It allows the user to leverage the power of the Mutation Annotated Tree file format and library in their Python scripts, 
allowing for efficient and effective analysis of global SARS-CoV-2 and other pathogen phylogenies. This package is generally intended 
as a replacement for ETE3, Biopython.Phylo, and similar Python phylogenetics packages for Mutation Annotated Trees (MATs). Using standard 
packages with MATs requires conversion to newick and the maintenance of mutation annotations as a separate data structure, generally 
causing inconvenience and slowing both development and runtime. BTE streamlines this process, allowing for efficient and convenient use of MATs in a Python development environment!

BTE can be found at its `repository <https://github.com/jmcbroome/BTE>`_. This repository includes detailed installation instructions,
a quickstart, and a `dedicated documentation <https://jmcbroome.github.io/BTE/build/html/index.html>`_.

-----------------
Installation
-----------------

BTE is available via bioconda.

.. code-block::

  conda install -c bioconda bte

Local installation instructions can be found `here <https://github.com/jmcbroome/BTE#build-from-source-instructions>`_.

-----------------
Quickstart
-----------------

Download the latest public SARS-CoV-2 tree:

.. code-block:: shell-session

  wget http://hgdownload.soe.ucsc.edu/goldenPath/wuhCor1/UShER_SARS-CoV-2/public-latest.all.masked.pb.gz

And proceed directly to your analysis in Python!

.. code-block::

  import bte
  tree = bte.MATree("public-latest.all.masked.pb.gz")

Example analyses can be found at the `BTE binder <https://mybinder.org/v2/gh/jmcbroome/bte-binder/HEAD>`_ and its `associated repository <https://github.com/jmcbroome/bte-binder>`_.