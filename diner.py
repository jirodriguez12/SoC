"""
 *****************************************************************************
   FILE:        diner.py
   AUTHOR:      Jonathan Rodriguez
   ASSIGNMENT:  Summer of Code Project 1
   DATE:        06/19/2020
   DESCRIPTION: Simulation of a worker at diner.
 *****************************************************************************
"""

import arcade
import random

SCREEN_WIDTH = 825
SCREEN_HEIGHT = 725
SCREEN_TITLE = "Diner Frenzy"
SPEED = 10


class Start_Card(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_SKY_BLUE)

    def on_draw(self):
        backdrop = arcade.Sprite("images/opening.png", scale=1.1, center_x=400, center_y=375)
        arcade.start_render()
        backdrop.draw()
        arcade.draw_text("Click Button\n    to Start",400, 50,
                         arcade.color.BLACK, font_size=40,anchor_x="center", font_name="Comic Sans MS")

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if x in range(250, 550, 1) and y in range(125, 525, 1):
                game = Game()
                game.setup()
                self.window.show_view(game)


class Game(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)

        #audio initializations
        self._cook_sound = None
        self._eat_sound = None
        self._wack_sound = None
        self._bell = None

        #sprite initializations
        self._background = None
        self._chef = None
        self._counter = None
        self._stove = None
        self._egg_carton = None
        self._bagels = None
        self._customer = None
        self._thought = None
        self._order = None
        self._item =None
        self._order_image = None
        self._held_item = None

        #keep track of score
        self._points = 0
        self._possible_points = 0

        #updates time allowed in game
        self.time = 0
        self._total_time = 60
        self._playing = True

        #keeps track of all items obtained by player
        self._items = []

        #used to generate a random order
        self._all_orders = ["egg bagel", "egg", "bagel"]
        self._order_requested = random.choice(self._all_orders)

        #boolian used to check if chef has item
        self._hold = False

        #boolian used to check if chef has the correct order for customer
        self._correct_order = False

    def setup(self):
        #audio declarations
        self._cook_sound = arcade.load_sound("audio/sizzle.mp3")
        self._eat_sound = arcade.load_sound("audio/eat.mp3")
        self._wack_sound = arcade.load_sound("audio/villager.mp3")
        self._bell_sound = arcade.load_sound("audio/bell.mp3")

        #sprite declarations
        self._background = arcade.Sprite("images/diners.png", scale=0.7, center_x=400, center_y=375)
        self._table = arcade.Sprite("images/table.png", scale=4, center_x=600, center_y=325)
        self._table1 = arcade.Sprite("images/table.png", scale=4, center_x=600, center_y=275)
        self._chef = arcade.Sprite("images/chef.png", scale=0.5, center_x=400, center_y=280)
        self._counter = arcade.Sprite("images/counter.png", scale=8.5, center_x=410, center_y=130)
        self._stove = arcade.Sprite("images/grill.png", scale=7, center_x=410, center_y=123)
        self._egg_carton = arcade.Sprite("images/egg_carton.png", scale=1.2, center_x=600, center_y=290)
        self._bagels = arcade.Sprite("images/bagels.png", scale=2, center_x=600, center_y=340)
        self._customer = arcade.Sprite("images/customer.png", scale=0.3, center_x=100, center_y=150)
        self._thought = arcade.Sprite("images/thought.png", scale=2, center_x=150, center_y=250)
        self._item = arcade.Sprite("images/x.png", scale=10, center_x=500000, center_y=50000)
        self._held_item = arcade.Sprite("images/x.png", scale=10, center_x=500000, center_y=50000)

        #declares a sprite based on the order generated
        self._order_requested = random.choice(self._all_orders)
        if self._order_requested == "egg":
            self._order_image = arcade.Sprite("images/egg.png", scale=1, center_x=175, center_y=255)

        elif self._order_requested == "bagel":
            self._order_image = arcade.Sprite("images/bagel.png", scale=1.8, center_x=175, center_y=250)

        else:
            self._order_image = arcade.Sprite("images/egg_bagel.png", scale=1.8, center_x=175, center_y=250)

        self._end = arcade.Sprite("images/end.png", scale=1.7, center_x=500, center_y=375)
        self._hs = arcade.Sprite("images/hs.png", scale=1, center_x=400, center_y=375)


    def on_draw(self):
        arcade.start_render()
        self._background.draw()
        self._table.draw()
        self._table1.draw()
        self._bagels.draw()
        self._egg_carton.draw()
        self._chef.draw()
        self._counter.draw()
        self._stove.draw()
        self._customer.draw()
        self._thought.draw()
        self._order_image.draw()
        self._item.draw()
        self._held_item.draw()

        # Messages
        points = f"Hill Card Points:\n {self._points}"
        arcade.draw_text(points, 600, 70, arcade.color.BLACK, 20)
        held = f"Held Item:"
        arcade.draw_text(held, 687, 680, arcade.color.BLACK, 25)
        time = f"{(self._total_time - self.time):.02f}"

        if self._total_time - self.time <= 0:
            time = "0.00"
            if self._playing:
                arcade.play_sound(self._bell_sound)
                end = End_Card(self._points)
                end.score_game()
                self._playing = False

            if not self._playing:
                self._end.draw()
                self._hs.draw()
                leaderboard = open('score_board.txt', 'r')
                total = leaderboard.read()
                leaderboard.close()
                arcade.draw_text(total, 400, 400,
                                 arcade.color.BLACK, font_size=43, anchor_x="center", font_name="GARA")

        arcade.draw_text(time, 10, 680, arcade.color.BLACK, 25)

    def on_update(self, time):
        self._chef.update()
        self.time += time

    def on_key_press(self, key, mod):
        if self._playing:
            if key == arcade.key.LEFT:
                self._chef.change_x = -SPEED
            elif key == arcade.key.RIGHT:
                self._chef.change_x = +SPEED

    def on_key_release(self, key, mod):
        if self._playing:
            if key == arcade.key.LEFT:
                self._chef.change_x = 0
            elif key == arcade.key.RIGHT:
                self._chef.change_x = 0
            elif key == arcade.key.UP:
                self._held_item = arcade.Sprite("images/x.png", scale=10, center_x=500000, center_y=50000)
                self._items = []
                self._possible_points = 0
                self._hold = False

    def on_mouse_press(self, x, y, button, key_modifiers):
        if self._playing:
            if button == arcade.MOUSE_BUTTON_LEFT:
                if not self._hold:
                    #eggs
                    if x in range(550, 650, 1) and y in range(275, 338, 1):
                        self._hold = True
                        self._items.append("egg")
                        self._held_item = arcade.Sprite("images/egg.png", scale=1, center_x=750, center_y=630)
                    #bagels
                    elif x in range(550, 650, 1) and y in range(340, 381, 1):
                        self._hold = True
                        self._items.append("bagel")
                        self._held_item = arcade.Sprite("images/bagel.png", scale=1.5, center_x=750, center_y=630)
                    #complete order
                    elif x in range(340, 460, 1) and y in range(140, 190, 1):
                        self._hold = True
                        self._item = arcade.Sprite("images/x.png", scale=10, center_x=500000, center_y=50000)
                        # checks if order held is what the customer ordered
                        self.check_order()

            elif button == arcade.MOUSE_BUTTON_RIGHT:
                if self._hold:
                #check x and y of mouse to image
                    #stove
                    if x in range(340, 460, 1) and y in range(140, 190, 1):
                        #place item on stove
                        self.draw_item(self._items[-1])
                        self._held_item = arcade.Sprite("images/x.png", scale=10, center_x=500000, center_y=50000)

                    elif x in range(35, 175, 1) and y in range(20, 260, 1):
                        #checks if order held is what the customer ordered
                        self.check_order()
                        if self._correct_order:
                            arcade.play_sound(self._eat_sound)
                            self.refresh_order()
                            self._points += self._possible_points
                            self._possible_points = 0
                            self._held_item = arcade.Sprite("images/x.png", scale=10, center_x=500000, center_y=50000)
                            self._correct_order = False
                        elif not self._correct_order:
                            self._points -= 10
                            self._held_item = arcade.Sprite("images/x.png", scale=10, center_x=500000, center_y=50000)
                            self.refresh_order()
                            arcade.play_sound(self._wack_sound)
                    self._hold = False

                    #else:
                        #print something

    def draw_item(self, item):
        """draws item on stove"""
        if item == "egg" and len(self._items) == 1:
            self._item = arcade.Sprite("images/egg.png", scale=1, center_x=400, center_y=157)

        elif item == "bagel" and len(self._items) == 1:
            self._item = arcade.Sprite("images/bagel.png", scale=1.5, center_x=400, center_y=157)

        elif len(self._items) > 1 and self._items[0] == "bagel" and self._items[1] == "egg":
            self._item = arcade.Sprite("images/egg_bagel.png", scale=1.5, center_x=400, center_y=157)

        arcade.play_sound(self._cook_sound)

    def check_order(self):
        order = None
        if self._items[0] == "egg" and len(self._items) == 1:
            order = "egg"
            self._possible_points += 10
            self._held_item = arcade.Sprite("images/egg.png", scale=1, center_x=750, center_y=630)
        elif self._items[0] == "bagel" and len(self._items) == 1:
            order = "bagel"
            self._possible_points += 10
            self._held_item = arcade.Sprite("images/bagel.png", scale=1.5, center_x=750, center_y=630)
        elif self._items[0] == "bagel" and self._items[1] == "egg" and len(self._items) == 2:
            order = "egg bagel"
            self._possible_points += 20
            self._held_item = arcade.Sprite("images/egg_bagel.png", scale=1.5, center_x=750, center_y=630)

        if order == self._order_requested:
            self._correct_order = True

    def refresh_order(self):
        self._order_requested = random.choice(self._all_orders)
        if self._order_requested == "egg":
            self._order_image = arcade.Sprite("images/egg.png", scale=1, center_x=175, center_y=255)

        elif self._order_requested == "bagel":
            self._order_image = arcade.Sprite("images/bagel.png", scale=1.8, center_x=175, center_y=250)

        else:
            self._order_image = arcade.Sprite("images/egg_bagel.png", scale=1.8, center_x=175, center_y=250)

        self._order_image.draw()
        self._items = []


class End_Card(arcade.View):
    def __init__(self, score):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_SKY_BLUE)
        self._score = score
        self._check = True
        leaderboard = open('score_board.txt', 'r')
        self._total = leaderboard.read()

    def score_game(self):

        leaderboard = open('score_board.txt', 'r')

        scores = leaderboard.readlines()
        all = 'Old High Scores:\n'
        for score in scores:
            all += score
        print(all)
        total_score = ''
        space_loc = None
        new_score = ''
        self._complete = False
        old_score = None
        num = 0

        while num < len(scores):
            if scores[num] == 'Empty\n':
                new_score = input('Enter your name:')
                new_score = new_score + ': ' + str(self._score) + '\n'
                total_score += new_score
                while num < len(scores) - 1:
                    total_score += 'Empty\n'
                    num+= 1
                total_score = total_score[:-1]
                break

            elif scores[num] == 'Empty':
                new_score = input('Enter your name:')
                new_score = new_score + ': ' + str(self._score)
                total_score += new_score
                break

            elif self._score > int(scores[num][scores[num].find(' ') + 1:]):
                new_score = input('Enter your name:')
                new_score = new_score + ': ' + str(self._score) + '\n'
                total_score += new_score
                self._complete = True
                old_score = scores[num]
                for i in range(num + 1, len(scores), 1):
                    if scores[i] == 'Empty\n':
                        total_score += old_score
                    elif scores[i] == 'Empty':
                        total_score += old_score[:-1]
                    elif old_score[old_score.find(' ') + 1:] > scores[i][scores[i].find(' ') + 1:]:
                        total_score += old_score
                    elif old_score[old_score.find(' ') + 1:] < scores[i][scores[i].find(' ') + 1:]:
                        self._complete = False
                    else:
                        total_score += scores[i]
                    if self._complete:
                        old_score = scores[i]
                    else:
                        total_score += scores[i]
                    num+=1
                break
            else:
                total_score += scores[num]
            num += 1
        if total_score[-1] == '\n':
            total_score = total_score[:-1]


        print('High Scores:\n', total_score)
        total = total_score
        self._total = total_score
        leaderboard.close()

        leaderboard = open('score_board.txt', 'w')
        leaderboard.write(total_score)
        leaderboard.close()

    def get_total(self):
        leaderboard = open('score_board.txt', 'r')
        total = leaderboard.read()
        leaderboard.close()
        return total


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start = Start_Card()
    window.show_view(start)
    arcade.run()


if __name__ == '__main__':
    main()
