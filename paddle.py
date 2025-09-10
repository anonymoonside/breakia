import pygame

class Paddle(pygame.sprite.Sprite):
    #Créer une class pour le paddle avec la fonction sprite de pygame

    def __init__(self, couleur, longueur, hauteur):
        #Appelle init qui construit notre objet
        super().__init__()

        #Afficher le paddle
        self.image = pygame.Surface([longueur, hauteur], pygame.SRCALPHA)  # Surface transparente
        pygame.draw.rect(self.image, couleur, [0, 0, longueur, hauteur])   # Remplissage

        #Récupérer le Rect correspondant à l’image et qui servira à gérer sa position
        self.rect = self.image.get_rect()

    def bougerGauche(self, pixels):
        self.rect.x -= pixels
        #Verifier si on va pas trop loin
        if self.rect.x < 0:
          self.rect.x = 0
          
    def bougerDroite(self, pixels):
        self.rect.x += pixels
        #Verifier si on va pas trop loin
        if self.rect.x > 700:
          self.rect.x = 700

