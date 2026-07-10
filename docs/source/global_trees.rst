=====================
Global UShER trees
=====================
UCSC provides downloadable tree and metadata files for trees of genetic sequences for multiple pathogens. With the exception of the tuberculosis tree, all trees are updated daily.

* :ref:`Dengue <header-dengue>`
* :ref:`Influenza <header-flu>`
* :ref:`Mpox (MPXV/hMPXV) <header-mpox>`
* :ref:`RSV <header-rsv>`
* :ref:`SARS-CoV-2 (Covid-19) <header-covid>`
* :ref:`Tuberculosis (MTBC) <header-tuberculosis>`

In addition to these trees, thanks to `viral_usher <https://github.com/AngieHinrichs/viral_usher>`_, UCSC additionally provides trees for hundreds of viral species updated daily, including `HIV-1 <https://www.taxonium.org/viral-usher/human_immunodeficiency_virus_1/NC_001802.1>`_, `Zika <https://www.taxonium.org/viral-usher/zika_virus/NC_012532.1>`_, `Measles <https://www.taxonium.org/viral-usher/measles_morbillivirus/NC_001498.1>`_, and more. 


`You can browse all available trees on Taxonium here <https://www.taxonium.org/browse>`_.

.. _header-dengue:

Dengue
------
The mosquito-borne dengue virus has four serotypes. UCSC maintains trees for each serotype based on INDSDC samples. These trees are best viewed on `taxonium.org <https://taxonium.org>`_ but are also available for direct download.

* `DENV-1 <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/862/125/GCF_000862125.1/UShER_DENV-1/>`_, based on NC_001477.1
* `DENV-2 <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/871/845/GCF_000871845.1/UShER_DENV-2/>`_, based on NC_001474.2
* `DENV-3 <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/866/625/GCF_000866625.1/UShER_DENV-3/>`_, based on NC_001475.2
* `DENV-4 <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/865/065/GCF_000865065.1/UShER_DENV-4/>`_, based on NC_002640.1


.. _header-flu:

Influenza
---------
Influenza A has a segmented viral genome, complicating phylogenetics. UCSC maintains a total of 58 daily-updated trees for influenza A, 56 of which represent one segment of a given RefSeq assembly. The two "concatenated" trees are focused on recent H5N1 outbreaks.

Per-Segment Trees
*****************
There are seven RefSeq assemblies for six serotypes of Influenza A (human seasonal H1N1 and H3N2; avian H2N2, H5N1, H7N9, H9N2). Each assembly includes eight sequences, one per segment of the influenza A virus. UCSC maintains daily-updated trees of all Influenza A sequences that align to each RefSeq reference sequence; for these trees, the appropriate RefSeq assembly is considered both the reference and the root. The table below links to the download directory for each strain. Each directory has eight subdirectories ``UShER_NC_...`` named with the RefSeq IDs of the sequences.

==============================  ========================
RefSeq strain                   RefSeq assembly/download
==============================  ========================
A/California/07/2009(H1N1)      `GCF_001343785.1 <https://hgdownload.gi.ucsc.edu/hubs/GCF/001/343/785/GCF_001343785.1/>`_
A/Puerto Rico/8/1934(H1N1)      `GCF_000865725.1 <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/865/725/GCF_000865725.1/>`_
A/New York/392/2004(H3N2)       `GCF_000865085.1 <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/865/085/GCF_000865085.1/>`_
A/Korea/426/1968(H2N2)          `GCF_000866645.1 <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/866/645/GCF_000866645.1/>`_
A/goose/Guangdong/1/1996(H5N1)  `GCF_000864105.1 <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/864/105/GCF_000864105.1/>`_
A/Shanghai/02/2013(H7N9)        `GCF_000928555.1 <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/928/555/GCF_000928555.1/>`_
A/Hong Kong/1073/99(H9N2)       `GCF_000851145.1 <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/851/145/GCF_000851145.1/>`_
==============================  ========================

`taxonium.org <https://taxonium.org>`_ has all 56 trees; search by subtype (e.g. H5N1) to see a list of per-segment trees.

Concatenated Trees
******************
These H5N1 trees are for sequences linked to recent outbreaks.

* H5N1 D1.1 2024 outbreak
	* `Taxonium version here <https://www.taxonium.org/flu/H5N1-Outbreak-D1-1>`_
	* `Download here <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/864/105/GCF_000864105.1/UShER_h5n1_D1.1_2024/>`_
	* Rooted to a concatenation of Genbank segement sequences PQ844107.1, OP597633.1, PQ885594.1, LC718226.1, PQ585621.1, PQ664459.1, OP597621.1, and PQ712157.1
* H5N1 B3.13 cattle 2024 outbreak
	* `Taxonium version here <https://www.taxonium.org/flu/H5N1-Outbreak>`_
	* `Download here <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/864/105/GCF_000864105.1/UShER_h5n1_outbreak_2024/>`_
	* Rooted to a concatenation of Genbank segement sequences PP755620.1, PP755619.1, PP755618.1, PP753693.1, PP755616.1, PP753695.1, PP755614.1, and PP753097.1


.. _header-mpox:

Mpox (MPXV/hMPXV)
-----------------
Mpox, `previously known as monkeypox <https://www.who.int/news/item/28-11-2022-who-recommends-new-name-for-monkeypox-disease>`_, is an orthopoxvirus with distinct clades. The clade designated IIb per `Happi et al. nomenclature <https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3001769>`_ is associated with an outbreak which gained global attention in 2022 although likely began circa 2017. You may `view the MPXV clade IIB tree on Taxonium  <https://www.taxonium.org/mpox/clade-IIb>`_ or download it `here <https://hgdownload.gi.ucsc.edu/hubs/GCF/014/621/545/GCF_014621545.1/UShER_hMPXV/>`_.

Clade I of MPVX `is also available <https://hgdownload.gi.ucsc.edu/hubs/GCF/000/857/045/GCF_000857045.1/UShER_MPXV_cladeI/>`_.


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
The global public SARS-CoV-2 tree includes over nine million sequences from a variety of sources. The public SARS-CoV-2 trees and information about their data sources `can be found here <https://hgdownload.gi.ucsc.edu/goldenPath/wuhCor1/UShER_SARS-CoV-2/>`_. You can also `click here to view the latest tree in taxonium <https://taxonium.org/sars-cov-2/public>`_. 

There is also a full tree that includes restricted-use GISAID sequences. This tree is not available for download, but sequences can be placed on it using `https://usher.bio <https://usher.bio>`_.


.. _header-tuberculosis:

Tuberculosis (MTBC)
-------------------
UShER isn't just for viruses. `As described in this preprint <https://www.medrxiv.org/content/10.1101/2025.07.22.25331806v1>`_, we built a tree of *Mycobacterium tuberculosis* bacterial complex (MTBC) annotated with resistance, country, and other metadata which you can `explore on Taxonium <https://www.taxonium.org/tuberculosis/SRA>`_. 

MTBC includes tuberculosis in the strict sense, as well as animal-adapted versions such as *Mycobacterium bovis* and *Mycobacterium pinnipedii*, but it excludes NTM (avium complex, etc). Although *Mycobacterium canettii* is considered a member of MTBC and was included in initial analysis, it is excluded from our tree on Taxonium due to being such an extreme outgroup that its inclusion would make navigating the rest of tree difficult.
