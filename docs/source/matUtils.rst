.. include:: includes.rst.txt

***************
matUtils
***************

matUtils is a suite of tools used to analyze, edit, and manipulate mutation annotated tree (.pb) files. 

-----------
Common Options
-----------

All matUtils subcommands include these parameters.

.. code-block:: shell-session

  --input-mat (-i): Input mutation-annotated tree file. (REQUIRED)
  --threads (-T): Number of threads to use when possible. Default = use all available cores.
  --help (-h): Print help messages.

----------
extract
----------

`matUtils extract` is used for tasks related to selection from and conversion of mutation annotated tree (.pb) files to other formats. 
Subtrees can be queried in a number of ways, including by sample certainty or clade membership. Output formats include newick and VCF.
A detailed explanation and examples usage can be found :ref:`here <extract>`.

Example Usage
----------

Write a vcf representing all samples within a clade.

.. code-block:: shell-session

  ./matUtils extract -i input.pb -c my_clade -v my_clade.vcf

Write a newick tree of all samples which contain either of two mutations of interest.

.. code-block:: shell-session

  ./matUtils extract -i input.pb -m my_mutation,my_other_mutation -t my_mutations.txt

Remove samples with a parsimony score greater than five and save a new pb without these samples.

.. code-block:: shell-session

  ./matUtils extract -i input.pb -a 5 -o filtered.pb

Specific Options
-----------

.. code-block:: shell-session

  --samples (-s): Select samples by explicitly naming them, one per line in a plain text file.
  --clade (-c): Select samples by membership in any of the indicated clade(s), comma delimited- e.g. -c clade1,clade2.
  --mutation (-m): Select samples by whether they contain any of the indicated mutation(s), comma delimited- e.g. -m mutation1,mutation2.
  --max-epps (-e): Select samples by whether they have less than or equal to the maximum number of indicated equally parsimonious placements. Explanation of equally parsimonious placements is here INSERT LINK.
  --max-parsimony (-a): Select samples by whether they have less than or equal to the indicated maximum parsimony score (terminal branch length). 
  --nearest-k (-k): Select a specific sample and X context samples, formatted as "sample_name:X".
  --get-representative (-r): Toggle to automatically select two representative samples per clade currently included in the tree, pruning all other samples from the tree. Applies after other selection steps.
  --prune (-p): Toggle to instead exclude all indicated samples from the subtree output.
  --resolve-polytomies (-R): Toggle to resolve all polytomies by assigning new internal nodes with branch length 0. Used for compatibility with other software.
  --output-directory (-D): Write all output files to the target directory. Default is current directory.
  --sample-paths (-S): Write the path of mutations defining all samples in the subtree to the indicated file.
  --clade-paths (-C): Write the path of mutations defining each clade in the subtree to the indicated file.
  --all-paths (-A): Write the mutations assigned to each node in the subtree in depth-first traversal order to the indicated file.
  --write-vcf (-v): Write a VCF representing the selected subtree to the target file.
  --no-genotypes (-n): Do not include sample genotype columns in VCF output. Used only with --write-vcf.
  --write-mat (-o): Write the selected subtree as a new protobuf file to the target file. 
  --collapse-tree (-O): Collapse the MAT before writing it to protobuf output. Used only with the write-mat option.
  --write-tree (-t): Write a newick string representing the selected subtree to the target file. 

-----------
summary
-----------

`matUtils summary` is used to get basic statistics and attribute information about the mat. 
If no specific arguments are set, prints the number of nodes, number of samples, number of condensed nodes, 
and total tree parsimony of the input mat to standard output.

Example Usage
-----------

Get a tsv containing all sample names and parsimony scores.

.. code-block:: shell-session

  ./matUtils summary -i input.pb --samples all_samples.text

Write all possible summary output files to a specific directory.

.. code-block:: shell-session

  ./matUtils summary -i input.pb -A -d input_summary/

Specific Options
-----------

.. code-block:: shell-session

  --output-directory (-d): Write all output files to the target directory. Default is current directory
  --samples (-s): Write a two-column tsv listing all samples in the tree and their parsimony score (terminal branch length). Auspice-compatible.
  --clades (-c): Write a tsv listing all clades and the count of associated samples in the tree.
  --mutations (-m): Write a tsv listing all mutations in the tree and their occurrence count.
  --aberrant (-a): Write a tsv listing potentially problematic nodes, including duplicates and internal nodes with no mutations and/or branch length 0.
  --get-all (-A): Write all possible tsv outputs with default file names (samples.txt, clades.txt, etc).

-----------
annotate
-----------

`matUtils annotate` is used to add clade assignment metadata. 
Generally this will use a simple algorithm to identify the clade root node when given a 
text file of samples associated with that clade. The input file is expected to be a two column tsv of sample and clade assignment.
A more detailed explanation and tutorial can be found :ref:`here <annotate>`.

Example Usage
-----------

Assign a new set of custom clade annotations to the tree.

.. code-block:: shell-session

  ./matUtils annotate -i input.pb -c my_clade_info.txt -o annotated.pb

Options
-----------

.. code-block:: shell-session

  --output-mat (-o): Path to output processed mutation-annotated tree file (REQUIRED)
  --clade-names (-c): Path to a file containing clade asssignments of samples. An algorithm automatically locates and annotates clade root nodes.
  --clade-to-nid (-C): Path to a tsv file mapping clades to their respective internal node identifiers. Use with caution.
  --allele-frequency (-f): Minimum allele frequency in input samples for finding the best clade root. Used only with -l. Default = 0.8.
  --set-overlap (-s): Minimum fraction of the lineage samples that should be desecendants of the assigned clade root. Defualt = 0.6.
  --clear-current (-l): Use to remove current annotations before applying new annotations.

-----------
uncertainty
-----------

`matUtils uncertainty` is used to calculate sample placement and tree quality metrics. 
Detailed explanations of these metrics and usage tutorial can be found :ref:`here <uncertainty>`.

Example Usage
-----------

Calculate uncertainty metrics for a specific set of samples.

.. code-block:: shell-session

  ./matUtils uncertainty -i input.pb -s my_samples.txt -e my_epps.tsv -n my_neighborhood.tsv

Options
-----------

.. code-block:: shell-session

  --samples (-s): File containing samples to calculate metrics for.
  --get-parsimony (-g): Calculate and print the total tree parsimony score.
  --find-epps (-e): Writes an Auspice-compatible two-column tsv of the number of equally parsimonious placements for each sample to the target file. 
  --find-neighborhood (-n): Writes an Auspice-compatible two-column tsv of the neighborhood size scores to the target file.

-----------
mask [EXPERIMENTAL]
-----------

`matUtils mask` is used to mask specific samples out of the pb, removing their mutations from visibility.

Example Usage
-----------

Mask out a specific set of samples.

.. code-block:: shell-session

  ./matUtils -i input.pb -s private_samples.txt -o masked.pb 

Options
-----------

.. code-block:: shell-session

  --output-mat (-o): Path to output processed mutation-annotated tree file (REQUIRED)
  --restricted-samples (-s): Sample names to restrict. Use to perform masking. 
