import pygame
from random import randint

class Robot:
    def __init__(self):
        self.image = pygame.image.load("assets\\robot.png")
        self.x = 320 - (self.image.get_width() / 2)
        self.y = 480 - self.image.get_height()
        self.left = False
        self.right = False

class Coin:
    def __init__(self):
        self.image = pygame.image.load("assets\\coin.png")
        self.x = randint(0, 640 - self.image.get_width())
        self.y = 0 - self.image.get_height()
        self.speed = randint(1, 3)

class Monster(Coin):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets\\monster.png")

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("A rain of coins")
        self.window = pygame.display.set_mode((640, 480))
        self.font = pygame.font.SysFont("Arial", 24)
        self.running = False
        self.title()

    # show title screen on first startup
    def title(self):
        self.window.fill((60, 60, 60))

        intro_text = self.font.render(f"Collect coins, avoid monsters!", True, (255, 255, 255))
        self.window.blit(intro_text, (320 - intro_text.get_width() / 2, 200 - intro_text.get_height() / 2))
        instr_text = self.font.render(f"L + R arrow keys to move", True, (255, 255, 255))
        self.window.blit(instr_text, (320 - instr_text.get_width() / 2, 240 - instr_text.get_height() / 2))
        info_text = self.font.render(f"Press ENTER to begin", True, (255, 255, 255))
        self.window.blit(info_text, (320 - info_text.get_width() / 2, 280 - info_text.get_height() / 2))

        self.window.blit(pygame.image.load("assets\\coin.png"), (200, 100))
        self.window.blit(pygame.image.load("assets\\monster.png"), (400, 80))
        self.window.blit(pygame.image.load("assets\\robot.png"), (295, 394))

        pygame.display.flip()

        while True:
            # wait for Enter press
            self.check_events()

    # start game from scratch
    def setup(self):
        self.clock = pygame.time.Clock()

        self.score = 0

        self.robot = Robot()
        self.coins = []
        self.monsters = []
        # increase spawn rate of robots over time
        self.montimer = 0
        self.upper = 200

        # progresses game logic
        self.running = True

        self.main_loop()

    def main_loop(self):
        while True:
            self.check_events()
            if self.running:    
                self.run()
            else:
                self.game_is_over()

    def check_events(self):
        for event in pygame.event.get():
            # check if on title screen or game over screen
            if self.running == False:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.setup()
            else:
                # move robot if keys are pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.robot.left = True
                    if event.key == pygame.K_RIGHT:
                        self.robot.right = True

                # stop moving robot when keys are released
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.robot.left = False
                    if event.key == pygame.K_RIGHT:
                        self.robot.right = False

            if event.type == pygame.QUIT:
                exit()

    def run(self):
        self.window.fill((255,255,255))

        # returns the bounding box of the robot, for collision detection
        robot_rect = self.update_robot()
        
        self.update_score()

        # update positions of coins and monsters, and judge collision
        self.update_coins(robot_rect)

        self.update_monsters(robot_rect)
        
        pygame.display.flip()
        self.clock.tick(60)
        self.montimer += 1

    def update_robot(self):
        if self.robot.right and self.robot.x < 640 - self.robot.image.get_width():
            self.robot.x += 3
        if self.robot.left and self.robot.x > 0:
            self.robot.x -= 3
        self.window.blit(self.robot.image, (self.robot.x, self.robot.y))
        robot_rect = self.robot.image.get_rect(topleft = (self.robot.x, self.robot.y))
        return robot_rect
    
    def update_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.window.blit(score_text, (630 - score_text.get_width(), score_text.get_height() / 2))

    def update_coins(self, robot_rect):
        # chance of generating a coin
        if randint(0,100) == 0:
            self.coins.append(Coin())

        # update position of each coin and apply its speed
        for coin in self.coins:
            self.window.blit(coin.image, (coin.x, coin.y))
            coin.y += coin.speed
            coin_rect = coin.image.get_rect(topleft = (coin.x, coin.y))
            # "delete" the coin on contact with robot
            if coin_rect.colliderect(robot_rect):
                self.score += 1
                coin.x = 641
                coin.y = 481            

    def update_monsters(self, robot_rect):
        # chance of generating a monster, increases over time
        if randint(0, self.upper) == 0:
            self.monsters.append(Monster())
        if self.montimer == 300 and self.upper > 60:
            self.montimer = 0
            self.upper -= 20

        # update position of each monster and apply its speed
        for monster in self.monsters:
            self.window.blit(monster.image, (monster.x, monster.y))
            monster.y += monster.speed
            monster_rect = monster.image.get_rect(topleft = (monster.x, monster.y))
            if monster_rect.colliderect(robot_rect):
                self.running = False

    # show game over screen
    def game_is_over(self):
        self.window.fill((255, 0, 0))
        go_text = self.font.render(f"Game over! Score: {self.score}", True, (0, 0, 0))
        self.window.blit(go_text, (320 - go_text.get_width() / 2, 200 - go_text.get_height() / 2))
        retry_text = self.font.render(f"Press ENTER to retry", True, (0, 0, 0))
        self.window.blit(retry_text, (320 - retry_text.get_width() / 2, 280 - retry_text.get_height() / 2))
        pygame.display.flip()

if __name__ == "__main__":
    Game()