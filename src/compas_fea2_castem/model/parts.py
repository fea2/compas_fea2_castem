from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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
*** Part {}
***------------------------------------------------------------------
*** - Nodes
***   -----
ALLNODE = VIDE 'TABU' (MOTS 'TAG' 'NOEU') 'LISTENTI'*2;
{}

***node_data
*** - Elements
***   --------
{}
***
""".format(
        obj.name, _generate_nodes_section(obj), _generate_elements_section(obj) or "***"
    )


def _generate_nodes_section(obj):
    return "\n".join([node.jobdata() for node in obj.nodes])


def _generate_elements_section(obj):
    part_data = []
    # Write elements(, elsets and sections)
    # this check is needed for rigid parts ->ugly, change!
    grouped_elements = obj._group_elements()
    if not isinstance(obj, RigidPart):
        part_data.append("MODTOT = VIDE 'MMODEL';")
        part_data.append("MATTOT = VIDE 'MCHAML';")

        for implementation, element_types in grouped_elements.items():
            part_data.append("\n***   >Elements de type {}".format(implementation))
            for element_type, sections in element_types.items():
                for section, elements in sections.items():
                    part_data.append("MAIL{0}{1} = VIDE 'MAILLAGE' ;".format(obj.input_key, section.input_key))
                    # Write elements
                    for element in elements:
                        part_data.append(
                            "\nE{0} = MANU {1} N{2} ;".format(element.jobdata()[0], element_type, element.jobdata()[1])
                        )  # la gestion des N devant les num de noeud n'est pas propre
                        part_data.append("MAIL{0}{1} = MAIL{0}{1} ET E{2} ;".format(obj.input_key, section.input_key, element.jobdata()[0]))
                    # Write material and section per group of elements
                    part_data.append("\n***       >Creation du materiau associe au groupe d elements")
                    part_data.append(
                        "MOD{0}{1} = MODE MAIL{0}{1} {2} {3};".format(
                            obj.input_key,
                            section.input_key,
                            section.material.jobdata()[0],
                            implementation,
                        )
                    )
                    part_data.append(
                        "MAT{0}{1} = MATE MOD{0}{1} {2} ;".format(
                            obj.input_key,
                            section.input_key,
                            section.material.jobdata()[1],
                        )
                    )
                    part_data.append("CARA{0}{1} = CARA MOD{0}{1} {2};".format(obj.input_key, section.input_key, section.jobdata()))
                    part_data.append("MODTOT = MODTOT ET MOD{0}{1};".format(obj.input_key, section.input_key))
                    part_data.append("MATTOT = MATTOT ET MAT{0}{1} ET CARA{0}{1};".format(obj.input_key, section.input_key))

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
        super(CastemPart, self).__init__(**kwargs)

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
