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
    return """
***------------------------------------------------------------------
*** Part {0}
***------------------------------------------------------------------
*** - Nodes
***   -----
{1}

***node_data
*** - Elements
***   --------

TABELE.({2}) = TABLE ;
TABELE.({2}).KEY = TABLE;
TABELE.({2}).ELE = TABLE;

{3}
***
""".format(
        obj.name, _generate_nodes_section(obj), obj.key, _generate_elements_section(obj) or "***"
    )


def _generate_nodes_section(obj):
    return "\n".join([node.jobdata() for node in obj.nodes])


def _generate_elements_section(obj):
    part_data = []
    # Write elements(, elsets and sections)
    # this check is needed for rigid parts ->ugly, change!
    grouped_elements = obj._group_elements()
    if not isinstance(obj, RigidPart):
        for implementation, element_types in grouped_elements.items():
            part_data.append("\n***   >Elements de type {}".format(implementation))
            for element_type, sections in element_types.items():
                for section, elements in sections.items():
                    part_data.append("MAIL{0}{1} = VIDE 'MAILLAGE' ;".format(obj.key, section.key))
                    # Write elements
                    for element in elements:
                        part_data.append(
                            "\nE{0} = MANU {1} N{2} ;".format(element.jobdata()[0], element_type, element.jobdata()[1])
                        )  # la gestion des N devant les num de noeud n'est pas propre
                        part_data.append("MAIL{0}{1} = MAIL{0}{1} ET E{2} ;".format(obj.key, section.key, element.jobdata()[0]))
                        part_data.append(
                            f"""
ID = DIME TABELE.({obj.key}).KEY;
TABELE.({obj.key}).KEY.ID = {element.jobdata()[0]};
TABELE.({obj.key}).ELE.ID = E{element.jobdata()[0]};
"""
                        )
                    # Write material and section per group of elements
                    part_data.append("\n***       >Creation du materiau associe au groupe d elements")
                    part_data.append(
                        "MOD{0}{1} = MODE MAIL{0}{1} {2} {3};".format(
                            obj.key,
                            section.key,
                            section.material.jobdata()[0],
                            implementation if not (implementation == "massif") else "",
                        )
                    )
                    if section.material.jobdata()[2]:
                        part_data.append(complementary_material_line for complementary_material_line in section.material.jobdata()[1])
                    part_data.append(
                        "MAT{0}{1} = MATE MOD{0}{1} {2} ;".format(
                            obj.key,
                            section.key,
                            section.material.jobdata()[1],
                        )
                    )
                    if section.jobdata():
                        part_data.append("CARA{0}{1} = CARA MOD{0}{1} {2};".format(obj.key, section.key, section.jobdata()))
                    part_data.append("MODTOT = MODTOT ET MOD{0}{1};".format(obj.key, section.key))
                    if section.jobdata():
                        part_data.append("MATTOT = MATTOT ET MAT{0}{1} ET CARA{0}{1};".format(obj.key, section.key))
                    else:
                        part_data.append("MATTOT = MATTOT ET MAT{0}{1};".format(obj.key, section.key))

    else:
        for implementation, elements in grouped_elements.items():
            elset_name = "aux_{}".format(implementation)
            part_data.append("*Element, type={}, elset={}".format(implementation, elset_name))
            for element in elements:
                part_data.append(element.jobdata())
    return "\n".join(part_data)


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
*** Part {self.name}
***------------------------------------------------------------------
*** - Nodes
***   -----
{self._generate_nodes_section()}

***node_data
*** - Elements
***   --------

TABELE.({self.key}) = TABLE ;
TABELE.({self.key}).KEY = TABLE;
TABELE.({self.key}).ELE = TABLE;

{self._generate_elements_section()}
***
"""

    def _generate_nodes_section(self):
        return "\n".join([node.jobdata() for node in self.nodes])

    def _generate_elements_section(self):
        part_data = []
        grouped_elements = self._group_elements()
        if not isinstance(self, RigidPart):
            for implementation, element_types in grouped_elements.items():
                part_data.append("\n***   >Elements de type {}".format(implementation))
                for element_type, sections in element_types.items():
                    for section, elements in sections.items():
                        part_data.append("MAIL{0}{1} = VIDE 'MAILLAGE' ;".format(self.key, section.key))
                        # Write elements
                        for element in elements:
                            part_data.append(
                                "\nE{0} = MANU {1} N{2} ;".format(element.jobdata()[0], element_type, element.jobdata()[1])
                            )  # la gestion des N devant les num de noeud n'est pas propre
                            part_data.append("MAIL{0}{1} = MAIL{0}{1} ET E{2} ;".format(self.key, section.key, element.jobdata()[0]))
                            part_data.append(
                                f"""
    ID = DIME TABELE.({self.key}).KEY;
    TABELE.({self.key}).KEY.ID = {element.jobdata()[0]};
    TABELE.({self.key}).ELE.ID = E{element.jobdata()[0]};
    """
                            )
                        # Write material and section per group of elements
                        part_data.append("\n***       >Creation du materiau associe au groupe d elements")
                        part_data.append(
                            "MOD{0}{1} = MODE MAIL{0}{1} {2} {3};".format(
                                self.key,
                                section.key,
                                section.material.jobdata()[0],
                                implementation if not (implementation == "massif") else "",
                            )
                        )
                        part_data.append(
                            "MAT{0}{1} = MATE MOD{0}{1} {2} ;".format(
                                self.key,
                                section.key,
                                section.material.jobdata()[1],
                            )
                        )
                        if section.jobdata():
                            part_data.append("CARA{0}{1} = CARA MOD{0}{1} {2};".format(self.key, section.key, section.jobdata()))
                        part_data.append("MODTOT = MODTOT ET MOD{0}{1};".format(self.key, section.key))
                        if section.jobdata():
                            part_data.append("MATTOT = MATTOT ET MAT{0}{1} ET CARA{0}{1};".format(self.key, section.key))
                        else:
                            part_data.append("MATTOT = MATTOT ET MAT{0}{1};".format(self.key, section.key))

        else:
            for implementation, elements in grouped_elements.items():
                elset_name = "aux_{}".format(implementation)
                part_data.append("*Element, type={}, elset={}".format(implementation, elset_name))
                for element in elements:
                    part_data.append(element.jobdata())
        return "\n".join(part_data)
