import pygame, sys

import pytmx
import pyscroll
import random

from assets.player import Player


class Game:

    def __init__(self):

        # resolution de l'écran
        self.WIDTH = 800
        self.HEIGHT = 600

        # background
        self.background = pygame.image.load("assets/bg.png")
        self.background = pygame.transform.scale(self.background, (800, 600))

        # language
        self.language = "English"

        # logo du jeu
        self.logoWidht = 150
        self.logoHeight = 150
        self.logo = pygame.image.load("assets/UrveskiLogo.png")
        self.logo = pygame.transform.scale(self.logo, (300, 150))

        # start bouton
        self.playButton = pygame.image.load("assets/StartButtonOff.png")
        self.playButton = pygame.transform.scale(self.playButton, (200, 100))
        self.playbtnRect = self.playButton.get_rect()
        self.playbtnRect.topleft = (self.WIDTH/2 - self.playbtnRect.width/2, self.HEIGHT/2 - self.playbtnRect.height/2 + 50)
        self.playbtnRect_midL = self.playbtnRect.midleft

        # load button
        self.loadButton = pygame.image.load("assets/LoadButtonOff.png")
        self.loadButton = pygame.transform.scale(self.loadButton, (200, 100))
        self.loadBtnRect = self.loadButton.get_rect()
        self.loadBtnRect.topleft = (self.WIDTH/2 - self.playbtnRect.width/2, self.HEIGHT/2 - self.playbtnRect.height/2 + 150)
        self.loadBtnRect_midL = self.loadBtnRect.left

        # bouton language francais
        self.frenchButton = pygame.image.load("assets/languageFrenchOff.png")
        self.frenchButton = pygame.transform.scale(self.frenchButton, (40, 50))
        self.frenchButtonRect = self.frenchButton.get_rect()
        self.frenchButtonRect.topleft = (760, 550)

        # bouton language Anglais
        self.englishButton = pygame.image.load("assets/languageEnglishOff.png")
        self.englishButton = pygame.transform.scale(self.englishButton, (40, 50))
        self.englishButtonRect = self.englishButton.get_rect()
        self.englishButtonRect.topleft = (720, 550)

        # credits
        self.creditFont = pygame.font.Font("assets/RomanAntique.ttf", 30)
        if self.language == "English" or self.language == "":
            self.creditText = self.creditFont.render("By LeMageNoob and Arcaniane", True, pygame.Color(0, 0, 0))
        if self.language == "French":
            self.creditText = self.creditFont.render("Par LeMageNoob et Arcaniane", True, pygame.Color(0, 0, 0))

        # RACES/CLASSES -------------------------------------------------------------------------------
        # description de la race
        self.descRace = ""
        # texte de description pour les races ?
        self.descFont = pygame.font.Font("assets/RomanAntique.ttf", 48)
        self.descText = self.descFont.render(f"{self.descRace}", True, pygame.Color(255, 255, 255))
        # texte au dessus des classes
        self.classTopFont = pygame.font.Font("assets/RomanAntique.ttf", 52)
        # images de classes
        # Menulisian
        self.menuImage = pygame.image.load("assets/menulisianBg.png")
        self.menuImage = pygame.transform.scale(self.menuImage, (100, 150))
        self.menuRect = self.menuImage.get_rect()
        self.menuRect.topleft = (50, 100)
        # Raullan
        self.raullaImage = pygame.image.load("assets/raullanBg.png")
        self.raullaImage = pygame.transform.scale(self.raullaImage, (100, 150))
        self.raullaRect = self.raullaImage.get_rect()
        self.raullaRect.topleft = (150, 100)
        # Askarian
        self.askarImage = pygame.image.load("assets/AskarianBg.png")
        self.askarImage = pygame.transform.scale(self.askarImage, (100, 150))
        self.askarRect = self.askarImage.get_rect()
        self.askarRect.topleft = (550, 100)
        # native
        self.nativeImage = pygame.image.load("assets/nativeBg.png")
        self.nativeImage = pygame.transform.scale(self.nativeImage, (100, 150))
        self.nativeRect = self.nativeImage.get_rect()
        self.nativeRect.topleft = (350, 100)

        # vhiunian
        self.vhiunImage = pygame.image.load("assets/VhiunianBg.png")
        self.vhiunImage = pygame.transform.scale(self.vhiunImage, (100, 150))
        self.vhiunRect = self.vhiunImage.get_rect()
        self.vhiunRect.topleft = (450, 100)
        # llyrian
        self.llyriaImage = pygame.image.load("assets/llyrianBg.png")
        self.llyriaImage = pygame.transform.scale(self.llyriaImage, (100, 150))
        self.llyriaRect = self.llyriaImage.get_rect()
        self.llyriaRect.topleft = (250, 100)
        # iqarian
        self.iqarImage = pygame.image.load("assets/iqarBg.png")
        self.iqarImage = pygame.transform.scale(self.iqarImage, (100, 150))
        self.iqarRect = self.iqarImage.get_rect()
        self.iqarRect.topleft = (650, 100)

        # variables/listes liées au particules
        self.particles = []
        self.colors = [(0, 240, 255), (1, 200, 254), (10, 150, 230), (0, 150, 220)]

        # vignette
        self.vignette = pygame.image.load("assets/Vignette.png")

        # texte
        self.textLine1 = ""
        self.textLine2 = ""
        self.textLine3 = ""

        # creer la fenetre du jeu
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Urveski --Closed Beta--")

        # charger la carte tmx
        tmx_data = pytmx.util_pygame.load_pygame("assets/map1.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # generer le joueur
        self.player_position = tmx_data.get_object_by_name("player")
        self.player = Player(self.player_position.x, self.player_position.y)

        # definir une liste de qui stocke les collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # definir une liste qui stocke les collision talk
        self.talkbox = []

        for obj in tmx_data.objects:
            if obj.type == "talkbox":
                self.talkbox.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.lava = []

        for obj in tmx_data.objects:
            if obj.type == "lava":
                self.lava.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.quitTuto = []

        for obj in tmx_data.objects:
            if obj.type == "quitTuto":
                self.quitTuto.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.ladder = []

        for obj in tmx_data.objects:
            if obj.type == "ladder":
                self.ladder.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=9)  # PLAYER LAYER HERE
        self.group.add(self.player)

# NPCS TALKBOX RECT -----------------------------------------------------------------------------

        # Définir les npcs
        loic = tmx_data.get_object_by_name("Loic")
        self.loic_rect = pygame.Rect(loic.x, loic.y, loic.width, loic.height)
        melania = tmx_data.get_object_by_name("Melania")
        self.melania_rect = pygame.Rect(melania.x, melania.y, melania.width, melania.height)
        enzo = tmx_data.get_object_by_name("Enzo")
        self.enzo_rect = pygame.Rect(enzo.x, enzo.y, enzo.width, enzo.height)

        # objets a acheter
        potion20 = tmx_data.get_object_by_name("potion20")
        self.potion20_rect = pygame.Rect(potion20.x, potion20.y, potion20.width, potion20.height)

        potionCliff20 = tmx_data.get_object_by_name("potionCliff20")
        self.potionCliff20_rect = pygame.Rect(potionCliff20.x, potionCliff20.y, potionCliff20.width, potionCliff20.height)

        # Panneaux
        signFolstarr = tmx_data.get_object_by_name("signFolstarr")
        self.signFolstarr_rect = pygame.Rect(signFolstarr.x, signFolstarr.y, signFolstarr.width, signFolstarr.height)
        signTuto = tmx_data.get_object_by_name("signTuto")
        self.signTuto_rect = pygame.Rect(signTuto.x, signTuto.y, signTuto.width, signTuto.height)
        signFolstarr2 = tmx_data.get_object_by_name("signFolstarr2")
        self.signFolstarr2_rect = pygame.Rect(signFolstarr2.x, signFolstarr2.y, signFolstarr2.width, signFolstarr2.height)
        signNcliff = tmx_data.get_object_by_name("signNcliff") # ncliff = near cliff
        self.signNcliff_rect = pygame.Rect(signNcliff.x, signNcliff.y, signNcliff.width, signNcliff.height)

        # definir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # definir la zone ou se trouve le joueur
        self.map = "world"

# FONCTIONS ---------------------------------------------------------------------------------------------------------
    def spawn(self):
        self.player.life = self.player.maxLife

    def heal(self, amount):
        if not self.player.life >= self.player.maxLife:
            self.player.life = self.player.life = self.player.life + amount

    def takeDamage(self, amount):
        self.player.life = self.player.life - amount

    def showParticles(self):
        self.particles.append([[self.mx + random.uniform(1, 16), self.my + random.uniform(-10, 20 + -10 / 2)], [random.uniform(-0.55, 0.55) + 0, -3.8], random.randint(5, 7)])
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.2
            particle[1][1] += 0.2
            pygame.draw.circle(self.screen, random.choice(self.colors), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 2:
                self.particles.remove(particle)

    def talk(self, textSize, R, G, B):
        self.police = pygame.font.Font("assets/Retro Gaming.ttf", textSize)
        self.texte = self.police.render(self.textLine1, True, pygame.Color(R, G, B))
        self.texte1 = self.police.render(self.textLine2, True, pygame.Color(R, G, B))
        self.texte2 = self.police.render(self.textLine3, True, pygame.Color(R, G, B))
        self.textRect = self.texte.get_rect()
        # textbox
        self.textBox = pygame.image.load("assets/textbox.png")
        self.textBox = pygame.transform.scale(self.textBox, (620, 210))
        self.textBoxRect = self.textBox.get_rect()

        self.screen.blit(self.textBox, (self.WIDTH / 2 - 600 / 2, self.HEIGHT / 2 - 200 / 2 + 200))
        self.screen.blit(self.texte, (self.WIDTH / 2 - 600 / 2 + 20, self.HEIGHT / 2 - 200 / 2 + 205))
        self.screen.blit(self.texte1, (self.WIDTH/2 - 600 / 2 + 20, self.HEIGHT/2 - 100 / 2 + 218))
        self.screen.blit(self.texte2, (self.WIDTH/2 - 600 / 2 + 20, self.HEIGHT/2 - 100 / 2 + 272))

    def choice(self):
        self.choicePolice = pygame.font.Font("assets/RomanAntique.ttf", 45)
        self.choiceYes = self.choicePolice.render("Yes", True, pygame.Color(255, 255, 255))
        self.choiceNo = self.choicePolice.render("No", True, pygame.Color(255, 255, 255))
        self.choiceYn = ""
        self.choiceIcon = pygame.image.load("assets/SelectIcon.png")
        self.choiceIcon = pygame.transform.scale(self.choiceIcon, (50, 50))
        self.choiceBg = pygame.image.load("assets/Choice.png")
        self.choiceBg = pygame.transform.scale(self.choiceBg, (120, 140))

        self.choiceYes_rect = self.choiceYes.get_rect()
        self.choiceNo_rect = self.choiceNo.get_rect()

        self.screen.blit(self.choiceBg, (680, 230))
        self.screen.blit(self.choiceYes, (712.5, 260))
        self.screen.blit(self.choiceNo, (712.5, 310))

    def mouse_input(self):
        pos = pygame.mouse.get_pos()
        if self.playbtnRect.collidepoint(pos):
            self.playButton = pygame.image.load("assets/StartButton.png")
            self.playButton = pygame.transform.scale(self.playButton, (200, 100))
            if pygame.mouse.get_pressed()[0] == 1:
                self.chooseClass = True
        else:
            self.playButton = pygame.image.load("assets/StartButtonOff.png")
            self.playButton = pygame.transform.scale(self.playButton, (200, 100))

        if self.loadBtnRect.collidepoint(pos):
            self.loadButton = pygame.image.load("assets/LoadButton.png")
            self.loadButton = pygame.transform.scale(self.loadButton, (200, 100))
            if pygame.mouse.get_pressed()[0] == 1:
                self.chooseClass = True
        else:
            self.loadButton = pygame.image.load("assets/LoadButtonOff.png")
            self.loadButton = pygame.transform.scale(self.loadButton, (200, 100))

        # boutons langues

        # Francais
        if self.frenchButtonRect.collidepoint(pos):
            self.frenchButton = pygame.image.load("assets/languageFrench.png")
            self.frenchButton = pygame.transform.scale(self.frenchButton, (40, 50))
            if pygame.mouse.get_pressed()[0] == 1:
                self.language = "French"
        else:
            self.frenchButton = pygame.image.load("assets/languageFrenchOff.png")
            self.frenchButton = pygame.transform.scale(self.frenchButton, (40, 50))

        # Anglais
        if self.englishButtonRect.collidepoint(pos):
            self.englishButton = pygame.image.load("assets/languageEnglish.png")
            self.englishButton = pygame.transform.scale(self.englishButton, (40, 50))
            if pygame.mouse.get_pressed()[0] == 1:
                self.language = "English"
        else:
            self.englishButton = pygame.image.load("assets/languageEnglishOff.png")
            self.englishButton = pygame.transform.scale(self.englishButton, (40, 50))

        # Boutons selections de classes
        if self.chooseClass == True:
            if self.language == "English" or self.language == "":
                self.classTopText = self.classTopFont.render("Select a homeland.", True, pygame.Color(253, 253, 253))
            if self.language == "French":
                self.classTopText = self.classTopFont.render("Choissisez une patrie.", True, pygame.Color(253, 253, 253))

        if self.chooseClass == True:
            if self.vhiunRect.collidepoint(pos):
                if self.language == "English" or self.language == "":
                    self.descRace = "Vhiun : Gives you the katana."
                if self.language == "French":
                    self.descRace = "Vhiunien : Vous possédez le katana."
                if pygame.mouse.get_pressed()[0] == 1:
                    self.isGameStarted = True
                    self.player.race = "vhiun"
                    self.player.weapon = "katana"
                    self.chooseClass = False
                    self.spawn()

        if self.chooseClass == True:
            if self.nativeRect.collidepoint(pos):
                if self.language == "English" or self.language == "":
                    self.descRace = "Native : Gives you regalia spell."
                if self.language == "French":
                    self.descRace = "Natif : Vous connaisez le sort regalia."
                if pygame.mouse.get_pressed()[0] == 1:
                    self.isGameStarted = True
                    self.player.race = "native"
                    self.player.weapon = "steel sword"
                    self.player.spells.append("regalia")  # the idea is from mario
                    self.chooseClass = False
                    self.spawn()

        if self.chooseClass == True:
            if self.menuRect.collidepoint(pos):
                if self.language == "English" or self.language == "":
                    self.descRace = "Menulis : Gives you saltis spell."
                if self.language == "French":
                    self.descRace = "Menulisien : Vous connaisez le sort Saltis."
                if pygame.mouse.get_pressed()[0] == 1:
                    self.isGameStarted = True
                    self.player.race = "menulis"
                    self.player.weapon = "steel sword"
                    self.player.spells.append("saltis")
                    self.chooseClass = False
                    self.spawn()

        if self.chooseClass == True:
            if self.askarRect.collidepoint(pos):
                if self.language == "English" or self.language == "":
                    self.descRace = "Askaria : Gives you +10 hp."
                if self.language == "French":
                    self.descRace = "Askarien : Vous donne +10 pv."
                if pygame.mouse.get_pressed()[0] == 1:
                    self.isGameStarted = True
                    self.player.race = "askaria"
                    self.player.weapon = "steel sword"
                    self.chooseClass = False
                    self.spawn()
        if self.chooseClass == True:
            if self.llyriaRect.collidepoint(pos):
                if self.language == "English" or self.language == "":
                    self.descRace = "Llyria : Gives you 8% resistance."
                if self.language == "French":
                    self.descRace = "Llyrien : Vous etes 8% plus resistant."
                if pygame.mouse.get_pressed()[0] == 1:
                    self.isGameStarted = True
                    self.player.race = "llyria"
                    self.player.weapon = "steel sword"
                    self.chooseClass = False
                    self.spawn()

        if self.chooseClass == True:
            if self.raullaRect.collidepoint(pos):
                if self.language == "English" or self.language == "":
                    self.descRace = "Raulla : You're faster."
                if self.language == "French":
                    self.descRace = "Raullien : Vous etes plus rapide."
                if pygame.mouse.get_pressed()[0] == 1:
                    self.isGameStarted = True
                    self.player.race = "raulla"
                    self.player.weapon = "steel sword"
                    self.chooseClass = False
                    self.spawn()

        if self.chooseClass == True:
            if self.iqarRect.collidepoint(pos):
                if self.language == "English" or self.language == "":
                    self.descRace = "Iqar : Gives more money after a fight."
                if self.language == "French":
                    self.descRace = "Iqarien : Vous obtenez plus d'argent."
                if pygame.mouse.get_pressed()[0] == 1:
                    self.isGameStarted = True
                    self.player.race = "iqar"
                    self.player.weapon = "steel sword"
                    self.chooseClass = False
                    self.spawn()

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LSHIFT]:
            self.player.isSprinting = True
        elif not pressed[pygame.K_LSHIFT]:
            self.player.isSprinting = False
        if pressed[pygame.K_z]:
            if self.canMove:
                self.player.move_up()
                self.player.change_animation("up1")

        elif pressed[pygame.K_s]:
            if self.canMove:
                self.player.move_down()
                self.player.change_animation("down1")
        elif pressed[pygame.K_q]:
            if self.canMove:
                self.player.move_left()
                self.player.change_animation("left1")
        elif pressed[pygame.K_d]:
            if self.canMove:
                self.player.move_right()
                self.player.change_animation("right1")

        elif pressed[pygame.K_a]:  # DEBUG ONLY
            self.heal(10)

        elif pressed[pygame.K_e]:
            if self.canTalk == True:
                if self.wantToTalk == False:
                    if self.talkCd == 1:
                        self.talkCd = 0
                        self.talkCdTime = pygame.time.get_ticks()
                        self.wantToTalk = True
                        self.canMove = False # pour que le joueur ne marche pas pendant le dialoque
        elif pressed[pygame.K_ESCAPE]:
            if self.wantToTalk == True:
                if self.talkCd == 1:
                    self.talkCd = 0
                    self.wantToTalk = False
                    self.canMove = True
                    self.talkCdTime = pygame.time.get_ticks()

    def switch_house(self):

        # charger la carte tmx
        tmx_data = pytmx.util_pygame.load_pygame("assets/house1.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # definir une liste de qui stocke les collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)  # PLAYER LAYER HERE IN THE HOUSE
        self.group.add(self.player)

        # definir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name("exithouse")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # recupérer le point de spawn devant la maison
        spawn_house_point = tmx_data.get_object_by_name("spawn_house")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y

    def switch_world(self):

        # charger la carte tmx
        tmx_data = pytmx.util_pygame.load_pygame("assets/map1.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # definir une liste de qui stocke les collisions
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=8)  # PLAYER LAYER HERE IN THE MAP
        self.group.add(self.player)

        # definir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # recupérer le point de spawn devant la maison
        spawn_house_point = tmx_data.get_object_by_name("enter_house_exit")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y
        self.screen.blit(self.lifeText, (70, 0))
        self.screen.blit(self.moneyText, (70, 60))

    def update(self):
        self.group.update()
        # definir le rectangle de collision pour entrer dans la maison
        # verif pour entrer dans la maison
        if self.player.race == "askaria":
            self.player.maxLife = 110

        if self.map == "world" and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = "house"

        # verif pour sortir dans la maison
        if self.map == "house" and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()
            self.map = "world"

        # verif collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.lava) > -1:
                if self.canTakeDamage == True:
                    self.isTakingDamage = True
                    self.takeDamage(10)
                    self.canTakeDamage = False
                    self.currentTimeDamage = pygame.time.get_ticks()

        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.ladder) > -1:
                self.player.speed = 2
                self.player.sprint = 3
            elif not sprite.feet.collidelist(self.ladder) > -1:
                self.player.speed = 3
                self.player.sprint = 4

        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.quitTuto) > -1:
                self.player.position[0] = 4192.00
                self.player.position[1] = 976.00
        # gui, Graphical User Interface
        # --LIFE ICON
        self.lifeIcon = pygame.image.load("assets/lifeIcon.png")
        self.lifeIcon = pygame.transform.scale(self.lifeIcon, (60, 45))
        # --MONEY ICON
        self.moneyIcon = pygame.image.load("assets/moneyIcon.png")
        self.moneyIcon = pygame.transform.scale(self.moneyIcon, (60, 45))
        # --LIFE TEXT
        self.lifeFont = pygame.font.Font("assets/RomanAntique.ttf", 50)
        self.lifeText = self.lifeFont.render(f"{self.player.life}", True, pygame.Color(250, 250, 250))

        # --MONEY TEXT
        self.moneyFont = pygame.font.Font("assets/RomanAntique.ttf", 50)
        self.moneyText = self.moneyFont.render(f"{self.player.rupee}", True, pygame.Color(250, 250, 250))

        # texte de description pour les races ?
        self.descFont = pygame.font.Font("assets/RomanAntique.ttf", 48)
        self.descText = self.descFont.render(f"{self.descRace}", True, pygame.Color(255, 255, 255))

        # Les Dialogues du jeu

        for sprite in self.group.sprites():
            pressed = pygame.key.get_pressed()
            if sprite.feet.collidelist(self.talkbox) > -1:
                if self.player.feet.colliderect(self.loic_rect):
                    self.canTalk = True
                    if self.language == "English" or self.language == "":
                        self.textLine1 = "Hi im Loic."
                        self.textLine2 = ""
                        self.textLine3 = ""
                    elif self.language == "French":
                        self.textLine1 = "Bonjour je suis Loic."
                        self.textLine2 = ""
                        self.textLine3 = ""

                elif self.player.feet.colliderect(self.melania_rect):
                    self.canTalk = True
                    if self.language == "English" or self.language == "":
                        self.textLine1 = "Howdy! im Melania."
                        self.textLine2 = ""
                        self.textLine3 = ""
                    elif self.language == "French":
                        self.textLine1 = "Bonjour! je suis"
                        self.textLine2 = "Mélania."
                        self.textLine3 = ""
                elif self.player.feet.colliderect(self.enzo_rect):
                    self.canTalk = True
                    if self.language == "English" or self.language == "":
                        self.textLine1 = "hello traveller !"
                        self.textLine2 = "I am Enzo the trader."
                        self.textLine3 = "Buy as much as you want."
                    elif self.language == "French":
                        self.textLine1 = "Bonjour voyageur!"
                        self.textLine2 = "Je suis enzo le marchand."
                        self.textLine3 = "Sois le bienvenu."
                elif self.player.feet.colliderect(self.signFolstarr_rect):
                    self.canTalk = True
                    if self.language == "English" or self.language == "":
                        self.textLine1 = "Welcome to Folstarr !"
                        self.textLine2 = "Where the sea reaches "
                        self.textLine3 = "the sea."
                    if self.language == "French":
                        self.textLine1 = "Bienvenu a Folstarr"
                        self.textLine2 = ""
                        self.textLine3 = ""
                elif self.player.feet.colliderect(self.signTuto_rect):
                    self.canTalk = True
                    if self.language == "English" or self.language == "":
                        self.textLine1 = "Press E to :"
                        self.textLine2 = "Talk"
                        self.textLine3 = "Interact"
                    if self.language == "French":
                        self.textLine1 = "appuiez sur E pour :"
                        self.textLine2 = "Parler"
                        self.textLine3 = "Interagir"
                elif self.player.feet.colliderect(self.signFolstarr2_rect):
                    self.canTalk = True
                    if self.language == "English" or self.language == "":
                        self.textLine1 = "You're at Folstarr"
                        self.textLine2 = "Kiki is in the south"
                        self.textLine3 = "Clifftown is in the west"
                    if self.language == "French":
                        self.textLine1 = "Vous etes a Folstarr"
                        self.textLine2 = "Kiki est au sud"
                        self.textLine3 = "Clifftown est au sud"
                elif self.player.feet.colliderect(self.signNcliff_rect):
                    self.canTalk = True
                    if self.language == "English" or self.language == "":
                        self.textLine1 = "north : Clifftown"
                        self.textLine2 = "west : Frostfall"
                        self.textLine3 = "east : Morokh"
                    if self.language == "French":
                        self.textLine1 = "nord : Clifftown"
                        self.textLine2 = "ouest : Frostfall"
                        self.textLine3 = "est : Morokh"

            elif not sprite.feet.collidelist(self.talkbox) > 1:
                self.canTalk = False
                self.isChoice = True

    def run(self):

        clock = pygame.time.Clock()

        # la boucle du jeu
        running = True
        self.isGameStarted = False
        self.chooseClass = False

        # variables liés au texte
        self.wantToTalk = False  # si le joueur veut parler au pnj alors True
        self.canTalk = False  # si le joueur peut parler au pnj alors True
        self.talkCd = 1
        self.talkCdTime = 0  # le premier delai
        self.isChoice = False

        # pour savoir si le joueur peut bouger ou non
        self.canMove = True

        # variables liés au dégats
        self.canTakeDamage = True
        self.isTakingDamage = False
        # variable pour montrer le Gui
        self.showGui = False

        # variables liés au cooldown
        self.currentTimeDamage = 0  # pour les degats
        self.currentTimeTextSwitch = 0  # pour savoir quand le texte peut etre switched

        while running:
            pygame.display.flip()  # actualisation de l'écran / TOUJOURS ACTUALISER L'ECRAN
            self.mx, self.my = pygame.mouse.get_pos()  # position de la souris : pour les paricules
            if not self.isGameStarted:
                self.mouse_input()
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.playButton, self.playbtnRect.topleft)
                self.screen.blit(self.logo, (self.WIDTH/2 - self.logoWidht, self.HEIGHT/2 - self.logoHeight - 125))
                self.screen.blit(self.loadButton, self.loadBtnRect.topleft)
                self.screen.blit(self.frenchButton, self.frenchButtonRect.topleft)
                self.screen.blit(self.englishButton, self.englishButtonRect.topleft)
                self.screen.blit(self.creditText, (0, 530))
                self.showParticles()

            if self.chooseClass == True :
                self.screen.fill((0, 0, 0))
                self.screen.blit(self.menuImage, (self.menuRect.topleft))  # menulisian
                self.screen.blit(self.raullaImage, (self.raullaRect.topleft))  # raullan
                self.screen.blit(self.llyriaImage, (self.llyriaRect.topleft))  # llyria
                self.screen.blit(self.nativeImage, (self.nativeRect.topleft))  # native
                self.screen.blit(self.vhiunImage, (self.vhiunRect.topleft) ) # vhiun
                self.screen.blit(self.askarImage, (self.askarRect.topleft))  # askarian
                self.screen.blit(self.iqarImage, (self.iqarRect.topleft))  # iqarian
                self.screen.blit(self.classTopText, (245, 0))
                self.screen.blit(self.descText, (0, 500))
                self.showParticles()
                self.update()

            if self.player.life == 0:  # le game over
                self.showGui = False
                self.isGameStarted = False

            elif self.wantToTalk:
                self.handle_input()
                self.talk(36, 255, 255, 255)
                # if self.isChoice == True:
                #    self.choice()

            elif self.isGameStarted:
                self.player.save_location() # ?
                self.handle_input()  # uptade de l'appui des touches
                self.update()  # la fonction uptade ?
                self.group.center(self.player.rect)  # Le groupe = scrolling
                self.group.draw(self.screen)  # fait apparaitre le group a l'écran
                self.showGui = True

            if self.showGui:
                self.screen.blit(self.lifeIcon, (0, 0))
                self.screen.blit(self.moneyIcon, (0, 50))
                self.screen.blit(self.lifeText, (60, 0))
                self.screen.blit(self.moneyText, (60, 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.currentTime = pygame.time.get_ticks()

            if self.currentTime - self.talkCdTime > 500:
               self.talkCd = 1

            if self.currentTime - self.currentTimeTextSwitch > 1000:
                self.canSwitch = True

            if self.currentTime - self.currentTimeDamage > 1000:
                self.canTakeDamage = True
                self.isTakingDamage = False

            clock.tick(60)

        pygame.quit()
