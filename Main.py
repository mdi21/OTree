"""
    Ce code utilise la classe "OTree" définie dans le fichier "OTree_.py" pour créer un octree.
    """
from OTree_ import *

"""La fonction main crée une liste de fichiers contenant des molécules, puis demande à l'utilisateur de choisir un 
fishier de molécule à partir de cette liste.
    
    Il utilise ensuite la fonction init_dot pour initialiser un Octree à partir du fichier choisi et le subdiviser en 
    utilisant la méthode subdivide3d.
    
    Il crée également une copie de cet Octree, calcule les forces de répulsion et d'attraction sur les points de 
    l'Octree,
    
    calcule les nouvelles positions des points en utilisant les forces calculées, met à jour les nouvelles positions 
    aux points de l'Octree,
    
    attribue les voisins aux points de l'Octree, subdivise de nouveau l'Octree avec les nouvelles positions, 
    puis affiche deux fenêtres,
    
    une pour l'Octree avant le calcul des forces et l'autre pour l'Octree après le calcul des forces. Il se termine 
    en quittant l'application."""

if __name__ == '__main__':
    threshhold = 1
    # creation d'une liste contenant les molecules
    filename = ['Quelques fichiers de test-20221116/Molécules/H2O.dot',
                'Quelques fichiers de test-20221116/Molécules/CH4.dot',
                'Quelques fichiers de test-20221116/Molécules/benzène.dot']

    # Boucle qui demande à l'utilisateur de choisir un fichier de molécule
    while True:
        print("Faites un choix:")
        print("1- H20")
        print("2- CH4")
        print("3- Benzène")
        choix = int(input("Quel est votre choix(Shiffre) ?:  "))
        if 1 <= choix <= 3:
            break
        else:
            print("\nEntez un nombre de la liste donner.\n")

    # Initialisation de l'Octree à partir du fichier de molécule choisi et le subdiviser
    my_octree, list1, list2 = init_dot(filename[choix - 1], threshhold)
    my_octree.subdivide3d()
    # Première fenêtre affichant l'Octree avant calcul des forces
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("L'Octree avant le calcul des forces")
    glWidget = GLWidget(my_octree)
    window.setCentralWidget(glWidget)
    window.setMinimumSize(800, 600)
    window.show()
    ###########################################################################
    # creation d'une copie de l'Octree
    O_after_force = copy.deepcopy(my_octree)
    # Calcul des forces de répulsion et d'attraction
    rep_f = list_forces_rep(O_after_force.root)
    att_f = list_forces_att(O_after_force.root)
    forces = rep_f + att_f
    # initialiser une liste de vitesse a 0
    vitess = [0 for i in range(len(O_after_force.root.points))]
    # calculer les nouvelles positions
    new_pos, vitess = new_positions(forces, O_after_force.root, vitess, dt)
    # met à jour les nouvelles positions a l'octree
    O_after_force.root.points = new_pos
    O_after_force.points = new_pos
    # subdivisions de l'octree avec les nouvelless possitions
    O_after_force.subdivide3d()
    # Affectation de nouveaux voisins à chaque point en fonction de leurs positions mises à jour
    for p in O_after_force.root.points:
        p.neighbours = []
    for l1, l2 in zip(list1, list2):
        O_after_force = assigner_des_voisins(O_after_force, l1, l2)
    # Deuxième fenêtre affichant l'Octree après calcul des forces
    window2 = QMainWindow()
    window2.setWindowTitle("L'Octree après le calcul des forces")
    glWidget = GLWidget(O_after_force)
    window2.setCentralWidget(glWidget)
    window2.setMinimumSize(800, 600)
    window2.show()
    sys.exit(app.exec_())
