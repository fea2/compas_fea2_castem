********************************************************************************
Introduction
********************************************************************************

Welcome to ``compas_fea2``, a powerful and flexible framework for finite element analysis (FEA) in Python. This package is part of the COMPAS framework, an open-source initiative aimed at providing computational tools for research and collaboration in architecture, engineering, and digital fabrication.

This documentation introduces ``compas_fea2_castem``, the Cast3M "backend" of compas_fea2 : the software Cast3m is used as a solver of the FEA problem defined in a compas_fea2 script. 

Cast3m is an opensource FEA software developped by the CEA organization in France. Cast3m can be installed on Windows, Linux and MacOS systems.
Please access the official `Cast3m website <https://www-cast3m.cea.fr/index.php>`_ for more detailed information about the software. 
The documentation of Cast3m is available in French and English.

The ``compas_fea2_castem`` plugin is not meant for direct user interaction. This plugin is :

- translating the FEA problem defined in a compas_fea2 script into a cast3m input file 
- extracting the results obtained from the Cast3M analysis and storing them in a unified compas_fea2 database (SQLlite by default),

However, the scripts defining a FEA problem must be written through the ``compas_fea2`` library. 
The backend must be defined at the beginning of the script with the following command :

.. code-block:: python

    import compas_fea2
    compas_fea2.set_backend("compas_fea2_castem")


For more detailed information and examples about ``compas_fea2`` and FEA, please refer to the specific documentation of `compas_fea2 core library <https://fea2.github.io/compas_fea2/latest/index.html>`_.

To see what is currently implemented in the plugin, please refer to its API documentation.
