=====================
Global UShER trees
=====================
UCSC provides downloadable tree and metadata files for trees of genetic sequences for the following pathogens.

* :ref:`Dengue <header-dengue>`
* :ref:`Influenza <header-flu>`
* :ref:`Mpox (MPXV/hMPXV) <header-mpox>`
* :ref:`RSV <header-rsv>`
* :ref:`SARS-CoV-2 (Covid-19) <header-covid>`
* :ref:`Tuberculosis (MTBC) <header-tuberculosis>`

.. _header-dengue:

Dengue
------
The mosquito-borne dengue virus has four serotypes. UCSC maintains trees for each serotype based on INDSDC samples.

* `DENV-1 <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/862/125/GCF_000862125.1/UShER_DENV-1/>`_, based on NC_001477.1
* `DENV-2 <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/871/845/GCF_000871845.1/UShER_DENV-2/>`_, based on NC_001474.2
* `DENV-3 <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/866/625/GCF_000866625.1/UShER_DENV-3/>`_, based on NC_001475.2
* `DENV-4 <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/865/065/GCF_000865065.1/UShER_DENV-4/>`_, based on NC_002640.1


.. _header-flu:

Influenza
---------
Trees for a variety of influenza A strains can be found `here <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/864/105/GCF_000864105.1/>`_. 

For most of our Influenza A assemblies we use a RefSeq assembly as reference and root. There are two exceptions, representing recent outbreaks:

* H5N1 D1.1 2024 outbreak
	* `Download here <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/864/105/GCF_000864105.1/UShER_h5n1_D1.1_2024/>`_
	* Rooted to a concatenation of Genbank segement sequences PQ844107.1, OP597633.1, PQ885594.1, LC718226.1, PQ585621.1, PQ664459.1, OP597621.1, and PQ712157.1
* H5N1 B3.13 cattle 2024 outbreak
	* `Taxonium version here <https://www.taxonium.org/flu/H5N1-Outbreak>`_
	* `Download here <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/864/105/GCF_000864105.1/UShER_h5n1_outbreak_2024/>`_
	* Rooted to a concatenation of Genbank segement sequences PP755620.1, PP755619.1, PP755618.1, PP753693.1, PP755616.1, PP753695.1, PP755614.1, and PP753097.1


.. _header-mpox:

Mpox (MPXV/hMPXV)
-----------------
Mpox, `previously known as monkeypox <https://www.who.int/news/item/28-11-2022-who-recommends-new-name-for-monkeypox-disease>`_, made news due to an outbreak in 2022. However, the disease is older than that, and the global MPXV tree includes INSDC samples from 2017 and later. 

The term "hMPXV" is used to reflect that these recent samples show sustained human-to-human transmission, designated clade IIb from the `Happi et al. nomenclature <https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3001769>`_. You can `view the hMPXV clade IIB tree on Taxonium  <https://www.taxonium.org/mpox/clade-IIb>`_ or download it `here <https://hgdownload.gi.ucsc.edu/hubs/GCF/014/621/545/GCF_014621545.1/UShER_hMPXV/>`_.

Clade I of MPVX `is also available <as well as `clade I of MPXV <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/857/045/GCF_000857045.1/UShER_MPXV_cladeI/>`_.


.. _header-rsv:

RSV
---
Respiratory Syncytial Virus (RSV) is divided into two antigenic types. Global trees developed using INDSDC samples for both RSV-A and RSV-B are available.

* `RSV-A <https://hgdownload.gi.ucsc.edu/hubs/GCF/002/815/475/GCF_002815475.1/UShER_RSV-A/>`_  
* `RSV-B <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/855/545/GCF_000855545.1/UShER_RSV-B/>`_  

You can also place samples on a tree with a reconstructed root `here <https://genome.ucsc.edu/cgi-bin/hgPhyloPlace?hgpp_org=rsv_rgcc>`_.


.. _header-covid:

SARS-CoV-2 (Covid-19)
---------------------
SARS-CoV-2 is the virus that causes COVID-19. The global SARS-CoV-2 tree includes sequences from a variety of sources, including but not limited to INSDC (GenBank/ENA/DDBJ). The SARS-CoV-2 trees and information about their data sources `can be found here <https://hgdownload.gi.ucsc.edu/goldenPath/wuhCor1/UShER_SARS-CoV-2/>`_. You can also `click here to view the latest tree in taxonium <https://taxonium.org/sars-cov-2/public>`_. 


.. _header-tuberculosis:

Tuberculosis (MTBC)
-------------------

UShER isn't just for viruses anymore. `As described in this preprint <https://www.medrxiv.org/content/10.1101/2025.07.22.25331806v1>`_, we built a tree of *Mycobacterium tuberculosis* bacterial complex (MTBC) annotated with metadata which you can `explore on Taxonium <https://www.taxonium.org/tuberculosis/SRA>`_.

Although *M. canettii* is considered a member of MTBC and was included in initial analysis, it is excluded from our tree on Taxonium due to being such an extreme outgroup that its inclusion would make navigating the rest of tree difficult.
