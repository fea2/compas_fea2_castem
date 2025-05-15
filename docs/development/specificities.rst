********************************************************************************
Input file specificities
********************************************************************************

This section provides explanations about specific aspects of Cast3M programming in the input file.

model
=================================

Node and element key
----------------------

After running an analysis, the results are stored in **MCHAML** (element field) or **CHPO** (point field) objects. 
In those objects, the nodes/elements are only refered through their Cast3m number identification. The tables **TABPOINTS** and **TABELE** store the points/elements and their ``compas_fea2`` key.
These tables will be then used for the result output, as explained below.


.. code-block::

    N1 =     -0.50000000     -0.50000000      0.50000000; #Definition of the node N1
    ID = DIME TABPOINTS.KEY;    #node number in Cast3M, corresponding to its order of creation
    TABPOINTS.KEY.ID = 1;   #the compas_fea2 key of the node is stored in the TABPOINTS table
    TABPOINTS.POINT.ID = N1;    #the corresponding Cast3M node is stored in the TABPOINTS table

.. code-block::

    E4 = MANU TET4 N68 N20 N23 N8 ;     #Definition of the element E4, a four-nodes TET4 element
    MAIL00 = MAIL00 ET E4 ;     #the element E4 is added to the global mesh of the part

    ID = DIME TABELE.(0).KEY;   #element number in Cast3M, corresponding to its order of creation
    TABELE.(0).KEY.ID = 4;      #the compas_fea2 key of the element is stored in the TABELE table
    TABELE.(0).ELE.ID = E4;     #the corresponding Cast3M element is stored in the TABPOINTS table

For nodes, the result values can be extracted from the node with the command :

.. code-block::

    VALi = EXTR CHOUT MOTi POINTi; 
    #CHOUT is the output node field
    #MOTi the name of the result component 
    #POINTi is the node for which a result is extracted

For elements, the result value can only be extracted from their Cast3m identification number, corresponding to its order of creation.


.. code-block::

    VALi = EXTR CHCONT MOTi NZONE NELE NGAUSS;
    #CHCONT is the output element field
    #MOTi the name of the result component 
    #NZONE is the zone of the element field (always 1 in our case)
    #NELE is the Cast3m identification number of the element
    #NGAUSS is the number of the GAUSS point 


problem
=================================

Loading definition (static analysis)
--------------------------------------

The **PASAPAS** analysis method, used here for both linear and non-linear static analyses (via the Newton-Raphson method), 
requires that loads be defined as functions of time.
This evolution is implemented in the **EVOLC** object (**EVOLUTION** object type). 
The number of steps and maximum values can be changed through the **load_step** attribute of the StaticStep class.


.. code-block::

    LISTEMP = PROG 0. 'PAS' 1. 10; #Time step
    LISC = PROG 0. 'PAS' 0.1 1.; #Loading step
    EVOLC = EVOL MANU 'TIME' LISTEMP 'CHARGE' LISC; #Evolution of loading through time

    CHCHAR= FORC FY -217.3913043478263 N53 ; #Definition of a force object on node N53
    EVCHAR = CHAR 'MECA' CHCHAR EVOLC;  #A evoluting load object from the force and general evolution object defined before
    CHARTOT = CHARTOT ET EVCHAR;    # The load is added to the general laod object


results
=================================

Output files
----------------------

The results obtained from the **PASAPAS** analysis can be saved in several format. 
In order to facilitate the compas_fea2_castem extraction of the results from the output files, the procedures **CHPOTAB**, **STRESSTAB** and **SFTAB** take as input, respectively, 
a point field, a stress element field or section force element field, and return the corresponding table associating the castem_fea2 key to the component results. 

The table is then published as an .csv file.