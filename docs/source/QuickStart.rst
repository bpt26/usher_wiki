.. include:: /Includes.rst.txt

***************
Quick Start
***************

To quickly install UShER, use the following conda instructions:

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


To get acquainted with UShER, we provide a simple example of placing 10 samples on an existing phylogeny, and doing basic analyses to assess the placements. First, download the example files.

.. code-block:: shell-session
  
  wget https://raw.githubusercontent.com/yatisht/usher/master/test/global_phylo.nh
  wget https://raw.githubusercontent.com/yatisht/usher/master/test/global_samples.vcf
  wget https://raw.githubusercontent.com/yatisht/usher/master/test/new_samples.vcf
  wget https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/2021/03/02/public-2021-03-02.all.masked.nextclade.pangolin.pb
  wget https://raw.githubusercontent.com/bpt26/usher_wiki/main/docs/source/example.vcf
  wget https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/2021/03/02/lineageToPublicName.gz
  gzip -dc lineageToPublicName.gz > lineageToPublicName
 

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

Now, let's use the pre-made mutation annotated tree that contains Nexclade and Pangolin clade annotations. First, use UShER to place the example sequences on the tree:

.. code-block:: shell-session

  usher -i public-2021-03-02.all.masked.nextclade.pangolin.pb -v example.vcf -d outdir

This will produce the regular output, as described above, as well as a text file containing two sets of clade assignments, for Nextclade and Pangolin:

.. code-block:: shell-session

  cat outdir/clades.txt

To remove and replace clade annotations, we would use the following commands:

.. code-block:: shell-session

  matUtils annotate -i public-2021-03-02.all.masked.nextclade.pangolin.pb -l -c lineageToPublicName -o public-2021-03-02.all.masked.pangolin.pb
  usher -i public-2021-03-02.all.masked.pangolin.pb -v example.vcf -d outdir-2
  cat outdir-2/clades.txt

Now, the resulting mutation annotated tree has only Pangolin clade annotations. To export this MAT to a newick file for easier visualization, we can use `matUtils extract`:

.. code-block:: shell-session

  matUtils extract -i public-2021-03-02.all.masked.pangolin.pb -t public-2021-03-02.nh
