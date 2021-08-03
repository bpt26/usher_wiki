.. include:: includes.rst.txt

***************
matOptimize
***************

matOptimize is a program used to optimize phylogenies using parsimony score. It is used on MAT files, which can be created by UShER.

-----------------
Installation
-----------------

To install matOptimize, simply follow the directions for `installing UShER <https://usher-wiki.readthedocs.io/en/latest/Installation.html>`_, and matOptimize will be included in your installation.

--------------
Options
--------------

.. code-block:: shell-session

  --vcf (-v): Input VCF file (in uncompressed or gzip-compressed .gz format. 
  --tree (-t): Input tree file.
  --load-mutation-annotated-tree (-i): Load mutation-annotated tree (MAT) object.
  --save-mutation-annotated-tree (-o): Save output mutation-annotated tree (MAT) object to the specified filename (REQUIRED).
  --save-intermediate-mutation-annotated-tree (-m): Save intermediate mutation-annotated tree (MAT) object to the specified filename.
  --radius (-r): Radius in which to restrict the SPR moves. Default = 10.
  --profitable-src-log (-S): The file to log from which node a profitable move can be found.
  --ambi-protobuf (-a): Continue from specified intermediate protobuf.
  --max-queued-moves (-q): Maximum number of profitable moves found before applying moves. Default = 1000.
  --minutes-between-save (-s): Length in minutes of intervals after which intermediate protobuf is saved. Default = 10.
  --do-note-write-intermediate-files (-n): If selected, matOptimize will not write any intermediate files.
  --exhaustive-mode (-e): Search every non-root node as source node.
  --max-hours (-M): Maximum number of hours to run.
  --transposed-vcf-path (-V): Auxiliary transposed VCF for ambiguous bases, used in combination with UShER protobuf (-i).
  --version: Print version number.
  --threads (-T): Number of threads to use when possible. Default = use all available cores.
  --help (-h): Print help messages.  

-----------------
Presentations
-----------------

Cheng Ye has presented matOptimize at The Annual International Conference on Intelligent Systems for Molecular Biology (ISMB), held virtually on July 25-30, 2021. `You can find his slides here <https://usher-wiki.readthedocs.io/en/latest/ismb.html>`_.