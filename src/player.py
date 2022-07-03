from game_core import Definitions


class Player(object):
    ID = "Player"
    FEATURE_TYPE = "Player"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = "Jayden"
        self.cur_img = 0
        self.spritesheet = Spritesheet("assets/player/Player_CS.png", 32, 40)
        self.img = self.spritesheet.get_image(0, 0)
        self.state = "idle"
        self.facing = Definitions.DOWN

        self.drawing_priority = 2
        self.image_offset_y = 0
        self.image_offset_x = 0
        self.img_width = None
        self.img_height = None
        self.base_size_y = 1
        self.base_size_x = 1

    def set_image(self, img_x, img_y):
        self.img = self.spritesheet.get_image(img_x, img_y)


class Player(Feature):
    NAME = "Player"

    def __init__(self, x, y):
        super().__init__(x, y)

        self.width = 32
        self.height = 40
        self.spritesheet =
        self.img = self.spritesheet.get_image(0, 0)
        self.name = self.NAME
        self.current_outfit = "Normal Outfit"
        self.offset_y = 16

    def load_location(self):
        ss_data = self.gd_input.spreadsheet_list["player_location"].spreadsheet_load_location()
        self.x = ss_data["player_x"]
        self.y = ss_data["player_y"]
        self.imagex = ss_data["player_image_x"]
        self.imagey = ss_data["player_image_y"]

    def put_on_outfit(self, new_outfit_spritesheet, name):
        self.spritesheet = new_outfit_spritesheet
        if self.facing == Definitions.DOWN:
            self.img = self.spritesheet.get_image(0, 0)
        if self.facing == Definitions.UP:
            self.img = self.spritesheet.get_image(0, 1)
        if self.facing == Definitions.RIGHT:
            self.img = self.spritesheet.get_image(0, 2)
        if self.facing == Definitions.LEFT:
            self.img = self.spritesheet.get_image(0, 3)
        self.current_outfit = name

    def teleport_to_ringside(self):
        self.empty_tile_standing()
        self.gc_input.current_room = "Ringside"
        self.x = 80
        self.y = 80
        self.gc_input.camera[0] = 0 - self.x
        self.gc_input.camera[1] = 0 - self.y

    def teleport_to_sandpiper(self):
        self.empty_tile_standing()
        self.gc_input.current_room = "Sandpiper"
        self.x = 22
        self.y = 60
        self.gc_input.camera[0] = 0 - self.x
        self.gc_input.camera[1] = 0 - self.y

    def empty_tile_standing(self):
        self.gd_input.positioner_list[self.gc_input.current_room].empty_tile(self)

    def activate_timer(self):
        pygame.time.set_timer(self.step_timer, 20)

    def draw(self, screen):
        self_x = (self.imagex * self.gd_input.square_size[0]) + self.gd_input.base_locator_x
        self_y = ((self.imagey * self.gd_input.square_size[1]) - self.offset_y) + self.gd_input.base_locator_y
        screen.blit(self.img, [(self.imagex * self.gd_input.square_size[0]) + self.gd_input.base_locator_x,
                               ((self.imagey * self.gd_input.square_size[1]) - self.offset_y) + self.gd_input.base_locator_y])

    def try_door(self, direction):
        self.direction = direction
        the_tile = self.check_adj_tile(self.direction).object_filling
        self.gd_input.positioner_list[self.gc_input.current_room].through_door(self.gd_input.room_list[self.gc_input.current_room].door_list[the_tile])
        self.set_state("idle")

    def try_walk(self, direction):
        self.turn_player(direction)

        # checks mapClasses - position_manager to see if the player is facing a wall or another object
        can_move_player = self.gd_input.positioner_list[self.gc_input.current_room].check_adj_square_full(self, direction)

        # Check if player is going to enter a door
        is_door = self.gd_input.positioner_list[self.gc_input.current_room].check_door(self, direction)
        if is_door:
            self.try_door(direction)

        #  checks to make sure the character doesn't have any obstacles in the direction they want to move
        elif can_move_player:
            self.walk_player(direction)

    def turn_player(self, direction):
        if direction is Definitions.LEFT:
            self.set_image(0, 3)
            self.facing = Definitions.LEFT
        elif direction is Definitions.RIGHT:
            self.set_image(0, 2)
            self.facing = Definitions.RIGHT
        elif direction is Definitions.UP:
            self.set_image(0, 1)
            self.facing = Definitions.UP
        elif direction is Definitions.DOWN:
            self.set_image(0, 0)
            self.facing = Definitions.DOWN

    def walk_player(self, direction):
        self.state = direction

        self.gd_input.positioner_list[self.gc_input.current_room].empty_tile(self)
        if direction is Definitions.LEFT:
            self.x -= 1
        elif direction is Definitions.RIGHT:
            self.x += 1
        elif direction is Definitions.UP:
            self.y -= 1
        elif direction is Definitions.DOWN:
            self.y += 1
        self.gd_input.positioner_list[self.gc_input.current_room].fill_tile(self)

    def walk_cycle(self):
        row = 0
        relevant_camera = None
        movement = 0
        if self.state == Definitions.LEFT:
            row = 3
            relevant_camera = 0
            movement = 1 / 4
        elif self.state == Definitions.RIGHT:
            row = 2
            relevant_camera = 0
            movement = -1 / 4
        elif self.state == Definitions.DOWN:
            row = 0
            relevant_camera = 1
            movement = -1 / 4
        elif self.state == Definitions.UP:
            row = 1
            relevant_camera = 1
            movement = 1 / 4

        if 0 <= self.cur_img < 3:
            self.cur_img += 1
            self.set_image(self.cur_img, row)
            self.gc_input.camera[relevant_camera] += movement

        elif self.cur_img == 3:
            self.cur_img = 0
            self.set_image(self.cur_img, row)
            self.gc_input.camera[relevant_camera] += movement
            self.set_state("idle")

        else:
            self.cur_img = 0
            self.set_image(0, row)

    def continue_walking(self):
        if self.state in [Definitions.LEFT, Definitions.RIGHT, Definitions.UP, Definitions.DOWN]:
            self.walk_cycle()

    def check_if_walking(self):
        if self.state in [Definitions.LEFT, Definitions.RIGHT, Definitions.UP, Definitions.DOWN]:
            return True
        else:
            return False

    def check_adj_tile(self, direction_to_check):
        self.direction_to_check = direction_to_check

        adj_tile_y = int(self.y)
        adj_tile_x = int(self.x)

        if direction_to_check == Definitions.UP:
            adj_tile_y = int(self.y - 1)

        elif direction_to_check == Definitions.DOWN:
            adj_tile_y = int(self.y + 1)

        elif direction_to_check == Definitions.LEFT:
            adj_tile_x = int(self.x - 1)

        elif direction_to_check == Definitions.RIGHT:
            adj_tile_x = int(self.x + 1)

        adj_tile = self.gd_input.room_list[self.gc_input.current_room].tiles_array[adj_tile_x][adj_tile_y]

        return adj_tile

    def interact_with(self):
        print("I'm interacting")
        facing_tile = self.check_adj_tile(self.facing)
        object_filling = facing_tile.object_filling
        filling_type = facing_tile.filling_type
        full = facing_tile.full

        if full:
            if filling_type in ["Generic_NPC", "NPC"]:
                self.gd_input.character_list[object_filling].get_interacted_with()

            elif filling_type == "Prop":
                self.gd_input.prop_list[object_filling].get_interacted_with()

            elif filling_type == "Door":
                pass

            else:
                pass

    def set_state(self, state_to_set):
        self.state = state_to_set

    def perform_diagnostic(self):
        # Player Image Location:
        print("PlayerImg: " + "(" + str(self.imagex) + ", " + str(self.imagey) + ")", "Camera: " +"(" + str(self.gc_input.camera[0]) + ", " + str(self.gc_input.camera[1]) + ")", "Player: " + "(" + str(self.x) + ", " + str(self.y) + ")")
        print("CharacterImg: " + "(" + str(self.gd_input.character_list["Jamara"].imagex) + ", " + str(self.gd_input.character_list["Jamara"].imagey) + ")", "Character: " + "(" + str(self.gd_input.character_list["Jamara"].x) + ", " + str(self.gd_input.character_list["Jamara"].y) + ")")

