.. include:: /Includes.rst.txt

***************
Quick Start Usher
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
  wget https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/2021/05/17/public-2021-05-17.all.masked.nextclade.pangolin.pb.gz
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

Now, let's use a pre-made mutation annotated tree that contains Nextclade and Pangolin clade annotations. First, use UShER to place the example sequences on the tree:

.. code-block:: shell-session

  usher -i public-2021-05-17.all.masked.nextclade.pangolin.pb.gz -v example.vcf -d outdir -o updated.pb

This will produce the regular output, as described above, as well as a text file containing two sets of clade assignments, for Nextclade and Pangolin:

.. code-block:: shell-session

  cat outdir/clades.txt

We can follow up on our placements by visualizing the tree context through the `Auspice <https://auspice.us/>`_ web interface and matUtils (see below). Simply drag-and-drop the JSON created
by the following command onto their web server.

.. code-block:: shell-session

  matUtils extract -i updated.pb -k hypothetical_uploaded_sequence_1:25 -j hseq1.json

In this case, we can see that three of our samples cluster here, aligning with what is suggested in the clades.txt file.

***************
Quick Start matUtils
***************

Though it is bundled and installed alongside UShER, matUtils is more than an output processor for UShER commands. 
It can be used in independent workflows that begin with one of our `publicly-provided MAT protobuf files <https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/>`_, 
or an Augur-formatted MAT JSON file as used by Nextstrain. matUtils can be used to explore large trees in deep detail, parsing and manipulating trees of a size
few other tools can manage efficiently.

The first step to using one of these public files is `matUtils summary`, which can calculate basic statistics or summarize sample, clade, or mutation-level frequency information.

.. code-block:: shell-session

  matUtils summary -i public-2021-05-17.all.masked.nextclade.pangolin.pb.gz 

This particular tree has 757500 unique samples represented in it. We can further explore this dataset with another `matUtils summary` command:

.. code-block:: shell-session

  matUtils summary -i public-2021-05-17.all.masked.nextclade.pangolin.pb.gz -A -d summary_out

Let's say we're interested in recurrent, or homoplasic, mutations across this tree. The mutations summary file contains the number of independent occurrences of a 
mutation across the tree. 

.. code-block:: shell-session

  awk '$2 >= 500' summary_out/mutations.tsv

C>T mutations are very overrepresented in this set, being a common mutation and error type. We're concerned about correctly identifying real homoplasic mutations,
instead of coincident or erroneous mutations, so we filter the dataset down to higher-quality placements and samples.

.. code-block:: shell-session

  matUtils extract -i public-2021-05-17.all.masked.nextclade.pangolin.pb.gz -a 3 -b 5 -o filtered.pb
  matUtils summary -i filtered.pb

After filtering, our tree contains 701375 samples, which is 92% of the original tree size. Let's see how our homoplasic mutation output looks.

.. code-block:: shell-session

  matUtils summary -i filtered.pb -m filtered_mutations.tsv
  awk '$2 > 500' filtered_mutations.tsv

By filtering 8% of our tree, we have removed most of the mutations with more than five hundred unique occurrences. The C>T bias is still present, 
but we can more comfortably proceed to analyze these mutations. The most homoplasic mutation, a significant outlier with more than a thousand occurrences
after filtering, is G7328T. This is a mutation in ORF1A, part of the replicase protein which the virus uses to duplicate itself in the host, which causes
an amino acid change from alanine to serine at position 2355.

If we were interested in following up on this potential homoplasy, we have a few options. We may want to generate a new protobuf file containing only 
samples with this specific mutation, along with a JSON for visualization and additional sample path information. We can perform all these operations with
a single command.

.. code-block:: shell-session

  matUtils extract -i filtered.pb -m G7328T -o G7328T.pb -j G7328T.json -S G7328T_sample_paths.txt 

If we upload this JSON to `Auspice <https://auspice.us/>`_, we can choose to highlight each branch and node by whether they contained our query mutation.
We can see that the majority of occurrences of G7328T are single nodes- having just occurred- and that the majority are from the USA, though from all across the phylogenetic tree.
Further analysis would be required to validate or interpet these results, but this procedure clearly demonstrates the potential for matUtils for 
rapid exploratory analysis using large public datasets.

Additional tutorials for other matUtils commands, focused on sample placement uncertainty and phylogeographic analysis, can be found `here <https://usher-wiki.readthedocs.io/en/latest/tutorials.html>`_.
The full manual page including detailed parameter information can be found `here <https://usher-wiki.readthedocs.io/en/latest/matUtils.html>`_.