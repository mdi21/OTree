# Objectif du programme:
Réaliser une visualisation d'un graphe en 3D montrant les positions des sommets avant et après un certain lapse de temps(dt) en prenant 
en compte les forces exercées sur chaque point, en s'inspirant de l'algorithme "forceAtlas". 
Sauvegarder les complexités en temps de calculs de toutes les opérations (calcul des forces et des nouvelles positions) pour 
différents Octo-trees de tailles différentes (nombre de points) dans un fichier "calcule_complexite"
Sauvegarder les anciennes et nouvelles positions des sommets dans des fichier distincts nommés "calcule_nouvelles_position_H2O" et "calcule_nouvelles_position_benzene" (On a choisi ces deux fichier dot pour faire les tests)


## Packages à installer : 
                            -numpy
                            -random
                            -matplotlib
                            -graphviz
                            -PyOpenGL
                            -PyQt5
                            -time
                            -sys
                            -math
                            -os
                            
# Comment executer le code :
Il vous suffit de tapper ceci sur votre terminal:
							sh launch.sh
				
assurez vous de vous placer dans le meme répéroitre que -launsh.sh

# Diréctives pour une bonnes expérience d'éxecution:
    1. Quand le programme vous demande de faire un choix veuillez tapper le numéro du choix et non la chaîne de caractère
    2. Lors de l'affichage des fenêtres du graphe avant et après changement de position il se peut des celles-ci soient superposées,
       il vous suffira donc de les séparer afin de voir clairement les deux fenêtres 
    3. A la génération des fichier qui contiendront les resultats des tests et le graphe de complexité ils seront enregistrés dans le dossier "resultats" 
       veuillez ne pas changer son emplaçement pour garantir qu'aucune erreur de chemin ne survienne.


# IMPORTANT:
    .La visualisation des fichiers qui ont plus de 20 000 point prend beaucoup de temps. 
    .Les points sont générés aléatoirement donc les temps de calculs peuvent être très différents.
    .C'est possible que dans une éxécution une erreur de nombre maxiamal d'appel recursive apparait.  Il suffit donc de relancer le programme.

    .Preuve du fonctionnement du projet: screenshot dans le dossier preuve. Plus une version jupiter notebook simplifier du projet(sans la visualisation 3D).
