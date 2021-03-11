.. include:: includes.rst.txt

*********************************************
Explanations and Tutorials
*********************************************

This document contains detailed explanations and example workflows for Usher and matUtils.

.. _extract:
--------------------------------------------
matUtils extract Explanation
--------------------------------------------

`matUtils extract` serves as a flexible prebuilt pipeline, which can quickly subset and convert an input MAT .pb file. 
Generally, its parameters can be grouped into four categories: 

1. Selection- these parameters define a subtree to use for further processing. If none are set, the whole input tree is used. Includes -c, -s, -m, and others.

2. Processing- these parameters, usually boolean in nature, apply specific processing steps to the subtree after selection. These can include selecting clade representative samples or collapsing the tree. Includes -O and -r among others.

3. Information- these parameters save information about the subtree which is not a direct representation of that subtree, such as mutations defining each clade in the subtree. Includes -C and -S among others.

4. Conversion- these parameters are used to request subtree representations in the indicated formats. Includes -v and -t among others.

These commands can be freely mixed and matched, allowing us to perform operations as simple as a direct vcf conversion by using a single conversion parameter:

.. code-block:: shell-session

  ./matUtils extract -i input.pb -v output.vcf

Rr as complex as multiple levels of selection of samples and writing of multiple output files by using parameters from all four categories.

.. code-block:: shell-session

    ./matUtils extract -i input.pb -c 19B -m A10042G -a 3 -S sample_paths.txt -O -o subtree.pb -t subtree.newick -d my_output/

`matUtils extract` is the workhorse function for manipulating MAT .pb files, particularly for any operations involving removing part of the .pb and converting .pb to other file formats.

.. _annotate:
---------------------------------
matUtils annotate Explanation
---------------------------------

`matUtils annotate` is a function for adding clade annotation information to the pb. This information can be accessed downstream by `matUtils extract` or other tools.

It has two general ways to add this information. The first, recommended fashion is to pass a simple two-column tsv containing clade and sample names. 
`matUtils annotate` will automatically identify the best clade root from this information with a three-step process.

1. It collects the set of mutations which are at at least -f allele frequency across the input samples; these represent the clade's likely defining mutations.

2. It creates a virtual sample from these mutations and uses Usher's highly optimized mapping algorithm to identify the internal nodes that it maps to best. These are candidate clade root nodes. Nodes directly ancestral to these sites are also considered as candidate roots.

3. For each of the candidate roots, the algorithm calculates the number of samples which are actually descendent of that node. The node which is ancestral to the most samples and which is not already assigned to another clade is assigned as the best clade root.

This does not guarantee that every sample that is member in the clade in the input will be a member of the clade at the end of assignment, but assignments are generally high quality.

The other option is simpler and more direct. Internal node identifiers can be passed directly through a two-column tsv and those nodes will be assigned as clade roots. 

.. warning::
    Internal node names are not maintained when saving and loading from a .pb file. It is not guaranteed that internal node names will correspond directly between two .pb files, so use the latter method with caution.

.. _uncertainty:
--------------------------------------------
matUtils uncertainty Explanation
--------------------------------------------

`matUtils uncertainty` calculates two specific metrics for sample placement certainty. These metrics can be very important to support contact tracing and reliable identification
of the origin of a newly placed sample.

The first of these is "equally parsimonious placements" (EPPs), which is the number of places on the tree a sample could be placed equally well. 
An EPPs score of 1 is a "perfect score", indicating that there is a single best placement for this sample on the tree. About 85% of samples on a normal SARS-COV-2 
phylogeny have an EPPs of 1. 

`matUtils uncertainty` calculates this metric by, for each sample in the input, remapping the sample against the same tree (disallowing it from mapping to itself) with Usher's optimized mapper function.
This function reports the number of best placements as part of the output, which is recorded by `matUtils uncertainty` and saved to the output.

The second metric is "neighborhood size score" (NSS), which is the longest direct traversable path between any two equally parsimonious placement locations for a given sample.
This metric is complementary to EPPs. When EPPs is 1, NSS is necessarily 0, as there are no traversable paths between pairs of placements when there's only one placement.

On an intuitive level, NSS is a representation of the distribution of equally parsimonious placements. For example, lets say we have two samples of interest. 
The first has five equally parsimonious placements, but they're all quite nearby each other on the tree with an LCA two nodes back.
The second has two equally parsimonious placements, but they're on opposite sides of the tree with an LCA at the root.
If we only looked at EPPs, we might assume that the second sample is more certain than the first. This is absolutely not the case-
the second sample could have originated from two different continents, while the first is likely from a specific local region. 
This is reflected in their NSS, which in the first case should be about 4, but in the latter could be in the tens to hundreds.

The most confident samples are ones which have an EPPs of 1 and an NSS of 0, followed by ones with low EPPS values and low NSS, followed by ones with higher EPPS and low NSS, and finally ones that are high on both metrics are least certain.

NSS is calculated by taking the set of equally parsimonious placements indicated by Usher's mapper function and identifying the LCA of all placements.
The two longest distances from the LCA to two placements are then summed and the result is reported as NSS- the longest direct path between two placements for the sample.

Both values are reported in distinct two-column tsvs, which are compatible with Auspice's metadata annotation for visualizing the samples. Information 
on this can be found `here <https://docs.nextstrain.org/projects/auspice/en/latest/advanced-functionality/drag-drop-csv-tsv.html>`_.

.. _protobuf:
-----------
The Mutation Annotated Tree (MAT) Protocol Buffer (.pb)
-----------

Google's `protocol buffer format <https://developers.google.com/protocol-buffers>`_ is a highly optimized, flexible binary storage format, with APIs for many languages. 
We use a specially formatted protocol buffer to store a Mutation Annotated Tree object. The .proto definition file can be found
in the Usher installation folder; we will describe it in brief here.

Our protobuf format has two major components. The first is a newick string, representing sample relationships for all samples included in the tree.
The second component is node information- including mutations, clade assignments, and condensed nodes. This second component is what makes
the mutation annotated tree such a powerful data storage method, as it simultaneously stores phylogenetic relationships and full mutation 
information for large numbers of samples in a compact format. 

When the protobuf is loaded, the tree is structured based on the stored newick string, 
then mutations and metadata are placed along the tree structure according to the node information vectors. 
The condensed nodes message is used to compact polytomies and other groups of identical samples, 
and the final step of loading is to uncondense these nodes back into full polytomies.

This structure allows us to perform both classical phylogenetic processes, such as traversing the tree and calculating parsimony scores,
while also being able to query samples as if they were a database of sequences, extracting a vcf of samples which contain a specific mutation for example.

Google also maintains a suite of general tools for working with protocol buffer format files, including interacting with protobufs across multiple languages.

Interacting with MAT Protobuf in Python [ADVANCED USERS]
----------

Advanced users may desire to interface directly with the protobuf. The following is a brief tutorial on doing so.
Google's general tutorial on interacting with protobuf in python can be found `here <https://developers.google.com/protocol-buffers/docs/pythontutorial#compiling-your-protocol-buffers>`_.
The instructions here can be applied to a number of additional languages supported by google as well, such as java, PHP, and ruby.

The first step is to call the protoc compiler to retrieve a MAT protobuf parser. Navigate to your Usher installation and call:

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

    print(my_mat.newick.count(":")
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
