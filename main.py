import arcade

SPRITE_SCALING = 0.5
NPC_SCALING = 0.8
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

TALK_DISTANCE = 100

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Mohg Quest"

MOVEMENT_SPEED = 5

BACKGROUND_1 = arcade.load_texture("assets/images/mohgwynpalacebg.png")
BACKGROUND_2 = arcade.load_texture("assets/images/MPBG2.png")


class Room:
    def __init__(self, background):
        self.wall_list = arcade.SpriteList()
        self.background = background

def setup_room_1():
    room = Room(BACKGROUND_1)
    return room

def setup_room_2():
    room = Room(BACKGROUND_2)
    return room

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.current_room = 0

        self.rooms = None
        self.player_sprite = None
        self.player_list = None
        self.physics_engine = None

    def setup(self):
        self.player_sprite = arcade.Sprite(
            "assets/images/ansbach.png",
            scale=SPRITE_SCALING,
        )
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 100
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.npc_sprite = arcade.Sprite(
            "assets/images/mohg.PNG",
            scale=NPC_SCALING
        )

        self.npc_sprite.center_x = 100
        self.npc_sprite.center_y = 150
        self.npc_list = arcade.SpriteList()
        self.npc_list.append(self.npc_sprite)

        self.rooms = []

        room = setup_room_1()
        self.rooms.append(room)

        room = setup_room_2()
        self.rooms.append(room)

        self.current_room = 0

        # Create a physics engine for this room
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            self.rooms[self.current_room].wall_list,
        )

        self.dialogue_lines = [
            "Dearest Ansbach...it seems we have a Tarnished visitor. Would you attend to them, please?",
            "At once, Lord Mohg.",
            "Thank you. Return to me when the deed is done."
        ]
        self.dialogue_index = 0
        self.show_dialogue = False
        self.dialogue_text = ""

        self.quest_given = False
    
    def display_dialogue(self, text):
        self.dialogue_text = text
        self.show_dialogue = True

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.rooms[self.current_room].background,
            rect=arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
        )

        self.rooms[self.current_room].wall_list.draw()

        self.player_list.draw()
        self.npc_list.draw()

        if self.show_dialogue:
            arcade.draw_lrbt_rectangle_filled(250, WINDOW_WIDTH, 0, 150, arcade.color.BLACK)
            arcade.draw_text(self.dialogue_text, 270, 100, arcade.color.WHITE, 16)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.E:
            distance = arcade.get_distance_between_sprites(self.player_sprite, self.npc_sprite)
            if distance < TALK_DISTANCE:
                if self.quest_given and not self.show_dialogue:
                    self.display_dialogue("Back so soon? Did you wish for a kiss before you left, my dear?")
                    return
                if not self.show_dialogue:
                    self.show_dialogue = True
                    self.dialogue_index = 0
                else:
                    self.dialogue_index += 1
                if self.dialogue_index < len(self.dialogue_lines):
                    self.display_dialogue(self.dialogue_lines[self.dialogue_index])
                else:
                    self.show_dialogue = False
                    self.quest_given = True

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):

        self.physics_engine.update()

        if self.player_sprite.center_x > WINDOW_WIDTH and self.current_room == 0:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(
                self.player_sprite,
                self.rooms[self.current_room].wall_list,
            )
            self.player_sprite.center_x = 0
        elif self.player_sprite.center_x < 0 and self.current_room == 1:
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(
                self.player_sprite,
                self.rooms[self.current_room].wall_list,
            )
            self.player_sprite.center_x = WINDOW_WIDTH


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    game = GameView()
    game.setup()

    window.show_view(game)

    arcade.run()


if __name__ == "__main__":
    main()