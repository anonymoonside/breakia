import pygame   #Importe la bibliothèque pygame pour créer le jeu et l'initialiser
from paddle import Paddle   #Importe la class Paddle dans paddle.py
from balle import Balle   #Importe la class Balle dans balle.py
from mur import Mur   #Importe la class Mur dans mur.py

#Définir les couleurs à utiliser
BLANC = (255,255,255)
NOIR = (0, 0, 0)
BLEUFONCE = (36 ,90 ,140)
BLEU = (0, 190, 242)
ROUGE = (204, 53, 53)
VERT = (80, 162, 45)
VIOLET = (156, 60, 185)
ORANGE = (255, 150, 31)
JAUNE = (245, 210, 10)

#Fonction principale
def main():
    
    pygame.init()   #Initialise le jeu pygame

    #Variables de vies, score et enCours pour la boucle princiaple
    vies = 3
    score = 0
    enCours  = True

    #Initialiser le paddle et ses caractéristiques
    paddle = Paddle(BLEU, 100, 20)
    paddle.rect.x = 350
    paddle.rect.y = 560

    ##Initialiser la balle et ses caractéristiques
    balle = Balle(BLANC, 15, 15)
    balle.rect.x = 345
    balle.rect.y = 300
    #Créer une liste qui contiendra tout les sprites du jeu
    sprites_liste = pygame.sprite.Group()

    #Ajouter les sprites seuls à la liste des sprites
    sprites_liste.add(paddle)
    sprites_liste.add(balle)

    #Créer 3 lignes de briques et les ajouter au groupe mur_briques pour créer un mur
    mur_briques = pygame.sprite.Group()
    for i in range(10):
        brique = Mur(VIOLET,80,30)
        brique.rect.x = i* 80
        brique.rect.y = 70
        sprites_liste.add(brique)
        mur_briques.add(brique)
    for i in range(10):
        brique = Mur(ROUGE,80,30)
        brique.rect.x = i* 80
        brique.rect.y = 100
        sprites_liste.add(brique)
        mur_briques.add(brique)
    for i in range(10):
        brique = Mur(ORANGE,80,30)
        brique.rect.x = i* 80
        brique.rect.y = 130
        sprites_liste.add(brique)
        mur_briques.add(brique)
    for i in range(10):
        brique = Mur(JAUNE,80,30)
        brique.rect.x = i* 80
        brique.rect.y = 160
        sprites_liste.add(brique)
        mur_briques.add(brique)



    #Réglages de la fenêtre
    tailleEcran = (800, 600)
    ecran = pygame.display.set_mode(tailleEcran)
    pygame.display.set_caption("BreakIA")

    #L'horloge pour contrôler la fréquence de rafraichissement
    horloge = pygame.time.Clock()

    #Boucle principale
    while enCours:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                enCours = False
                #Mode pause quand on appuye sur ECHAP
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                while True: #Boucle infinie tant qu'on appuye pas sur ESC
                    event = pygame.event.wait()
                    police = pygame.font.Font("C:/Users/alexw/Desktop/Code/Python/Projet_BreakAI/ressources/font/dogica.otf", 64)
                    texte = police.render("PAUSE", 1, BLANC)
                    ecran.blit(texte, (248,300))
                    pygame.display.flip()
                    if event.type == pygame.QUIT:
                        enCours = False
                        break
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        break #Retourner au jeu

        #Bouger le paddle selon la touche
        touche = pygame.key.get_pressed()
        if touche[pygame.K_LEFT] or touche[pygame.K_q]:   #Gauche
            paddle.bougerGauche(7)
        if touche[pygame.K_RIGHT] or touche[pygame.K_d]:  #Droite
            paddle.bougerDroite(7) 
        
        #Updater les différents sprites chaque frame
        sprites_liste.update()

        if balle.rect.x >= 790:
            balle.velocity[0] = -balle.velocity[0]
        if balle.rect.x <= 0:
            balle.velocity[0] = -balle.velocity[0]
        if balle.rect.y <= 40:
            balle.velocity[1] = -balle.velocity[1]
        if balle.rect.y >= 595: #Mur du bas
            balle.velocity[1] = -balle.velocity[1]
            vies -= 1   #Quand la balle tombe en dessous du paddle, on perd une vie
            if vies == 0:   #S'il n'y a plus de vies, on perd
                #Message Game Over
                police = pygame.font.Font("C:/Users/alexw/Desktop/Code/Python/Projet_BreakAI/ressources/font/dogica.otf", 64)
                texte = police.render("GAME OVER", 1, BLANC)
                ecran.blit(texte, (120,300))
                pygame.display.flip()
                pygame.time.wait(3000)
                #Ferme le jeu après défaite
                main()
                return

        #Gérer la collision balle paddle, et faire rebondir la balle
        if pygame.sprite.collide_mask(balle, paddle):
            balle.rect.x -= balle.velocity[0]
            balle.rect.y -= balle.velocity[1]
            balle.rebond()

        #Gérer la collision balle brique, et faire rebondir et disparaître une brique
        collision_briques = pygame.sprite.spritecollide(balle, mur_briques, False) #Liste de tout les sprites qui entrent en collision avec la balle
        for brique in collision_briques:
            balle.rect.x -= balle.velocity[0]
            balle.rect.y -= balle.velocity[1]
            balle.rebond()
            score += 1  #Augmenter le score quand une brique est touchée
            pygame.time.wait(10)
            brique.kill()
            if len(mur_briques)==0: #S'il n'y a plus de briques on gagne et on ferme le jeu
            #Afficher un message gg
                police = pygame.font.Font("C:/Users/alexw/Desktop/Code/Python/Projet_BreakAI/ressources/font/dogica.otf", 64)
                texte = police.render("BRAVO GG!", 1, BLANC)
                pygame.time.wait(25)
                ecran.blit(texte, (120,300))
                pygame.display.flip()
                pygame.time.wait(1500)
                #Fermer le jeu
                main()
                return

        #Eviter que la balle reste coincée à l'horizontale
        if balle.velocity[1] == 0:
            balle.velocity[1] += 5
            print("La balle est restée bloquée à l'horizontale")

        if balle.rect.centerx > paddle.rect.centerx:
            paddle.bougerDroite(7)
        if balle.rect.centerx < paddle.rect.centerx:
            paddle.bougerGauche(7)

        #Code d'affichage des éléments
        #Mettre une couleur à l'écran
        ecran.fill(BLEUFONCE)
        pygame.draw.line(ecran, BLANC, [0, 40], [800, 40], 2)

        #Afficher le score et les vies en haut de l'écran
        police = pygame.font.Font("C:/Users/alexw/Desktop/Code/Python/Projet_BreakAI/ressources/font/dogica.otf", 32)  #Choisir une police
        texte = police.render("Score: " + str(score), 0, BLANC)
        ecran.blit(texte, (25,9))
        texte = police.render("Vies: " + str(vies), 0, BLANC)
        ecran.blit(texte, (550,9))

        #Afficher tout les sprites à l'écran avec cette ligne
        sprites_liste.draw(ecran)
    
        #Afficher à l'écran ce qu'on vient de définir en haut
        pygame.display.flip()
        
        #Limite à 60 fps
        horloge.tick(60)
    
    pygame.quit

#Lancer le jeu seulement si le fichier est exécuté directement
if __name__ == "__main__":
    main()




