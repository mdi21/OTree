import time

import matplotlib.pyplot as plt

"""
Ce code utilise la classe "OTree" définie dans le fichier "OTree_.py" pour créer un octree.
"""
from OTree_ import *

if __name__ == '__main__':
    x = []
    y = []
    # Stockez la valeur d'origine de stdout pour la restaurer ultérieurement
    orig_stdout = sys.stdout
    # Afficher un message pour indiquer la création du fichier
    print("création du fichier calcule complexites")
    # Ouvrir un fichier pour écrire les résultats
    f = open('resultats/calcule_complexites.txt', 'w')
    # Rediriger la sortie standard vers le fichier
    sys.stdout = f
    threshold = 30
    for i in range(30, 1000, 10):
        # creation d'un Octree
        o = OTree(threshold, i)
        # subdivition de l'octree
        o.subdivide3d()
        start_time = time.time()
        # Calcul des forces de répulsion et d'attraction
        rep_f = list_forces_rep(o.root)
        att_f = list_forces_att(o.root)
        forces = rep_f + att_f
        # initialiser une liste de vitesse a 0
        vitess = [0 for i in range(len(o.root.points))]
        # calculer les nouvelles positions
        new_pos, vitess = new_positions(forces, o.root, vitess, dt)

        end_time = time.time()
        # calcule la duree de l'operation calcule force
        duration = end_time - start_time
        x.append(i)
        y.append(duration)
        print(f"Duration pour calcule position de {i} points: {duration} ", )

    # Réinitialisation de stdout et fermeture du fichier
    sys.stdout = orig_stdout
    f.close()
    # Affichage d'un message pour indiquer la fin de calcule de complexite
    print("fin de création du fichier calcule complexites")
    plt.plot(x, y)
    plt.xlabel('Nombre des points')
    plt.ylabel('le Temps de Calcule')
    plt.title('Graphe de temps de calcule par nombre de points ')
    plt.savefig('resultats/Graphe_de_temps_de_calcule_par_nombre_de_points.pdf')
