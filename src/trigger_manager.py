import copy


class TriggerManager(object):
    def __init__(self, gc):
        self.gc = gc
        self.trigger_list = {}

    def setup_trigger_list(self):
        for room in self.gc.game_data.room_data_list.values():
            self.gc.gs.trigger_list[room.room_name] = {}
            for tile in room.return_list_all_cubes():
                self.gc.gs.trigger_list[room.room_name][(tile.x, tile.y)] = []

    def add_triggers(self, room_object, trigger_dict):
        for key in trigger_dict.keys():
            if self.check_if_coord_outside_room(key, room_object):
                pass
            else:
                coords = (key[0], key[1])
                self.gc.gs.trigger_list[room_object.room_name][coords].append(trigger_dict[key])

    def check_if_coord_outside_room(self, coords, room_object):
        outside = False
        if (coords[0] > room_object.x_size) or coords[0] < 1 or (coords[1] > room_object.y_size) or coords[1] < 1:
            outside = True
        else:
            pass
        return outside

    def update_features_triggers(self, room_object, feature_ghost):
        remove_trigger_list = copy.copy(feature_ghost.trigger_list)
        self.remove_triggers(room_object, feature_ghost)
        add_trigger_list = feature_ghost.produce_trigger_list()
        self.add_triggers(room_object, add_trigger_list)

    def print_all_triggers(self, room_object):
        print(self.gc.gs.trigger_list[room_object.room_name])

    def remove_all_triggers(self, room_object):
        for tile in self.gc.gs.trigger_list[room_object.room_name]:
            self.gc.gs.trigger_list[room_object.room_name][tile].clear()

    def remove_triggers(self, room_object, feature_ghost):
        tracker = 0
        for existing_trigger in self.gc.gs.trigger_list[room_object.room_name].values():
            for trigger in existing_trigger:
                if trigger[0] == feature_ghost.unique_name:
                    existing_trigger.pop(existing_trigger.index(trigger))
                    tracker += 1

    def check_for_map_triggers(self, player_x, player_y):
        room = self.gc.gs.get_current_room()
        triggers = copy.copy(self.check_for_triggers(room, player_x, player_y))
        for trigger in triggers:
            self.gc.trigger_a_bird(trigger[0], room, trigger[1])

    def check_for_triggers(self, room_object, x, y):
        return self.gc.gs.trigger_list[room_object.room_name][x, y]

    def advanced_trigger_test(self, bird_species_name):
        advanced_test = False
        if bird_species_name == "Seagull":
            # checks to see if there is more than one Seagull currently active on the map
            features_in_room = self.gc.gs.get_all_features_in_room(self.gc.gs.get_current_room().room_name)
            seagull_count = 0
            for feature in features_in_room:
                if feature.special_designation != "Player":
                    if feature.active and feature.species == "Seagull":
                        seagull_count += 1

            if seagull_count <= 1:
                advanced_test = True

        else:
            advanced_test = True
        return advanced_test