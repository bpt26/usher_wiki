.. include:: /Includes.rst.txt

***************
Quick Start
***************

To get acquainted with UShER, we have provided a simple example of placing 10 samples on an existing phylogeny, and doing basic analyses to assess the placements. If you have not yet installed UShER, `please follow the instructions here <https://usher-wiki.readthedocs.io/en/latest/UShER.html#installation>`_ before continuing with this example.

------------------------
Files you will need
------------------------

* `pruned_10.nh <https://usher-wiki.readthedocs.io/en/latest/pruned_10.nh>`_ (newick file containing the initial phylogeny)
* `pruned_10.vcf.gz <https://usher-wiki.readthedocs.io/en/latest/pruned_10.vcf.gz>`_ (.vcf.gz file informing the initial phylogeny)
* `missing_10.vcf.gz <https://usher-wiki.readthedocs.io/en/latest/missing_10.vcf.gz>`_ (.vcf.gz file containing samples to be placed)
* `full_tree.nh <https://usher-wiki.readthedocs.io/en/latest/full_tree.nh>`_ (newick file containing the full tree, to assess UShER's performance)

------------------------
Making the protobuf
------------------------

A major part of UShER's speed and memory-efficiency is its usage of .pb protobuf files to encode mutation annotated trees. To create the mutation annotated tree we'll need here, use the following command:

`usher --tree pruned_10.nh --vcf pruned_10.vcf.gz --collapse-tree --save-mutation-annotated-tree pruned_10.pb`

This command will read in both the newick file and the .vcf and output a .pb file storing all mutations as well as the structure of the tree.

------------------------
Placing samples
------------------------

Now, we want to place the samples from `missing_10.vcf.gz` onto our tree. We can do this by using the following command:

`usher --vcf MISSING_VCF/missing_10.vcf.gz --load-mutation-annotated-tree pruned_10.pb --write-uncondensed-final-tree`

This command will output three files:

* `final-tree.nh` (newick-formatted tree with identical samples condensed)
* `uncondensed-final-tree.nh` (newick-formatted tree containing all samples)
* `mutation-paths.txt` (tab-separated file containing each sample, the nodes leading to that sample in the final tree, and the mutations at those nodes)

------------------------
Assessing performance
------------------------

To compare the final tree output by UShER to 