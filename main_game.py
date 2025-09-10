import pygame   #Importe la bibliothèque pygame pour créer le jeu et l'initialiser
import numpy as np  #Importe numpy en tant que np
import random   #Importe random pour générer des nombres aléatoires
import os   #Importe pour sauvegarder l'état de mon IA
from paddle import Paddle   #Importe la class Paddle dans paddle.py
from balle import Balle   #Importe la class Balle dans balle.py
from mur import Mur   #Importe la class Mur dans mur.py
from simple_ai import SimpleAI  #Importe la class SimpleAI dans simple_ai.py

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

#Dimensions écran
screen_width = 800
screen_height = 600


#Actions possibles par l'IA
actions = ['GAUCHE', 'DROITE', 'RIEN']

# Q-learning avec états simplifiés
#Discrétiser pour l'IA
nb_pos_paddle = 10   #10 si c'est pas assez car reduit le nombre d'états possible
nb_pos_x_balle = 12  #12 pareil
nb_pos_y_balle = 12  #12 pareil
nb_vx = 2   # gauche/0/droite
nb_vy = 2   # haut/0/bas

# Q-learning avec états simplifiés
Q = np.zeros((nb_pos_paddle,
              nb_pos_x_balle,
              nb_pos_y_balle,
              nb_vx, 
              nb_vy,
              len(actions)))

alpha = 0.1
gamma = 0.95

if os.path.exists("C:/Users/alexw/Desktop/Code/Python/Projet_BreakAI/scores/Q_table.npy"):
    Q = np.load("C:/Users/alexw/Desktop/Code/Python/Projet_BreakAI/scores/Q_table.npy")
    print("Q-table chargée depuis le fichier.")
else:
    Q = np.zeros((nb_pos_paddle,
                  nb_pos_x_balle,
                  nb_pos_y_balle,
                  nb_vx, 
                  nb_vy,
                  len(actions)))
    print("Nouvelle Q-table créée.")

#Reduire la taille de l'écran pour moins de possibilités
def get_state(balle, paddle, screen_width, screen_height):
    x = int(balle.rect.x / (screen_width / nb_pos_x_balle))
    y = int(balle.rect.y / (screen_height / nb_pos_y_balle))
    vx = 0 if balle.velocity[0] < 0 else 1
    vy = 0 if balle.velocity[1] < 0 else 1
    r = int(paddle.rect.x / (screen_width / nb_pos_paddle))

    #Eviter les dépassements
    x = min(nb_pos_x_balle - 1, x)
    y = min(nb_pos_y_balle - 1, y)
    r = min(nb_pos_paddle - 1, r)

    return (r, x, y, vx, vy)

#Choisir une action
def choose_action(state, epsilon):
    if random.uniform(0,1) < epsilon:
        return random.choice(actions)
    else:
        action_index = np.argmax(Q[state + (slice(None),)])
        return actions[action_index]

#Mise à jour Q-learning
def update_Q(state, action, reward, next_state):
    action_index = actions.index(action)
    old_value = Q[state + (action_index,)]
    next_max = np.max(Q[next_state + (slice(None),)])
    #Formule du Q Learning sur la Q table
    Q[state + (action_index,)] = np.clip((1 - alpha) * old_value + alpha * (reward + gamma * next_max), -50, 50) #Bornes à la fin



#Fonction principale
def run_game(total_games):

    vies = 3
    score = 0
    game_speed = 10000000  # vitesse par défaut
    perdreVies = False
    
    enCours  = True
    pygame.init()   #Initialise le jeu pygame

    #Initialiser le paddle et ses caractéristiques
    paddle = Paddle(BLANC, 100, 20)
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

        reward = 0

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None  # signal pour arrêter complètement le programme
            
            #Mode basse vitesse (à corriger)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    # Toggle entre lent et rapide
                    if game_speed == 10000000:
                        game_speed = 60   # mode très lent
                    else:
                        game_speed = 10000000   # revenir à normal

            #Mode pause quand on appuye sur ECHAP
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                while True: #Boucle infinie tant qu'on appuye pas sur ESC
                    event = pygame.event.wait()
                    police = pygame.font.Font("C:/Users/alexw/Desktop/Code/Python/Projet_BreakAI/ressources/font/dogica.otf", 64)
                    texte = police.render("PAUSE", 1, BLANC)
                    ecran.blit(texte, (248,300))
                    pygame.display.flip()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return None  # signal pour arrêter complètement le programme
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        break #Retourner au jeu
                    
        
        #Updater les différents sprites chaque frame
        sprites_liste.update()

        if balle.rect.x >= 790:
            balle.velocity[0] = -balle.velocity[0]
        if balle.rect.x <= 10:
            balle.velocity[0] = -balle.velocity[0]
        if balle.rect.y <= 40:
            balle.velocity[1] = -balle.velocity[1]
        if balle.rect.y >= 599:  # Mur du bas
            vies -= 1
            perdreVies = True

            if vies > 0:
                # Réinitialiser la balle au centre de l’écran
                balle.rect.x = 345
                balle.rect.y = 300
                # Lui donner une nouvelle vitesse aléatoire comme au début
                balle.velocity = [random.choice([-4, 4]), random.choice([-4, 4])]
            else:
                return score  # Partie terminée quand plus de vies

        if len(mur_briques) == 0:
                reward += 10.0
                return score

        #Gérer la collision balle brique, et faire rebondir et disparaître une brique
        collision_briques = pygame.sprite.spritecollide(balle, mur_briques, False) #Liste de tout les sprites qui entrent en collision avec la balle
        for brique in collision_briques:
            reward += 0.3
            balle.rect.x -= balle.velocity[0]
            balle.rect.y -= balle.velocity[1]
            balle.rebond()
            score += 1  #Augmenter le score quand une brique est touchée
            brique.kill()


        if balle.velocity[1] == 0:
            balle.velocity[1] = random.choice([-1, 1])
        if balle.velocity[0] == 0:
            balle.velocity[0] = random.choice([-1, 1])


        #Code d'affichage des éléments
        #Mettre une couleur à l'écran
        ecran.fill(NOIR)
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
        

        # État courant
        state = get_state(balle, paddle, screen_width, screen_height)
        # epsilon décroissant pour plus d’exploitation
        epsilon = max(0.05, 0.995 ** total_games)
        action = choose_action(state, epsilon)


        if action == 'DROITE':
            direction = 'DROITE'
        elif action == 'RIEN':
            direction = 'RIEN'
        elif action == 'GAUCHE':
            direction = 'GAUCHE'

        #Déplacement de l'IA selon ce qu'elle choisis
        if direction == 'DROITE':
            paddle.rect.x += 7
        elif direction == 'GAUCHE':
            paddle.rect.x -= 7
        elif direction == 'RIEN':
            paddle.rect.x += 0

        #Eviter que le pad traverse l'écran dans les bordures
        if paddle.rect.x < 0:
            paddle.rect.x = 0
        if paddle.rect.x > screen_width - paddle.rect.width:
            paddle.rect.x = screen_width - paddle.rect.width

        #Variable de distance avec entre la balle et le pad en valeur absolue
        #dist = abs((paddle.rect.centerx) - (balle.rect.centerx))
        
        #Encourager à rester sous la balle
        #reward += (-dist / screen_width) * 0.1  # shaping plus léger

        #Gérer la collision balle paddle, et faire rebondir la balle
        if pygame.sprite.collide_mask(balle, paddle):
            balle.rect.x -= balle.velocity[0]
            balle.rect.y -= balle.velocity[1]
            balle.rebond()
            # Récompense pour toucher la balle
            reward += 0.7  #bonus immédiat

        #Perdre des points si on perd une vie
        if perdreVies:
            reward -= 1.0
            perdreVies = False


        #Définir le prochain état et mettre à jour la table Q
        next_state = get_state(balle, paddle, screen_width, screen_height)
        update_Q(state, action, reward, next_state)


        #Limite à "game_speed" fps
        pygame.display.update()
        horloge.tick(game_speed)
    pygame.quit


def main():
    total_games = 0
    while True:
        score = run_game(total_games)
        if score is None:   #Si la fenêtre a été fermée
            break
        print(f"Partie {total_games} terminée - Score: {score}")
        with open("C:/Users/alexw/Desktop/Code/Python/Projet_BreakAI/scores/scores.log", "a") as f:
            f.write(f"{total_games},{score}\n")
        total_games += 1    #+1 le nombre de parties totales

        if total_games % 50 == 0:  # toutes les 100 parties
            np.save("C:/Users/alexw/Desktop/Code/Python/Projet_BreakAI/scores/Q_table.npy", Q)
            print("Q-table sauvegardée !")

    pygame.quit()

#Lancer le jeu seulement si le fichier est exécuté directement
if __name__ == "__main__":
    main()