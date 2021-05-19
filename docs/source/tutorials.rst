.. include:: includes.rst.txt

*********************************************
Tutorials
*********************************************

This document contains example workflows for UShER and matUtils.

.. _basic-matUtils-workflow:

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

.. _uncertainty-tutorial:

Example Uncertainty Workflow
----------

In this example we will calculate uncertainty metrics for samples belonging to clade B.1.500 and visualize them on `auspice <https://auspice.us/>`_.

Download the example protobuf file `public-2021-05-17.all.masked.nextclade.pangolin.pb.gz <https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/2021/05/17/public-2021-05-17.all.masked.nextclade.pangolin.pb.gz>`_ (protobuf file containing the mutation annotated tree with clade annotations)

The first step is generating a visualizable JSON of the clade of interest, along with getting the names of samples involved.
This is done with matUtils extract. In our example, we will get the samples associated with a small pangolin clade.

.. code-block:: shell-session

    matUtils extract -i public-2021-05-17.all.masked.nextclade.pangolin.pb.gz -c B.1.500 -u b1500_samples.txt -j b1500_viz.json

The second step is to call matUtils uncertainty. The input PB is the original PB, with the sample selection text file, instead of a subtree pb generated with -o.
This is because its going to search for placements all along the original tree; if a subtree .pb was passed, it would only search for placements within that subtree.

.. code-block:: shell-session

    matUtils uncertainty -i public-2021-05-17.all.masked.nextclade.pangolin.pb.gz -s b1500_samples.txt -e b1500_epps.tsv -n b1500_ns.tsv

These can now be uploaded for visualization by drag and drop onto the `auspice <https://auspice.us/>`_ website. Drag and drop the b1500_viz.json first, then the tsv files second.
Alternatively, the metadata can be included in JSON generation by matUtils extract. The metadata must be combined into a single tsv/csv first.

.. code-block:: shell-session

    awk '{print $2}' b1500_ns.tsv | paste b1500_epps.tsv - > b1500_combined.tsv
    matUtils extract -i public-2021-05-17.all.masked.nextclade.pangolin.pb.gz -s b1500_samples.txt -M b1500_combined.tsv -j b1500_annotated.json

.. _introduce-tutorial:

Example Introduce Workflow
----------

.. note:: 
    THIS FEATURE IS EXPERIMENTAL. We are actively soliciting feedback on the usefulness of the current implementation, additional features
    that would be valuable, or directions to take this type of analysis. Please reach out on the GitHub or directly to me via my email, 
    jmcbroom@ucsc.edu.

In this example we will infer and investigate introductions of SARS-CoV-2 into Spain using public information
on the command line and visualize an example introduction of interest with Auspice.

Before beginning, download the example protobuf file `public-2021-04-20.all.masked.nextclade.pangolin.pb <https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/2021/03/02/public-2021-04-20.all.masked.nextclade.pangolin.pb>`_ 

We need a region to analyze; in this example, we are going to use Spain, as it has a few hundred associated samples in the public data
and is a solid representative example. We need to generate the two-column tab-separated file we use as input to `matUtils introduce`.

.. code-block:: shell-session

    matUtils summary -i public-2021-04-20.all.masked.nextclade.pangolin.pb -s 420_sample_parsimony.txt
    grep “Spain” 420_sample_parsimony.txt | awk ‘{print $1”\tSpain”}’ > spanish_samples.txt

We can now apply `matUtils introduce` using this file as input.

.. code-block:: shell-session

    matUtils introduce -i public-2021-04-20.all.masked.nextclade.pangolin.pb -s spanish_samples.txt -o spanish_introductions.txt

The output table (spanish_introductions.txt) has columns for the sample, the identifier of the introduction node, the confidence of that introduction point being in region,
the confidence of the parent of that introduction point being in region, the number of mutations between the sample and this introduction point,
any clades associated with the introduction point, and the path of mutations to the point of introduction.

Generally the confidence of the introduction point will be greater than 0.5 and the confidence of the parent of the introduction point will be less than 0.5,
marking the point on the history where we stop being confident that the represented ancestral sequence was local to the region. 

We can count the number of unique introductions into our region of interest- in this case Spain- using awk.

.. code-block:: shell-session

    awk '{print $2}' spanish_introductions.tsv | sort | uniq -c | sort -r | head -25 

We find 216 unique introductions into Spain, of which 175 are associated with only a single sample, from 295 total samples.
This may suggest that Spain has a lot of movement in and out of the country, or that sampling is biased towards travelers. 
It may also simply reflect that Spain is undersampled and the relative number of introductions is high enough that most
new regional clades are sampled only once or not at all. 

There are some interesting cases of clades from a single introduction, however. The clade introduced at the internal node "96055" 
contains 9 closely related samples from Spain and are all members of the variant of concern B.1.1.7.

.. code-block:: shell-session

    awk '$2 == "96055"' spanish_introductions.tsv

.. warning::
    Internal node names are not maintained in the protobuf and are not guaranteed to be consistent between protobufs with differing content.
    The path of mutations to the point of introduction will generally be consistent, however.

The first entry of this output is reproduced here, sans the mutation path.

.. code-block:: shell-session

    ESP/hCoV-19_Spain_CT-HUVH-76622_2021/2021|MW769758.1|21-01-19	96055	1	0.0431655	2	20I/501Y.V1,B.1.1.7,B.1.1.28,20B,B.1.1,20A,B.1.1.171,B.1,19A,B	

We can see that this introduction point is very confidently in Spain (confidence of 1 in column 3, as every descendent is from Spain) but that 
the parent of that introduction point is very confidently NOT from Spain (confidence of 0.043 to be in Spain). This makes this a strongly supported introduction
of a variant of concern into our region. Let's take a closer look by visualizing it on the `Auspice <https://auspice.us/>`_ web interface.

To do this, first we will need to generate an auspice-compatible JSON containing our introduction set and some context samples. We can do this 
by selecting one of our samples and extracting the context to a JSON with `matUtils extract`.

.. code-block:: shell-session

    matUtils extract -i public-2021-04-20.all.masked.nextclade.pangolin.pb -k "ESP/hCoV-19_Spain_CT-HUVH-76622_2021/2021|MW769758.1|21-01-19:50" -j spanish_introduction.json

This JSON can be drag-and-dropped onto the Auspice web inferface. The resulting image is reproduced here.

.. image:: colored_spanish_introduction.png
    :width: 1500px
    :align: center

Samples from England appear in blue, Spain in green, and Wales in yellow in this image. We can see that our group of 9 B.1.1.7 samples forms a clear clade that was likely introduced into Spain from England.

Additional steps we could include are the generation of metadata tsv/csv for Auspice, the inclusion of more regions, and the inclusion of phylogeographic statistics with
-a on our call to `matUtils introduce`. The latter increases the runtime of the introduce command from a few seconds to about two minutes in this case.

Spain has an overall association index of 10.4 under a 95% confidence interval of (28.95,40.19) for the null that 
samples from this region are not phylogenetically associated.
This is a very, very significant association score, which is normal for geographic regions, as naturally samples from the same region
are more closely related to one another. The largest monophyletic clade size is 9, representing our specific introduction of interest.

Our specific introduction of interest itself also has a monophyletic clade size of 9 (being pure with 9 samples) and an association index of 0,
representing that it is purely in-region and is maximally associated. 

Including additional public region information in the input two-column tsv would also allow us to explore potential origins of each introduction,
such as how England appears to be the origin in our example, or estimate relative levels of migration to and from Spain to other countries across the world.
Origin and migration must be interpreted cautiously, however, due to extensive sampling bias by country (England and the UK contribute a large part
of publicly available sequence information, and are therefore more likely to be identified as the origin of an introduction, et cetera).

.. _protobuf-tutorial:

Interacting with MAT Protobuf in Python [ADVANCED USERS]
----------

Advanced users may desire to interface directly with the protobuf. The following is a brief tutorial on doing so.
Google's general tutorial on interacting with protobuf in python can be found `here <https://developers.google.com/protocol-buffers/docs/pythontutorial#compiling-your-protocol-buffers>`_.
The instructions here can be applied to a number of additional languages supported by google as well, such as java, PHP, and ruby.

The first step is to call the protoc compiler to retrieve a MAT protobuf parser. Navigate to your Usher installation (or clone the github if you installed via conda) and call:

.. code-block:: shell-session

    protoc -I=./ --python_out=./ ./parsimony.proto

This will generate the python file "parsimony_pb2.py". 

You can import this file into your favorite python IDE and use it to access the MAT like so:

.. code-block:: python

    import parsimony_pb2
    pb_file = open('input.pb', 'rb')
    my_mat = parsimony_pb2.data()
    my_mat.ParseFromString(pb_file.read())
    pb_file.close()

The my_mat object now contains the protobuf information, with general protobuf class attributes and four MAT specific attributes.
These are newick, condensed_nodes, metadata, and node_mutations. 

The newick attribute is simply the newick string representing the tree, as stored in the protobuf.

.. code-block:: python

    print(my_mat.newick.count(":"))
    print(my_mat.newick[:100])

The metadata attribute is a list of metadata message objects, which each have a single attribute which is a list of strings.
These strings are the clade annotations for any given node. The mutation list is similar, being a list of lists. Each list contains a 
series of mutation messages, which have attributes describing their position and identity. Each list corresponds to a single node on the tree.

.. code-block:: python

    print(len(my_mat.metadata))
    print(len(my_mat.node_mutations))

Individual node mutations are encoded as integers instead of characters for efficiency. These are in ACGT order- that is, 0 is A, 1 is C, 2 is G, and 3 is T. 
Additionally, the mut_nuc (new mutation) is another list-like attribute.

.. code-block:: python

    convert = {i:s for i,s in enumerate("ACGT")}
    for t in my_mat.node_mutations:
        if len(t.mutation) > 0:
            first_mut = t.mutation[0]
            print("First mutation encountered identifier string is: {}".format(
                convert[first_mut.ref_nuc] +
                str(first_mut.position) +
                convert[first_mut.mut_nuc[0]]))
            break

Condensed nodes is a special format container that essentially acts as a list of objects. Each object has a node_name attribute 
which is the string naming that node and another container which is essentially a list of strings of sample names.

.. code-block:: python

    print(my_mat.condensed_nodes[0].node_name)
    print(len(my_mat.condensed_nodes[0].condensed_leaves))

These are the essentials for writing a custom analysis directly interacting with the protobuf. For most user's purposes, however,
matUtils should provide the tools necessary for interacting with a MAT .pb file.
