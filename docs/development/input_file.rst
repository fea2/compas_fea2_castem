********************************************************************************
Input file 
********************************************************************************

jobdata methods
=================================

Each ``compas_fea2_castem`` class is inherited from its corresponding ``compas_fea2`` class. 

The backend class adds : 

- eventual complementary attributes
- a jobdata method

The **jobdata** method aims at translating the ``compas_fea2`` commands into the plugin language and constructing the input file for the analysis. Each jobdata method returns a string or a list of strings.

For example, for a node :

.. code-block:: python

  from compas_fea2.model import Node

  class CastemNode(Node):

      def jobdata(self):
          x, y, z = self.xyz
          coordinates = "{0}{1}{2}{4:>15.8f}{3}{5:>15.8f}{3}{6:>15.8f}{7}".format("N", self.key, " = ", " ", x, y, z, ";")
          tabpoints_data = f"""
  ID = DIME TABPOINTS.KEY;
  TABPOINTS.KEY.ID = {self.key};
  TABPOINTS.POINT.ID = N{self.key};
  """
          return coordinates + tabpoints_data



Input file structure
=================================

This section described the general structure of the input file (.dgibi) created by the ``compas_fea2_castem`` plugin.


.. code-block::

    |_ Header

    |_ Procedures for post-treatment 
        (specific procedures for the extraction of results)

    |_ Model
        |_ Parts & Material & Section
            |_ part1
                |_ Nodes
                |_ Elements
                |_ Model, Material and Section
            |_ part2
                |_ Nodes
                |_ Elements
                |_ Model, Material and Section
            |_ part3
                |_ ...
        |_ Initial conditions
            |_ Boundary Conditions
        |_ Interaction and interfaces
            |_....
        |_ Connectors
            |_....

    |_ Problem
        |_ Loads
        |_ Imposed Displacements
        |_ Predefined Fields

    |_ Analysis
        (parameters for the analysis )

    |_ Output results
        (the procedures defined at the beginning of the document are called 
        for the results extraction)
        