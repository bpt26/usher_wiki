.. include:: /Includes.rst.txt

**************************
Strain_Phylogenetics
**************************

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

----------------------------------------
Presentations
----------------------------------------

We have presented this package and analyses on GISAID data at the Covid-19 Dynamics & Evolution Meeting, held virtually on October 19-20, 2020. You can find our slides `here <https://usher-wiki.readthedocs.io/en/latest/sp_meet.html>`_.


----------------------------------------
Publications
----------------------------------------

- Turakhia Y, De Maio N, Thornlow B, Gozashti L, Lanfear R, Walker C, Hinrichs A, Fernandes J, Borges R, Slodkowicz G, Weilguny L, Haussler D, Goldman N, and Corbett-Detig R. `Stability of SARS-CoV-2 Phylogenies. <https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1009175>`_ PLOS Genetics. 2020. 16(11): e1009175.

- De Maio N, Walker C, Turakhia Y, Lanfear R, Corbett-Detig R, and Goldman N. `Mutation rates and selection on synonymous mutations in SARS-CoV-2. <https://www.biorxiv.org/content/10.1101/2021.01.14.426705v1.abstract>`_ bioRxiv. 2020.

- DeMaio N, Walker C, Borges R, Weilguny L, Slodkowicz G, and Goldman N. `Issues with SARS-CoV-2 sequencing data. <http://virological.org/t/issues-with-sars-cov-2-sequencing-data/473>`_ Virological. 2020.

- Gozashti L, Walker C, Goldman N, Corbett-Detig R, and DeMaio N. `Updated analysis with data from 13th November 2020. <https://virological.org/t/issues-with-sars-cov-2-sequencing-data/473/14>`_ Virological. 2020.

