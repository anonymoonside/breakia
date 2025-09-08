import pygame

class SimpleAI():
    #Créer une class pour le paddle avec la fonction sprite de pygame

    def __init__(self):
        #Appelle init qui construit notre objet
        self.aDejaPrevu = False   # état interne de l'IA
        self.xPredit = None 
        
    #Projeter la trajectoire de la  balle pour prédire sa  fin en x
    def projection(self, ballex, balley, velox, veloy, paddley):
        #Declarer des variables locales qui prennent les positions et la vitesse de balle pour les modifier localement
        x = ballex
        y = balley
        v0 = velox
        v1 = veloy
        py = paddley
        #Calculer la trajectoire en imitant simplment le mouvement de la balle
        while y < py:
            x += v0
            y += v1
            if x <= 0 or x >= 800:  #Si la balle touche un des murs
                v0 *= -1  #Inverse la vitesse
        return x
            
