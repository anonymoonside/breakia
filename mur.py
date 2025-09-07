import pygame

class Mur(pygame.sprite.Sprite):
    #Créer une class pour le mur des briques avec la fonction sprite de pygame

    def __init__(self, couleur, longueur, hauteur):
        #Appelle init qui construit notre objet
        super().__init__()

        #Afficher le mur
        self.image = pygame.Surface([longueur, hauteur], pygame.SRCALPHA)  # Surface transparente
        pygame.draw.rect(self.image, couleur, [0, 0, longueur, hauteur])   # Remplissage

        #Récupérer le Rect correspondant à l’image et qui servira à gérer sa position
        self.rect = self.image.get_rect()