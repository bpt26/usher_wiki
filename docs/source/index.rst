*****
UShER Wiki
*****

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
cd usher`

Then install using either **Docker**, **conda**, or one of the provided **installation scripts**:

Docker
--------

`docker build --no-cache -t usher .
docker run -t -i usher /bin/bash`

or

`docker pull yatisht/usher:latest
docker run -t -i yatisht/usher:latest /bin/bash`


conda
-------

`conda env create -f environment.yml
conda activate usher
git clone https://github.com/oneapi-src/oneTBB
cd oneTBB
git checkout cc2c04e2f5363fb8b34c10718ce406814810d1e6
cd ..
mkdir build
cd build
cmake  -DTBB_DIR=${PWD}/../oneTBB  -DCMAKE_PREFIX_PATH=${PWD}/../oneTBB/cmake ..
make -j
cd ..`

followed by, if on a MacOS system:

`rsync -aP rsync://hgdownload.soe.ucsc.edu/genome/admin/exe/macOSX.x86_64/faToVcf .
chmod +x faToVcf
mv faToVcf scripts/`

if on a Linux system:

`rsync -aP rsync://hgdownload.soe.ucsc.edu/genome/admin/exe/linux.x86_64/faToVcf .
chmod +x faToVcf
mv faToVcf scripts/`

Installation Scripts
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

--------------
Usage
--------------


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
