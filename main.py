import arcade
from constants import *
from rooms import Room1, Room2

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.current_room = 0

        self.rooms = None
        self.player_sprite = None
        self.player_list = None
        self.physics_engine = None

        self.music = arcade.load_sound("assets/sounds/BGM1.ogg", streaming=True)
        arcade.play_sound(self.music, volume=0.1, loop=True)

    def setup(self):
        self.player_sprite = arcade.Sprite(
            "assets/images/ansbach.png",
            scale=SPRITE_SCALING,
        )
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 100
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)


        self.rooms = []
        self.rooms.append(Room1())
        self.rooms.append(Room2())

        self.current_room = 0

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            self.rooms[self.current_room].wall_list,
        )

        self.quest_given = False

    def on_draw(self):
        self.clear()
    
        current_room = self.rooms[self.current_room]

        arcade.draw_texture_rect(
        current_room.background,
        rect=arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
        )

        current_room.wall_list.draw()
        current_room.room_sprites.draw()

        self.player_list.draw()
        
        current_room.draw_ui(self.player_sprite)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.scale_x = -SPRITE_SCALING
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.scale_x = SPRITE_SCALING
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.E:
            current_room = self.rooms[self.current_room]
            if hasattr(current_room, "npc_sprite"):
                distance = arcade.get_distance_between_sprites(self.player_sprite, current_room.npc_sprite)
                if distance < TALK_DISTANCE:
                    if self.quest_given and not current_room.show_dialogue:
                        current_room.speaker_text_object.text = "Mohg, Lord of Blood"
                        current_room.dialogue_text_object.text = "Back so soon? Did you wish for a kiss before you left, my dear?"
                        current_room.show_dialogue = True
                        return
                    if not current_room.show_dialogue:
                        current_room.dialogue_index = 0
                        current_room.show_dialogue = True
                        current_room.update_dialogue()
                    else:
                        current_room.dialogue_index += 1
                        if current_room.dialogue_index < len(current_room.dialogue_lines):
                            current_room.update_dialogue()
                        else:
                            current_room.show_dialogue = False
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