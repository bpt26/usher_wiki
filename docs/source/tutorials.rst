.. include:: includes.rst.txt

*********************************************
Explanations and Tutorials
*********************************************

This document contains example workflows for Usher and matUtils.

.. _uncertainty-tutorial:

Example Workflow
----------

In this example we will calculate uncertainty metrics for samples belonging to clade A.2.4 and visualize them on `auspice <https://auspice.us/>`_.

Download the example protobuf file `public-2021-03-02.all.masked.nextclade.pangolin.pb <https://hgwdev.gi.ucsc.edu/~angie/UShER_SARS-CoV-2/2021/03/02/public-2021-03-02.all.masked.nextclade.pangolin.pb>`_ (protobuf file containing the mutation annotated tree with clade annotations)

The first step is generating a visualizable JSON of the clade of interest, along with getting the names of samples involved.
This is done with matUtils extract.

.. code-block:: shell-session

    matUtils extract -i public-2021-03-02.all.masked.nextclade.pangolin.pb -c A.2.4 -u a24_samples.txt -j a24_viz.json

The second step is to call matUtils uncertainty. The input PB is the original PB, with the sample selection text file, instead of a subtree pb generated with -o.
This is because its going to search for placements all along the original tree; if a subtree .pb was passed, it would only search for placements within that subtree.

.. code-block:: shell-session

    matUtils uncertainty -i public-2021-03-02.all.masked.nextclade.pangolin.pb -s a24_samples.txt -e a24_epps.tsv -n a24_ns.tsv

These can now be uploaded for visualization by drag and drop onto the `auspice <https://auspice.us/>`_ website. Drag and drop the a24_viz.json first, then a24_epps.tsv second.

.. _protobuf-tutorial:

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
