import arcade
import os
from constants import *


BACKGROUND_1 = arcade.load_texture("assets/images/MPBG.png")
BACKGROUND_2 = arcade.load_texture("assets/images/MPBG2.png")

class Room:
    def __init__(self, background):
        self.background = background
        self.wall_list = arcade.SpriteList()
        self.room_sprites = arcade.SpriteList()
    
    def draw_ui(self, player):
        pass
    
class Room1(Room):
    def __init__(self):
        super().__init__(BACKGROUND_1)

        self.npc_sprite = arcade.Sprite(
            "assets/images/mohg.PNG",
            scale=NPC_SCALING
        )

        self.npc_sprite.center_x = 100
        self.npc_sprite.center_y = 150
        self.room_sprites.append(self.npc_sprite)

        arcade.load_font("assets/fonts/Quintessential-Regular.ttf")

        self.tutorial_text_object = arcade.Text(
            text="Talk [E]",
            x=50,
            y= 300,
            color=arcade.color.WHITE,
            font_size=40,
            font_name="Quintessential"
        )

        self.speaker_text_object = arcade.Text(
            text="Mohg, Lord of Blood",
            x=275,
            y=160,
            color=arcade.color.RED,
            font_size=20,
            font_name="Quintessential"
        )

        self.dialogue_text_object = arcade.Text(
            text="",
            x=290,
            y=100,
            color=arcade.color.WHITE,
            font_size=20,
            font_name="Quintessential",
            multiline=True,
            width=800
        )

        self.dialogue_lines = [
            {"speaker": "Mohg, Lord of Blood", "text": "Dearest Ansbach...it seems we have a Tarnished visitor."},
            {"speaker": "Mohg, Lord of Blood", "text": "They're disturbing the Albinaurics at the entrance to our domain.\nWould you attend to them, please?"},
            {"speaker": "Pureblood Knight Ansbach", "text": "At once, Lord Mohg."},
            {"speaker": "Mohg, Lord of Blood", "text": "Thank you. Return to me when the deed is done."}
        ]
        self.dialogue_index = 0
        self.show_dialogue = False

    def update_dialogue(self):
        if self.dialogue_index < len(self.dialogue_lines):
            current_line = self.dialogue_lines[self.dialogue_index]
        
            self.speaker_text_object.text = current_line["speaker"]
            self.dialogue_text_object.text = current_line["text"]

            if current_line["speaker"] == "Pureblood Knight Ansbach":
                self.speaker_text_object.color = arcade.color.SILVER
            else:
                self.speaker_text_object.color = arcade.color.RED
            
            self.show_dialogue = True

    def draw_ui(self, player):
        distance = arcade.get_distance_between_sprites(player, self.npc_sprite)
        if distance < TALK_DISTANCE and not self.show_dialogue:
            self.tutorial_text_object.draw()

        if self.show_dialogue:
            arcade.draw_lrbt_rectangle_filled(250, 1100, 30, 200, arcade.color.BLACK)
            arcade.draw_lrbt_rectangle_outline(
            250, 
            1100, 
            30, 
            200, 
            arcade.color.GOLD, 
            border_width=4
        )
            self.dialogue_text_object.draw()
            self.speaker_text_object.draw()

class Room2(Room):
    def __init__(self):
        super().__init__(BACKGROUND_2)

        self.enemy_sprite = arcade.Sprite(
            "assets/images/tarnished.png",
            scale=ENEMY_SCALING,
        )

        self.enemy_sprite.center_x = 1050
        self.enemy_sprite.center_y = 100
        self.room_sprites.append(self.enemy_sprite)
    
    def draw_ui(self, player):
        pass
