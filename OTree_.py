# import bibliotheque
import copy
import math
import os
import random
import sys

import matplotlib.patches as patches
import numpy as np
import PyQt5.QtGui
from graphviz import Digraph
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.raw.GLU import gluPerspective
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget

"""Constantes Globales d'ajustement de force"""
k = 1  # constante pour les forces de repultions
kr = 1  # constante pour les forces de attractions

dt = 0.15  # differentiel de temps



class Point3d:
    """
    :description: Cette fonction est le constructeur de la classe Point3d. Elle prend en entrée les coordonnées x, y,
    z, un label, une masse et une liste de voisins. Elle initialise les attributs de l'objet avec les valeurs
    fournies. 
    :param x: coordonnée x du point 
    :param y: coordonnée y du point 
    :param z: coordonnée z du point 
    :param label: label du point 
    :param mass: masse du point 
    :param voisins: liste des voisins du point
    """

    def __init__(self, x, y, z, label, mass, voisins):
        self.label = label
        self.x = x
        self.y = y
        self.z = z
        self.mass = mass
        self.neighbours = voisins

    def distance_to(self, other):
        """
                Calcule la distance entre l'objet courant et un autre point.
        """
        return ((other.x - self.x) ** 2 + (other.y - self.y) ** 2 + (other.z - self.z) ** 2) ** 0.5



class Node3d:
    """
    :description: Cette fonction est le constructeur de la classe Node3d. Elle prend en entrée les coordonnées x0,
    y0, z0, la largeur w, la hauteur h, la profondeur d et une liste de points. Elle initialise les propriétés x0,
    y0, z0, width, height, depth, points, children, mass et leaf à leurs valeurs respectives. 
    :param x0 : coordonnée x du point central de ce noeud 
    :param y0 : coordonnée y du point central de ce noeud 
    :paramz0 : coordonnée z du point central 
    :param de ce noeud w : largeur de ce noeud 
    :param h : hauteur de ce noeud 
    :param d : profondeur de ce noeud 
    :param points : liste des points contenus dans ce noeud 
    :return: None
    """

    def __init__(self, x0, y0, z0, w, h, d, points):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.width = w
        self.height = h
        self.depth = d
        self.points = points
        self.children = []
        self.mass = 0
        self.leaf = True

    def get_width(self):
        """
                Retourne la largeur du noeud.
        """
        return self.width

    def get_height(self):
        """
                Retourne la hauteur du noeud.
        """
        return self.height

    def get_depth(self):
        """
                Retourne la profondeur du noeud.
        """
        return self.depth

    def get_points(self):
        """
                Retourne les points contenus dans le noeud.
        """
        return self.points



class OTree:
    """
    :description: Cette fonction est utilisée pour initialiser un objet OTree. Elle prend en entrée un seuil k et un
    nombre n de points. 
    :param: k: le seuil qui détermine la limite de subdivisions de l'octree. 
    :param: n: le nombre de points dans l'octree. 
    :return: un objet OTree avec k comme seuil et n points générés aléatoirement dans l'espace.
    """

    def __init__(self, k, n):
        self.threshold = k
        self.points = [
            Point3d(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), '', 1, []) for x in
            range(n)]
        self.root = Node3d(0, 0, 0, 1, 1, 1, self.points)

    def add_point(self, x, y, z, mass, neighbours):
        """
                Ajoute un point à l'arbre avec les coordonnées x, y, z, la masse et les voisins.
        """
        self.points.append(Point3d(x, y, z, '', mass, neighbours))

    def get_points(self):
        """
                Retourne tous les points de l'arbre.
        """
        return self.points

    def subdivide3d(self):
        """
                Effectue une subdivision récursive de l'arbre en utilisant le seuil donné.
        """
        recursive_subdivide3d(self.root, self.threshold)


# O(n)
def contains(x, y, z, w, h, d, points):
    """
        :description: Cette fonction prend en entrée les coordonnées x, y, z, la largeur w, la hauteur h, la profondeur d et une liste de points.
        Elle retourne une liste de 8 sous-listes de points qui se trouvent dans chacune des 8 zones définies par les coordonnées x, y, z, w, h et d.
        :param: x: coordonnée x de la zone
        :param: y: coordonnée y de la zone
        :param: z: coordonnée z de la zone
        :param: w: largeur de la zone
        :param: h: hauteur de la zone
        :param: d: profondeur de la zone
        :param: points: liste de points
        :return: (pts1, pts2, pts3, pts4, pts5, pts6, pts7, pts8) : une liste de 8 sous-listes de points qui se trouvent dans chacune des 8 zones.
    """
    pts1 = []
    pts2 = []
    pts3 = []
    pts4 = []
    pts5 = []
    pts6 = []
    pts7 = []
    pts8 = []
    for point in points:
        if point.x <= x and point.y > y and point.z > z:
            pts1.append(point)
        elif point.x > x and point.y > y and point.z > z:
            pts2.append(point)
        elif point.x <= x and point.y <= y and point.z > z:
            pts3.append(point)
        elif point.x > x and point.y <= y and point.z > z:
            pts4.append(point)
        elif point.x <= x and point.y > y and point.z <= z:
            pts5.append(point)
        elif point.x > x and point.y > y and point.z <= z:
            pts6.append(point)
        elif point.x <= x and point.y <= y and point.z <= z:
            pts7.append(point)
        else:
            pts8.append(point)
    return (pts1, pts2, pts3, pts4, pts5, pts6, pts7, pts8)


# O(n log n)
def recursive_subdivide3d(node, S):
    """
        Cette fonction subdivise récursivement un noeud d'octree 3D en 8 sous-noeuds en utilisant le seuil k.
        :param node: Le noeud de l'octree que l'on souhaite subdiviser
        :param S: Le seuil à partir duquel on subdivise le noeud
        :return: Si le nombre de points dans le noeud est inférieur ou égal à k, la fonction s'arrête.
                Sinon, elle subdivise le noeud en 8 sous-noeuds et met à jour la liste des enfants de l'objet node pour inclure les 8 sous-noeuds créés.
    """
    if len(node.points) <= S:
        return
    node.leaf = False
    w_ = float(node.width / 2)
    h_ = float(node.height / 2)
    d_ = float(node.depth / 2)
    # appelle la fonction contains3d pour déterminer les points contenus dans chaque sous-noeud
    p1, p2, p3, p4, p5, p6, p7, p8 = contains(node.x0, node.y0, node.z0, w_, h_, d_, node.points)

    x1 = Node3d(node.x0 - w_ / 2, node.y0 + h_ / 2, node.z0 + d_ / 2, w_, h_, d_, p1)
    recursive_subdivide3d(x1, S)

    x2 = Node3d(node.x0 + w_ / 2, node.y0 + h_ / 2, node.z0 + d_ / 2, w_, h_, d_, p2)
    recursive_subdivide3d(x2, S)

    x3 = Node3d(node.x0 - w_ / 2, node.y0 - h_ / 2, node.z0 + d_ / 2, w_, h_, d_, p3)
    recursive_subdivide3d(x3, S)

    x4 = Node3d(node.x0 + w_ / 2, node.y0 - h_ / 2, node.z0 + d_, w_, h_, d_, p4)
    recursive_subdivide3d(x4, S)

    x5 = Node3d(node.x0 - w_ / 2, node.y0 + h_ / 2, node.z0 - d_ / 2, w_, h_, d_, p5)
    recursive_subdivide3d(x5, S)

    x6 = Node3d(node.x0 + w_ / 2, node.y0 + h_ / 2, node.z0 - d_ / 2, w_, h_, d_, p6)
    recursive_subdivide3d(x6, S)

    x7 = Node3d(node.x0 - w_ / 2, node.y0 - h_ / 2, node.z0 - d_ / 2, w_, h_, d_, p7)
    recursive_subdivide3d(x7, S)

    x8 = Node3d(node.x0 + w_ / 2, node.y0 - h_ / 2, node.z0 - d_ / 2, w_, h_, d_, p8)
    recursive_subdivide3d(x8, S)
    """la liste des enfants de l'objet node est mise à jour pour inclure les 8 sous-noeuds créés."""
    node.children = [x1, x2, x3, x4, x5, x6, x7, x8]


# O(n)
def init_dot(file_name, S):
    """
    :description: Cette fonction prend en entrée un nom de fichier, qui contient des informations sur des noeuds et
    des arêtes d'un graphe. Elle ouvre ce fichier, lit les lignes, sépare les lignes qui décrivent les arêtes des
    lignes qui décrivent les noeuds, et enregistre ces informations dans des listes distinctes. Ensuite,
    elle parcourt ces listes pour créer un dictionnaire qui associe à chaque noeud un label. Puis elle crée un arbre
    octree avec nombre de noeuds et pour chaque noeud, elle ajoute le label correspondant. Enfin, elle parcourt ces
    listes pour ajouter des arêtes entre les noeuds.

    :param file_name: nom de fichier
    :param S: nombre de noeuds
    :return: l'octree et deux listes
    """
    with open(file_name, 'r') as file:
        lines = file.readlines()
    nodes = []
    edges = []
    for line in lines:
        if '--' in line:
            edges.append(line.strip().split('--'))
        elif '[' in line:
            nodes.append(line.strip())
    list1 = []
    list2 = []
    for l in edges:
        list1.append(l[0].replace(' ', ''))
        list2.append(l[1].replace(' ', ''))
    point_dict = {}
    for node in nodes:
        dict = node.split(' ')[0]
        value_dict = node.split('"')[1]
        point_dict[dict.replace(' ', '')] = value_dict.replace(' ', '')
    my_octree = OTree(S, len(nodes))
    for i, e in enumerate(my_octree.root.points):
        e.label = list(point_dict.keys())[i]
    for l1, l2 in zip(list1, list2):
        my_octree = assigner_des_voisins(my_octree, l1, l2)

    return my_octree, list1, list2


# O(n)
def assigner_des_voisins(octree, l1, l2):
    """
    Assigne des voisins à deux points dans un octree en fonction de leurs étiquettes.

    :param octree: une instance de la classe OTree
    :param l1: la première étiquette à rechercher
    :param l2: la deuxième étiquette à rechercher
    :return: l'instance d'octree modifiée, O

    La fonction recherche les points dans l'octree qui ont les étiquettes spécifiées,
    et ajoute l'un des points à la liste des voisins de l'autre point et vice versa.
    """
    for e in octree.root.points:
        if e.label == l1:
            break
    for e2 in octree.root.points:
        if e2.label == l2:
            break
    e.neighbours.append(e2)
    e2.neighbours.append(e)
    return octree


# clacule des forces
#O(1)
def acceleration(f, m):
    """
    :description: Cette fonction peut être utilisée pour déterminer l'accélération d'un objet en fonction de la force qui lui est appliquée et de sa masse.
    :param f: la force
    :param m: la masse
    :return: l'accélération en utilisant la formule de base accélération = force / masse.
    """
    return f / m


# calculer la vélocité
# O(1)
def velocite(v_old, delta_time, acc):
    """
        :description: Cette fonction permet de calculer la vitesse courante en utilisant la vitesse précédente, le temps écoulé (delta_time) et l'accélération.
        :param v_old: la vitesse précédente
        :param delta_time: le temps écoulé depuis la dernière mise à jour de la vitesse
        :param acc: l'accélération
        :return: la nouvelle vitesse courante en utilisant la formule vitesse = vitesse précédente + accélération * delta_time + (1/2) * accélération * delta_time^2
    """
    return v_old + acc * delta_time + (1 / 2) * acc


# O(1)
def position(old_pos, velocite_, delta_time):
    """
    :description: Cette fonction calcule la nouvelle position d'un point en utilisant sa position précédente, sa vitesse et le temps écoulé.
    :param old_pos: la position précédente du point sous forme d'un tuple (x, y, z)
    :param velocite_: la vitesse du point
    :param delta_time: le temps écoulé depuis la dernière mise à jour de la position
    :return: la nouvelle position du point sous forme d'un tuple (x, y, z)
    """
    x = old_pos.x + (velocite_ * delta_time)
    y = old_pos.y + (velocite_ * delta_time)
    z = old_pos.z + (velocite_ * delta_time)

    return (x, y, z)


# Complexite < n²
def rep_force(node, point):
    """
    :description: Cette fonction calcule la force de répulsion entre un point et un noeud d'octree.
    :param: node: un noeud d'octree
    :param: point: un point
    :return: La force de répulsion entre le point et le noeud d'octree
    """
    if node.leaf:  # or point.distance_to(Point('',node.x0,node.y0,1,[])) > 1.5:
        res = 0
        pts = node.points

        if pts == []:
            return 0
        elif len(pts) == 1 and pts[0] == point:
            return 0
        else:
            gc_x, gc_y, gc_z, gc_mass = 0, 0, 0, 0
            for p in pts:
                gc_x += p.x
                gc_y += p.y
                gc_z += p.z
                gc_mass += p.mass
            gc_point = Point3d(gc_x / len(pts), gc_y / len(pts), gc_z / len(pts), '', gc_mass / len(pts), [])
            return k / point.distance_to(gc_point)
    else:
        val = 0
        for e in node.children:
            val = val + rep_force(e, point)
        return k / val


# O(n²) uniquement dans le cas d'un graphe complet
def att_force(point):
    """
    :description: Cette fonction calcule la force d'attraction entre un point et ses voisins.
    :param point: Le point pour lequel on calcule la force d'attraction.
    :return: La force d'attraction totale entre le point et ses voisins.
    """
    res = 0
    for e in point.neighbours:
        res += point.distance_to(e)
    return -kr * res


# Complexite < n²
def list_forces_rep(root):
    """
    :description: Cette fonction prend en entrée la racine de l'octree.
                Elle parcourt chaque point de l'octree pour calculer la force de répulsion entre ce point et les autres points de l'octree.
    :param root: La racine de l'octree.
    :return: La liste des forces de répulsion de chaque point de l'octree.
    """
    rep_forces = []
    for e in root.points:
        rep_forces.append(rep_force(root, e))
    return np.array(rep_forces)


# Complexite < n²
def list_forces_att(root):
    """
    :description: Cette fonction prend en paramètre un noeud de l'Octree appelé "root" et retourne une liste de forces d'attraction pour chaque point contenu dans ce noeud.
    :param root: noeud de Octree
    :return: liste de forces d'attraction pour chaque point contenu dans le noeud "root"
    """
    att_forces = []
    for e in root.points:
        att_forces.append(att_force(e))
    return np.array(att_forces)


# O(n)
def new_positions(forces, root, vitess, dt_):
    """
    :description: Cette fonction prend en paramètre les forces, un noeud de l'Octree appelé "root", les vitesses et
    le temps "dt" et retourne les nouvelles positions des points contenus dans ce noeud. Elle utilise une boucle pour
    itérer sur chaque point dans "root.points" et utilise des fonctions pour calculer la nouvelle accélération,
    vitesse, et position pour chaque point. Les nouveaux points sont ensuite ajoutés à une liste "new_points" et les
    nouvelles vitesses sont retournées. 
    :param forces: les forces appliquées sur chaque point 
    :param root: noeud de Octree 
    :param vitess: les vitesses actuelles de chaque point 
    :param dt_: le temps pour lequel les calculs sont effectués 
    :return: nouvelles positions des points contenus dans le noeud "root" et les nouvelles vitesses
    """
    acc = acceleration(forces, root.points[0].mass)
    new_points = []
    for i, p in enumerate(root.points):
        vitess[i] = velocite(vitess[i], dt_, acc[i])
        x, y, z = position(p, vitess[i], dt_)

        new_points.append(Point3d(x, y, z, p.label, p.mass, p.neighbours))
    return new_points, vitess


class GLWidget(QOpenGLWidget):
    """
    :description: Cette classe hérite de QOpenGLWidget, elle prend en paramètre un Octree et initialise un widget OpenGL pour afficher les points de l'Octree.
        Elle a une variable d'angle qui est utilisée pour faire tourner les points affichés, un timer qui est utilisé pour mettre à jour l'affichage,
        et une variable "octree" qui contient l'Octree à afficher.

    Les méthodes "initializeGL", "paintGL" sont utilisées pour initialiser et peindre l'affichage OpenGL.

    :param octree: objet Octree à afficher
    :return: Affiche les points de l'Octree dans un widget OpenGL tournant
    """

    def __init__(self, octree):
        super().__init__()  # call the __init__ method of the superclass
        self.octree = octree
        self.angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def initializeGL(self):
        """
        :description: Cette méthode est utilisée pour initialiser l'affichage OpenGL. Elle définit la couleur de
        fond, active les tests de profondeur, configure la matrice de projection pour une projection en perspective,
        réinitialise la matrice de vue, et définit la taille de la fenêtre d'affichage. :return: Initialise les
        options d'affichage pour le widget OpenGL
        """
        glClearColor(1.0, 1.0, 1.0, 1.0)  # set clear color to white
        glEnable(GL_DEPTH_TEST)  # enable depth testing
        glMatrixMode(GL_PROJECTION)  # set the projection matrix
        glLoadIdentity()  # reset the projection matrix
        gluPerspective(45, 1, 0.1, 100)  # set up a perspective projection
        glMatrixMode(GL_MODELVIEW)  # set the modelview matrix
        glLoadIdentity()  # reset the modelview matrix
        glViewport(0, 0, 800, 600)  # set the viewport

    def paintGL(self):
        """
        :description: Cette méthode est utilisée pour peindre l'affichage OpenGL. Elle efface les buffers de couleur
        et de profondeur, réinitialise la matrice de vue, déplace la caméra loin de l'origine, fait tourner les
        points affichés en utilisant la variable d'angle, appelle les fonctions pour dessiner le cube de l'Octree et
        les points, incrémente la variable d'angle pour la prochaine frame et vérifie si elle dépasse 360 pour la
        remettre à zéro. :return: Affiche les points de l'Octree dans un widget OpenGL tournant
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clear the color and depth buffer
        glLoadIdentity()  # reset the modelview matrix
        glTranslatef(0, 0, -5)  # move the camera away from the origin
        glRotatef(self.angle, 1, 1, 1)  # rotate the cube around the x, y, and z axes
        draw_cube(self.octree.root)
        scatter_points(self.octree)
        self.angle += 1  # increment the angle for the next frame
        if self.angle >= 360:  # reset the angle if it exceeds 360
            self.angle = 0


# O(1)
def draw_cube(node):
    """
    :description: Cette fonction dessine un cube en utilisant les fonctions de la bibliothèque OpenGL.
    Elle utilise les coordonnées et les dimensions d'un noeud de l'Octree pour définir les sommets du cube.
    Elle utilise également les fonctions de la bibliothèque OpenGL pour dessiner les lignes du cube en mode fil de fer,
    définir la couleur des lignes en noir, et réinitialiser les buffers de couleur et de profondeur.
    :param node: noeud de Octree dont les coordonnées et dimensions sont utilisées pour définir les sommets du cube
    :return: Dessine un cube représentant le noeud de l'Octree dans un widget OpenGL
    """
    x, y, z = node.x0, node.y0, node.z0
    width, height, depth = node.width, node.height, node.depth
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # Passez à GL_LINE pour dessiner le wireframe
    glLineWidth(2)  # augmenter la largeur des lignes
    glClearColor(1.0, 1.0, 1.0, 1.0)  # définir la couleur claire sur blanc
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # effacer le tampon(buffer) de couleur
    glColor3f(0, 0, 0)  # mettre la couleur des lignes en noir

    glBegin(GL_QUADS)
    glVertex3f(x + width, y - height, z + depth)
    glVertex3f(x + width, y + height, z + depth)
    glVertex3f(x - width, y + height, z + depth)
    glVertex3f(x - width, y - height, z + depth)

    glVertex3f(x + width, y - height, z - depth)
    glVertex3f(x + width, y + height, z - depth)
    glVertex3f(x - width, y + height, z - depth)
    glVertex3f(x - width, y - height, z - depth)

    glVertex3f(x + width, y + height, z + depth)
    glVertex3f(x + width, y + height, z - depth)
    glVertex3f(x - width, y + height, z - depth)
    glVertex3f(x - width, y + height, z + depth)

    glVertex3f(x + width, y - height, z + depth)
    glVertex3f(x + width, y - height, z - depth)
    glVertex3f(x - width, y - height, z - depth)
    glVertex3f(x - width, y - height, z + depth)

    glVertex3f(x - width, y + height, z + depth)
    glVertex3f(x - width, y - height, z + depth)
    glVertex3f(x - width, y - height, z - depth)
    glVertex3f(x - width, y + height, z - depth)

    glVertex3f(x + width, y - height, z + depth)
    glVertex3f(x + width, y + height, z + depth)
    glVertex3f(x + width, y + height, z - depth)
    glVertex3f(x + width, y - height, z - depth)
    glEnd()


# O(n²) uniquement dans le cas d'un graphe complet
def scatter_points(octree):
    """
    :description: Cette fonction permet de tracer des points en 3D en utilisant la bibliothèque OpenGL.
    Elle prend en paramètre un objet Octree, définit la taille et la couleur des points à tracer,
    puis utilise les fonctions de OpenGL pour tracer un point pour chaque point de l'octree à des coordonnées (x, y, z) spécifiques,
    et pour chaque voisin d'un point tracer une ligne entre le point et son voisin.
    :param octree: objet Octree contenant les points à tracer
    :return: Trace des points et des lignes entre voisins dans un widget OpenGL
    """
    glPointSize(5.0)  # définir la taille des points
    for point in octree.root.points:
        glBegin(GL_POINTS)
        glColor3f(abs(point.x), abs(point.y), abs(point.z))  # définir la couleur des points différemment
        glVertex3f(point.x, point.y, point.z)
        glEnd()
        for neighbor in point.neighbours:
            glBegin(GL_LINES)
            glVertex3f(point.x, point.y, point.z)
            glVertex3f(neighbor.x, neighbor.y, neighbor.z)
            glEnd()
