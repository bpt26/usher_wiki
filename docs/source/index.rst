***************
UShER Wiki
***************

Welcome to the manual for UShER, MAT Utils, and other related SARS-CoV-2 Phylogenetics tools.

Programs
========
* UShER_
* matUtils_
* RotTrees_

.. toctree::
   :hidden:

   index.rst

.. _UShER:

UShER
=======
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

`docker build --no-cache -t usher .  
docker run -t -i usher /bin/bash  `

or

`docker pull yatisht/usher:latest  
docker run -t -i yatisht/usher:latest /bin/bash  `


conda
-------

.. code-block:: bash
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

.. code-block:: bash
   rsync -aP rsync://hgdownload.soe.ucsc.edu/genome/admin/exe/macOSX.x86_64/faToVcf .  
   chmod +x faToVcf  
   mv faToVcf scripts/ 

if on a Linux system:

.. code-block:: bash
   rsync -aP rsync://hgdownload.soe.ucsc.edu/genome/admin/exe/linux.x86_64/faToVcf .  
   chmod +x faToVcf  
   mv faToVcf scripts/  

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


.. _matUtils:

matUtils
=========

matUtils is a set of tools to be used for analyses relating to **m**\ utation\  **a**\ nnotated\  **t**\ rees, such as the protobuf (.pb) files used in UShER. This toolkit is currently under development and will be publicized shortly.

.. _RotTrees:

RotTrees
==========

RotTrees enables quick inference of congruence of tanglegrams. This is particularly useful for SARS-CoV-2 phylogenomics due to multiple groups independently analyzing data-sets with many identical samples. Previous tanglegram visualization software relied on fewer rotations to minimize crossings over:

.. image:: tanglegrams_comparison.png
    :width: 700px
    :align: center

RotTrees produces a merged tree from two input trees that is maximally resolved and compatible with both input trees (refer to our `manuscript, <ttps://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1009175>`_ for more details). 

.. image:: rotation.gif
    :width: 700px
    :align: center
