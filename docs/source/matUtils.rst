.. include:: /Includes.rst.txt

***************
matUtils
***************

matUtils is a suite of tools used to analyze, edit, and manipulate mutation annotated tree (.pb) files. 

-----------
annotate
-----------

`matUtils annotate` is used to add metadata, and to calculate and store uncertainty metrics.

Options
-----------

.. code-block:: shell-session

  --input-mat (-i): Input mutation-annotated tree file. (REQUIRED)
  --output-mat (-o): Path to output processed mutation-annotated tree file (REQUIRED)
  --clade-names (-c): Path to a file containing clade asssignments of samples. Use to locate and annotate clade root nodes. 
  --allele-frequency (-f): Minimum allele frequency in input samples for finding the best clade root. Used only with -l. Default = 0.800000012.
  --set-overlap (-s): Minimum fraction of the lineage samples that should be desecendants of the assigned clade root. Defualt = 0.600000024.
  --threads (-T): Number of threads to use when possible. Default = use all available cores.
  --help (-h): Print help messages.

----------
filter
----------

`matUtils filter` is used to mask or strip high-uncertainty samples from a .pb file.

Options
-----------

.. code-block:: shell-session

  --input-mat (-i): Input mutation-annotated tree file. (REQUIRED) 
  --output-mat (-o): Path to output processed mutation-annotated tree file (REQUIRED)
  --restricted-samples (-s): Sample names to restrict. Use to perform masking. 
  --threads (-T): Number of threads to use when possible. Default = use all available cores.
  --help (-h): Print help messages.

----------
convert
----------

`matUtils convert` is used to convert a .pb file into either a newick-formatted tree, or a .vcf file.

Options
-----------

.. code-block:: shell-session

  --input-mat (-i): Input mutation-annotated tree file. (REQUIRED) 
  --write-vcf (-v): Output VCF file.  
  --no-genotypes (-n): Do not include sample genotype columns in VCF. output. Used only with the --write-vcf option.  
  --write-tree (-t): Use to write a newick tree to the indicated file.
  --threads (-T): Number of threads to use when possible. Default = use all available cores.  
  --help (-h): Print help messages.

-----------
prune
-----------

`matUtils prune` works similarly to the prune functions in `tree_doctor <http://manpages.ubuntu.com/manpages/bionic/man1/tree_doctor.1.html>`_ and is used for fast pruning of phylogenies to include only the desired samples.


Options
-----------

.. code-block:: shell-session

  --input-mat (-i): Input mutation-annotated tree file. (REQUIRED)  
  --output-mat (-o): Path to output processed mutation-annotated tree file. (REQUIRED)
  --prune-samples (-p): File containing names of samples (one per line) to be pruned from the input MAT.
  --prune-all-but-samples (-P): File containing names of samples (one per line) to be maintained (remaining are pruned) from the input MAT.
  --threads (-T): Number of threads to use when possible. Default = use all available cores.
  --help (-h): Print help messages.

-----------
describe
-----------

`matUtils describe` takes a mutation annotated tree object and a list of samples of interest as inputs, and outputs the mutation paths for those samples.

Options
-----------

.. code-block:: shell-session

  --input-mat (-i): Input mutation-annotated tree file. (REQUIRED)  
  --mutation-paths (-m): File containing sample names for which mutation paths should be displayed. (REQUIRED])  
  --threads (-T): Number of threads to use when possible. Default = use all available cores.
  --help (-h): Print help messages.
