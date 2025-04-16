from compas_fea2.model import Part
from compas_fea2.model import RigidPart


def jobdata(obj):
    """Generate the string information for the input file.

    Parameters
    ----------
    None

    Returns
    -------
    str
        input file data lines.
    """
    return f"""
***------------------------------------------------------------------
*** Part {obj.name}
***------------------------------------------------------------------
*** - Nodes
***   -----
{obj._generate_nodes_section()}

***node_data
*** - Elements
***   --------

TABELE.({obj.key}) = TABLE ;
TABELE.({obj.key}).KEY = TABLE;
TABELE.({obj.key}).ELE = TABLE;

{obj._generate_elements_section()}
***
"""


class CastemPart(Part):
    """Castem implementation of :class:`compas_fea2.model.DeformablePart`.

    Note
    ----

    """

    __doc__ += Part.__doc__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _group_elements(self):
        """Group the elements. This is used internally to generate the input
        file.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            {implementation:{element_type {section: [elements]},}
        """

        # group elements by type and section
        implementations = set(map(lambda x: x._implementation, self.elements))
        # group by type
        grouped_elements = {implementation: [el for el in self.elements if el._implementation == implementation] for implementation in implementations}

        for implementation, elements in grouped_elements.items():
            element_types = set(map(lambda x: x._type_element, elements))
            elements = {element_type: [el for el in elements if el._type_element == element_type] for element_type in element_types}
            # subgroup by section
            for element_type, sub_elements in elements.items():
                sections = set(map(lambda x: x.section, sub_elements))
                elements_by_section = {section: [el for el in sub_elements if el.section == section] for section in sections}
                elements[element_type] = elements_by_section
            grouped_elements[implementation] = elements

        return grouped_elements

    # =========================================================================
    #                       Generate input file data
    # =========================================================================

    def jobdata(self):
        return jobdata(self)

    def _generate_nodes_section(self):
        return "\n".join([node.jobdata() for node in self.nodes])

    def _generate_elements_section(self):
        """Generate a string of all the linesneeded for generation of the elements in the input file.
        Parameters
        ----------
        None

        Returns
        -------
        str

        """

        part_data = []
        grouped_elements = self._group_elements()

        # Initialization of MOD/MAT/MAIL for the part
        part_data.append("MOD{0} = VIDE 'MMODEL' ;".format(self.key))
        part_data.append("MAT{0} = VIDE 'MCHAML' ;".format(self.key))
        part_data.append("MAIL{0} = VIDE 'MAILLAGE' ;".format(self.key))

        # the creation of the element of the part is created according to the element type and then the section type
        for implementation, element_types in grouped_elements.items():
            part_data.append("\n***   >Elements de type {}".format(implementation))

            for element_type, sections in element_types.items():
                for section, elements in sections.items():
                    # Initialization of empty object for the mesh relative to elementtype and section
                    part_data.append("MAIL{0}{1} = VIDE 'MAILLAGE' ;".format(self.key, section.key))

                    # Write elements
                    for element in elements:
                        part_data.append("\nE{0} = MANU {1} N{2} ;".format(element.jobdata()[0], element_type, element.jobdata()[1]))
                        # newly created element is stored in the mesh
                        part_data.append("MAIL{0}{1} = MAIL{0}{1} ET E{2} ;".format(self.key, section.key, element.jobdata()[0]))

                        # the castem key (ID), the compas key (KEY) and the castem element of the newly created element are stored in TABELE
                        part_data.append(
                            f"""
ID = DIME TABELE.({self.key}).KEY;
TABELE.({self.key}).KEY.ID = {element.jobdata()[0]};
TABELE.({self.key}).ELE.ID = E{element.jobdata()[0]};
"""
                        )
                    # Write material and section per group of elements
                    part_data.append("\n***       >Creation du materiau associe au groupe d elements")

                    # Model Object that implements the type of behaviour and the type of implementation
                    part_data.append(
                        f"MOD{self.key}{section.key} = MODE MAIL{self.key}{section.key} {section.material.jobdata()[0]} {'' if implementation == 'massif' else implementation};"
                    )
                    # Mate Object that implements the parameters relative to the behaviour
                    part_data.append(f"MAT{self.key}{section.key} = MATE MOD{self.key}{section.key} {section.material.jobdata()[1]} ;")

                    # The implementation/section MODE/MAT/MESH are added to the part size one
                    part_data.append("MOD{0} = MOD{0} ET MOD{0}{1};".format(self.key, section.key))
                    part_data.append("MAT{0} = MAT{0} ET MAT{0}{1};".format(self.key, section.key))
                    part_data.append("MAIL{0} = MAIL{0} ET MAIL{0}{1};".format(self.key, section.key))

                    # Eventual supplementary caracteristics for modelization
                    if section.jobdata():
                        part_data.append("CARA{0}{1} = CARA MOD{0}{1} {2};".format(self.key, section.key, section.jobdata()))
                        part_data.append("MAT{0} = MAT{0} ET CARA{0}{1};".format(self.key, section.key))

        # Part objects are added to model objects
        part_data.append(f"MATTOT = MATTOT ET MAT{self.key};")
        part_data.append(f"MODTOT = MODTOT ET MOD{self.key};")
        part_data.append(f"MAILTOT = MAILTOT ET MAIL{self.key};")

        return "\n".join(part_data)


class CastemRigidPart(RigidPart):
    """Castem implementation of the :class:`RigidPart`.

    ----------------------------------------------
    WARNING :
    ----------------------------------------------

    The control of the whole part via a reference point is not implemented yet.
    To do so, either apply the load on all the nodes composing the cube.

    A pist of implementation could be done via the SUPER-ELEMENT amd master nodes.
    https://www-cast3m.cea.fr/index.php?page=notices&notice=SUPE

    -----------------------------------------------
     \n"""

    __doc__ += RigidPart.__doc__

    def __init__(self, name=None, **kwargs):
        super(CastemRigidPart, self).__init__(name=name, **kwargs)

    # =========================================================================
    #                       Generate input file data
    # =========================================================================

    def _group_elements(self):
        """Group the elements. This is used internally to generate the input
        file.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            {implementation:{section:{orientation: [elements]},},}
        """

        # group elements by type and section
        implementations = set(map(lambda x: x._implementation, self.elements))
        # group by type
        grouped_elements = {implementation: [el for el in self.elements if el._implementation == implementation] for implementation in implementations}
        # # subgroup by section
        # for implementation, elements in grouped_elements.items():
        #     grouped_elements[implementation] = elements

        return grouped_elements

    def jobdata(self):
        return jobdata(self)

    def _generate_nodes_section(self):
        return "\n".join([node.jobdata() for node in self.nodes])

    def _generate_elements_section(self):
        part_data = []
        grouped_elements = self._group_elements()
        part_data.append("MOD{0} = VIDE 'MMODEL' ;".format(self.key))
        part_data.append("MAT{0} = VIDE 'MCHAML' ;".format(self.key))
        part_data.append("MAIL{0} = VIDE 'MAILLAGE' ;".format(self.key))
        for implementation, elements in grouped_elements.items():
            part_data.append(f"\n***   >Elements de type {implementation}")
            part_data.append(f"MAIL{self.key}{implementation} = VIDE 'MAILLAGE' ;")
            for element in elements:
                # Write elements

                part_data.append(
                    "\nE{0} = MANU {1} N{2} ;".format(element.jobdata()[0], element._type_element, element.jobdata()[1])
                )  # la gestion des N devant les num de noeud n'est pas propre
                part_data.append(f"MAIL{self.key}{implementation} = MAIL{self.key}{implementation} ET E{element.jobdata()[0]} ;")
                part_data.append(
                    f"""
ID = DIME TABELE.({self.key}).KEY;
TABELE.({self.key}).KEY.ID = {element.jobdata()[0]};
TABELE.({self.key}).ELE.ID = E{element.jobdata()[0]};
"""
                )
            part_data.append(f"CORRIG{self.key} = RELA 'CORI' 'DEPL' 'ROTA' MAIL{self.key}{implementation};")
            part_data.append(f"CRIGTOT = CRIGTOT ET CORRIG{self.key};")
            part_data.append(f"MAILTOT = MAILTOT ET MAIL{self.key}{implementation};")
            part_data.append("\n***       >Creation du materiau associe au groupe d elements")
            part_data.append(
                "MOD{0}{1} = MODE MAIL{0}{1} {2} {3};".format(
                    self.key, implementation, element.section.material.jobdata()[0], "" if implementation == "massif" else implementation
                )
            )
            part_data.append(f"MAT{self.key}{implementation} = MATE MOD{self.key}{implementation} {element.section.material.jobdata()[1]} ;")
            if element.section.jobdata():
                part_data.append("CARA{0}{1} = CARA MOD{0}{1} {2};".format(self.key, implementation, element.section.jobdata()))
            part_data.append("MOD{0} = MOD{0} ET MOD{0}{1};".format(self.key, implementation))
            if element.section.jobdata():
                part_data.append("MAT{0} = MAT{0} ET MAT{0}{1} ET CARA{0}{1};".format(self.key, implementation))
            else:
                part_data.append("MAT{0} = MAT{0} ET MAT{0}{1};".format(self.key, implementation))
            part_data.append("MAIL{0} = MAIL{0} ET MAIL{0}{1};".format(self.key, implementation))
        part_data.append(f"MATTOT = MATTOT ET MAT{self.key};")
        part_data.append(f"MODTOT = MODTOT ET MOD{self.key};")

        return "\n".join(part_data)
