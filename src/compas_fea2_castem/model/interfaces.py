from compas_fea2.model import Interface
from compas_fea2.model import _Element3D


class CastemInterface(Interface):
    """Castem implementation of :class:`Interface`.

    Note
    ----
    There is no concept of master and slave in the generation of the interface.
    In Castem, the interface is created by a specific JOINT element, that links the nodes of
    a first mesh to a second one, accordingly a tolerance.

    The creation of a joint in Castem needs a specific configuration in the nodes :
        > the nodes must be facing each other two-by-two
        > the order of creation of the nodes must be the same in the two meshes
        
                      
            1 ------JOINT------- 1
            ¦ \                 ¦ \ 
            ¦  \                ¦  \                 
    MESH A  ¦   3 ----JOINT-----¦---3  MESH B
            ¦  /                ¦  /
            ¦ /                 ¦ /       
            2 ------JOINT-------2         
    

    """

    __doc__ += Interface.__doc__
    __doc__ += """
    Additional Parameters
    ---------------------
    tolerance : float
        tolerance criteria for the distance between two nodes
    """

    def __init__(self, master, slave, behavior, tolerance=0.1, **kwargs):
        super(CastemInterface, self).__init__(master=master, slave=slave, behavior=behavior, **kwargs)

        self.tolerance = tolerance

    def castem_groupmesh(self, meshname, group):
        """Method for a compact implementation of a mesh in Castem.

        Length of lines are limited to 50 characters and A same command is limited to 450 characters.
        Otherwise Castem raises an error.


        """

        groupmesh_data = []
        # Initialization of the mesh object
        groupmesh_data.append(meshname + "= VIDE 'MAILLAGE';")

        mail_data = meshname + " = " + meshname
        n_directive = len(mail_data)  # count the nb of character in a command

        for single in list(group):
            element = single.element

            # nb of character of a line has depassed 50 characters
            if (len(mail_data) + 4 + len(str(element.key))) > 50:
                # the command contains more than 450 characters.
                # the command is closed and a new one is generated
                if n_directive > 450:
                    mail_data += ";"
                    groupmesh_data.append(mail_data)
                    mail_data = meshname + " = " + meshname
                    n_directive = 0

                else:
                    groupmesh_data.append(mail_data)
                    mail_data = ""
            else:
                mail_data += f" ET E{element.key}"
                n_directive += len(f" ET E{element.key}")
        groupmesh_data.append(mail_data + ";")

        return "\n".join(groupmesh_data)

    def jobdata(self):
        """The interface/joint element is created via the GENJ method.
        https://www-cast3m.cea.fr/index.php?page=notices&notice=genj

        Warning
        ----------
        Only the interface for 3D element is implemented for now.



        """

        if isinstance(self._registration.elements[0], _Element3D):
            return f"""
{self.castem_groupmesh(meshname="MAILMAS", group=self.master.members)}
{self.castem_groupmesh(meshname="MAILESC", group=self.slave.members)}
DEELIM = 0.001;
ELIM MAILMAS DEELIM;
ELIM MAILESC DEELIM;
MAILINT = MAILMAS ET MAILESC;
JOINJ = GENJ (MAILINT) {self.tolerance};
MODJ = MODE JOINJ {self.behavior._jointmodel} JOT3  ;
MATJ = MATE MODJ {self.behavior.jobdata()};

MODJTOT = MODJTOT ET MODJ;
MATJTOT = MATJTOT ET MATJ;
"""
        else:
            raise NotImplementedError
