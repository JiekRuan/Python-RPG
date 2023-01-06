import arcade
from arcade.gui import UIManager, UITextureButton, UIOnClickEvent
import arcade.gui
from arcade.gui.widgets import UITextArea, UITexturePane


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__()
        self.selected_skill = skills[0]
        self.game_view = GameView()
        self.inventory_view = InventoryView()
        self.menu_view = MenuView()
        self.settings_view = SettingsView()
        self.key_bindings_view = KeyBindingsView()
        self.show_view(self.game_view)
    
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.camera= arcade.Camera()
        self.HUD_camera = arcade.Camera()
        self.manager = arcade.gui.UIManager()

        chest = arcade.load_texture('png/chest.png')
        open_chest = arcade.load_texture('png/open_chest.png')
        self.inventory_button = arcade.gui.UITextureButton(750,550,  texture=chest, texture_hovered= open_chest)
        self.inventory_button.on_click = self.inventory_button_clicked
        self.manager.add(self.inventory_button)
        self.skill_icon = arcade.load_texture(self.window.selected_skill.filename)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)
    
    def play_button_clicked(self, event):
        self.window.show_view(self.window.game_view)

    def inventory_button_clicked(self, event):
        self.window.show_view(self.window.inventory_view)

    def on_show_view(self):
        self.manager.enable()
        self.skill_icon = arcade.load_texture(self.window.selected_skill.filename)


    def on_hide_view(self):
        self.manager.disable()    

    def on_draw(self): 
        self.clear()
        self.HUD_camera.use()
        self.manager.draw()
        arcade.set_background_color(arcade.color.WENGE)
        arcade.draw_scaled_texture_rectangle(457, 520, texture=self.skill_icon, scale=0.3)
 


class InventoryView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        cross = arcade.load_texture('png/cross.png')
        cross_hovered = arcade.load_texture('png/cross_hovered.png')

        self.cross_button = arcade.gui.UITextureButton(750,550,  texture=cross, texture_hovered= cross_hovered)


        self.cross_button.on_click = self.cross_button_clicked
        self.manager.add(self.cross_button)

        bg_tex = arcade.load_texture('png/panel_brown.png')

        self.skill_title = UITextArea(
            x= 100,
            y= 515, 
            width =210,
            height= 50, 
            text=self.window.selected_skill.name, 
            font_size=20, 
            text_color=(0,0,0,255))

        self.manager.add(
            UITexturePane(
                self.skill_title.with_space_around(right= 10, left= 25),
                tex= bg_tex,
                padding = (10,10,10,10)
            )
        )

        self.skill_description = UITextArea(
            x= 100,
            y= 200, 
            width =210,
            height= 300, 
            text=LOREM_IPSUM, 
            text_color=(0,0,0,255))

        self.manager.add(
            UITexturePane(
                self.skill_description.with_space_around(right= 10, left= 25),
                tex= bg_tex,
                padding = (30,30,30,30)
            )
        )
        self.skill_effect = UITextArea(
            x= 380,
            y= 190, 
            width =190,
            height= 60, 
            text=f"{self.window.selected_skill.effect}\n cost :  {self.window.selected_skill.cost} mana : ", 
            text_color=(0,0,0,255))

        self.manager.add(
            UITexturePane(
                self.skill_effect.with_space_around(right= 10, left= 25),
                tex= bg_tex,
                padding = (20,20,20,20)
            )
        )

        for i, skill in enumerate(skills):
            tex= arcade.load_texture(skill.filename)
            tex_hovered= arcade.load_texture(skill.fileaname_hovered)
            button = UITextureButton(80+ i* 100, 80, texture=tex, texture_hovered=tex_hovered,
            width=80, height=80)
            button.skill = skill
            button.on_click = self.skill_pressed
            
    
            self.manager.add(button)

    def skill_pressed (self,event):
        button = event.source
        self.skill_description.text = button.skill.description
        self.skill_effect.text = f"{button.skill.effect}\n cost :  {button.skill.cost} mana : "
        self.skill_title.text = button.skill.name
        self.window.selected_skill = button.skill

        



    def cross_button_clicked(self, event):
        self.window.show_view(self.window.game_view)
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)
            
    def on_show_view(self):
        self.manager.enable()
        self.skill_icon = arcade.load_texture(self.window.selected_skill.filename)

        arcade.set_background_color(arcade.color.SLATE_GRAY)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.set_background_color(arcade.color.UMBER)
        
 
class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        play = arcade.load_texture('png/play.png')
        play_hovered = arcade.load_texture('png/play_hovered.png')
        settings = arcade.load_texture('png/settings.png')
        settings_hovered = arcade.load_texture('png/settings_hovered.png')
        quit = arcade.load_texture('png/quit.png')
        quit_hovered = arcade.load_texture('png/quit_hovered.png')

        self.play_button = arcade.gui.UITextureButton(286,401,  texture= play, texture_hovered= play_hovered)
        self.settings_button = arcade.gui.UITextureButton(245,278,  texture= settings, texture_hovered= settings_hovered)
        self.quit_button = arcade.gui.UITextureButton(286,159,  texture= quit, texture_hovered= quit_hovered)

        self.play_button.on_click = self.play_button_clicked
        self.manager.add(self.play_button)
        self.settings_button.on_click = self.settings_button_clicked
        self.manager.add(self.settings_button)
        self.quit_button.on_click = self.quit_button_clicked
        self.manager.add(self.quit_button)

    def play_button_clicked(self, event):
        self.window.show_view(self.window.game_view)
    
    def settings_button_clicked(self, event):
        self.window.show_view(self.window.settings_view)

    def quit_button_clicked(self, event):
        arcade.exit()

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.set_background_color(arcade.color.TUSCAN_RED)

class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        back = arcade.load_texture('png/back.png')
        back_hovered = arcade.load_texture('png/back_hovered.png')
        bindings = arcade.load_texture('png/bindings.png')
        bindings_hovered = arcade.load_texture('png/bindings_hovered.png')

        self.back_button = arcade.gui.UITextureButton(286,105,  texture=back, texture_hovered= back_hovered)
        self.bindings_button = arcade.gui.UITextureButton(245,320,  texture=bindings, texture_hovered= bindings_hovered)

        self.back_button.on_click = self.back_button_clicked
        self.manager.add(self.back_button)
        self.bindings_button.on_click = self.bindings_button_clicked
        self.manager.add(self.bindings_button)

    def back_button_clicked(self, event):
        self.window.show_view(self.window.menu_view)
    
    def bindings_button_clicked(self, event):
        self.window.show_view(self.window.key_bindings_view)

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.set_background_color(arcade.color.TUSCAN_RED)      
    
class KeyBindingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        back = arcade.load_texture('png/back.png')
        back_hovered = arcade.load_texture('png/back_hovered.png')

        self.back_button = arcade.gui.UITextureButton(286,105,  texture=back, texture_hovered= back_hovered)

        self.back_button.on_click = self.back_button_clicked
        self.manager.add(self.back_button)

    def back_button_clicked(self, event):
        self.window.show_view(self.window.settings_view)
    
    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

        arcade.draw_rectangle_outline(180, 430, 200,200, arcade.color.BLACK, 3)

        arcade.draw_text("CONTROLS", 90, 545 , arcade.color.BLACK, font_size= 23,align="left")
        
        arcade.draw_text("Forward : Z", 90, 500 , arcade.color.BLACK, font_size= 15,align="left")
        arcade.draw_text("Backward: S", 90, 475 , arcade.color.BLACK, font_size= 15,align="left")
        arcade.draw_text("Left: Q", 90, 450, arcade.color.BLACK, font_size= 15,align="left")
        arcade.draw_text("Right: D ", 90, 425, arcade.color.BLACK, font_size= 15,align="left")
        arcade.draw_text("Crouch: Left ctrl", 90, 400, arcade.color.BLACK, font_size= 15,align="left")
        arcade.draw_text("Jump: Space", 90, 375, arcade.color.BLACK, font_size= 15,align="left")
        arcade.draw_text("test :i", 90, 350, arcade.color.BLACK, font_size= 15,align="left")

        arcade.set_background_color(arcade.color.TUSCAN_RED)





class Skill:
    def __init__(self, name, description, effect, cost):
        self.name = name
        self.description = description
        self.effect = effect
        self.cost = cost 
        self.filename = f"png/{self.name}.png"
        self.fileaname_hovered = f"png/{self.name}_hovered.png"

"""you used...that gives you..."""       

skills = [
    Skill(
        'confusion',
        'jsp',
        'stun enemies for 3 seconds',
        8,
    ),
    Skill(
        'confusion1',
        'jsp',
        'stun enemies for 3nds',
        2,
    ),
    Skill(
        'confusion2',
        'jsp',
        'stuc for 3 seconds',
        18,
    ),
    Skill(
        'confusion3',
        'jsp',
        'stun enemiescz',
        1,
    ),

]

LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Nisl nisi scelerisque eu ultrices vitae auctor. Vitae sapien pellentesque habitant morbi. Consequat semper viverra nam libero justo laoreet sit amet cursus. Placerat in egestas erat imperdiet sed euismod nisi porta lorem. Cursus metus aliquam eleifend mi. Sit amet consectetur adipiscing elit. Amet cursus sit amet dictum sit amet justo donec. Sed tempus urna et pharetra pharetra massa massa. Sit amet volutpat consequat mauris nunc. Libero justo laoreet sit amet cursus sit amet. Morbi tristique senectus et netus et malesuada fames ac. Turpis massa sed elementum tempus. Magna sit amet purus gravida quis blandit turpis cursus. Lobortis scelerisque fermentum dui faucibus in ornare. Ornare quam viverra orci sagittis eu volutpat odio facilisis mauris. Egestas maecenas pharetra convallis posuere. Enim praesent elementum facilisis leo vel."
"Luctus accumsan tortor posuere ac ut consequat. Aliquet sagittis id consectetur purus ut faucibus pulvinar elementum integer. Egestas integer eget aliquet nibh. Felis eget velit aliquet sagittis id consectetur purus ut. Interdum velit euismod in pellentesque massa. Aliquam id diam maecenas ultricies mi eget mauris pharetra et. Amet consectetur adipiscing elit ut aliquam purus. Rhoncus est pellentesque elit ullamcorper dignissim cras. Elit ut aliquam purus sit amet luctus. Orci sagittis eu volutpat odio facilisis. Mauris rhoncus aenean vel elit scelerisque mauris pellentesque. Urna cursus eget nunc scelerisque viverra mauris in. Sit amet est placerat in egestas erat imperdiet"
"Euismod quis viverra nibh cras pulvinar. Quis eleifend quam adipiscing vitae proin. Quis hendrerit dolor magna eget est lorem ipsum dolor. Duis convallis convallis tellus id interdum velit laoreet id donec. Mattis molestie a iaculis at erat. Fringilla est ullamcorper eget nulla facilisi. Consequat id porta nibh venenatis. Dui ut ornare lectus sit amet est placerat in egestas. Sit amet porttitor eget dolor morbi non. Non odio euismod lacinia at quis risus sed vulputate. Mauris nunc congue nisi vitae suscipit tellus mauris a diam. Facilisis leo vel fringilla est ullamcorper eget. Nunc scelerisque viverra mauris in aliquam sem fringilla"
"Adipiscing elit ut aliquam purus sit amet luctus venenatis. Lobortis mattis aliquam faucibus purus. Quisque egestas diam in arcu cursus euismod quis. Lorem sed risus ultricies tristique nulla aliquet enim. Posuere ac ut consequat semper viverra nam libero justo laoreet. Quisque sagittis purus sit amet. Ornare lectus sit amet est placerat. Enim nec dui nunc mattis enim. Ornare suspendisse sed nisi lacus sed viverra tellus in. Donec enim diam vulputate ut pharetra sit amet. Maecenas ultricies mi eget mauris pharetra et ultrices. Urna porttitor rhoncus dolor purus non enim praesent. Vulputate enim nulla aliquet porttitor lacus luctus. Egestas quis ipsum suspendisse ultrices gravida. Pellentesque sit amet porttitor eget dolor morbi non arcu risus. Auctor urna nunc id cursus metus aliquam. Libero enim sed faucibus turpis in eu. Dui vivamus arcu felis bibendum."
"Amet tellus cras adipiscing enim eu turpis egestas. Tristique senectus et netus et malesuada fames ac turpis egestas. Scelerisque purus semper eget duis. Purus faucibus ornare suspendisse sed nisi lacus sed viverra tellus. Sem fringilla ut morbi tincidunt augue interdum. Et molestie ac feugiat sed lectus vestibulum mattis ullamcorper velit. Metus aliquam eleifend mi in nulla posuere sollicitudin aliquam ultrices. Dolor purus non enim praesent. In massa tempor nec feugiat nisl pretium fusce. Faucibus nisl tincidunt eget nullam non nisi est sit. Eget magna ermentum iaculis eu non. Dictum non consectetur a erat nam at lectus urna duis. Ipsum suspendisse ultrices gravida dictum fusce ut placerat. Dolor sit amet consectetur adipiscing. Lorem ipsum dolor sit amet consectetur adipiscing elit ut. Vel quam elementum pulvinar etiam non quam lacus suspendisse. Vel pharetra vel turpis nunc eget lorem. Gravida cum sociis natoque penatibus et magnis dis. A iaculis at erat pellentesque adipiscing commodo elit at imperdiet."
"Sit amet consectetur adipiscing elit duis. Lacus viverra vitae congue eu consequat ac felis. Mauris pellentesque pulvinar pellentesque habitant morbi tristique. Dictumst quisque sagittis purus sit amet volutpat consequat. Eu tincidunt tortor aliquam nulla facilisi cras. Augue lacus viverra vitae congue eu consequat. Eu volutpat odio facilisis mauris. Velit ut tortor pretium viverra. Pharetra et ultrices neque ornare aenean euismod elementum nisi. Vulputate ut pharetra sit amet aliquam id diam maecenas."
"Ultricies mi quis hendrerit dolor magna eget est. Pellentesque id nibh tortor id aliquet lectus proin nibh nisl. In ornare quam viverra orci. Molestie ac feugiat sed lectus vestibulum. Gravida dictum fusce ut placerat orci nulla pellentesque dignissim enim. Dignissim diam quis enim lobortis. Turpis cursus in hac habitasse platea. Natoque penatibus et magnis dis parturient montes nascetur ridiculus mus. Et malesuada fames ac turpis egestas integer eget aliquet nibh. Ipsum dolor sit amet consectetur adipiscing elit duis tristique sollicitudin. Magna etiam tempor orci eu lobortis elementum nibh tellus molestie. Ut eu sem integer vitae justo eget. Tortor posuere ac ut consequat semper viverra nam."
"Fermentum iaculis eu non diam phasellus vestibulum. Tincidunt augue interdum velit euismod in pellentesque. Aenean et tortor at risus viverra adipiscing at. Ultrices vitae auctor eu augue ut lectus arcu bibendum. Sed euismod nisi porta lorem mollis aliquam ut. Risus nec feugiat in fermentum posuere urna nec. Adipiscing tristique risus nec feugiat in fermentum posuere urna nec. Faucibus turpis in eu mi bibendum. Erat nam at lectus urna duis convallis convallis tellus. Diam in arcu cursus euismod quis viverra nibh cras. Ultricies tristique nulla aliquet enim tortor at auctor urna nunc. Pellentesque elit ullamcorper dignissim cras tincidunt. Tempor orci eu lobortis elementum nibh. Et ultrices neque ornare aenean euismod elementum nisi quis. Pulvinar etiam non quam lacus. Lacus vel facilisis volutpat est velit egestas. Et malesuada fames ac turpis egestas sed tempus urna et. Elementum pulvinar etiam non quam. Volutpat diam ut venenatis tellus in metus."
"Mollis nunc sed id semper risus in hendrerit gravida rutrum. Elementum integer enim neque volutpat ac tincidunt. Sagittis nisl rhoncus mattis rhoncus urna neque viverra. Pulvinar elementum integer enim neque volutpat ac tincidunt. Senectus et netus et malesuada fames ac turpis. Lorem mollis aliquam ut porttitor leo. Elit sed vulputate mi sit amet. Praesent elementum facilisis leo vel fringilla. Eleifend mi in nulla posuere sollicitudin aliquam ultrices sagittis orci. Leo integer malesuada nunc vel"
"Sed vulputate odio ut enim blandit volutpat maecenas volutpat. Posuere urna nec tincidunt praesent. Quis ipsum suspendisse ultrices gravida. Mauris vitae ultricies leo integer malesuada nunc vel. Turpis in eu mi bibendum neque egestas congue quisque. Nibh cras pulvinar mattis nunc. Sed turpis tincidunt id aliquet risus. Commodo sed egestas egestas fringilla phasellus faucibus scelerisque eleifend donec. Semper quis lectus nulla at volutpat diam ut venenatis tellus. Viverra aliquet eget sit amet tellus. Lectus urna duis convallis convallis tellus id. Id aliquet lectus proin nibh nisl. Sem nulla pharetra diam sit amet nisl suscipit adipiscing bibendum. Eget mauris pharetra et ultrices. Vivamus arcu felis bibendum ut tristique."
"Donec et odio pellentesque diam volutpat commodo sed egestas egestas. Nibh ipsum consequat nisl vel pretium lectus quam. Risus ultricies tristique nulla aliquet. Vel eros donec ac odio tempor orci. Cras fermentum odio eu feugiat pretium nibh. Consectetur purus ut faucibus pulvinar elementum. Non arcu risus quis varius quam. Montes nascetur ridiculus mus mauris. Quis lectus nulla at volutpat diam ut venenatis. Habitant morbi tristique senectus et netus et. Ullamcorper dignissim cras tincidunt lobortis feugiat vivamus at augue. Cras adipiscing enim eu turpis egestas. Quisque egestas diam in arcu cursus euismod quis viverra nibh. Justo eget magna fermentum iaculis eu non. Sit amet mauris commodo quis imperdiet. Semper eget duis at tellus at urna condimentum mattis pellentesque. Enim sit amet venenatis urna cursus."
"Vitae justo eget magna fermentum iaculis. Amet justo donec enim diam vulputate ut pharetra sit. Dictum fusce ut placerat orci nulla. Fringilla ut morbi tincidunt augue interdum. Pretium aenean pharetra magna ac placerat vestibulum. Tortor at auctor urna nunc id cursus. Lacus sed viverra tellus in hac. Penatibus et magnis dis parturient montes nascetur ridiculus mus mauris. In vitae turpis massa sed elementum tempus. Aliquet porttitor lacus luctus accumsan tortor posuere ac ut. Est ullamcorper eget nulla facilisi. Commodo ullamcorper a lacus vestibulum sed. Nunc aliquet bibendum enim facilisis gravida. Consectetur libero id faucibus nisl tincidunt eget nullam. Scelerisque felis imperdiet proin fermentum leo vel orci. Nulla pharetra diam sit amet nisl suscipit adipiscing. Felis bibendum ut tristique et egestas quis ipsum suspendisse. Tortor at auctor urna nunc id."
"Eget sit amet tellus cras adipiscing enim eu. Sollicitudin tempor id eu nisl nunc mi ipsum faucibus vitae. Tellus integer feugiat scelerisque varius. In egestas erat imperdiet sed euismod nisi. Odio aenean sed adipiscing diam donec adipiscing tristique. At quis risus sed vulputate odio ut enim. Enim nunc faucibus a pellentesque sit amet porttitor. Pulvinar proin gravida hendrerit lectus. Viverra adipiscing at in tellus integer. Tortor consequat id porta nibh venenati"
"Dolor morbi non arcu risus quis varius. Et tortor consequat id porta nibh venenatis cras. Ornare aenean euismod elementum nisi quis eleifend. Ut pharetra sit amet aliquam id. Non quam lacus suspendisse faucibus interdum posuere lorem. Aliquet risus feugiat in ante metus dictum at. Aliquam ut porttitor leo a diam sollicitudin tempor id. Mattis nunc sed blandit libero volutpat sed cras ornare arcu. Aenean sed adipiscing diam donec adipiscing tristique risus nec. Accumsan sit amet nulla facilisi. Dolor sed viverra ipsum nunc aliquet bibendum enim facilisis gravida. Sit amet tellus cras adipiscing enim eu. Nisl vel pretium lectus quam id leo in vitae."
"Adipiscing bibendum est ultricies integer. Vulputate ut pharetra sit amet aliquam id diam. Proin sagittis nisl rhoncus mattis rhoncus urna neque. Imperdiet sed euismod nisi porta lorem. Risus commodo viverra maecenas accumsan lacus vel facilisis volutpat. Amet volutpat consequat mauris nunc. Lobortis elementum nibh tellus molestie nunc non blandit. Malesuada proin libero nunc consequat. Fringilla urna porttitor rhoncus dolor purus non enim. Non pulvinar neque laoreet suspendisse interdum consectetur. In cursus turpis massa tincidunt dui ut ornare lectus sit."
"Nulla aliquet porttitor lacus luctus accumsan. Duis convallis convallis tellus id interdum. Laoreet sit amet cursus sit amet dictum sit. Ornare quam viverra orci sagittis eu. Ornare suspendisse sed nisi lacus sed. Sollicitudin tempor id eu nisl nunc. Ut eu sem integer vitae justo eget. Enim neque volutpat ac tincidunt vitae semper quis. Potenti nullam ac tortor vitae. Felis eget velit aliquet sagittis id consectetur purus ut faucibus. Turpis egestas pretium aenean pharetra. Gravida neque convallis a cras semper auctor. Fames ac turpis egestas integer eget aliquet nibh praesent. Imperdiet dui accumsan sit amet nulla facilisi morbi tempus."
"Mollis nunc sed id semper risus in hendrerit gravida rutrum. Nunc mi ipsum faucibus vitae aliquet nec. Phasellus vestibulum lorem sed risus ultricies tristique nulla. Vitae nunc sed velit dignissim sodales ut eu. Sed arcu non odio euismod. Mollis aliquam ut porttitor leo a. Viverra maecenas accumsan lacus vel facilisis volutpat. Massa sed elementum tempus egestas sed sed risus pretium. Eget velit aliquet sagittis id consectetur purus ut. Non odio euismod lacinia at quis risus sed. Feugiat sed lectus vestibulum mattis ullamcorper."
"Ut tellus elementum sagittis vitae et leo duis ut. Dignissim suspendisse in est ante in. Sit amet venenatis urna cursus eget. Ut faucibus pulvinar elementum integer enim neque volutpat ac. Ante metus dictum at tempor. Odio aenean sed adipiscing diam donec. Eu tincidunt tortor aliquam nulla facilisi cras fermentum odio eu. Ipsum dolor sit amet consectetur adipiscing. Arcu cursus vitae congue mauris rhoncus aenean vel elit scelerisque. Adipiscing commodo elit at imperdiet dui accumsan. Nullam non nisi est sit amet facilisis. Orci porta non pulvinar neque laoreet suspendisse interdum. Eu turpis egestas pretium aenean pharetra magna."
"At tellus at urna condimentum mattis pellentesque id nibh. Molestie nunc non blandit massa. Eget mi proin sed libero enim sed faucibus turpis. Vulputate ut pharetra sit amet aliquam id diam maecenas ultricies. Amet luctus venenatis lectus magna. Eu volutpat odio facilisis mauris sit. Pretium fusce id velit ut tortor pretium viverra. Ultricies mi eget mauris pharetra et. Mi ipsum faucibus vitae aliquet nec ullamcorper. Aliquam ut porttitor leo a diam sollicitudin tempor id. Vestibulum lorem sed risus ultricies tristique nulla aliquet enim. Pharetra et ultrices neque ornare aenean euismod elementum nisi quis. Donec massa sapien faucibus et molestie ac feugiat."
"Mauris vitae ultricies leo integer malesuada. Elit pellentesque habitant morbi tristique senectus et netus et. Vulputate sapien nec sagittis aliquam malesuada bibendum. Nulla facilisi morbi tempus iaculis urna. Ornare arcu odio ut sem nulla pharetra diam sit. Placerat orci nulla pellentesque dignissim. Pharetra sit amet aliquam id. Sollicitudin nibh sit amet commodo nulla facilisi nullam vehicula. A arcu cursus vitae congue mauris rhoncus aenean. Convallis a cras semper auctor neque vitae tempus quam pellentesque. Vitae proin sagittis nisl rhoncus mattis rhoncus urna. Tortor aliquam nulla facilisi cras fermentum odio. Ipsum nunc aliquet bibendum enim facilisis gravida. Feugiat in ante metus dictum at tempor commodo ullamcorper. Turpis egestas pretium aenean pharetra magna ac placerat. Lorem ipsum dolor sit amet consectetur adipiscing elit duis. Egestas fringilla phasellus faucibus scelerisque eleifend donec pretium vulputate sapien."
"Vitae justo eget magna fermentum iaculis. Vehicula ipsum a arcu cursus vitae congue mauris rhoncus. Ornare suspendisse sed nisi lacus sed viverra tellus in. Mauris in aliquam sem fringilla ut. Nisi lacus sed viverra tellus in hac habitasse platea dictumst. Ac tortor vitae purus faucibus. In ante metus dictum at tempor commodo. Ultrices gravida dictum fusce ut placerat orci nulla pellentesque dignissim. Dictum sit amet justo donec enim diam vulputate ut pharetra. Consequat mauris nunc congue nisi. Et netus et malesuada fames ac turpis egestas. Tristique senectus et netus et malesuada fames ac. Massa vitae tortor condimentum lacinia quis vel eros. Proin sagittis nisl rhoncus mattis rhoncus urna neque viverra justo. Vivamus arcu felis bibendum ut tristique et egestas quis. Sapien faucibus et molestie ac feugiat sed."
"Ridiculus mus mauris vitae ultricies leo. Blandit massa enim nec dui nunc mattis enim ut. Quis imperdiet massa tincidunt nunc pulvinar sapien et ligula ullamcorper. Elementum facilisis leo vel fringilla est ullamcorper eget nulla. Urna condimentum mattis pellentesque id nibh. Ut pharetra sit amet aliquam id diam maecenas. Faucibus in ornare quam viverra orci sagittis eu. In vitae turpis massa sed elementum. Nisi quis eleifend quam adipiscing. Consequat mauris nunc congue nisi vitae suscipit tellus."
"Quam nulla porttitor massa id. Nisl tincidunt eget nullam non nisi est. Amet massa vitae tortor condimentum lacinia. Gravida neque convallis a cras semper auctor. Vitae sapien pellentesque habitant morbi tristique senectus et netus. Fermentum posuere urna nec tincidunt. Purus non enim praesent elementum facilisis leo vel fringilla. Ornare massa eget egestas purus viverra accumsan. Turpis massa sed elementum tempus egestas sed sed risus pretium. Enim diam vulputate ut pharetra sit amet aliquam id."
"Lacus vel facilisis volutpat est velit egestas. Ultrices sagittis orci a scelerisque purus semper eget duis at. Purus sit amet volutpat consequat. Orci a scelerisque purus semper eget duis at tellus at. Eros in cursus turpis massa tincidunt dui ut ornare lectus. Lobortis feugiat vivamus at augue eget arcu. Nibh cras pulvinar mattis nunc sed blandit. Auctor eu augue ut lectus arcu bibendum at varius vel. Mattis enim ut tellus elementum sagittis vitae et leo. Viverra justo nec ultrices dui. Ut tellus elementum sagittis vitae et leo. Cursus euismod quis viverra nibh. Massa massa ultricies mi quis hendrerit dolor magna. A pellentesque sit amet porttitor eget dolor. Dolor morbi non arcu risus quis varius quam quisque id. Amet cursus sit amet dictum sit amet justo donec. Id aliquet lectus proin nibh nisl condimentum. Cras fermentum odio eu feugiat pretium nibh ipsum. Tellus pellentesque eu tincidunt tortor."
def main():
    window=GameWindow()
    arcade.run()

if __name__ == "__main__":
    main()



