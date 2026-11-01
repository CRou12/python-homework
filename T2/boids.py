"""T2 – Boids : le code de départ (étape 0).

D'après le TP « boids » de Thierry Parmentelat (flotpython), réécrit pour le
cours AP Python et pour arcade 3.

Lancez-le avec :  uv run boids.py
Testez-le avec :  uv run pytest
"""

import math  #(servira à l'étape 2)
from pathlib import Path
from random import uniform  #(servira à l'étape 4)

import arcade

WIDTH, HEIGHT = 800, 800
BACKGROUND = arcade.color.BLUE

# Les images, cherchées à côté de ce fichier, d'où qu'on le lance.
HERE = Path(__file__).parent
ARROW = HERE / "media" / "arrow.png"
OBSTACLE = HERE / "media" / "obstacle.png"
SKY = HERE / "media" / "sea.jpg"  # le décor (étape 9)

SPEED = 100  # pixels par seconde (étape 2)
TURN_SPEED = 180  # degrés par seconde, tant qu'une flèche est enfoncée (étape 5)
NOISE = 3  # écart maximal du cap à chaque mise à jour, en degrés (étape 5)
N_BOIDS = 20  # (étape 4)
GRID = 10  # GRID × GRID obstacles (étape 6)
RADIUS = 30  # rayon de détection des voisins, en pixels (étapes 7 et 8)


# --- les objets du jeu -------------------------------------------------------
# Ces classes et fonctions sont vérifiées par les tests (tests/test_boids.py) :
# gardez leur nom et leurs paramètres.
#
# Chaque `raise NotImplementedError("étape …")` est un trou à remplir. S'il est
# atteint, le programme s'arrête net, avec ce message : il dit à quelle étape
# écrire ce morceau. Quand vous y arrivez, effacez la ligne et écrivez votre code.
# À l'étape 0, la fenêtre n'utilise encore aucune de ces classes : rien ne casse.


class Boid(arcade.Sprite):
    """Un oiseau : une flèche qui avance dans la direction où elle pointe."""

    def __init__(self, x, y, angle, speed=SPEED, others=None):
        super().__init__(ARROW, center_x=x, center_y=y, angle=angle)
        self.speed = speed
        self.turning = 0
        if others is None:
            self.others = []
        else: 
            self.others = others
        #raise NotImplementedError("étape 2 (et 7 pour others)")

    def update(self, delta_time=1 / 60, *args, **kwargs):
        """Appelée par arcade (via la SpriteList) à chaque mise à jour."""
        rad = math.radians(self.angle)
        self.center_x += self.speed * delta_time * math.cos(rad)
        self.center_x = self.center_x % 800
        self.center_y -= self.speed * delta_time * math.sin(rad)
        self.center_y = self.center_y % 800
        self.angle += self.turning*TURN_SPEED*delta_time
        self.angle += uniform(-NOISE,NOISE)
        dx, dy = self.separation(self.others)
        self.center_x += dx
        self.center_y += dy
        #raise NotImplementedError("étapes 2, 3, 5, 7 et 8")

    def neighbours(self, others, radius=RADIUS):
        """Les objets de `others` à moins de `radius` pixels, sauf soi-même."""
        l_neighbours = []
        for other in others:
            if math.dist(self.position, other.position)<=radius and other is not self:
                l_neighbours.append(other)
        return l_neighbours

    def separation(self, others, radius=RADIUS):
        """Le déplacement (dx, dy) qui écarte le boid de ses voisins."""
        dx, dy = 0, 0
        for other in self.neighbours(others) : 
            dx += (self.center_x-other.center_x)*(1/2)*(1-math.dist(self.position, other.position)/radius)
            dy += (self.center_y-other.center_y)*(1/2)*(1-math.dist(self.position, other.position)/radius)
        return((dx,dy))


class Obstacle(arcade.Sprite):
    """Un obstacle immobile."""

    def __init__(self, x, y):
        super().__init__(OBSTACLE, center_x=x, center_y=y)


def random_boids(n, others=None):
    """n boids placés et orientés au hasard, qui évitent tous `others`."""
    n_boids = []
    for i in range(n):
        x = uniform(0, WIDTH)
        y = uniform(0, HEIGHT)
        r = uniform(-180,180)
        n_boids.append(Boid(x,y,r,others=others))
    return n_boids


def obstacle_grid(n):
    """n × n obstacles régulièrement espacés, au centre de leur carré."""
    grid = []
    pas_x = WIDTH/n
    pas_y = HEIGHT/n
    x = pas_x/2
    for i in range(n):
        y = pas_y/2
        for j in range(n):
            grid.append(Obstacle(x,y))
            y += pas_y
        x += pas_x
    return grid


# --- la fenêtre ---------------------------------------------------------------


class MyWindow(arcade.Window):
    def __init__(self):
        # d'abord, ce que fait toute fenêtre d'arcade : s'ouvrir, en WIDTH × HEIGHT
        # pixels, avec « Boids » pour titre (super() : on y revient en séance)
        super().__init__(WIDTH, HEIGHT, "Boids")
        self.background_color = BACKGROUND  # la couleur que self.clear() étale

        # pour l'instant, un simple Sprite : une image posée en (100, 100),
        # comptés depuis le coin en bas à gauche
        boid = Boid(100, 100, -45)
        others = []
        
        # une SpriteList : une liste de sprites, qu'arcade dessine d'un coup
        self.obstacles = arcade.SpriteList()
        self.obstacles.extend(obstacle_grid(GRID))

        self.boids = arcade.SpriteList()
        self.boids.append(boid)
        self.boids.extend(random_boids(N_BOIDS,others=others))

        self.sky = arcade.SpriteList()
        self.sky.append(arcade.Sprite(SKY,center_x = WIDTH/2, center_y=HEIGHT/2, alpha=200))

        for boid in self.boids :
            others.append(boid)  # noqa: PERF402
        for obstacle in self.obstacles :
            others.append(obstacle)  # noqa: PERF402

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            for boid in self.boids:    
                boid.turning = -1

        elif symbol == arcade.key.RIGHT:
            for boid in self.boids:   
                boid.turning = 1   
        elif symbol == arcade.key.Q :
            self.close()

    def on_key_release(self, symbol, modifiers):
        for boid in self.boids:
            boid.turning = 0

    def on_update(self, delta_time):
        self.boids.update(delta_time)

    def on_draw(self):
        self.clear()
        self.sky.draw()
        self.obstacles.draw()
        self.boids.draw()

def main():
    MyWindow()
    arcade.run()


# Ce bloc ne s'exécute que si l'on lance ce fichier (uv run boids.py),
# pas quand un autre fichier fait `import boids` (les tests, par ex.).
if __name__ == "__main__":
    main()
