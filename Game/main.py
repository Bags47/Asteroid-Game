import sys
import pygame
import pygame.font
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(high_score):
    with open("highscore.txt", "w") as file:
        file.write(str(high_score))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 36)
    score = 0
    high_score = load_high_score()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        player.activate_one_time_shield()
            
            updatable.update(dt)
            player.wrap(SCREEN_WIDTH, SCREEN_HEIGHT)            
                        
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    if player.shield_active:
                            player.shield_collision()
                            print("Shield absorbed the hit!")
                            asteroids.remove(asteroid)
                    else:
                        print("Game Over!")
                        raise SystemExit
             
            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        if asteroid.radius > 40:
                            score += 10
                        elif asteroid.radius > 30:
                            score += 50
                        else:
                            score += 100

                        asteroid.split()
                        shot.kill()

            if score > high_score:
                high_score = score

            screen.fill("black")

            for obj in drawable:
                obj.draw(screen)

            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            screen.blit(high_score_text, (10, 50))  

            pygame.display.flip()
            dt = clock.tick(60) / 1000

    finally:
        save_high_score(high_score)
        pygame.quit()
        sys.exit

if __name__ == "__main__":
    main()