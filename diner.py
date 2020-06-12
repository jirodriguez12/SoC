import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Diner"
SPEED = 10


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.APPLE_GREEN)
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

        self._stove_x = 400
        self._stove_y = 0

        self._items = []
        self._all_orders = ["egg bagel", "egg", "bagel"]
        self._order_requested = random.choice(self._all_orders)
        #boolian used to check if chef has item
        self._hold = False
        #boolian used to check if chef has the correct order for customer
        self._correct_order = False

    def setup(self):
        self._background = arcade.Sprite("images/diners.png", scale=1, center_x=0, center_y=0)

        self._chef = arcade.Sprite("images/chef.png", scale=0.5, center_x=0, center_y=0)

        self._counter = arcade.Sprite("images/counter.png", scale=1, center_x=0, center_y=0)

        self._stove = arcade.Sprite("images/stove.png", scale=1, center_x=-self._stove_x, center_y=self._stove_y)

        self._egg_carton = arcade.Sprite("images/egg_carton.png", scale=0.2, center_x=0, center_y=0)

        self._bagels = arcade.Sprite("images/bagels.png", scale=0.2, center_x=0, center_y=0)

        self._customer = arcade.Sprite("images/customer.png", scale=0.5, center_x=400, center_y=0)

        self._thought = arcade.Sprite("images/thought.png", scale=0.7, center_x=400, center_y=50)

        self.refresh_order()


    def on_draw(self):
        arcade.start_render()
        self._background.draw()
        self._chef.draw()
        self._counter.draw()
        self._stove.draw()
        self._egg_carton.draw()
        self._bagels.draw()

    # def on_update(self, time):
    #     self._chef.update()
    #     self.time += time

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

    def on_mouse_press(self, x, y, button, key_modifiers):
        if self._hold:
            if button == self._stove:
                pass
                #place item on stove
                self.draw_item(self._items[-1])

            elif button == self._customer:
                #checks if order held is what the customer ordered
                self.check_order()
                if self._correct_order:
                    self.refresh_order()
            self._hold = False

            #else:
                #print something
        else:
            if button == self._egg_carton:
                self._hold = True
                self._items.append("egg")

            elif button == self._bagels:
                self._hold = True
                self._items.append("bagel")

            elif button == self._item:
                self._hold = True

    def draw_item(self, item):
        """draws item on stove"""
        if item == "egg":
            self._item = arcade.Sprite("images/egg.png", scale=0.1, center_x=self._stove_x, center_y=self._stove_y)
        elif item == "bagel":
            self._item = arcade.Sprite("images/bagel.png", scale=0.1, center_x=self._stove_x, center_y=self._stove_y)

        self._item.draw()

    def check_order(self):
        order = None
        if self._items[0] == "bagel" and self._items[1] == "egg" and len(self._items) == 2:
            order = "egg bagel"
        elif self._items[0] == "egg" and len(self._items) == 1:
            order = "egg"
        elif self._items[0] == "bagel" and len(self._items) == 1:
            order = "bagel"

        if order == self._order_requested:
            self._correct_order = True

    def refresh_order(self):
        self._order_requested = random.choice(self._all_orders)
        if self._order_requested == "egg":
            self._order_image = arcade.Sprite("images/egg.png", scale=0.1, center_x=0, center_y=0)
        elif self._order_requested == "bagel":
            self._order_image = arcade.Sprite("images/bagel.png", scale=0.1, center_x=0, center_y=0)
        elif self._order_requested == "egg_bagel":
            self._order_image = arcade.Sprite("images/egg_bagel.png", scale=0.1, center_x=0, center_y=0)

        self._order_image.draw()
        self._items = []



def main():
    window = Game()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
