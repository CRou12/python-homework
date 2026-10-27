"""T1 – Snake procédural : le code de départ (étape 1).

D'après le TP « Snake » de Thierry Parmentelat et Aurélien Noce
(github.com/flotpython/exos-python), réécrit pour le cours AP Python.

Lancez-le avec :  uv run snake.py
Testez-le avec :  uv run pytest
"""

from random import randint

import pygame as pg


# Le plateau : X × Y cases de W × H pixels (étape 3).
X, Y = 30, 30
W, H = 20, 20

UP, DOWN, LEFT, RIGHT = (0, -1), (0, +1), (-1, 0), (+1, 0)


# --- logique du jeu : aucune fonction ici ne dessine -------------------------
# Ces fonctions sont vérifiées par les tests (tests/test_snake.py) :
# gardez leur nom et leurs paramètres.


def in_scope(tile):
    """Vrai si la case `tile` = (x, y) est sur le plateau."""
    raise NotImplementedError("étape 5")


def next_head(snake, direction):
    """La case où arrive la tête (le dernier élément de `snake`)."""
    raise NotImplementedError("étape 5")


def turn(direction, key):
    """La nouvelle direction après l'appui sur la touche `key` (ex. pg.K_UP)."""
    raise NotImplementedError("étape 6")


def move(snake, direction, fruit):
    """Avance le serpent d'une case, en modifiant la liste `snake` sur place.

    Renvoie ce qui s'est passé : "ate", "moved", "self-bite" ou "out-of-board".
    """
    raise NotImplementedError("étapes 5, 7 et 8")


def random_fruit(snake):
    """Une case libre du plateau, tirée au hasard."""
    raise NotImplementedError("étape 7")


# --- la boucle de jeu --------------------------------------------------------
def draw_tile(screen, tile, color):
    x, y = tile
    rect = pg.Rect(x*W, y*H, W, H)
    pg.draw.rect(screen, color, rect)

def draw(screen, snake):
    for x in range(X):
        for y in range(Y):
            if (x+y)%2==1:
                draw_tile(screen, (x,y), (200,200,200))
            else:
                draw_tile(screen, (x,y), (255,255,255))
    
    for tile in snake:
        draw_tile(screen, tile, (50,255,100))

def main():
    running = True
    pg.init()
    screen = pg.display.set_mode((X*W, Y*H))
    clock = pg.time.Clock()

    while running:
        # au plus 1 image par seconde
        clock.tick(1)

        # 1. les événements : il faut les lire, sinon la fenêtre ne répond pas
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
                running = False
            pass
        
        # 2. l'état (rien pour l'instant)

        # 3. l'affichage : on prépare l'image en mémoire...
        #screen.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
        snake = [(10, 15), (11, 15), (12, 15)]
        draw(screen, snake)

        # ... puis on l'envoie à l'écran, une seule fois par tour de boucle
        pg.display.update()
    pg.quit()



# Ce bloc ne s'exécute que si l'on lance ce fichier (uv run snake.py),
# pas quand un autre fichier fait `import snake` (les tests, par ex.).
if __name__ == "__main__":
    main()
