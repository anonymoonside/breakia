import pygame
from random import randint
NOIR = (0, 0, 0)

class Balle(pygame.sprite.Sprite):
    #Créer une class pour la balle avec la fonction sprite de pygame

    def __init__(self, couleur, longueur, hauteur):
        #Appelle init qui construit notre objet
        super().__init__()

        #Afficher une surface pour la balle et la remplir (ok c'est un peu carré pour une balle)
        self.image = pygame.Surface([longueur, hauteur], pygame.SRCALPHA)  # Surface transparente
        pygame.draw.rect(self.image, couleur, [0, 0, longueur, hauteur])   # Remplissage

        #Initialiser la vitesse de la balle
        self.velocity = [randint(4,8),randint(-8,8)]

        #Récupérer le Rect correspondant à l’image et qui servira à gérer sa position
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
    
    def rebond(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8,8)