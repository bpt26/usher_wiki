.. include:: /Includes.rst.txt

***************
Quick Start
***************

--------------
Quick install
--------------

To quickly install the UShER package, use the following conda instructions:

.. code-block:: shell-session

  # Create a new environment for UShER
  conda create -n usher-env
  # Activate the newly created environment
  conda activate usher-env
  # Set up channels
  conda config --add channels defaults
  conda config --add channels bioconda
  conda config --add channels conda-forge
  # Install the UShER package
  conda install usher
  
--------------
UShER
--------------

To get acquainted with UShER, we provide a simple example of placing 10 samples on an existing phylogeny. First, download the example files.

.. code-block:: shell-session
  
  wget https://raw.githubusercontent.com/yatisht/usher/master/test/global_phylo.nh
  wget https://raw.githubusercontent.com/yatisht/usher/master/test/global_samples.vcf
  wget https://raw.githubusercontent.com/yatisht/usher/master/test/new_samples.vcf 

Then, create a mutation annotated tree object:

.. code-block:: shell-session

  usher --tree global_phylo.nh --vcf global_samples.vcf --collapse-tree --save-mutation-annotated-tree global_phylo.pb

Now, we want to place the samples from `missing_10.vcf.gz` onto our tree. We can do this by using the following command:

.. code-block:: shell-session

  usher --vcf new_samples.vcf --load-mutation-annotated-tree global_phylo.pb --write-uncondensed-final-tree

This yields the following three files:

* `final-tree.nh` (newick-formatted tree with identical samples condensed)
* `uncondensed-final-tree.nh` (newick-formatted tree containing all samples)
* `mutation-paths.txt` (tab-separated file containing each sample, the nodes leading to that sample in the final tree, and the mutations at those nodes)

--------------
matUtils
--------------

matUtils is a toolkit for rapid exploratory analysis and manipulation of mutation-annotated trees (MATs).
The full manual page including detailed parameter information can be found `here <https://usher-wiki.readthedocs.io/en/latest/matUtils.html>`_. matUtils is installed with the UShER package (see above installation instructions using conda).

.. code-block:: shell-session

  wget https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/2021/05/17/public-2021-05-17.all.masked.nextclade.pangolin.pb.gz

matUtils can quickly survey the contents of MAT files with `matUtils summary`.

.. code-block:: shell-session

  matUtils summary -i public-2021-05-17.all.masked.nextclade.pangolin.pb.gz

matUtils is capable of quickly filtering on a variety of conditions and generating a series of outputs with a single call to `matUtils extract`.
These outputs include newick, vcf, other pb, and Augur JSON capable of being visualized on the `Auspice <https://auspice.us/>`_ web platform.

.. code-block:: shell-session

  matUtils extract -i public-2021-05-17.all.masked.nextclade.pangolin.pb.gz -a 3 -b 10 -k "Scotland/QEUH-13C22D1/2021|21-03-10:100" -v my_subset.vcf -t my_subset.newick -j my_subset.json

The above command filters samples with higher parsimony scores than 3 and ancestral branches with a greater length than 10, then collects a subtree representing 
the nearest 100 samples to our indicated sample. From this subtree this command generates a vcf containing all sample mutation information, a newick representing the subtree, and an Auspice-uploadable JSON in mere seconds.

Tutorials for matUtils, including an example workflow, sample placement uncertainty, and phylogeographic analysis, can be found `here <https://usher-wiki.readthedocs.io/en/latest/tutorials.html>`_.
