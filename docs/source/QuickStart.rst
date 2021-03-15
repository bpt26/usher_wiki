.. include:: /Includes.rst.txt

***************
Quick Start
***************

UShER
------------------------

To get acquainted with UShER, we provide a simple example of placing 10 samples on an existing phylogeny, and doing basic analyses to assess the placements. If you have not yet installed UShER, `please follow the instructions here <https://usher-wiki.readthedocs.io/en/latest/UShER.html#installation>`_ before continuing with this example.

------------------------
Files you will need
------------------------

* `global_phylo.nh <https://github.com/yatisht/usher/tree/master/test/global_phylo.nh>`_ (newick file containing the initial phylogeny)
* `global_samples.vcf <https://github.com/yatisht/usher/tree/master/test/global_samples.vcf>`_ (.vcf file informing the initial phylogeny)
* `new_samples.vcf <https://github.com/yatisht/usher/blob/master/test/new_samples.vcf>`_ (.vcf file containing samples to be placed)

------------------------
Making the protobuf
------------------------

A major part of UShER's speed and memory-efficiency is its usage of .pb protobuf files to encode mutation annotated trees. To create the mutation annotated tree we'll need here, use the following command:

.. code-block:: shell-session

  usher --tree global_phylo.nh --vcf global_samples.vcf --collapse-tree --save-mutation-annotated-tree global_phylo.pb

This command will read in both the newick file and the .vcf and output a .pb file storing all mutations as well as the structure of the tree.

------------------------
Placing samples
------------------------

Now, we want to place the samples from `missing_10.vcf.gz` onto our tree. We can do this by using the following command:

.. code-block:: shell-session

  usher --vcf new_samples.vcf --load-mutation-annotated-tree global_phylo.pb --write-uncondensed-final-tree

This command will output three files:

* `final-tree.nh` (newick-formatted tree with identical samples condensed)
* `uncondensed-final-tree.nh` (newick-formatted tree containing all samples)
* `mutation-paths.txt` (tab-separated file containing each sample, the nodes leading to that sample in the final tree, and the mutations at those nodes)

.. _matutils-quickstart:

matUtils
------------------------

Upon installation of UShER, matUtils is in the `build` directory and can be used for editing and analyzing mutation annotated tree `.pb` files. To get acquainted with matUtils, we provide a simple example.

------------------------
Files you will need
------------------------

* `public-2021-03-02.all.masked.nextclade.pangolin.pb <https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/2021/03/02/public-2021-03-02.all.masked.nextclade.pangolin.pb>`_ (protobuf file containing the mutation annotated tree with clade annotations)
* `example.vcf <https://github.com/bpt26/usher_wiki/raw/main/docs/source/example.vcf>`_ (.vcf file containing example sequences to be placed)
* `lineageToPublicName <https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/2021/03/02/lineageToPublicName>`_ (tab-separated text file containing samples and their clade assignments)

--------------------------------------------------
Adding clade annotations to the tree
--------------------------------------------------

First, use usher to place the example sequences on the mutation annotated tree file, which is annotated with Nextclade and Pangolin/Pangolearn clade assignments:

.. code-block:: shell-session

  usher -i public-2021-03-02.all.masked.nextclade.pangolin.pb -v example.vcf -d outdir

This will produce the regular output, as described above, as well as a text file containing clade assignments:

.. code-block:: shell-session

  cat outdir/clades.txt

Upon inspecting this file, you will notice that 3 samples get assigned to the B.1.521 Pangolin/Pangolearn lineage (and 20C Nextclade clade) and 2 samples get assigned B.1.440 Pangolin/Pangolearn lineage (20A Nextclade clade). Currently, our clade assignments will not perfectly match Pangolin/Pangolearn assignments, but they are nearly perfect for Nextclade.

matUtils has two ways to annotate clades. In the first case, we will use the tab-separated file as input that maps samples to lineage names.First, we will use our original MAT file and clear all clade annotations using the `-l` option, then learn new annotations from the lineageToPublicName:

.. code-block:: shell-session

  matUtils annotate -i public-2021-03-02.all.masked.nextclade.pangolin.pb -l -c lineageToPublicName -o public-2021-03-02.all.masked.pangolin.pb

Now, let's use this new MAT to place sequences again:

.. code-block:: shell-session

  usher -i public-2021-03-02.all.masked.pangolin.pb -v example.vcf -d outdir-2

This time you will find only the Pangolin lineages in clades.txt:

.. code-block:: shell-session

  cat outdir-2/clades.txt

We could have also generated the same output MAT by using the second approach to assign lineage roots, which takes an input .tsv file to map each lineage to its corresponding internal node id in the tree:

.. code-block:: shell-session

  matUtils annotate -i public-2021-03-02.all.masked.nextclade.pangolin.pb -l -C lineageToNodeId -o public-2021-03-02.all.masked.pangolin.pb

To export this MAT to a newick file for easier visualization, we can use `matUtils extract`:

.. code-block:: shell-session

  matUtils extract -i public-2021-03-02.all.masked.nextclade.pangolin.pb -t public-2021-03-02.nh


















