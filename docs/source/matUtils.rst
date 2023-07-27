.. include:: includes.rst.txt

***************
matUtils
***************

matUtils is a suite of tools used to analyze, edit, and manipulate mutation annotated tree (.pb) files, such as the ones shared in our public SARS-CoV-2 MAT database (http://hgdownload.soe.ucsc.edu/goldenPath/wuhCor1/UShER_SARS-CoV-2/) or those constructed via UShER (read `this <https://usher-wiki.readthedocs.io/en/latest/UShER.html#converting-raw-sequences-into-vcf-for-usher-input>`__ and `this <https://usher-wiki.readthedocs.io/en/latest/UShER.html#pre-processing-global-phylogeny>`__ for steps to construct a MAT from an input phylogeny and an alignment). 

.. _protobuf:

-----------------
Installation
-----------------

To install matUtils, simply follow the directions for `installing UShER <https://usher-wiki.readthedocs.io/en/latest/Installation.html>`_, and matUtils will be included in your installation.

------------------------------------------------------------
The Mutation Annotated Tree (MAT) Protocol Buffer (.pb)
------------------------------------------------------------

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

-----------------------------
matUtils Common Options
-----------------------------

All matUtils subcommands include these parameters.

.. code-block:: sh

  --input-mat (-i): Input mutation-annotated tree file. (REQUIRED)
  --threads (-T): Number of threads to use when possible. Default = use all available cores.
  --help (-h): Print help messages.

-----------
summary
-----------

`matUtils summary` is used to get basic statistics and attribute information about the mat. 
If no specific arguments are set, prints the number of nodes, number of samples, number of condensed nodes, 
and total tree parsimony of the input mat to standard output.

**Amino acid translations**

``matUtils summary --translate <output.tsv> -i <input.pb> -g <annotations.gtf> -f <reference.fasta>`` 

performs phylogenetically informed annotation of amino acid mutations. 

The user provides as input a protobuf file, a GTF file containing gene annotations, and a FASTA reference sequence.

.. note:: 
    The input GTF must follow the conventions specified `here <https://mblab.wustl.edu/GTF22.html>`__.
    If multiple ``CDS`` features are associated with a single ``gene_id``,
    they must be ordered by start position. An example GTF for SARS-CoV-2 can be found `here <http://hgdownload.soe.ucsc.edu/goldenPath/wuhCor1/bigZips/genes/ncbiGenes.gtf.gz>`__.

The output format is a TSV file with four columns, with one line per node (only including nodes with mutations), e.g.

.. code-block::

    node_id     aa_mutations            nt_mutations        codon_changes        leaves_sharing_mutations
    Sample1     ORF7a:E121D;ORF7b:M1L   A27756T;A27756T     GAG>GTG;GAG>GTG        1
    Sample2     S:R905R                 G24277A             GGG>AGG        1
    Sample5     S:Y756N                 T23828A             CCT>CCA        1
    node_2      M:V60G;M:V66A           T26701G;T26719C     GTA>GGA;ACT>ACC        2
    Sample4     M:G60R;M:A66V           G26700C;C26719T     GTA>CTA;ACC>ACT        1
    Sample3     M:T30A                  A26610G             TTA>TTG        1

``aa_mutations`` are always delimited by a ``;`` character, and can be matched with their corresponding nucleotide mutations in the ``nt_mutations`` column (also delimited by ``;``). Codon changes are encoded similarly. 
 
If there are multiple nucleotide mutations in one node affecting a single codon (rare), they will be separated by commas in the ``nt_mutations`` column.


In the case that a single nucleotide mutation affects multiple codons,
the affected codons are listed sequentially, and the nucleotide mutation is repeated in the ``nt_mutation`` column.

``leaves_sharing_mutations`` indicates the number of descendant leaves of the node that share its set of mutations (including itself, if the node is a leaf).

**RoHo score**

Additionally, `matUtils summary` can quickly calculate the RoHo score and related values described in `van Dorp et al 2020 <https://doi.org/10.1038/s41467-020-19818-2>`_.
Briefly, the RoHo or Ratio of Homoplasic Offspring is the ratio of the number of descendents in sister clades with or without a specific mutation over the occurrence of 
all mutations; homoplasic and positively-selected mutations will recur with increased descendent clade sizes at each occurrence. This can be used to quickly
and conservatively scan for variants of concern. A full explanation of our implementation and tutorial can be found :ref:`here.<roho-tutorial>`

Example Usage
----------------------

1. Get a tsv containing all sample names and parsimony scores.

.. code-block:: sh

  matUtils summary -i input.pb --samples samples.txt

.. code-block:: sh

  matUtils summary -i public-2021-06-09.all.masked.nextclade.pangolin.pb.gz --samples 06-09_samples.txt

2. Write all possible summary output files to a specific directory.

.. code-block:: sh

  matUtils summary -i input.pb -A -d input_summary/

3. Get amino acid translations of each node in a tree

.. code-block:: sh

  matUtils summary -t translate_output.tsv -i input.pb -g annotation.gtf -f reference.fasta


**Example command**

Files needed:

a. `public-2021-06-09.all.masked.nextclade.pangolin.pb.gz <https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/2021/06/09/public-2021-06-09.all.masked.nextclade.pangolin.pb.gz>`_

.. code-block:: sh

  matUtils summary -i public-2021-06-09.all.masked.nextclade.pangolin.pb.gz -A -d 06-09_summary/

Specific Options
----------------------

.. code-block:: sh

  --input-mat (-i): Input mutation-annotated tree file [REQUIRED]. If only this argument is set, print the count of samples and nodes in the tree.
  --input-gtf (-g): Input GTF annotation file. Required for --translate (-t)
  --input-fasta (-g): Input FASTA reference sequence. Required for --translate (-t)
  --output-directory (-d): Write all output files to the target directory. Default is current directory
  --samples (-s): Write a two-column tsv listing all samples in the tree and their parsimony score (terminal branch length). Auspice-compatible.
  --clades (-c): Write a tsv listing all clades and the count of associated samples in the tree.
  --mutations (-m): Write a tsv listing all mutations in the tree and their occurrence count.
  --translate (-t): Write a tsv listing the amino acid and nucleotide mutations at each node.
  --aberrant (-a): Write a tsv listing potentially problematic nodes, including duplicates and internal nodes with no mutations and/or branch length 0.
  --haplotype (-H): Write a tsv listing haplotypes represented by comma-delimited lists of mutations and their count across the tree.
  --sample-clades (-C): Write a tsv listing all samples and their clades. 
  --calculate-roho (-R): Write a tsv listing, for each mutation occurrence that is valid, the number of offspring and other numbers for RoHo calculation.
  --expanded-roho (-E): Use to include date and other contextual information in the RoHO output. Significantly slows calculation time.
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

Example Syntax and Usage
----------------------------

1. Write a vcf representing all samples within a clade.

.. code-block:: sh

  matUtils extract -i input.pb -c my_clade -v my_clade.vcf

.. code-block:: sh

  matUtils extract -i public-2021-06-09.all.masked.nextclade.pangolin.pb.gz -c B.1.351 -v 351_samples.vcf
  
The VCF file can be converted to a Fasta files (one for each sequence in the VCF) using vcf2fasta (see installation instructions `here <https://github.com/vcflib/vcflib#install>`_) and the reference sequence (in NC_045512v2.fa) as follows:
  
.. code-block:: sh

  vcfindex 351_samples.vcf
  vcf2fasta -f NC_045512v2.fa 351_samples.vcf
  
Note that indels are ignored in the above approach since they're not included in the MAT.

2. Write a newick tree of all samples which contain either of two mutations of interest.

.. code-block:: sh

  matUtils extract -i input.pb -m my_mutation,my_other_mutation -t my_mutations.nwk

.. code-block:: sh

  matUtils extract -i public-2021-06-09.all.masked.nextclade.pangolin.pb.gz -m G7328T,A8653G -t double_mutant.nwk

3. Convert a MAT JSON into a .pb file, while removing branches with length greater than 7.

.. code-block:: sh

  matUtils extract -i input.json -b 7 -o filtered.pb

.. code-block:: sh

  matUtils extract -i usa_group.json -b 7 -o filtered_usa_group.pb

4. Generate a MAT JSON representing a subtree of size 25 around a sample of interest, including multiple metadata files and filtering low-scoring samples.

.. code-block:: sh

  matUtils extract -i input.pb -a 5 -M my_metadata_1.tsv,my_metadata_2.tsv -k my_sample:25 -j my_sample_context.json


**Example command**

Files needed:

a. `public-2021-06-09.all.masked.nextclade.pangolin.pb.gz <https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/2021/06/09/public-2021-06-09.all.masked.nextclade.pangolin.pb.gz>`_

b. :download:`usa_group.json <./usa_group.json>`

c. :download:`region.tsv <./meta_1.tsv>`

d. :download:`misc.tsv <./meta_2.tsv>`

.. code-block:: sh

  matUtils extract -i public-2021-06-09.all.masked.nextclade.pangolin.pb.gz -a 5 -M meta_1.tsv,meta_2.tsv -k "Scotland/CVR6436/2020|2020-12-30:25" -j cluster.json


Specific Options
----------------------

.. code-block:: sh

  --input-mat (-i): For this specific command, the input can either be a standard MAT protobuf or an Augur-v2-formatted MAT JSON, ala Nextstrain.
  --input-gtf (-g): Input GTF annotation file. Required for --write-taxodium.
  --input-fasta (-f): Input FASTA reference sequence. Required for --write-taxodium.
  --samples (-s): Select samples by explicitly naming them, one per line in a plain text file.
  --metadata (-M): Comma delimited names of tsvs or csvs containing sample identifiers in the first column and an arbitrary number of metadata values in separate columns, including a header line in each file. Used only with -j and -K.
  --clade (-c): Select samples by membership in any of the indicated clade(s), comma delimited- e.g. -c clade1,clade2.
  --mutation (-m): Select samples by whether they contain any of the indicated mutation(s), comma delimited- e.g. -m mutation1,mutation2.
  --match (-H): Select samples by whether their identifier matches the indicated regex pattern.
  --max-epps (-e): Select samples by whether they have less than or equal to the maximum number of indicated equally parsimonious placements. Explanation of equally parsimonious placements is here INSERT LINK.
  --max-parsimony (-a): Select samples by whether they have less than or equal to the indicated maximum parsimony score (terminal branch length). 
  --max-branch-length (-b): Remove samples which have branches of greater than the indicated length in their ancestry.
  --max-path-length (-P): Select samples which have a total path length (number of mutations different from reference) less than or equal to the indicated value.
  --nearest-k (-k): Select a specific sample and X context samples, formatted as "sample_name:X".
  --nearest-k-batch (-K): Pass a text file of sample IDs and a number of the number of context samples, formatted as sample_file.txt:k. These will be automatically written to a series of json files named "*sample-name*_context.json". Used for special large-scale operations.
  --get-internal-descendents (-I): Select the set of samples descended from the indicated internal node.
  --from-mrca (-U): Select all samples which are descended from the most recent common ancestor of the indicated set of samples. Applied before filling background with random samples.
  --set-size (-z): Automatically add or remove samples at random from the selected sample set until it is the indicated size.
  --limit-to-lca (-Z): Use to limit random samples chosen with -z or -W to below the most recent common ancestor of all other samples.
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
  --write-taxodium (-l): Write a taxodium-format protobuf to the target file.
  --x-scale (-G): Specifies custom X-axis scaling for Taxodium output. Does not affect other output formats.
  --title (-B): Title to include in --write-taxodium output.
  --description (-D): Description to include in --write-taxodium output.
  --include-nt (-J): Include nucleotide changes in the taxodium output.
  --extra-fields (-F): Comma delimited list of additional fields to include in --write-taxodium output.
  --minimum-subtrees-size (-N): Use to generate a series of JSON or Newick format files representing subtrees of the indicated size covering all queried samples. Uses and overrides -j and -t output arguments.
  --reroot (-y): Indicate an internal node ID to reroot the output tree to. Applied before all other manipulation steps.
  --usher-single-subtree-size (-X): Use to produce an usher-style single sample subtree of the indicated size with all selected samples plus random samples to fill. Produces .nh and .txt files in the output directory.
  --usher-minimum-subtrees-size(-x): Use to produce an usher-style minimum set of subtrees of the indicated size which include all of the selected samples. Produces .nh and .txt files in the output directory.
  --usher-clades-txt: Use to write an usher-style clades.txt alongside an usher-style subtree with -x or -X.
  --add-random (-W): Add exactly W samples to your selection at random. Affected by -Z and overridden by -z.
  --closest-relatives (-V): Write a tsv file of the closest relative(s) (in mutations) of each selected sample to the indicated file. All equidistant closest samples are included unless --break-ties is set.
  --break-ties (-q): Only output one closest relative per sample (used only with --closest-relatives). If multiple closest relatives are equidistant, the lexicographically smallest sample ID is chosen.
  --select-nearest (-Y): Set to add to the sample selection the nearest Y samples to each of your samples, without duplication.
  --dump-metadata (-Q): Set to write all final stored metadata as a tsv.
  --whitelist (-L): Pass a list of samples, one per line, to always retain in the output regardless of any other parameters.

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

Example Syntax and Usage
-----------------------------

1. Assign a new set of custom clade annotations to the tree.

.. code-block:: sh

  matUtils annotate -i input.pb -c my_clade_info.txt -o annotated.pb

**Example command**

Files needed:

a. `public-2021-06-09.all.masked.pb.gz <https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/2021/06/09/public-2021-06-09.all.masked.pb.gz>`_

b. `cladeToPublicName.gz <https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/2021/06/09/cladeToPublicName.gz>`_

.. code-block:: sh

  gunzip -c cladeToPublicName.gz > clade_info.txt
  matUtils annotate -i public-2021-06-09.all.masked.pb.gz -c clade_info.txt -o nxts_annotated.pb


Specific Options
------------------

.. code-block:: sh

  --output-mat (-o): Path to output processed mutation-annotated tree file (REQUIRED)
  --clade-names (-c): Path to a file containing clade asssignments of samples. An algorithm automatically locates and annotates clade root nodes.
  --clade-to-nid (-C): Path to a tsv file mapping clades to their respective internal node identifiers. Use with caution.
  --clade-paths (-P): Path to a tsv file mapping clades to mutation paths which must exist in the tree.  Format is the same as the first and third columns of the output of matUtils extract --clade-paths.
  --clade-mutations (-M): Path to a tsv file mapping clades to sets of mutations (separated by spaces,commas and/or >s) which will be used instead of extracting mutations from samples named in the --clade-names file.  If used together with --clade-names, this takes precedence.
  --allele-frequency (-f): Minimum allele frequency in input samples for finding the best clade root. Used only with -l. Default = 0.8.
  --mask-frequency (-m): Minimum allele frequency below -f in input samples that should be masked for finding the best clade root. Used only with -c.
  --clip-sample-frequency (-p): Maximum proportion of samples in a branch that are exemplars from -c to consider when sorting candidate clade root nodes. Default 0.1
  --set-overlap (-s): Minimum fraction of the lineage samples that should be desecendants of the assigned clade root. Defualt = 0.6.
  --clear-current (-l): Use to remove current annotations before applying new annotations.
  --output-directory (-d): Write output files to the target directory.
  --write-mutations (-u): Write a tsv listing each clade and the mutations found in at least [-f] of the samples. Used only with -c.
  --write-details (-D): Write a tsv with details about the nodes considered for each clade root. Used only with -c

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

Example Syntax and Usage
-----------------------------

1. Calculate uncertainty metrics for a specific set of samples.

.. code-block:: sh

  matUtils uncertainty -i input.pb -s my_samples.txt -e my_uncertainty.tsv

**Example command**

Files needed:

a. `public-2021-06-09.all.masked.nextclade.pangolin.pb.gz <https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/2021/06/09/public-2021-06-09.all.masked.nextclade.pangolin.pb.gz>`_

b. :download:`eng_samples.txt<./eng_samples.txt>`

.. code-block:: sh

  matUtils uncertainty -i public-2021-06-09.all.masked.nextclade.pangolin.pb.gz -s eng_samples.txt -e eng_uncertainty.tsv


Options
-----------

.. code-block:: sh

  --samples (-s): File containing samples to calculate metrics for.
  --find-epps (-e): Writes an Auspice-compatible two-column tsv of the number of equally parsimonious placements and neighborhood sizes for each sample to the target file. 
  --record-placements (-o): Name for an Auspice-compatible two-column tsv which records potential parents for each sample in the query set.
  --dropout-mutations (-d): Name a file to calculate and store locally-recurrent mutations which may be associated with primer dropout. [EXPERIMENTAL]

----------------------
introduce 
----------------------

`matUtils introduce` is used aid the analysis of the number of new introductions of the virus genome into a geographic region. `matUtils introduce` can calculate the association index (Wang et al. 2001) or the maximum monophyletic clade size statistic (Salemi et al. 2005; Parker et al. 2008) for arbitrary sets of samples, and also uses a new heuristic (currently experimental and described below) for estimating the points of introduction.

It requires a two-column tsv as input alongside the protobuf containing names of samples
and associated regions in the first and second columns respectively. Multiple regions can be processed simultaneously; in this mode, introduction points will be checked for whether 
they have significant support for originating from another input region.

matUtils introduce uses date ranges to sort the output so that the largest clusters occurring in the shortest timespan are printed first. 
Date can be automatically parsed from the sample name if the sample has standard formatting or passed in as a separate file with -M. In the 
latter case, the first row should be a header containing "sample_id" and "date" (other columns will be ignored). Each date included should be formatted as XXXX-XX-XX with 
zeroes filled in as needed (e.g. 2021-01-03) and samples excluded from this file but included in the sample region input (-s) will have their date 
ignored for the purposes of establishing active date ranges for their cluster.

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

Introduction points are identified as the point along a sample's history where the confidence of the 
relevant node being in the region drops below 0.5. In many sample's cases, this may be the direct parent of the sample, implying that the
sample is a novel introduction to a region; in other cases, it may share the introduction point with a number of other samples from that region.

Introductions are calculated for each region independently with multiple region input, but after introductions are identified the support for 
the origin point for membership in each other region is checked. Origins with a confidence of >0.5 membership in other regions are recorded
in the output, and if none are found the origin is labeled as indeterminate.

`matUtils introduce` yields a by-sample output table which includes cluster level statistics in the first few columns. Notable among these is
cluster growth score, which is simply the number of samples from the cluster divided by one plus the number of weeks separating the oldest and most
recent samples of the cluster, rounded down. Clusters are printed in order of their rank by this score, putting putative outbreaks and groups 
of most concern at the top of the output file.

Phylogeographic Statistics and Other Options
----------------------------------------------

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

Example Syntax and Usage
-----------------------------

1. Generate a tsv containing inferred introduction information, one sample per row.

.. code-block:: sh

  matUtils introduce -i public.pb -s my_region_samples.txt -o my_region_introductions.tsv
  
**Example command**

Files needed:

a. `public-2021-06-09.all.masked.nextclade.pangolin.pb.gz <https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/2021/06/09/public-2021-06-09.all.masked.nextclade.pangolin.pb.gz>`_

b. :download:`regional-samples.txt <./regional-samples.txt>`

.. code-block:: sh

  matUtils introduce -i public-2021-06-09.all.masked.nextclade.pangolin.pb.gz -s regional-samples.txt -o regional-introductions.tsv


Options
-----------

.. code-block:: sh

  --population-samples (-s): Two-column tab-separated text file containing sample names and region membership respectively (REQUIRED)
  --output (-o): Name of the output tab-separated table containing inferred introductions, one sample per row (REQUIRED)
  --additional-info (-a): Use to calculate additional phylogeographic statistics about your region and inferred introductions.
  --clade-regions (-c): Set to optionally write a tab-separated table containing inferred origins for each clade currently annotated in the tree from among your regions.
  --date-metadata (-M): Pass a TSV or CSV containing a 'date' column to use for date information. If not used, date will be inferred from the sample name where possible.
  --origin-confidence (-C): Set to a confidence value between 0 and 1 at which to state that a node is in-region. Default is 0.5
  --evaluate-metadata (-E): Set to assign each leaf a confidence value based on distance-weighted ancestor confidence.
  --dump-assignments (-D): Indicate a directory to which to write two-column text files containing node-confidence assignments for downstream processing.
  --cluster-output (-u): Write a one-cluster-per-row version of the output table to the indicated file.
  --latest-date (-l): Limit reported clusters to ones with at least one sample past the indicated date.
  --earliest-date (-L): Limit reported clusters to ones with ALL samples past the indicated date.
  --num-to-report (-r): Report the top r scoring potential origins for each cluster. Set to 0 to report all passing baseline.
  --minimum-to-report (-R): Report only potential origins with at least the indicated confidence score.
  --minimum-gap (-G): The minimum number of mutations between the last ancestor inferred to be in region to its parent to use the ancestor to define the cluster instead of the parent. Set to higher values to merge sibling clusters. Default 0.
  --num-to-look (-X): Additionally require that the next X nodes on the path to the root from the putative introduction point have lower confidences than the introduction point. Set to higher numbers to merge nested clusters. Default 0.

--------------
Publications
--------------

- McBroome J, Thornlow B, Hinrichs AS, Kramer A, De Maio N, Goldman N, Haussler D, Corbett-Detig R, and Turakhia Y. `A daily-updated database and tools for comprehensive SARS-CoV-2 mutation-annotated trees., <https://academic.oup.com/mbe/advance-article/doi/10.1093/molbev/msab264/6361626>`_ *Molecular Biology and Evolution*. 2021.
