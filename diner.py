import arcade
import random

SCREEN_WIDTH = 825
SCREEN_HEIGHT = 725
SCREEN_TITLE = "Diner"
SPEED = 10


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.WHITE)

        self._cook_sound = None
        self._eat_sound = None

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

        self._points = 0
        self._possible_points = 0
        self.time = 0

        self._items = []
        self._all_orders = ["egg bagel", "egg", "bagel"]
        self._order_requested = random.choice(self._all_orders)
        #boolian used to check if chef has item
        self._hold = False
        #boolian used to check if chef has the correct order for customer
        self._correct_order = False

    def setup(self):
        self._cook_sound = arcade.load_sound("audio/sizzle.mp3")

        self._eat_sound = arcade.load_sound("audio/eat.mp3")

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

        # Messages
        points = f"Hill Card Points:\n {self._points}"
        arcade.draw_text(points, 600, 70, arcade.color.BLACK, 20)

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

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if not self._hold:
                #eggs
                if x in range(550, 650, 1) and y in range(275, 338, 1):
                    print('hello')
                    self._hold = True
                    self._items.append("egg")
                #bagels
                elif x in range(550, 650, 1) and y in range(340, 381, 1):
                    print('hello')
                    self._hold = True
                    self._items.append("bagel")
                #complete order
                elif x in range(340, 460, 1) and y in range(140, 190, 1):
                    self._hold = True
                    self._item = arcade.Sprite("images/x.png", scale=10, center_x=500000, center_y=50000)

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            if self._hold:
            #check x and y of mouse to image
                #stove
                if x in range(340, 460, 1) and y in range(140, 190, 1):
                    #place item on stove
                    self.draw_item(self._items[-1])

                elif x in range(35, 175, 1) and y in range(20, 260, 1):
                    #checks if order held is what the customer ordered
                    self.check_order()
                    if self._correct_order:
                        arcade.play_sound(self._eat_sound)
                        self.refresh_order()
                        self._points += self._possible_points
                        self._possible_points = 0
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
        elif self._items[0] == "bagel" and len(self._items) == 1:
            order = "bagel"
            self._possible_points += 10
        elif self._items[0] == "bagel" and self._items[1] == "egg" and len(self._items) == 2:
            order = "egg bagel"
            self._possible_points += 20

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
