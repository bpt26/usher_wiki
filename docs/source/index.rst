.. toctree::
   :hidden:

   index.rst
   Presentations.rst
   Publications.rst

***************
UShER Wiki
***************

Welcome to the manual for UShER, MAT Utils, and other related SARS-CoV-2 Phylogenetics tools.


Programs
=================
* UShER_
* matUtils_
* StrainPhylogenetics_



.. _UShER:

=================
UShER
=================
.. image:: usher_logo.png
    :width: 700px
    :align: center

UShER is a program for rapid, accurate placement of samples to existing phylogenies. It is available for downloading `here <https://github.com/yatisht/usher>`_ and is updated regularly. While not restricted to SARS-CoV-2 phylogenetic analyses, it has enabled real-time phylogenetic analyses and genomic contact tracing in that its placement is orders of magnitude faster and more memory-efficient than previous methods, and is being widely used by several SARS-CoV-2 research groups, including the `UCSC Genome Browser team <https://genome.ucsc.edu/cgi-bin/hgPhyloPlace>`_ and `Rob Lanfear's global phylogeny releases <https://github.com/roblanf/sarscov2phylo/releases>`_.

--------------
Installation
--------------

A pre-compiled binary is available for download `here <http://public.gi.ucsc.edu/~yatisht/data/binaries/usher>`_. Otherwise, to download and compile from source, first clone the GitHub repository:

`git clone https://github.com/yatisht/usher.git  
cd usher  `

Then install using either **Docker**, **conda**, or one of the provided **installation scripts**:

Docker
--------

\::
   docker build --no-cache -t usher .
   docker run -t -i usher /bin/bash

or\::
   docker pull yatisht/usher:latest
   docker run -t -i yatisht/usher:latest /bin/bash


conda
-------

::
   conda env create -f environment.yml
   
   conda activate usher
   
   git clone https://github.com/oneapi-src/oneTBB
   
   cd oneTBB
   
   git checkout cc2c04e2f5363fb8b34c10718ce406814810d1e6
   
   cd ..
   
   mkdir build
   
   cd build
   
   cmake  -DTBB_DIR=${PWD}/../oneTBB  -DCMAKE_PREFIX_PATH=${PWD}/../oneTBB/cmake ..
   
   make -j
   
   cd ..


followed by, if on a MacOS system:

   `rsync -aP rsync://hgdownload.soe.ucsc.edu/genome/admin/exe/macOSX.x86_64/faToVcf .`
   
   `chmod +x faToVcf`

   `mv faToVcf scripts/`

if on a Linux system::
   rsync -aP rsync://hgdownload.soe.ucsc.edu/genome/admin/exe/linux.x86_64/faToVcf .
   chmod +x faToVcf 
   mv faToVcf scripts

Installation scripts
------------------------

For MacOS 10.14 or above:

`./installMacOS.sh`

For Ubuntu 18.04 and above (requires sudo privileges):

`./installUbuntu.sh`

For CentOS 7 and above (requires sudo privileges):

`./installCentOS.sh`

--------------
Methodology
--------------

Given existing samples, whose genotypes and phylogenetic tree is known, and the genotypes of new samples, UShER aims to incorporate new samples into the phylogenetic tree while preserving the topology of existing samples and maximizing parsimony. UShER’s algorithm consists of two phases: (i) the pre-processing phase and (ii) the placement phase.

Pre-processing
------------------------

In the pre-processing phase, UShER accepts the phylogenetic tree of existing samples in a Newick format and their genotypes, specified as a set of single-nucleotide variants with respect to a reference sequence (UShER currently ignores indels), in a VCF format. For each site in the VCF, UShER uses the `Fitch-Sankoff algorithm <https://evolution.gs.washington.edu/gs541/2010/lecture1.pdf>`_ to find the most parsimonious nucleotide assignment for every node of the tree (UShER automatically labels internal tree nodes). When a sample contains **ambiguous genotypes**, multiple nucleotides may be most parsimonious at a node. To resolve these, UShER assigns it any one of the most parsimonious nucleotides with preference, when possible, given to the reference base. UShER also allows the VCF to specify ambiguous bases in samples using `IUPAC format <https://www.bioinformatics.org/sms/iupac.html>`_, which are also resolved to a unique base using the above strategy. When a node is found to carry a mutation, i.e. the base assigned to the node differs from its parent, the mutation gets added to a list of mutations corresponding to that node. Finally, UShER uses `protocol buffers <https://developers.google.com/protocol-buffers>`_ to store in a file, the Newick string corresponding to the input tree and a list of lists of node mutation, which we refer to as **mutation-annotated tree object**, as shown in the figure below.

.. image:: pre-processing.png
    :width: 700px
    :align: center

The mutation-annotated tree object carries sufficient information to derive parsimony-resolved genotypes for any tip of the tree using the sequence of mutations from the root to that tip. For example, in the above figure, S5 can be inferred to contain variants G1149U, C7869U, G3179A and A2869G with respect to the reference sequence. Compared to other tools that use full multiple-sequence alignment (MSA) to guide the placement, UShER's mutation-annotated tree object is compact and is what helps make it **fast**.

Placement
------------------------

In the **placement phase**, UShER loads the pre-processed mutation-annotated tree object and the genotypes of new samples in a VCF format and **sequentially** adds the new samples to the tree. For each new sample, UShER computes the additional parsimony score required for placing it at every node in the current tree while considering the full path of mutations from the root of the tree to that node. Next, UShER places the new sample at the node that results in the smallest additional parsimony score. When multiple node placements are equally parsimonious, UShER picks the node with a greater number of descendant leaves for placement. If the choice is between a parent and its child node, the parent node would always be selected by this rule. However, a more accurate placement should reflect the number of leaves uniquely attributable to the child versus parent node. Therefore, in these cases, UShER picks the parent node if the number of descendant leaves of the parent that are not shared with the child node exceed the number of descendant leaves of the child. The figure below shows a new sample, S7, containing variants G1149U and C9977A being added to the previous mutation-annotated tree object in a parsimony-optimal fashion (with a parsimony score of 1 for the mutation C9977A). UShER also automatically imputes and reports **ambiguous genotypes** for the newly added samples and ignores **missing bases**, such as 'N' or '.' (i.e. missing bases never contribute to the parsimony score).

.. image:: placement.png
    :width: 700px
    :align: center

At the end of the placement phase, UShER allows the user to create another protocol-buffer (protobuf) file containing the mutation-annotated tree object for the newly generated tree including added samples as also shown in the example figure above. This allows for another round of placements to be carried out over and above the newly added samples. 

--------------
Usage
--------------

Display help message
------------------------

To familiarize with the different command-line options of UShER, it would be useful to view its help message using the command below:

`./build/usher --help`


Pre-processing global phylogeny
------------------------------------

The following example command pre-processes the existing phylogeny (`global_phylo.nh`) and using the genotypes (`global_samples.vcf`) and generates the mutation-annotated tree object that gets stored in a protobuf file (`global_assignments.pb`). Note that UShER would automatically place onto the input global phylogeny any samples in the VCF (to convert a fasta sequence to VCF, consider using Fasta2USHER that are missing in the input global phylogeny using its parsimony-optimal placement algorithm. This final tree is written to a file named `final-tree.nh` in the folder specified by `--outdir` or `-d` option (if not specified, default uses current directory). 

`./build/usher -t test/global_phylo.nh -v test/global_samples.vcf -o global_assignments.pb -d output/`  

By default, UShER uses **all available threads** but the user can also specify the number of threads using the `--threads` or `-T` command-line parameter.

UShER also allows an option during the pre-processing phase to collapse nodes (i.e. delete the node after moving its child nodes to its parent node) that are not inferred to contain a mutation through the Fitch-Sankoff algorithm as well as to condense nodes that contain identical sequences into a single representative node. This is the **recommended usage** for UShER as it not only helps in significantly reducing the search space for the placement phase but also helps reduce ambiguities in the placement step and can be done by setting the `--collapse-tree` or `-c` parameter. The collapsed input tree is stored as `condensed-tree.nh` in the output directory. 

`./build/usher -t test/global_phylo.nh -v test/global_samples.vcf -o global_assignments.pb -c -d output/`

Note the the above command would condense identical sequences, namely S2, S3 and S4, in the example figure above into a single condensed new node (named something like *node_1_condensed_3_leaves*). If you wish to display the collapsed tree without condensing the nodes, also set the `--write-uncondensed-final-tree` or `-u` option, for example, as follows:

`./build/usher -t test/global_phylo.nh -v test/global_samples.vcf -o global_assignments.pb -c -u -d output/`

The above commands saves the collapsed but uncondensed tree as `uncondensed-final-tree.nh` in the output directory. 

Placing new samples
------------------------------------

Once the pre-processing is complete and a mutation-annotated tree object is generate (e.g. `global_assignments.pb`), UShER can place new sequences whose variants are called in a VCF file (e.g. `new_samples.vcf`) to existing tree as follows:

`./build/usher -i global_assignments.pb -v test/new_samples.vcf -u -d output/`

Again, by default, UShER uses **all available threads** but the user can also specify the number of threads using the *--threads* command-line parameter.

The above command not only places each new sample sequentially, but also reports the parsimony score and the number of parsimony-optimal placements found for each added sample. UShER displays warning messages if several (>=4) possibilities of parsimony-optimal placements are found for a sample. This can happen due to several factors, including (i) missing data in new samples, (ii) presence of ambiguous genotypes in new samples and (iii) structure and mutations in the global phylogeny itself, including presence of multiple back-mutations. 

In addition to the global phylogeny, one often needs to contextualize the newly added sequences using subtrees of closest *N* neighbouring sequences, where *N* is small. UShER allows this functionality using `--write-subtrees-size` or `-k` option, which can be set to an arbitrary *N*, such as 20 in the example below:

`./build/usher -i global_assignments.pb -v test/new_samples.vcf -u -k 20 -d output/`

The above command writes subtrees to files names `subtree-<subtree-number>.nh`. It also write a text file for each subtree (named `subtree-<subtree-number>-mutations.txt` showing mutations at each internal node of the subtree. If the subtrees contain condensed nodes, it writes the expanded leaves for those nodes to text files named `subtree-<subtree-number>-expanded.txt`. 

Finally, the new mutation-annotated tree object can be stored again using `--save-mutation-annotated-tree` or `-o` option (overwriting the loaded protobuf file is allowed).

`./build/usher -i global_assignments.pb -v test/new_samples.vcf -u -o new_global_assignments.pb -d output/`

--------------
Features
--------------

In addition to simply placing samples on an existing phylogeny, UShER provides the user with several points of additional information, and is capable of auxiliary analyses:

Uncertainty in placing new samples
-------------------------------------------


Branch Parsimony Score
-------------------------------------------

UShER also allows quantifying the uncertainty in placing new samples by reporting the parsimony scores of adding new samples to all possible nodes in the tree **without** actually modifying the tree (this is because the tree structure, as well as number of possible optimal placements could change with each new sequential placement). In particular, this can help the user explore which nodes of the tree result in a small and optimal or near-optimal parsimony score. This can be done by setting the `--write-parsimony-scores-per-node` or `-p` option, for example, as follows:

`./build/usher -i global_assignments.pb -v test/new_samples.vcf -p -d output/`

The above command writes a file `parsimony-scores.tsv` containing branch parsimony scores to the output directory. Note that because the above command does not perform the sequential placement on the tree, the number of parsimony-optimal placements reported for the second and later samples could differ from those reported with actual placements.

The figure below shows how branch parsimony score could be useful for uncertainty analysis. The figure shows color-coded parsimony score of placing a new sample at different branches of the tree with black arrow pointing to the branch where the placement is optimal. As can be seen from the color codes, the parsimony scores are low (implying good alternative placement) for several neighboring branches of the optimal branch. 

.. image:: bps.png
    :width: 300px
    :align: center


Multiple parsimony-optimal placements
-------------------------------------------

To further aid the user to quantify phylogenetic uncertainty in placement, UShER has an ability to enumerate all possible topologies resulting from equally parsimonious sample placements. UShER does this by maintaining a list of mutation-annotated trees (starting with a single mutation-annotated tree corresponding to the input tree of existing samples) and sequentially adds new samples to each tree in the list while increasing the size of the list as needed to accommodate multiple equally parsimonious placements for a new sample. This feature is available using the `--multiple-placements` or `-M` option in which the user specifies the maximum number of topologies that UShER should maintain before it reverts back to using the default tie-breaking strategy for multiple parsimony-optimal placements in order to keep the runtime and memory usage of UShER reasonable. 

`./build/usher -i global_assignments.pb -v <USER_PROVIDED_VCF> -M -d output/`

Note that if the number of equally parsimonious placements for the initial samples is large, the tree space can get too large too quickly and slow down the placement for the subsequent samples. Therefore, UShER also provides an option to sort the samples first based on the number of equally parsimonious placements using the `-S` option. 

`./build/usher -i global_assignments.pb -v <USER_PROVIDED_VCF> -M -S -d output/`

There are many ways to interpret and visualize the forest of trees produced by multiple placements. One method is to use DensiTree, as shown using an example figure (generated using the `phangorn <https://cran.r-project.org/web/packages/phangorn/>`_ package) below:

Updating multiple input trees
-------------------------------------------

UShER is also fast enough to allow users to update multiple input trees incorporating uncertainty in tree resonstruction, such as multiple bootstrap trees. While we do not provide an explicit option to input multiple trees at once, UShER can be run independently for each input tree and place new samples. We recommend the user to use the `GNU parallel utility <https://www.gnu.org/software/parallel/>`_ to do so in parallel using multiple CPU cores while setting `-T 1` for each UShER task.

--------------
Fasta2UShER
--------------

We also provide a tool, Fasta2UShER.py, that converts SARS-CoV-2 genomic data in fasta format into a merged VCF viable for input to UShER. Fasta2UShER.py can take a multiple sequence alignment (MSA) file as input (including standard MSA output from the `SARS-CoV-2 ARTIC Network protocol <https://artic.network/ncov-2019>_`). Fasta2UShER.py also possesses an input option for unalifgned SARS-CoV-2 data. In this case Fasta2UShER.py employs multiple alignment using Fast Fourier Transform ([MAFFT](https://mafft.cbrc.jp/alignment/software/)) to construct an alignment for each user specified sequence with the SARS-CoV-2 reference. In addition, Fasta2UShER.py considers missing data and can automatically filter variants at `problematic sites <https://virological.org/t/issues-with-sars-cov-2-sequencing-data/473/12>`_ (also see this `pre-print <https://www.biorxiv.org/content/biorxiv/early/2020/06/09/2020.06.08.141127.full.pdf>`_). Fasta2UShER no longer supports multiple msa files as input. If you possess multiple independently generated msa's, please remove gaps and use the unaligned input option.

Input
-------------

Fasta2UShER takes a single MSA file or unaligned full SARS-CoV-2 genomic sequence(s) in fasta format.

Options
-------------

Usage
-------------

Please ensure that faToVcf exists in the same directory as Fasta2UShER.py! Example command:

`python3 scripts/Fasta2UShER.py -reference ./test/NC_045512v2.fa  -inpath ./test/Fasta2UShER/ -unaligned -output ./test/test_merged.vcf`

Output
-------------

Fasta2UShER outputs a merged VCF with missing data for a particular sample denoted as "." in the corresponding genotype column. The above example command would yield a new VCF *test/test_merged.vcf* (identical to the one already provided), which can be used by UShER to place the new samples.

.. _matUtils:

matUtils
=========

matUtils is a set of tools to be used for analyses relating to **m**\ utation\  **a**\ nnotated\  **t**\ rees, such as the protobuf (.pb) files used in UShER. 

-----------
Input
-----------

matUtils takes as an input a mutation-annotated tree file generated by UShER.

-----------
Options
-----------

**-i**: Input mutation-annotated tree file. (**REQUIRED**)`<br />`
**-v**: Output VCF file.`<br />`
**-t**: Output Newick tree file.`<br />`
**-n**: Do not include sample genotype columns in VCF output (used only with -v).`<br />`
**-p**: Calculate and store total tree parsimony.`<br />`
**-e**: Calculate and store equally parsimonious placements for all samples in the tree.`<br />`
**-s**: Use to mask specific samples from the tree.`<br />`
**-h**: Print help message.`<br />`

-----------
Usage
-----------

An example usage of matUtils:  

`./build/matUtils -i global_assignments.pb -v global_assignments.vcf -t global_assignments.nh`

-----------
Output
-----------

The above example command generates a VCF file named `global_assignments.vcf` and the output tree named `global_assignments.nh`.




.. _StrainPhylogenetics:

StrainPhylogenetics
=======================

----------
RotTrees
----------

RotTrees enables quick inference of congruence of tanglegrams. This is particularly useful for SARS-CoV-2 phylogenomics due to multiple groups independently analyzing data-sets with many identical samples. Previous tanglegram visualization software, such as `cophylo <ttps://www.rdocumentation.org/packages/phytools/versions/0.7-20/topics/cophylo>`_ and `Dendroscope3 <http://dendroscope.org/>`_ rely on fewer rotations to minimize crossings over, which is inadequate for phylogenies on the scale of SARS-CoV-2. We implemented a quick heuristic to produce vastly improved tanglegrams.

`./build/rotate_trees --T1 tree/pruned-sumtree-for-cog.nh --T2 tree/pruned-cog-for-sumtree.nh --T1_out rot-pruned-sumtree-for-cog.nh --T2_out rot-pruned-cog-for-sumtree.nh`

The above command produces rotated trees (rot-pruned-cog-for-sumtree.nh and rot-pruned-sumtree-for-cog.nh) with a much improved tanglegram as seen below (images generated with the help of `cophylo <https://www.rdocumentation.org/packages/phytools/versions/0.7-20/topics/cophylo>`_, setting rotate to FALSE).

.. image:: tanglegrams_comparison.png
    :width: 700px
    :align: center

Below is a GIF of approximately 20 frames showing various operations of the tree rotation algorithm operating on a much larger pair of trees (~4k leaves)

.. image:: rotation.gif
    :width: 700px
    :align: center

----------
TreeMerge
----------

`python3 scripts/tree_merge.py -T1 tree/pruned-sumtree-for-cog.nh -T2 tree/pruned-cog-for-sumtree.nh -symmetric 1 -T_out symm-merged-sumtree-cog.nh`

The above command produces a merged tree (*symm-merged-sumtree-cog.nh*) from two input trees (*pruned-sumtree-for-cog.nh* and *pruned-cog-for-sumtree.nh*) that is maximally resolved and compatible with both input trees (refer to our `manuscript <https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1009175>`_ for more details). Below are the resulting tanglegrams of the resulting merged tree with the two input trees (after applying tree rotation). The above command can also be used without the symmetric flag for its asymmetric version (where the first input tree is given a priority to resolve the merged tree) or using the intersectOnly flag that produces a simple consensus of the two input trees.  

.. image:: merged.png
    :width: 700px
    :align: center

----------------------------------------
Identify and plot extremal sites
----------------------------------------

`python3 scripts/identify_extremal_sites.py -in pruned-sumtree-for-cog_PARSIMONY.txt`

The above command can be used for identifying and flagging extremal sites i.e. sites having exceptional parsimony scores relative to their allele frequencies and therefore also suspected to contain systematic errors. The above command identifies 6 extremal sites (C11074T, C27046T, T13402G, A3778G, G24390C, G26144T) with a phylogenetic instability value of 3.03. For the precise definition of extremal sites and phylogenetic instability, refer to our manuscript referenced at the bottom. The code also provides an ability to ignore high-frequency C\>T and G\>T mutations using optional flags

`python3 scripts/identify_extremal_sites.py -in pruned-sumtree-for-cog_PARSIMONY.txt -ignoreCtoT=1 -ignoreGtoT=1`

The above command identifies three extremal sites (T13402G, A3778G, G24390C) with a phylogenetic instability value of 2.32. To create a figure requires `installing R <https://docs.rstudio.com/resources/install-r/>`_ and the `plyr package <https://www.rdocumentation.org/packages/plyr>`_.

`python3 scripts/generate_plot_extremal_sites_data.py -in pruned-sumtree-for-cog_PARSIMONY.txt > plot_extremal_sites_data.txt`

The above commands create raw input data for the extremal sites plot.

`Rscript --vanilla scripts/plot_parsimony.r plot_extremal_sites_data.txt extremal_sites_plot.pdf`

Next, the R command accepts the generated data and creates a log(allele count) by parsimony plot for all variant sites in a given vcf. It produces three plots, one of all data, one ignoring C>U mutations and one ignoring C>U and G>U mutations, as shown below.

.. image:: extremal.png
    :width: 700px
    :align: center