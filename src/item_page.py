from definitions import Types, Direction
from spritesheet import Spritesheet


class TempItem(object):
    '''
    :type gc: GameController
    :return: None
    '''
    NAME = None
    def __init__(self, gc):
        self.gc = gc
        self.name = self.NAME
        self.sell_price = 0
        self.image_size_x = 90
        self.image_size_y = 76
        # spritesheet = Spritesheet("items", "assets/spritesheets/item_spritesheets/food_images.png", 24, 24).get_image(0, 0)
        # base = Spritesheet("base", "assets/spritesheets/menu_spritesheets/yes_no_menu.png", self.image_size_x, self.image_size_y).get_image(0, 0)
        spritesheet = None
        base = None
        # base.blit(spritesheet, [30, 20])
        # self.menu_image = base

    def item_use(self):
        pass

    def use_requirements(self):
        result = True
        return result

    def fail_to_use_item(self):
        self.gc.update_game_dialogue("You can't use that now")


class Cheese(TempItem):
    NAME = "Cheese"

    def __init__(self, gc):
        super().__init__(gc)
        self.sell_price = 5

    def item_use(self):
        self.gc.menu_controller.post_notice("The " + self.NAME + " healed 20 HP")

    def use_requirements_met(self):
        result = True
        # if self.gc.gs.current_inventory[self.NAME]["quantity"] > 0:
        #     result = True
        return result

    def fail_to_use_item(self):
        pass


class Egg(Cheese):
    NAME = "Egg"

    def __init__(self, gc):
        super().__init__(gc)


class Rice(Cheese):
    NAME = "Rice"

    def __init__(self, gc):
        super().__init__(gc)


class Meat(Cheese):
    NAME = "Meat"

    def __init__(self, gc):
        super().__init__(gc)


class Pizza(Cheese):
    NAME = "Pizza"

    def __init__(self, gc):
        super().__init__(gc)


class Card(Cheese):
    NAME = "Card"

    def __init__(self, gc):
        super().__init__(gc)


class Game(Cheese):
    NAME = "Game"

    def __init__(self, gc):
        super().__init__(gc)


class Match(Cheese):
    NAME = "Match"

    def __init__(self, gc):
        super().__init__(gc)


class Mouse(Cheese):
    NAME = "Mouse"

    def __init__(self, gc):
        super().__init__(gc)


class Spoon(Cheese):
    NAME = "Spoon"

    def __init__(self, gc):
        super().__init__(gc)


class Mike(Cheese):
    NAME = "Mike"

    def __init__(self, gc):
        super().__init__(gc)


class Orange(Cheese):
    NAME = "Orange"

    def __init__(self, gc):
        super().__init__(gc)


class Apple(Cheese):
    NAME = "Apple"

    def __init__(self, gc):
        super().__init__(gc)
        spritesheet = Spritesheet("items", "assets/spritesheets/item_spritesheets/food_images.png", 24, 24).get_image(1, 0)
        base = Spritesheet("base", "assets/spritesheets/menu_spritesheets/yes_no_menu.png", 90, 76).get_image(0, 0)
        base.blit(spritesheet, [30, 20])
        self.menu_image = base


class Banana(Cheese):
    NAME = "Banana"

    def __init__(self, gc):
        super().__init__(gc)


class Cream(Cheese):
    NAME = "Cream"

    def __init__(self, gc):
        super().__init__(gc)


class Milk(Cheese):
    NAME = "Milk"

    def __init__(self, gc):
        super().__init__(gc)



class KeyItem(object):
    '''
    :type gc: GameController
    :return: None
    '''
    NAME = None
    def __init__(self, gc):
        self.gc = gc
        self.name = self.NAME
        self.image_size_x = 90
        self.image_size_y = 76
        spritesheet = Spritesheet("items", "assets/spritesheets/item_spritesheets/food_images.png", 24, 24).get_image(0, 0)
        base = Spritesheet("base", "assets/spritesheets/menu_spritesheets/yes_no_menu.png", self.image_size_x, self.image_size_y).get_image(0, 0)
        base.blit(spritesheet, [30, 20])
        self.menu_image = base

    def item_use(self, details):
        pass

    def use_requirements_met(self, details):
        result = True
        return result

    def fail_to_use_item(self):
        self.gc.update_game_dialogue("You can't use that now")


class Hammer(KeyItem):
    NAME = "Hammer"

    def __init__(self, gc):
        super().__init__(gc)

    def item_use(self, details):
        self.gc.position_manager.despawn_feature(details["adjacent_tile_filling"], details["room"])

    def use_requirements_met(self, details):
        result = False
        if details["filling_type"] == "Rock":
            result = True
        return result

    def get_success_message(self, details):
        return "You used the Hammer"

    def get_failure_message(self, details):
        message = None
        if details["filling_subtype"] == Types.CHARACTER:
            message = "That's a disgusting idea."
        else:
            message = "You can't use the Hammer now"

        return message

class MermaidCrown(KeyItem):
    NAME = "Mermaid Crown"

    def __init__(self, gc):
        super().__init__(gc)


class GhostEye(KeyItem):
    NAME = "Ghost Eye"

    def __init__(self, gc):
        super().__init__(gc)


class Shovel(KeyItem):
    NAME = "Shovel"

    def __init__(self, gc):
        super().__init__(gc)


class Pickaxe(KeyItem):
    NAME = "Pickaxe"

    def __init__(self, gc):
        super().__init__(gc)

    def item_use(self, details):
        self.gc.pickaxe_make_door()

    def use_requirements_met(self, details):
        result = self.gc.check_if_pickaxe_worked()
        return result

    def get_success_message(self, details):
        return "You used the Pickaxe"

    def get_failure_message(self, details):
        message = None
        if details["filling_subtype"] == Types.CHARACTER:
            message = "That's a disgusting idea."

        elif details["adjacent_tile_terrain"] == self.gc.gs.gd.get_terrain_number_or_word(None, "wall")[0] and self.gc.gs.get_player_ghost().facing == Direction.UP:
            message = "The wall appears to be solid"
            self.gc.play_sound("pickaxe_fail")
        else:
            message = "You can't use the Pickaxe now"

        return message


class ArbutusPermit(KeyItem):
    NAME = "Arbutus Permit"

    def __init__(self, gc):
        super().__init__(gc)


class OakPermit(KeyItem):
    NAME = "Oak Permit"

    def __init__(self, gc):
        super().__init__(gc)


class PinePermit(KeyItem):
    NAME = "Pine Permit"

    def __init__(self, gc):
        super().__init__(gc)

class Wrench(KeyItem):
    NAME = "Wrench"

    def __init__(self, gc):
        super().__init__(gc)

class GreenSeed(KeyItem):
    NAME = "Green_Seed"

    def __init__(self, gc):
        super().__init__(gc)

class YellowSeed(KeyItem):
    NAME = "Yellow_Seed"

    def __init__(self, gc):
        super().__init__(gc)

class RedSeed(KeyItem):
    NAME = "Red_Seed"

    def __init__(self, gc):
        super().__init__(gc)

class PurpleSeed(KeyItem):
    NAME = "Purple_Seed"

    def __init__(self, gc):
        super().__init__(gc)

class OrangeSeed(KeyItem):
    NAME = "Orange_Seed"

    def __init__(self, gc):
        super().__init__(gc)

class PinkSeed(KeyItem):
    NAME = "Pink_Seed"

    def __init__(self, gc):
        super().__init__(gc)


class Axe(KeyItem):
    NAME = "Axe"

    def __init__(self, gc):
        super().__init__(gc)

    def item_use(self, details):
        self.gc.position_manager.despawn_feature(details["adjacent_tile_filling"], details["room"])

    def use_requirements_met(self, details):
        result = False
        if details["filling_type"] in ["Tree", "Pine", "Arbutus", "Oak"]:
            result = True
        return result

    def get_success_message(self, details):
        return "Used Axe to cut down " + details["filling_type"]

    def get_failure_message(self, details):
        message = None
        print(details["filling_type"])
        if details["filling_type"] == Types.ACTOR:
            message = "That's a disgusting idea."
        else:
            message = "You can't use the Axe now"

        return message


class BirdPage(object):
    '''
    :type gc: GameController
    :return: None
    '''
    def __init__(self, gc, bird, segment, colour, size, call, approach):
        self.gc = gc
        self.bird = bird
        self.segment = segment
        self.page_name = bird + segment
        self.colour = colour
        self.size = size
        self.call = call
        self.approach = approach
