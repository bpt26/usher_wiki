.. include:: includes.rst.txt

*********************************************
Explanations and Tutorials
*********************************************

This document contains detailed explanations and example workflows for Usher and matUtils.

.. _protobuf:
------------------------------------------------------------------
The Mutation Annotated Tree (MAT) Protocol Buffer (.pb)
------------------------------------------------------------------

Google's protocol buffer format is a highly optimized, flexible binary storage format, with APIs for many languages. 
We use a specially formatted protocol buffer to store a Mutation Annotated Tree object.

.. _extract:
--------------------------------------------
matUtils extract Explanation
--------------------------------------------

`matUtils extract` serves as a flexible prebuilt pipeline, which can quickly subset and convert an input MAT .pb file. 
Generally, its parameters can be grouped into four categories: 

1. Selection- these parameters define a subtree to use for further processing. If none are set, the whole input tree is used. Includes -c, -s, -m, and others.

2. Processing- these parameters, usually boolean in nature, apply specific processing steps to the subtree after selection. These can include selecting clade representative samples or collapsing the tree. Includes -O and -r among others.

3. Information- these parameters save information about the subtree which is not a direct representation of that subtree, such as mutations defining each clade in the subtree. Includes -C and -S among others.

4. Conversion- these parameters are used to request subtree representations in the indicated formats. Includes -v and -t among others.

These commands can be freely mixed and matched, allowing us to perform operations as simple as a direct vcf conversion by using a single conversion parameter:

.. code-block:: shell-session

  ./matUtils extract -i input.pb -v output.vcf

Rr as complex as multiple levels of selection of samples and writing of multiple output files by using parameters from all four categories.

.. code-block:: shell-session

    ./matUtils extract -i input.pb -c 19B -m A10042G -a 3 -S sample_paths.txt -O -o subtree.pb -t subtree.newick -d my_output/

`matUtils extract` is the workhorse function for manipulating MAT .pb files, particularly for any operations involving removing part of the .pb and converting .pb to other file formats.

.. _annotate:
---------------------------------
matUtils annotate Explanation
---------------------------------

`matUtils annotate` is a function for adding clade annotation information to the pb. This information can be accessed downstream by `matUtils extract` or other tools.

It has two general ways to add this information. The first, recommended fashion is to pass a simple two-column tsv containing clade and sample names. 
`matUtils annotate` will automatically identify the best clade root from this information with a three-step process.

1. It collects the set of mutations which are at at least -f allele frequency across the input samples; these represent the clade's likely defining mutations.

2. It creates a virtual sample from these mutations and uses Usher's highly optimized mapping algorithm to identify the internal nodes that it maps to best. These are candidate clade root nodes. Nodes directly ancestral to these sites are also considered as candidate roots.

3. For each of the candidate roots, the algorithm calculates the number of samples which are actually descendent of that node. The node which is ancestral to the most samples and which is not already assigned to another clade is assigned as the best clade root.

This does not guarantee that every sample that is member in the clade in the input will be a member of the clade at the end of assignment, but assignments are generally high quality.

The other option is simpler and more direct. Internal node identifiers can be passed directly through a two-column tsv and those nodes will be assigned as clade roots. 

.. warning::
    Internal node names are not maintained when saving and loading from a .pb file. It is not guaranteed that internal node names will correspond directly between two .pb files, so use the latter method with caution.

.. _uncertainty:
--------------------------------------------
matUtils uncertainty Explanation
--------------------------------------------

`matUtils uncertainty` calculates two specific metrics for sample placement certainty. These metrics can be very important to support contact tracing and reliable identification
of the origin of a newly placed sample.

The first of these is "equally parsimonious placements" (EPPs), which is the number of places on the tree a sample could be placed equally well. 
An EPPs score of 1 is a "perfect score", indicating that there is a single best placement for this sample on the tree. About 85% of samples on a normal SARS-COV-2 
phylogeny have an EPPs of 1. 

`matUtils uncertainty` calculates this metric by, for each sample in the input, remapping the sample against the same tree (disallowing it from mapping to itself) with Usher's optimized mapper function.
This function reports the number of best placements as part of the output, which is recorded by `matUtils uncertainty` and saved to the output.

The second metric is "neighborhood size score" (NSS), which is the longest direct traversable path between any two equally parsimonious placement locations for a given sample.
This metric is complementary to EPPs. When EPPs is 1, NSS is necessarily 0, as there are no traversable paths between pairs of placements when there's only one placement.

On an intuitive level, NSS is a representation of the distribution of equally parsimonious placements. For example, lets say we have two samples of interest. 
The first has five equally parsimonious placements, but they're all quite nearby each other on the tree with an LCA two nodes back.
The second has two equally parsimonious placements, but they're on opposite sides of the tree with an LCA at the root.
If we only looked at EPPs, we might assume that the second sample is more certain than the first. This is absolutely not the case-
the second sample could have originated from two different continents, while the first is likely from a specific local region. 
This is reflected in their NSS, which in the first case should be about 4, but in the latter could be in the tens to hundreds.

The most confident samples are ones which have an EPPs of 1 and an NSS of 0, followed by ones with low EPPS values and low NSS, followed by ones with higher EPPS and low NSS, and finally ones that are high on both metrics are least certain.

NSS is calculated by taking the set of equally parsimonious placements indicated by Usher's mapper function and identifying the LCA of all placements.
The two longest distances from the LCA to two placements are then summed and the result is reported as NSS- the longest direct path between two placements for the sample.

Both values are reported in distinct two-column tsvs, which are compatible with Auspice's metadata annotation for visualizing the samples. Information on this can be found `here <https://docs.nextstrain.org/projects/auspice/en/latest/advanced-functionality/drag-drop-csv-tsv.html>`_.