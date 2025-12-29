from spritesheet import Spritesheet


class TempItem(object):
    '''
    :type gc_input: GameController
    :return: None
    '''
    NAME = None
    def __init__(self, gc_input):
        self.gc_input = gc_input
        self.name = self.NAME
        self.sell_price = 0
        self.image_size_x = 90
        self.image_size_y = 76
        spritesheet = Spritesheet("items", "assets/spritesheets/item_spritesheets/food_images.png", 24, 24).get_image(0, 0)
        base = Spritesheet("base", "assets/spritesheets/menu_spritesheets/yes_no_menu.png", self.image_size_x, self.image_size_y).get_image(0, 0)
        base.blit(spritesheet, [30, 20])
        self.menu_image = base

    def item_use(self):
        pass

    def use_requirements(self):
        result = True
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("You can't use that now")


class Cheese(TempItem):
    NAME = "Cheese"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        self.sell_price = 5

    def item_use(self):
        self.gc_input.menu_manager.post_notice("The " + self.NAME + " healed 20 HP")

    def use_requirements(self):
        result = True
        # if self.gc_input.game_state.current_inventory[self.NAME]["quantity"] > 0:
        #     result = True
        return result

    def fail_to_use_item(self):
        pass


class Egg(Cheese):
    NAME = "Egg"

    def __init__(self, gc_input):
        super().__init__(gc_input)


class Rice(Cheese):
    NAME = "Rice"

    def __init__(self, gc_input):
        super().__init__(gc_input)


class Meat(Cheese):
    NAME = "Meat"

    def __init__(self, gc_input):
        super().__init__(gc_input)


class Pizza(Cheese):
    NAME = "Pizza"

    def __init__(self, gc_input):
        super().__init__(gc_input)


class Card(Cheese):
    NAME = "Card"

    def __init__(self, gc_input):
        super().__init__(gc_input)


class Game(Cheese):
    NAME = "Game"

    def __init__(self, gc_input):
        super().__init__(gc_input)


class Match(Cheese):
    NAME = "Rice"

    def __init__(self, gc_input):
        super().__init__(gc_input)


class Mouse(Cheese):
    NAME = "Mouse"

    def __init__(self, gc_input):
        super().__init__(gc_input)


class Spoon(Cheese):
    NAME = "Spoon"

    def __init__(self, gc_input):
        super().__init__(gc_input)


class Mike(Cheese):
    NAME = "Mike"

    def __init__(self, gc_input):
        super().__init__(gc_input)


class Orange(Cheese):
    NAME = "Orange"

    def __init__(self, gc_input):
        super().__init__(gc_input)


class Apple(Cheese):
    NAME = "Apple"

    def __init__(self, gc_input):
        super().__init__(gc_input)
        spritesheet = Spritesheet("items", "assets/spritesheets/item_spritesheets/food_images.png", 24, 24).get_image(1, 0)
        base = Spritesheet("base", "assets/spritesheets/menu_spritesheets/yes_no_menu.png", 90, 76).get_image(0, 0)
        base.blit(spritesheet, [30, 20])
        self.menu_image = base


class Banana(Cheese):
    NAME = "Banana"

    def __init__(self, gc_input):
        super().__init__(gc_input)


class Cream(Cheese):
    NAME = "Cream"

    def __init__(self, gc_input):
        super().__init__(gc_input)


class Milk(Cheese):
    NAME = "Milk"

    def __init__(self, gc_input):
        super().__init__(gc_input)



class KeyItem(object):
    '''
    :type gc_input: GameController
    :return: None
    '''
    NAME = None
    def __init__(self, gc_input):
        self.gc_input = gc_input
        self.name = self.NAME
        self.image_size_x = 90
        self.image_size_y = 76
        spritesheet = Spritesheet("items", "assets/spritesheets/item_spritesheets/food_images.png", 24, 24).get_image(0, 0)
        base = Spritesheet("base", "assets/spritesheets/menu_spritesheets/yes_no_menu.png", self.image_size_x, self.image_size_y).get_image(0, 0)
        base.blit(spritesheet, [30, 20])
        self.menu_image = base

    def item_use(self):
        pass

    def use_requirements(self):
        result = True
        return result

    def fail_to_use_item(self):
        self.gc_input.update_game_dialogue("You can't use that now")


class Hammer(KeyItem):
    NAME = "Hammer"

    def __init__(self, gc_input):
        super().__init__(gc_input)


class Shovel(KeyItem):
    NAME = "Shovel"

    def __init__(self, gc_input):
        super().__init__(gc_input)


class Wrench(KeyItem):
    NAME = "Wrench"

    def __init__(self, gc_input):
        super().__init__(gc_input)
