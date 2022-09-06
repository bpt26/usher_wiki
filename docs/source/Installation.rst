
***************
Installation
***************

UShER package can be installed using three different options: (i) conda, (ii) Docker and (iii) installation scripts, as described below.

Conda
--------

A quick method is via `conda`:

.. code-block:: sh

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

   
Conda Local Build
---------------------

.. code-block:: sh

  git clone https://github.com/yatisht/usher.git
  cd usher/install
  conda env create -f environment.yml
  conda activate usher
  cd ..
  mkdir build
  cd build
  wget https://github.com/oneapi-src/oneTBB/archive/2019_U9.tar.gz 
  tar -xvzf 2019_U9.tar.gz
  cmake  -DTBB_DIR=${PWD}/oneTBB-2019_U9  -DCMAKE_PREFIX_PATH=${PWD}/oneTBB-2019_U9/cmake ..
  make -j
  cd ..

followed by, if on a MacOS system:

.. code-block:: sh

  rsync -aP rsync://hgdownload.soe.ucsc.edu/genome/admin/exe/macOSX.x86_64/faToVcf .
  chmod +x faToVcf
  mv faToVcf scripts/


or if on a Linux system:

.. code-block:: sh

  rsync -aP rsync://hgdownload.soe.ucsc.edu/genome/admin/exe/linux.x86_64/faToVcf . 
  chmod +x faToVcf
  mv faToVcf scripts/

Executables will be located in the build and scripts directories. Make sure they're on your path for your system as appropriate, 
or that you modify your commands to indicate their location.

.. code-block:: sh

  export PATH=$PATH:/path/to/install/usher/build/
  export PATH=$PATH:/path/to/install/usher/scripts/

Docker
--------

From DockerHub:

.. code-block:: sh

  docker pull pathogengenomics/usher:latest
  docker run -t -i pathogengenomics/usher:latest /bin/bash
  
OR locally:

.. code-block:: sh

   git clone https://github.com/yatisht/usher.git
   cd usher
   docker build --no-cache -t usher install/
   docker run -t -i usher /bin/bash



Installation scripts
------------------------

.. code-block:: sh
  
  git clone https://github.com/yatisht/usher.git
  cd usher
  
For MacOS 10.14 or above:

.. code-block:: sh

  ./install/installMacOS.sh

For Ubuntu 18.04 and above (requires sudo privileges):

.. code-block:: sh

  ./install/installUbuntu.sh

For CentOS 7 and above (requires sudo privileges):

.. code-block:: sh

  ./install/installCentOS.sh
