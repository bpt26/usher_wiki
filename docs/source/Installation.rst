
***************
Installation
***************

UShER package can be installed using three different options: (i) conda, (ii) Docker and (iii) installation scripts, as described below.

Conda
--------

A quick method is via `conda`:

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

   
Conda Local Build
-------

.. code-block:: shell-session

  git clone https://github.com/yatisht/usher.git
  cd usher
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

.. code-block:: shell-session

  rsync -aP rsync://hgdownload.soe.ucsc.edu/genome/admin/exe/macOSX.x86_64/faToVcf .
  chmod +x faToVcf
  mv faToVcf scripts/ 


or if on a Linux system:

.. code-block:: shell-session

  rsync -aP rsync://hgdownload.soe.ucsc.edu/genome/admin/exe/linux.x86_64/faToVcf . 
  chmod +x faToVcf
  mv faToVcf scripts  

Executables will be located in the build and scripts directories. Make sure they're on your path for your system as appropriate, 
or that you modify your commands to indicate their location.

.. code-block:: shell-session

  export PATH=$PATH:/path/to/install/usher/build/
  export PATH=$PATH:/path/to/install/usher/scripts/

Docker
--------

From DockerHub:

.. code-block:: shell-session

  docker pull yatisht/usher:latest
  docker run -t -i yatisht/usher:latest /bin/bash
  
OR locally:

.. code-block:: shell-session

   git clone https://github.com/yatisht/usher.git
   cd usher
   docker build --no-cache -t usher .
   docker run -t -i usher /bin/bash



Installation scripts
------------------------

.. code-block:: shell-session
  
  git clone https://github.com/yatisht/usher.git
  cd usher
  
For MacOS 10.14 or above:

.. code-block:: shell-session

  ./installMacOS.sh

For Ubuntu 18.04 and above (requires sudo privileges):

.. code-block:: shell-session

  ./installUbuntu.sh

For CentOS 7 and above (requires sudo privileges):

.. code-block:: shell-session

  ./installCentOS.sh
