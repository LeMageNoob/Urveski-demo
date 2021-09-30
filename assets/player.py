import pygame, sys


class Player (pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("assets/1620294984-you.png")
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.sprint = 4
        self.isSprinting = False

        # statistiques du joueur
        self.speed = 3
        self.rupee = 100
        self.life = 100
        self.maxLife = 100
        self.mana = 100
        self.maxMana = 100
        self.stamina = 20
        self.maxStamina = 20
        self.race = ""
        self.inventory = []
        self.spells = []
        self.weapon = ""

        self.images = {
            "down": self.get_image(0, 0),
            "left": self.get_image(0, 32),
            "right": self.get_image(0, 64),
            "up": self.get_image(0, 96),

            # animations supplementaires DOWN

            "down1": self.get_image(32, 0),
            "down2": self.get_image(64, 0),

            # animations supplementaires LEFT

            "left1": self.get_image(32, 32),
            "left2": self.get_image(96, 32),

            # animations supplementaires RIGHT

            "right1": self.get_image(32, 64),
            "right2": self.get_image(64, 64),

            # animations supplementaires UP

            "up1": self.get_image(32, 96),
            "up2": self.get_image(64, 96),

        }
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

    def save_location(self): self.old_position = self.position.copy()

    def change_animation(self, name):
        self.image = self.images[name]
        self.image.set_colorkey((0, 0, 0))
    # déplacement normal ZQSD

    def move_right(self):
        if self.race == "raulla":
            self.speed = 4
            self.sprint = 5
        elif not self.race == "raulla":
            self.speed = 3
            self.sprint = 4
        if self.isSprinting == False:
            self.position[0] += self.speed
        elif self.isSprinting == True:
            self.position[0] += self.sprint

    def move_left(self):
        if self.race == "raulla":
            self.speed = 4
            self.sprint = 5
        elif not self.race == "raulla":
            self.speed = 3
            self.sprint = 4
        if self.isSprinting == False:
            self.position[0] -= self.speed
        elif self.isSprinting == True:
            self.position[0] -= self.sprint

    def move_up(self):
        if self.race == "raulla":
            self.speed = 4
            self.sprint = 5
        elif not self.race == "raulla":
            self.speed = 3
            self.sprint = 4
        if self.isSprinting == False:
            self.position[1] -= self.speed
        elif self.isSprinting == True:
            self.position[1] -= self.sprint

    def move_down(self):
        if self.race == "raulla":
            self.speed = 4
            self.sprint = 4.5
        elif not self.race == "raulla":
            self.speed = 3
            self.sprint = 4
        if self.isSprinting == False:
            self.position[1] += self.speed
        elif self.isSprinting == True:
            self.position[1] += self.sprint

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))

        return image
