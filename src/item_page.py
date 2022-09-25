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
        self.gc_input.post_notice("The " + self.NAME + " healed 20 HP")

    def use_requirements(self):
        result = False
        if self.gc_input.game_state.current_inventory[self.NAME]["quantity"] > 1:
            result = True
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

