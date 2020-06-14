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


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.WHITE)

        #audio initializations
        self._cook_sound = None
        self._eat_sound = None
        self._wack_sound = None

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

        #updates player movement
        self.time = 0

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

    def on_update(self, time):
        self._chef.update()
        self.time += time

    def on_key_press(self, key, mod):
        if key == arcade.key.LEFT:
            self._chef.change_x = -SPEED
        elif key == arcade.key.RIGHT:
            self._chef.change_x = +SPEED

    def on_key_release(self, key, mod):
        if key == arcade.key.LEFT:
            self._chef.change_x = 0
        elif key == arcade.key.RIGHT:
            self._chef.change_x = 0
        elif key == arcade.key.UP:
            self._held_item = arcade.Sprite("images/x.png", scale=10, center_x=500000, center_y=50000)
            self._items = []
            self._hold = False

    def on_mouse_press(self, x, y, button, key_modifiers):
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
                        self._points -= 100000
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



def main():
    window = Game()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
