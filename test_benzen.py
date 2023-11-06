"""
Ce code utilise la classe "OTree" définie dans le fichier "OTree_.py" pour créer un octree.
"""
from OTree_ import *

if __name__ == '__main__':
    threshold = 1
    # Stockez la valeur d'origine de stdout pour la restaurer ultérieurement
    orig_stdout = sys.stdout
    # Initialisation de l'octree à partir d'un fichier de molécule et la subdiviser
    o, list1, list2 = init_dot('Quelques fichiers de test-20221116/Molécules/benzène.dot', threshold)
    o.subdivide3d()
    # initialiser une liste de vitesse a 0
    vitess = [0 for i in range(len(o.root.points))]
    # Afficher un message pour indiquer la création du fichier
    print("création du fichier calcule nouvelles positions benzene")
    # Ouvrir un fichier pour écrire les résultats
    f = open('resultats/calcule_nouvelles_positions_benzene.txt', 'w')
    # Rediriger la sortie standard vers le fichier
    sys.stdout = f
    print('')
    # Affichage des positions initiales
    for p in o.root.points:
        print(f'Position Initiale,  (x : {p.x:.4f}, y : {p.y:.4f}, z : {p.z:.4f} )')
    # Calcul des forces de répulsion et d'attraction
    rep_f = list_forces_rep(o.root)
    att_f = list_forces_att(o.root)
    forces = rep_f + att_f
    # calculer les nouvelles positions
    new_pos, vitess = new_positions(forces, o.root, vitess, dt)
    # Création d'un nouvel objet OTree avec les positions mises à jour des points
    tmpo = OTree(1, len(o.root.points))
    tmpo.root.points = new_pos
    tmpo.points = new_pos
    # Subdivision de l'arbre
    tmpo.subdivide3d()

    # Affectation de nouveaux voisins à chaque point en fonction de leurs positions mises à jour
    for p in tmpo.root.points:
        p.neighbours = []
    for l1, l2 in zip(list1, list2):
        tmpo = assigner_des_voisins(tmpo, l1, l2)

    # Affichage des nouvelles positions de chaque point après la première itération de mise à jour
    print('')
    for p in tmpo.root.points:
        print(f'Aprés Itteration 1, (x : {p.x:.4f}, y : {p.y:.4f}, z : {p.z:.4f} )')

    # Exécution d'une seconde itération de mise à jour
    rep_f = list_forces_rep(tmpo.root)
    att_f = list_forces_att(tmpo.root)
    forces = rep_f + att_f
    new_pos, vitess = new_positions(forces, tmpo.root, vitess, dt)

    tmpo2 = OTree(1, len(o.root.points))
    tmpo2.root.points = new_pos
    tmpo2.points = new_pos
    tmpo.subdivide3d()

    # Affectation de nouveaux voisins à chaque point en fonction de leurs positions mises à jour
    for p in tmpo2.root.points:
        p.neighbours = []
    for l1, l2 in zip(list1, list2):
        tmpo2 = assigner_des_voisins(tmpo2, l1, l2)
    # Affichage des nouvelles positions de chaque point après la seconde itération de mise à jour
    print('')
    for p in tmpo2.root.points:
        print(f'Aprés Itteration 2, (x : {p.x:.4f}, y : {p.y:.4f}, z : {p.z:.4f} )')
    #####
    # Réinitialisation de stdout et fermeture du fichier
    sys.stdout = orig_stdout
    f.close()
    # Affichage d'un message pour indiquer la fin des calculs de mise à jour de position
    print("fin de création du fichier calcule des nouvelles positions benzene")
