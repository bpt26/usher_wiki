.. include:: includes.rst.txt

***************
matOptimize
***************

matOptimize is a program used to optimize phylogenies using parsimony score. It is used on MAT files, which can be created by UShER.

-----------------
Installation
-----------------

To install matOptimize, simply follow the directions for :doc:`installing UShER <Installation>`, and matOptimize will be included in your installation.

--------------
Options
--------------

.. code-block:: sh

 -v [ --vcf ] arg                      Input VCF file (in uncompressed or 
                                        gzip-compressed .gz format) 
  -t [ --tree ] arg                     Input tree file
  -T [ --threads ] arg (=12)            Number of threads to use when possible 
                                        [DEFAULT uses all available cores, 12 
                                        detected on this machine]
  -i [ --load-mutation-annotated-tree ] arg
                                        Load mutation-annotated tree object
  -o [ --save-mutation-annotated-tree ] arg
                                        Save output mutation-annotated tree 
                                        object to the specified filename 
                                        [REQUIRED]
  -r [ --radius ] arg (=-1)             Radius in which to restrict the SPR 
                                        moves.
  -S [ --profitable-src-log ] arg (=/dev/null)
                                        The file to log from which node a 
                                        profitable move can be found.
  -a [ --ambi-protobuf ] arg            Continue from intermediate protobuf
  -s [ --minutes-between-save ] arg (=0)
                                        Minutes between saving intermediate 
                                        protobuf
  -m [ --min-improvement ] arg (=0.000500000024)
                                        Minimum improvement in the parsimony 
                                        score as a fraction of the previous 
                                        score in ordder to perform another 
                                        iteration.
  -d [ --drift_iteration ] arg (=0)     Iterations permiting equally 
                                        parsimonious moves after parsimony 
                                        score no longer improves
  -n [ --do-not-write-intermediate-files ] 
                                        Do not write intermediate files.
  -N [ --max-iterations ] arg (=1000)   Maximum number of optimization 
                                        iterations to perform.
  -M [ --max-hours ] arg (=0)           Maximium number of hours to run
  -V [ --transposed-vcf-path ] arg      Auxiliary transposed VCF for ambiguous 
                                        bases, used in combination with usher 
                                        protobuf (-i)
  --version                             Print version number
  -z [ --node_proportion ] arg (=2)     the proportion of nodes to search
  -y [ --node_sel ] arg                 Random seed for selecting nodes to 
                                        search
  -h [ --help ]                         Print help messages

-----------------
Presentations
-----------------

Cheng Ye has presented matOptimize at The Annual International Conference on Intelligent Systems for Molecular Biology (ISMB), held virtually on July 25-30, 2021. :doc:`You can find his slides here <presentations/ismb>`.
