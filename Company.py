import pygame
import random


class CompanyGame:

    class Shop:
        def __init__(self):
            self.child = 0  # a child is a worker that makes you earn automatically 1$ every sec
            self.child_price = 25  # basic child price without the augmentation
            self.teen = 0  # a teenager is a worker that makes you earn automatically 5$ every second
            self.teen_price = 200 # basic teen price without the augmentation
            self.augmentation_per_second = 1.3  # price augmentation
            self.power = 1  # number of $ you will get for each click on the main button
            self.power_up_price = 300  # basic price of the first double power
            self.augmentation_power = 2  # double power's price double each time you buy one

        def buy_item(self):
            pass

        def price_changes(self):
            pass

    shop = Shop()

    class Player:   #_some lambda data, most won't be used for now
        def __init__(self, shop):
            self.entry_pseudo = 'lil Pseudo'
            self.pseudo = self.entry_pseudo
            self.id = random.randint(100000, 999999)   # have to operate some changes here to create a new unique id for each player
            self.level = 1
            self.items_waiting = 0
            self.items_done = 0
            self.get_item_time = 5
            self.job = "Crafter"
            self.crafter_xp = 0
            self.played_time = 0          # would like to set a timer to be able to know the time spent in game
            self.money = 1500
            self.money_per_second = 0.2 * shop.child + shop.teen





        def print_data(self):
            print("-------------Stats------------")
            print("Pseudo : " + self.pseudo + "\n")
            print("Id : " + str(self.id) + "\n")
            print("Level : " + str(self.level) + "\n")
            print("Job : " + self.job + "\n")
            print("Played Time : " + str(self.played_time) + "\n")
            print("Crafter xp : " + str(self.crafter_xp) + "\n")
            print("Time needed to craft an item : " + str(self.get_item_time) + "\n")
            print("Numbers of items done : " + str(self.items_done) + "\n")
            print("Numbers of waitings items : " + str(self.items_waiting) + "\n")
            print("-----------End of Stats------------")

        def game_stats_print(self, screen):
            fontstats = pygame.font.SysFont('comicsans', 20)
            moneytxt = "Your Money : " + str(round(self.money))
            textstats = fontstats.render((moneytxt), 1, (225, 225, 225))
            screen.blit(textstats, (400 - textstats.get_width()/2, 500 - textstats.get_height()))


    class Clickbutton():
        def __init__(self, color, x, y, width, height, text=''):
            self.color = color
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text

        def draw(self, screen, outline=None, size='60'):  # Call this method to draw the button on the screen
            if outline:
                pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
                pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)

            if self.text != '':
                font = pygame.font.SysFont('comicsans', size)
                text = font.render(self.text, 1, (15,15,15))
                screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        def isOver(self, pos):  # Pos is the mouse position or a tuple of (x,y) coordinates
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    return True
            return False

    def __init__(self):

        pygame.init()
        pygame.font.init()
        self.width, self.height = 1200, 800
        self.button_width = 250
        self.button_height = 100
        # 2
        # initialize the screen
        self.screen = pygame.display.set_mode((self.width, self.height))  # screen size
        pygame.display.set_caption("Company Farm")      # app name displaying on window
        # 3
        # initialize pygame clock
        self.clock = pygame.time.Clock()

        self.clack = pygame.time.Clock()
        self.time_spent_loop = 0
        self.clickbutton = self.Clickbutton((233, 55, 110), (self.width/2-(self.button_width/2)), (self.height/2-self.button_height/2), self.button_width, self.button_height, 'Click !')  # define ouf main button and centering
        self.player = self.Player(self.shop)


    def update(self):
        # sleep to make the game 60 fps
        self.clock.tick(60)
        # clear the screen
        self.screen.fill(15)
        self.clickbutton.draw(self.screen, (250, 250, 250), 60)
        self.buy_child_button = self.Clickbutton((247, 151, 10), (self.width / 1.5), (self.height / 6), self.button_width,
                                                 self.button_height / 2.2,
                                                 'Earn 1$ every seconds for ' + str(round(self.shop.child_price)) + '$')
        self.buy_teen_button = self.Clickbutton((247, 151, 10), (self.width / 1.5), (self.height / 6 + (self.button_height)),
                                                 self.button_width,
                                                 self.button_height / 2.2,
                                                 'Earn 5$ every seconds for ' + str(round(self.shop.teen_price)) + '$')
        self.double_power_button = self.Clickbutton((247, 151, 10), (self.width / 1.5),
                                                (self.height / 6 + 2*(self.button_height)),
                                                self.button_width + 50,
                                                self.button_height / 2.2,
                                                'Increase your power tap from ' + str(self.shop.power) + ' to ' + str(self.shop.power + 1) + ' for ' + str(self.shop.power_up_price) + ' $')

        self.buy_child_button.draw(self.screen, (150, 150, 150), 20)
        self.buy_teen_button.draw(self.screen, (150, 150, 150), 20)
        self.double_power_button.draw(self.screen, (150, 150, 150), 20)
        self.player.game_stats_print(self.screen)
        self.player.money_per_second = self.shop.child + self.shop.teen * self.shop.augmentation_power
        # one seconds actions loop
        dt = self.clack.tick()
        self.time_spent_loop += dt

        if self.time_spent_loop > 1000:
            self.player.money += float(round(self.player.money_per_second))
            self.time_spent_loop = 0

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            # quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.clickbutton.isOver(pos):
                    self.player.money += int(self.shop.power)


                if self.buy_child_button.isOver(pos):
                    if self.player.money >= self.shop.child_price:
                        print('You bought a child to help you to rise money ! ')
                        self.player.money -= self.shop.child_price
                        self.shop.child += 1
                        self.shop.child_price = self.shop.child_price * self.shop.augmentation_per_second
                    else:
                        print('Sorry you didnt have enough money for this, you need ', self.shop.child_price, '$')

                if self.buy_teen_button.isOver(pos):
                    if self.player.money >= self.shop.teen_price:
                        print('You bought a teen to help you to rise money ! ')
                        self.player.money -= self.shop.teen_price
                        self.shop.teen += 1
                        self.shop.teen_price = self.shop.teen_price * self.shop.augmentation_per_second
                    else:
                        print('Sorry you didnt have enough money for this, you need ', self.shop.teen_price, '$')

                if self.double_power_button.isOver(pos):
                    if self.player.money >= self.shop.power_up_price:
                        print('You bought more power tap to raise more money ! ')
                        self.player.money -= self.shop.power_up_price
                        self.shop.power += 1
                        self.shop.power_up_price = self.shop.power_up_price * 5
                    else:
                        print('Sorry you didnt have enough money for this, you need ', self.shop.power_up_price, '$')

            if event.type == pygame.MOUSEMOTION:

                if self.clickbutton.isOver(pos):
                    self.clickbutton.color = (233, 55, 110)
                else:
                    self.clickbutton.color = (234, 55, 157)

                if self.buy_child_button.isOver(pos):
                    self.buy_child_button.color = (247, 200, 10)
                else:
                    self.buy_child_button.color = (255, 111, 0)

                if self.buy_teen_button.isOver(pos):
                    self.buy_teen_button.color = (247, 200, 10)
                else:
                    self.buy_teen_button.color = (255, 111, 0)

                if self.double_power_button.isOver(pos):
                    self.double_power_button.color = (247, 200, 10)
                else:
                    self.double_power_button.color = (255, 111, 0)


        # update the screen
        pygame.display.flip()


cg = CompanyGame()  # __init__ is called right here

while 1:

    cg.update()   # refreshing infinite loop


