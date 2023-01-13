import arcade
import os
import time
import json


CHARACTER_SCALING = 0.8
TILE_SCALING = 1

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 960
SCREEN_TITLE = "Super Jeu de la MORT fait pas Hugo, Faustine, Roland, Jiek, Tom"
SPRITE_PIXEL_SIZE = 64
DEFAULT_FONT_SIZE = 10
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

PLAYER_MOVEMENT_SPEED = 5

with open("map.json", "r") as f:
    current_map = json.loads(f.read())


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.tile_map = None

        self.player_list = None

        self.player_sprite = None

        self.physics_engine = None

        self.view_left = 0
        self.view_bottom = 0

        self.game_over = False

        self.last_time = None
        self.frame_count = 0
        self.fps_message = None

        self.end_of_map_right = 0
        self.end_of_map_left = 0
        self.end_of_map_top = 0
        self.end_of_map_bottom = 0

        self.current_room = current_map["START"]
        self.name_map_message = self.current_room["name"]

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.Sprite("asset/images/animated_characters/robot/robot_idle.png",
                                           CHARACTER_SCALING)

        self.player_sprite.center_x = 160
        self.player_sprite.center_y = 748
        self.player_list.append(self.player_sprite)
        
        self.load_level(self.current_room)

        self.game_over = False

    def load_level(self, room):
        self.tile_map = arcade.load_tilemap(
            f"asset/maps/{self.current_room['id']}.tmx", scaling=TILE_SCALING
        )

        # self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE
        self.end_of_map_right = self.tile_map.width * GRID_PIXEL_SIZE
        self.end_of_map_left = 0
        self.end_of_map_top = self.tile_map.height * GRID_PIXEL_SIZE
        self.end_of_map_bottom = 0


        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.tile_map.sprite_lists["GROUND"])

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

            self.view_left = 0
            self.view_bottom = 0

        print(self.current_room["id"])

    def on_draw(self):
        self.frame_count += 1

        self.clear()

        self.tile_map.sprite_lists["background"].draw()
        self.tile_map.sprite_lists["GROUND"].draw()
        self.tile_map.sprite_lists["bottom"].draw()

        self.player_list.draw()

        self.tile_map.sprite_lists["top"].draw()

        start_x = self.tile_map.height * GRID_PIXEL_SIZE - 5
        start_y = self.tile_map.width * GRID_PIXEL_SIZE
        arcade.draw_text(self.name_map_message,
                         start_x,
                         start_y,
                         arcade.color.WHITE,
                         DEFAULT_FONT_SIZE * 2,
                         width=SCREEN_WIDTH,
                         align="left",
                         bold=True,
                         anchor_x="right",
                         anchor_y="top"
                         )

        if self.last_time and self.frame_count % 60 == 0:
            fps = 1.0 / (time.time() - self.last_time) * 60
            self.fps_message = f"FPS: {fps:5.0f}"

        if self.fps_message:
            arcade.draw_text(
                self.fps_message,
                self.view_left + 10,
                self.view_bottom + 10,
                arcade.color.WHITE,
                14,
            )

        if self.frame_count % 60 == 0:
            self.last_time = time.time()

        if self.game_over:
            arcade.draw_text(
                "GAME OVER",
                self.view_left + 200,
                self.view_bottom + 200,
                arcade.color.BLACK,
                30,
            )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0

    def on_update(self, delta_time: float):

        if self.player_sprite.center_x >= self.end_of_map_right:
            if self.current_room["links"]["Right"] is not None:
                self.current_room = current_map[self.current_room["links"]["Right"]]
                self.load_level(self.current_room)
                self.player_sprite.center_x = 10
                self.player_sprite.center_y = self.player_sprite.center_y
                self.name_map_message = self.current_room["name"]
            else:
                self.player_sprite.center_x += -5

        elif self.player_sprite.center_x <= self.end_of_map_left:
            if self.current_room["links"]["Left"] is not None:
                self.current_room = current_map[self.current_room["links"]["Left"]]
                self.load_level(self.current_room)
                self.player_sprite.center_x = self.end_of_map_right - 20
                self.player_sprite.center_y = self.player_sprite.center_y
                self.name_map_message = self.current_room["name"]
            else:
                self.player_sprite.center_x += 5

        elif self.player_sprite.center_y >= self.end_of_map_top:
            if self.current_room["links"]["Top"] is not None:
                self.current_room = current_map[self.current_room["links"]["Top"]]
                self.load_level(self.current_room)
                self.player_sprite.center_x = self.player_sprite.center_x
                self.player_sprite.center_y = 10
                self.name_map_message = self.current_room["name"]
            else:
                self.player_sprite.center_y += -5

        elif self.player_sprite.center_y <= self.end_of_map_bottom:
            if self.current_room["links"]["Bottom"] is not None:
                self.current_room = current_map[self.current_room["links"]["Bottom"]]
                self.load_level(self.current_room)
                self.player_sprite.center_x = self.player_sprite.center_x
                self.player_sprite.center_y = self.end_of_map_top - 20
                self.name_map_message = self.current_room["name"]
            else:
                self.player_sprite.center_y += 5

        if not self.game_over:
            self.physics_engine.update()


def main():
    """Main method"""
    window = MyGame()
    window.setup()
    arcade.run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()