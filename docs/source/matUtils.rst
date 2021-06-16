.. include:: includes.rst.txt

***************
matUtils
***************

matUtils is a suite of tools used to analyze, edit, and manipulate mutation annotated tree (.pb) files. 

.. _protobuf:
-----------
The Mutation Annotated Tree (MAT) Protocol Buffer (.pb)
-----------

Google's `protocol buffer format <https://developers.google.com/protocol-buffers>`_ is a highly optimized, flexible binary storage format, with APIs for many languages. 
We use a specially formatted protocol buffer to store a Mutation Annotated Tree object. The .proto definition file can be found
in the Usher installation folder; we will describe it in brief here.

Our protobuf format has two major components. The first is a newick string, representing phylogenetic relationships between all samples included in the tree.
The second component is node information- including mutations, clade assignments, and condensed nodes. These components combined make the MAT into a powerful
data storage format, as it efficiently simultaneously represents phylogenetic relationships and full mutation information for large numbers of samples. 

When the protobuf is loaded into matUtils, the tree is structured based on the stored newick string, 
then mutations and metadata are placed along the tree structure according to the node information vectors. 
The condensed nodes message is used to compact polytomies and other groups of identical samples, 
and the final step of loading is to uncondense these nodes back into full polytomies.

This structure allows us to perform both classical phylogenetic processes, such as traversing the tree and calculating parsimony scores,
while also being able to query the structure as if it was a database of sequences, extracting a vcf of samples which contain a specific mutation for example.

----------------------
matUtils Common Options
----------------------

All matUtils subcommands include these parameters.

.. code-block:: shell-session

  --input-mat (-i): Input mutation-annotated tree file. (REQUIRED)
  --threads (-T): Number of threads to use when possible. Default = use all available cores.
  --help (-h): Print help messages.

-----------
summary
-----------

`matUtils summary` is used to get basic statistics and attribute information about the mat. 
If no specific arguments are set, prints the number of nodes, number of samples, number of condensed nodes, 
and total tree parsimony of the input mat to standard output.

Example Usage
----------------------

Get a tsv containing all sample names and parsimony scores.

.. code-block:: shell-session

  matUtils summary -i input.pb --samples all_samples.text

Write all possible summary output files to a specific directory.

.. code-block:: shell-session

  matUtils summary -i input.pb -A -d input_summary/

Specific Options
----------------------

.. code-block:: shell-session

  --input-mat (-i): Input mutation-annotated tree file [REQUIRED]. If only this argument is set, print the count of samples and nodes in the tree.
  --output-directory (-d): Write all output files to the target directory. Default is current directory
  --samples (-s): Write a two-column tsv listing all samples in the tree and their parsimony score (terminal branch length). Auspice-compatible.
  --clades (-c): Write a tsv listing all clades and the count of associated samples in the tree.
  --mutations (-m): Write a tsv listing all mutations in the tree and their occurrence count.
  --aberrant (-a): Write a tsv listing potentially problematic nodes, including duplicates and internal nodes with no mutations and/or branch length 0.
  --sample-clades (-C): Write a tsv listing all samples and their closest associated clade root in each annotation type column. 
  --get-all (-A): Write all possible tsv outputs with default file names (samples.txt, clades.txt, etc).


----------
extract
----------

`matUtils extract` serves as a flexible prebuilt pipeline, and serves as the primary tool for subsetting and converting a MAT pb to other file formats.
Generally, its parameters can be grouped into four categories: 

1. Selection- these parameters define a set of samples constituting a subtree to use for downstream analysis. If none are set, the whole input tree is used. Includes -c, -s, -m, and others.

2. Processing- these parameters, usually boolean, apply specific processing steps to the subtree after sample selection. These can include selecting clade representative samples or collapsing the tree. Includes -O and -r among others.

3. Information- these parameters save information about the subtree which is not a direct representation of that subtree, such as mutations defining each clade in the subtree. Includes -C and -S among others.

4. Conversion- these parameters are used to request subtree representations in the indicated formats. Includes -v and -t among others.

`matUtils extract` is the workhorse function for manipulating MAT .pb files, particularly for any operations involving removing part of the .pb and converting .pb to other file formats.

Example Usage
---------------------

Write a vcf representing all samples within a clade.

.. code-block:: shell-session

  matUtils extract -i input.pb -c my_clade -v my_clade.vcf

Write a newick tree of all samples which contain either of two mutations of interest.

.. code-block:: shell-session

  matUtils extract -i input.pb -m my_mutation,my_other_mutation -t my_mutations.txt

Convert a MAT JSON into a .pb file, while removing branches with length greater than 7.

.. code-block:: shell-session

  matUtils extract -i input.json -b 7 -o filtered.pb

Generate a MAT JSON representing a subtree of size 250 around a sample of interest, including multiple metadata files and filtering low-scoring samples.

.. code-block:: shell-session

  matUtils extract -i input.pb -a 5 -M my_metadata_1.tsv,my_metadata_2.tsv -k my_sample:250 -j my_sample_context.json

Specific Options
----------------------

.. code-block:: shell-session

  --input-mat (-i): For this specific command, the input can either be a standard MAT protobuf or an Augur-v2-formatted MAT JSON, ala Nextstrain.
  --samples (-s): Select samples by explicitly naming them, one per line in a plain text file.
  --metadata (-M): Comma delimited names of tsvs or csvs containing sample identifiers in the first column and an arbitrary number of metadata values in separate columns, including a header line in each file. Used only with -j and -K.
  --clade (-c): Select samples by membership in any of the indicated clade(s), comma delimited- e.g. -c clade1,clade2.
  --mutation (-m): Select samples by whether they contain any of the indicated mutation(s), comma delimited- e.g. -m mutation1,mutation2.
  --match (-H): Select samples by whether their identifier matches the indicated regex pattern.
  --max-epps (-e): Select samples by whether they have less than or equal to the maximum number of indicated equally parsimonious placements. Explanation of equally parsimonious placements is here INSERT LINK.
  --max-parsimony (-a): Select samples by whether they have less than or equal to the indicated maximum parsimony score (terminal branch length). 
  --max-branch-length (-b): Remove samples which have branches of greater than the indicated length in their ancestry.
  --nearest-k (-k): Select a specific sample and X context samples, formatted as "sample_name:X".
  --nearest-k-batch (-K): Pass a text file of sample IDs and a number of the number of context samples, formatted as sample_file.txt:k. These will be automatically written to a series of json files named "*sample-name*_context.json". Used for special large-scale operations.
  --set-size (-z): Automatically add or remove samples at random from the selected sample set until it is the indicated size.
  --get-representative (-r): Toggle to automatically select two representative samples per clade currently included in the tree, pruning all other samples from the tree. Applies after other selection steps.
  --prune (-p): Toggle to instead exclude all indicated samples from the subtree output.
  --resolve-polytomies (-R): Toggle to resolve all polytomies by assigning new internal nodes with branch length 0. Used for compatibility with other software.
  --output-directory (-d): Write all output files to the target directory. Default is current directory.
  --used-samples (-u): Write a simple text file containing selected sample names.
  --sample-paths (-S): Write the path of mutations defining all samples in the subtree to the indicated file.
  --clade-paths (-C): Write the path of mutations defining each clade in the subtree to the indicated file.
  --all-paths (-A): Write the mutations assigned to each node in the subtree in depth-first traversal order to the indicated file.
  --write-vcf (-v): Write a VCF representing the selected subtree to the target file.
  --no-genotypes (-n): Do not include sample genotype columns in VCF output. Used only with --write-vcf.
  --write-mat (-o): Write the selected subtree as a new protobuf file to the target file. 
  --collapse-tree (-O): Collapse the MAT before writing it to protobuf output. Used only with the write-mat option.
  --write-json (-j): Write an Auspice-compatbile json representing the selected subtree.
  --retain-branch-length (-E): Use to not recalculate branch lengths with saving newick output. Used only with -t
  --write-tree (-t): Write a newick string representing the selected subtree to the target file. 
  --minimum_subtrees_size (-N): Use to generate a series of JSON or Newick format files representing subtrees of the indicated size covering all queried samples. Uses and overrides -j and -t output arguments.
  --usher_single_subtree_size (-X): Use to produce an usher-style single sample subtree of the indicated size with all selected samples plus random samples to fill. Produces .nh and .txt files in the output directory.
  --usher_minimum_subtrees_size(-x): Use to produce an usher-style minimum set of subtrees of the indicated size which include all of the selected samples. Produces .nh and .txt files in the output directory.


-----------
annotate
-----------

`matUtils annotate` is a function for adding clade annotation information to the pb. This information can be accessed downstream by `matUtils extract` or other tools.

It has two general ways to add this information. The first, recommended fashion is to pass node identifiers to be be assigned as clade roots for each clade directly through a two-column tsv.

With the second method, the user can provide a set of names for the representative sequences for each clade in a two-column tsv from which the clade roots can be automatically inferred.
Specifically, `matUtils annotate` expects clades in the first column and sample identifiers in the second, as in the lineageToPublicName files available in our `database <https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/>`_.
The algorithm is described below:

1. It collects the set of mutations which are at at least -f allele frequency across the input samples; these represent the clade's likely defining mutations.

2. It creates a virtual sample from these mutations and uses Usher's highly optimized mapping algorithm to identify the internal nodes that it maps to best. These are candidate clade root nodes. Nodes directly ancestral to these sites are also considered as candidate roots.

3. For each of the candidate roots, the algorithm calculates the number of samples which are actually descendent of that node. The node which is ancestral to the most samples and which is not already assigned to another clade is assigned as the best clade root.

This method does not guarantee that every sample that is member in the clade in the input will be a member of the clade at the end of assignment, but assignments are generally high quality.



Example Usage
----------------------

Assign a new set of custom clade annotations to the tree.

.. code-block:: shell-session

  matUtils annotate -i input.pb -c my_clade_info.txt -o annotated.pb

Options
-----------

.. code-block:: shell-session

  --output-mat (-o): Path to output processed mutation-annotated tree file (REQUIRED)
  --clade-names (-c): Path to a file containing clade asssignments of samples. An algorithm automatically locates and annotates clade root nodes.
  --clade-to-nid (-C): Path to a tsv file mapping clades to their respective internal node identifiers. Use with caution.
  --allele-frequency (-f): Minimum allele frequency in input samples for finding the best clade root. Used only with -l. Default = 0.8.
  --set-overlap (-s): Minimum fraction of the lineage samples that should be desecendants of the assigned clade root. Defualt = 0.6.
  --clear-current (-l): Use to remove current annotations before applying new annotations.

----------------------
uncertainty
----------------------

`matUtils uncertainty` calculates two specific metrics for sample placement certainty. These metrics can be very important to support contact tracing and reliable identification
of the origin of a newly placed sample.

The first of these is "equally parsimonious placements" (EPPs), which is the number of places on the tree a sample could be placed equally well. 
An EPPs score of 1 is a "perfect score", indicating that there is a single best placement for this sample on the tree. About 85% of samples on a normal SARS-COV-2 
phylogeny have an EPPs of 1. 

`matUtils uncertainty` calculates this metric by, for each sample in the input, remapping the sample against the same tree (disallowing it from mapping to itself) with Usher's optimized mapper function.
This function reports the number of best placements as part of the output, which is recorded by `matUtils uncertainty` and saved to the text file.

The second metric is "neighborhood size score" (NSS), which is the longest direct traversable path between any two equally parsimonious placement locations for a given sample.
This metric is complementary to EPPs. When EPPs is 1, NSS is necessarily 0, as there are no traversable paths between pairs of placements when there's only one placement.

On an intuitive level, NSS is a representation of the distribution of equally parsimonious placements. For example, lets say we have two samples of interest. 
The first has five equally parsimonious placements, but they're all quite nearby each other on the tree with the LCA two nodes back.
The second has two equally parsimonious placements, but they're on opposite sides of the tree with the LCA at the root.
If we only looked at EPPs, we might assume that the second sample is more certain than the first. This is absolutely not the case-
the second sample could have originated from two different continents, while the first is likely from a specific local region. 
This is reflected in their NSS, which in the first case should be less than five, but in the latter case could be in the dozens.

The most confident samples are ones which have an EPPs of 1 and an NSS of 0, followed by ones with low EPPS values and low NSS, followed by ones with higher EPPS and low NSS, and finally ones that are high on both metrics.

NSS is calculated by taking the set of equally parsimonious placements indicated by Usher's mapper function and identifying the LCA of all placements.
The two longest distances from the LCA to two placements are then summed and the result is reported as NSS- the longest direct path between two placements for the sample.

An example workflow for calculating and visualizing uncertainty metrics can be found :ref:`here <uncertainty-tutorial>`.

Example Usage
----------------------

Calculate uncertainty metrics for a specific set of samples.

.. code-block:: shell-session

  matUtils uncertainty -i input.pb -s my_samples.txt -e my_uncertainty.tsv

Options
-----------

.. code-block:: shell-session

  --samples (-s): File containing samples to calculate metrics for.
  --find-epps (-e): Writes an Auspice-compatible two-column tsv of the number of equally parsimonious placements and neighborhood sizes for each sample to the target file. 
  --record-placements (-o): Name for an Auspice-compatible two-column tsv which records potential parents for each sample in the query set.
  
----------------------
introduce 
----------------------

`matUtils introduce` is used aid the analysis of the number of new introductions of the virus genome into a geographic region. `matUtils introduce` can calculate the association index (Wang et al. 2001) or the maximum monophyletic clade size statistic (Salemi et al. 2005; Parker et al. 2008) for arbitrary sets of samples, and also uses a new heuristic (currently experimental and described below) for estimating the points of introduction.

It requires a two-column tsv as input alongside the protobuf containing names of samples
and associated regions in the first and second columns respectively. Multiple regions can be processed simultaneously; in this mode, introduction points will be checked for whether 
they have significant support for originating from another input region.

An example workflow for inferring and visualizing geographic introductions can be found :ref:`here <introduce-tutorial>`.

Heuristic
-----------

The heuristic we use is a confidence metric which weights both the number and distance to the nearest descendent leaf which is a member of the input region
to infer whether each internal node is likely to represent sequences from that region. When the confidence metric is greater than 0.5, 
it is considered to be in the region. 

Leaves have their confidence heuristic as either 0 or 1 based on whether they are included in the regional input list. Internal nodes
are assigned as in-region if all descendent leaves are in-region, and similarly out if all descendent leaves are out-region. 
If their descendents are a mix of samples, we use the following calculation:

Do = the distance in mutations to the nearest descendent leaf that is not in region

Di = the distance in mutations to the nearest descendent leaf that is in the region

No = the number of leaf descendents which are not in the region

Ni = the number of leaf descendents which are in the region

confidence = 1 / (1 + ((Di/Ni)/(Do/No)))

This is essentially a ratio placed under a squash function such that equal numbers of leaves and distance to the nearest leaf for both in and out
of the region yield a confidence of 0.5, while descendents nearly being purely either in or out of the region will yield ~1 and ~0 respectively.

-----------
Introductions
-----------

Introduction points are identified as the point along a sample's history where the confidence of the 
relevant node being in the region drops below 0.5. In many sample's cases, this may be the direct parent of the sample, implying that the
sample is a novel introduction to a region; in other cases, it may share the introduction point with a number of other samples from that region.

Introductions are calculated for each region independently with multiple region input, but after introductions are identified the support for 
the origin point for membership in each other region is checked. Origins with a confidence of >0.5 membership in other regions are recorded
in the output, and if none are found the origin is labeled as indeterminate.

Phylogeographic Statistics and Other Options
-----------

`matUtils introduce` supports the calculation and recording of maximum monophyletic clade size and association index, statistics
for phylogeographic trait association, on a per-region and per-introduction basis. Maximum monophyletic clade size is simply the largest 
monophyletic clade of samples which are in the region; it is larger for regions which have relatively fewer introductions per sample and 
correlates with overall sample number (Parker et al 2008). Association index is a more complex metric, related to our heuristic,
which performs a weighted summation across the tree account for the number of child nodes and the frequency of the most common trait (Wang et al 2001). 
Association index is smaller for stronger phylogeographic association; it increases with the relative number of introductions into a region.
For association index, `matUtils introduce` also performs a series of permutations to establish an expected range of values for the random distribution of samples across the tree.

Most proper regions will have association indeces significantly smaller than this range; the ratio between the actual and mean expected
association indices can be informative for the overall level of isolation or relative level of community spread for a region.

Calculating these statistics adds significantly to runtime, so they are optional to calculate and intended for users who want a 
stronger statistical grounding for their results.

Finally, it supports inference of the region of origin for all annotated clade roots currently in the tree based on 
these confidence metrics, though only from among input regions. 

Wang, T.H., Donaldson, Y.K., Brettle, R.P., Bell, J.E., and Simmonds, P. (2001). Identification of Shared Populations of Human Immunodeficiency Virus Type 1 Infecting Microglia and Tissue Macrophages outside the Central Nervous System. Journal of Virology 75, 11686–11699.

Salemi M, Lamers SL, Yu S, de Oliveira T, Fitch WM, McGrath MS. 2005. Phylodynamic Analysis of Human Immunodeficiency Virus Type 1 in Distinct Brain Compartments Provides a Model for the Neuropathogenesis of AIDS. J Virol 79:11343–11352.

Parker, J., Rambaut, A., and Pybus, O.G. (2008). Correlating viral phenotypes with phylogeny: Accounting for phylogenetic uncertainty. Infection, Genetics and Evolution 8, 239–246.

Example Usage
----------------------

Generate a tsv containing inferred introduction information, one sample per row.

.. code-block:: shell-session

  matUtils introduce -i public.pb -s my_region_samples.txt -o my_region_introductions.tsv

Options
-----------

.. code-block:: shell-session

  --population-samples (-s): Two-column tab-separated text file containing sample names and region membership respectively (REQUIRED)
  --output (-o): Name of the output tab-separated table containing inferred introductions, one sample per row (REQUIRED)
  --additional-info (-a): Use to calculate additional phylogeographic statistics about your region and inferred introductions.
  --clade-regions (-c): Set to optionally write a tab-separated table containing inferred origins for each clade currently annotated in the tree from among your regions.
  --origin-confidence (-C): Set to a confidence value between 0 and 1 at which to state that a node is in-region. Default is 0.5
  --evaluate-metadata (-E): Set to assign each leaf a confidence value based on distance-weighted ancestor confidence.
  --dump-assignments (-D): Indicate a directory to which to write two-column text files containing node-confidence assignments for downstream processing.

----------------------
mask [EXPERIMENTAL]
----------------------

`matUtils mask` is used to mask specific samples out of the pb, removing their mutations from visibility.

Example Usage
----------------------

Mask out a specific set of samples.

.. code-block:: shell-session

  matUtils mask -i input.pb -s private_samples.txt -o masked.pb 

Options
-----------

.. code-block:: shell-session

  --output-mat (-o): Path to output processed mutation-annotated tree file (REQUIRED)
  --restricted-samples (-s): Sample names to restrict. Use to perform masking. 
