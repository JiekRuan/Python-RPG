#Import des librairies utilisées
import arcade
from arcade.gui import UITextureButton
from arcade.gui.widgets import UITextArea, UITexturePane
from map import play

# Valeur qui détermine sur quel écran le joueur se trouve (Menu interface/Menu jeu)
interface = 0

class GameWindow(arcade.Window):
    def __init__(self):
        #Taille de la fenêtre
        super().__init__(960, 960, "Python game")
        self.selected_armor = armors[0]
        self.selected_weapon = weapons[0]
        self.selected_consumable = consumables[0]
        self.selected_misc = miscs[0]

        self.start_view = StartView()
        self.game_view = GameView()
        self.inventory_view = InventoryView()
        self.menu_view = MenuView()
        self.settings_view = SettingsView()
        self.key_bindings_view = KeyBindingsView()
        self.armor_view = ArmorView()
        self.weapon_view = WeaponView()
        self.consumable_view = ConsumableView()
        self.misc_view = MiscView()

        #Fenêtre lancée au démarrage du jeu
        self.show_view(self.start_view)


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        #Import des images utilisées
        play = arcade.load_texture('Assets/png/buttons/play.png')
        play_hovered = arcade.load_texture('Assets/png/buttons/play_hovered.png')
        settings = arcade.load_texture('Assets/png/buttons/settings.png')
        settings_hovered = arcade.load_texture('Assets/png/buttons/settings_hovered.png')
        save = arcade.load_texture('Assets/png/buttons/save.png')
        save_hovered = arcade.load_texture('Assets/png/buttons/save_hovered.png')
        load = arcade.load_texture('Assets/png/buttons/load.png')
        load_hovered = arcade.load_texture('Assets/png/buttons/load_hovered.png')
        quit = arcade.load_texture('Assets/png/buttons/quit.png')
        quit_hovered = arcade.load_texture('Assets/png/buttons/quit_hovered.png')
        
        #Création des boutons, comportant les coordonnées et les différentes textures
        self.play_button = arcade.gui.UITextureButton(381,673,  texture= play, texture_hovered= play_hovered,)
        self.settings_button = arcade.gui.UITextureButton(337,560,  texture= settings, texture_hovered= settings_hovered)
        self.save_button = arcade.gui.UITextureButton(271,437,  texture= save, texture_hovered= save_hovered)
        self.load_button = arcade.gui.UITextureButton(491,437,  texture= load, texture_hovered= load_hovered)
        self.quit_button = arcade.gui.UITextureButton(381,314,  texture= quit, texture_hovered= quit_hovered)

        #Ajouts des boutons sur la fenêtre
        self.play_button.on_click = self.play_button_clicked
        self.manager.add(self.play_button)
        self.settings_button.on_click = self.settings_button_clicked
        self.manager.add(self.settings_button)
        self.save_button.on_click = self.quit_button_clicked
        self.manager.add(self.save_button)
        self.load_button.on_click = self.quit_button_clicked
        self.manager.add(self.load_button)
        self.quit_button.on_click = self.quit_button_clicked
        self.manager.add(self.quit_button)
        
        
        self.background = arcade.load_texture("Assets/png/background.png")

               
    #Fonctions qui renvoie sur une autre fenêtre lorsqu'un bouton est cliqué
    def play_button_clicked(self, event):
        global interface
        interface = 1
        self.window.show_view(self.window.game_view)
    
    def settings_button_clicked(self, event):
        self.window.show_view(self.window.settings_view)

    def save_button_clicked(self, event):
        pass
    
    def load_button_clicked(self, event):
        pass

    def quit_button_clicked(self, event):
        arcade.exit()

    #Permet d'activer l'utilisation de la fenêtre lorsqu'on l'utilise
    def on_show_view(self):
        self.manager.enable()

    #Permet de désactiver l'utilisation de la fenêtre lorsqu'on ne l'utilise pas
    def on_hide_view(self):
        self.manager.disable()
        
    # Remet l'affichage de l'écran à 0
    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_lrwh_rectangle_textured(0, 0, 960, 960, self.background, alpha = 40)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.camera= arcade.Camera()
        self.HUD_camera = arcade.Camera()
        self.manager = arcade.gui.UIManager()

        chest = arcade.load_texture('Assets/png/buttons/chest.png')
        open_chest = arcade.load_texture('Assets/png/buttons/open_chest.png')
        self.inventory_button = arcade.gui.UITextureButton(910,910, texture=chest, texture_hovered= open_chest)
        self.inventory_button.on_click = self.inventory_button_clicked
        self.manager.add(self.inventory_button)

    #Fonction appellée lors de l'utilisation d'une touche. Ici la touche permet de changer de fenêtre
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)

    def inventory_button_clicked(self, event):
        self.window.show_view(self.window.inventory_view)
    
    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()    

    def on_draw(self): 
        self.clear()
        self.HUD_camera.use()
        self.manager.draw()
        arcade.set_background_color(arcade.color.SACRAMENTO_STATE_GREEN)


class InventoryView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        cross = arcade.load_texture('Assets/png/buttons/cross.png')
        cross_hovered = arcade.load_texture('Assets/png/buttons/cross_hovered.png')
        armor_img = arcade.load_texture('Assets/png/buttons/armor.png')
        weapon_img = arcade.load_texture('Assets/png/buttons/armes.png')
        consumable_img = arcade.load_texture('Assets/png/buttons/potions.png')
        misc_img = arcade.load_texture('Assets/png/buttons/divers.png')

        self.cross_button = arcade.gui.UITextureButton(910,910,  texture=cross, texture_hovered= cross_hovered)
        self.armor_button = arcade.gui.UITextureButton(260,630,  texture=armor_img)
        self.weapon_button = arcade.gui.UITextureButton(560,630,  texture=weapon_img)
        self.consumable_button = arcade.gui.UITextureButton(260,350,  texture=consumable_img)
        self.misc_button = arcade.gui.UITextureButton(560,350,  texture=misc_img)

        self.cross_button.on_click = self.cross_button_clicked
        self.manager.add(self.cross_button)

        self.armor_button.on_click = self.armor_button_clicked
        self.manager.add(self.armor_button)

        self.weapon_button.on_click = self.weapon_button_clicked
        self.manager.add(self.weapon_button)

        self.consumable_button.on_click = self.consumable_button_clicked
        self.manager.add(self.consumable_button)

        self.misc_button.on_click = self.misc_button_clicked
        self.manager.add(self.misc_button)

    def cross_button_clicked(self, event):
        self.window.show_view(self.window.game_view)
    
    def armor_button_clicked(self, event):
        self.window.show_view(self.window.armor_view)
    
    def weapon_button_clicked(self, event):
        self.window.show_view(self.window.weapon_view)
    
    def consumable_button_clicked(self, event):
        self.window.show_view(self.window.consumable_view)

    def misc_button_clicked(self, event):
        self.window.show_view(self.window.misc_view)
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.set_background_color(arcade.color.GRAY)


class ArmorView(arcade.View):  
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager() 

        back = arcade.load_texture('Assets/png/armors/back.png')
        back_hovered = arcade.load_texture('Assets/png/armors/back_hovered.png')
        select = arcade.load_texture('Assets/png/armors/select.png')
        select_hovered = arcade.load_texture('Assets/png/armors/select_hovered.png')

        self.back_button = arcade.gui.UITextureButton(50,900,  texture=back, texture_hovered= back_hovered)
        self.select_button = arcade.gui.UITextureButton(700,200,  texture=select, texture_hovered= select_hovered)

        self.back_button.on_click = self.back_button_clicked
        self.manager.add(self.back_button)
        self.select_button.on_click = self.select_button_clicked
        self.manager.add(self.select_button)

        #   Import de l'image
        bg_tex = arcade.load_texture('Assets/png/panel.png')

        #Création d'une zone de texte scrollable
        self.armor_title = UITextArea(
            x= 479,
            y= 750, 
            width =130,
            height= 50, 
            font_size=20, 
            text_color=(242, 243, 244)
        )
        #Ajout du fond pour la zone de texte
        self.manager.add(
            UITexturePane(
                self.armor_title.with_space_around(),
                tex= bg_tex,
                padding = (10,10,10,10)
            )
        )

        self.armor_description = UITextArea(
            x= 460,
            y= 340, 
            width =185,
            height= 400, 
            text_color=(242, 243, 244)
        )
        self.manager.add(
            UITexturePane(
                self.armor_description.with_space_around(right= 10, left= 25),
                tex= bg_tex,
                padding = (30,30,30,30)
            )
        )
        self.armor_effect = UITextArea(
            x= 730,
            y= 330, 
            width =190,
            height= 60, 
            text_color=(242, 243, 244)
        )
        self.manager.add(
            UITexturePane(
                self.armor_effect.with_space_around(right= 10, left= 25),
                tex= bg_tex,
                padding = (20,20,20,20)
            )
        )

        #Affiche les icônes pour chaque items dans la class 'armor'
        for i, armor in enumerate(armors):
            tex= arcade.load_texture(armor.filename)
            tex_hovered= arcade.load_texture(armor.fileaname_hovered)
            x= 90+(i%4) *70
            y= 750 - (i//4)* 70
            button = UITextureButton(x, y, texture=tex, texture_hovered=tex_hovered,
            width=50, height=50)
            button.armor = armor
            button.on_click = self.armor_pressed
            
            self.manager.add(button)

    #Affiche la description, les effets et le titre pour chaque items dans la class 'armor' dans les zones prédéfinies 
    def armor_pressed (self,event):
        button = event.source
        self.armor_description.text = button.armor.description
        self.armor_effect.text = f"{button.armor.effect}\n cost :  {button.armor.cost} mana"
        self.armor_title.text = button.armor.name
        self.window.selected_armor = button.armor

    def on_show_view(self):
        self.manager.enable()
        self.armor_icon = arcade.load_texture(self.window.armor.filename)

    def on_hide_view(self):
        self.manager.disable()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)
    
    def back_button_clicked(self, event):
        self.window.show_view(self.window.inventory_view)

    def select_button_clicked(self, event):
        self.window.show_view(self.window.game_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text("Armors",415,910,arcade.color.WHITE, 25)
        arcade.set_background_color(arcade.color.GRAY)


class WeaponView(arcade.View):  
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager() 

        back = arcade.load_texture('Assets/png/armors/back.png')
        back_hovered = arcade.load_texture('Assets/png/armors/back_hovered.png')
        select = arcade.load_texture('Assets/png/armors/select.png')
        select_hovered = arcade.load_texture('Assets/png/armors/select_hovered.png')

        self.back_button = arcade.gui.UITextureButton(50,900,  texture=back, texture_hovered= back_hovered)
        self.select_button = arcade.gui.UITextureButton(700,200,  texture=select, texture_hovered= select_hovered)

        self.back_button.on_click = self.back_button_clicked
        self.manager.add(self.back_button)
        self.select_button.on_click = self.select_button_clicked
        self.manager.add(self.select_button)

        #Import de l'image 
        bg_tex = arcade.load_texture('Assets/png/panel.png')

        #Création d'une zone de texte scrollable
        self.weapon_title = UITextArea(
            x= 479,
            y= 750, 
            width =130,
            height= 50, 
            font_size=20, 
            text_color=(242, 243, 244)
        )
        #Ajout du fond pour la zone de texte
        self.manager.add(
            UITexturePane(
                self.weapon_title.with_space_around(),
                tex= bg_tex,
                padding = (10,10,10,10)
            )
        )

        self.weapon_description = UITextArea(
            x= 460,
            y= 340, 
            width =185,
            height= 400, 
            text_color=(242, 243, 244)
        )
        self.manager.add(
            UITexturePane(
                self.weapon_description.with_space_around(right= 10, left= 25),
                tex= bg_tex,
                padding = (30,30,30,30)
            )
        )
        self.weapon_effect = UITextArea(
            x= 730,
            y= 330, 
            width =190,
            height= 60, 
            text_color=(242, 243, 244)
        )
        self.manager.add(
            UITexturePane(
                self.weapon_effect.with_space_around(right= 10, left= 25),
                tex= bg_tex,
                padding = (20,20,20,20)
            )
        )

        #Affiche les icônes pour chaque items dans la class 'weapon'
        for i, weapon in enumerate(weapons):
            tex= arcade.load_texture(weapon.filename)
            tex_hovered= arcade.load_texture(weapon.fileaname_hovered)
            x= 90+(i%4) *70
            y= 750 - (i//4)* 70
            button = UITextureButton(x, y, texture=tex, texture_hovered=tex_hovered,
            width=50, height=50)
            button.weapon = weapon
            button.on_click = self.weapon_pressed
            
            self.manager.add(button)

    #Affiche la description, les effets et le titre pour chaque items dans la class 'weapon' dans les zones prédéfinies 
    def weapon_pressed (self,event):
        button = event.source
        self.weapon_description.text = button.weapon.description
        self.weapon_effect.text = f"{button.weapon.effect}\n cost :  {button.weapon.cost} mana"
        self.weapon_title.text = button.weapon.name
        self.window.selected_weapon = button.weapon

    def on_show_view(self):
        self.manager.enable()
        self.armor_icon = arcade.load_texture(self.window.weapon.filename)

    def on_hide_view(self):
        self.manager.disable()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)
    
    def back_button_clicked(self, event):
        self.window.show_view(self.window.inventory_view)

    def select_button_clicked(self, event):
        self.window.show_view(self.window.game_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text("Weapons",415,910,arcade.color.WHITE, 25)
        arcade.set_background_color(arcade.color.GRAY)


class ConsumableView(arcade.View):  
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager() 

        back = arcade.load_texture('Assets/png/armors/back.png')
        back_hovered = arcade.load_texture('Assets/png/armors/back_hovered.png')
        select = arcade.load_texture('Assets/png/armors/select.png')
        select_hovered = arcade.load_texture('Assets/png/armors/select_hovered.png')

        self.back_button = arcade.gui.UITextureButton(50,900,  texture=back, texture_hovered= back_hovered)
        self.select_button = arcade.gui.UITextureButton(700,200,  texture=select, texture_hovered= select_hovered)

        self.back_button.on_click = self.back_button_clicked
        self.manager.add(self.back_button)
        self.select_button.on_click = self.select_button_clicked
        self.manager.add(self.select_button)

        #Import de l'image 
        bg_tex = arcade.load_texture('Assets/png/panel.png')

        #Création d'une zone de texte scrollable
        self.consumable_title = UITextArea(
            x= 479,
            y= 750, 
            width =130,
            height= 50, 
            font_size=20, 
            text_color=(242, 243, 244)
        )
        #Ajout du fond pour la zone de texte
        self.manager.add(
            UITexturePane(
                self.consumable_title.with_space_around(),
                tex= bg_tex,
                padding = (10,10,10,10)
            )
        )

        self.consumable_description = UITextArea(
            x= 460,
            y= 340, 
            width =185,
            height= 400, 
            text_color=(242, 243, 244)
        )
        self.manager.add(
            UITexturePane(
                self.consumable_description.with_space_around(right= 10, left= 25),
                tex= bg_tex,
                padding = (30,30,30,30)
            )
        )
        self.consumable_effect = UITextArea(
            x= 730,
            y= 330, 
            width =190,
            height= 60, 
            text_color=(242, 243, 244)
        )
        self.manager.add(
            UITexturePane(
                self.consumable_effect.with_space_around(right= 10, left= 25),
                tex= bg_tex,
                padding = (20,20,20,20)
            )
        )

        #Affiche les icônes pour chaque items dans la class 'consumable'
        for i, consumable in enumerate(consumables):
            tex= arcade.load_texture(consumable.filename)
            tex_hovered= arcade.load_texture(consumable.fileaname_hovered)
            x= 90+(i%4) *70
            y= 750 - (i//4)* 70
            button = UITextureButton(x, y, texture=tex, texture_hovered=tex_hovered,
            width=50, height=50)
            button.consumable = consumable
            button.on_click = self.consumable_pressed
            
            self.manager.add(button)

    #Affiche la description, les effets et le titre pour chaque items dans la class 'consumable' dans les zones prédéfinies 
    def consumable_pressed (self,event):
        button = event.source
        self.consumable_description.text = button.consumable.description
        self.consumable_effect.text = f"{button.consumable.effect}\n cost :  {button.consumable.cost} mana"
        self.consumable_title.text = button.consumable.name
        self.window.selected_consumable = button.consumable

    def on_show_view(self):
        self.manager.enable()
        self.armor_icon = arcade.load_texture(self.window.consumable.filename)

    def on_hide_view(self):
        self.manager.disable()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)
    
    def back_button_clicked(self, event):
        self.window.show_view(self.window.inventory_view)

    def select_button_clicked(self, event):
        self.window.show_view(self.window.game_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text("Consumables",415,910,arcade.color.WHITE, 25)
        arcade.set_background_color(arcade.color.GRAY)


class MiscView(arcade.View):  
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager() 

        back = arcade.load_texture('Assets/png/armors/back.png')
        back_hovered = arcade.load_texture('Assets/png/armors/back_hovered.png')
        select = arcade.load_texture('Assets/png/armors/select.png')
        select_hovered = arcade.load_texture('Assets/png/armors/select_hovered.png')

        self.back_button = arcade.gui.UITextureButton(50,900,  texture=back, texture_hovered= back_hovered)
        self.select_button = arcade.gui.UITextureButton(700,200,  texture=select, texture_hovered= select_hovered)

        self.back_button.on_click = self.back_button_clicked
        self.manager.add(self.back_button)
        self.select_button.on_click = self.select_button_clicked
        self.manager.add(self.select_button)

        #Import de l'image 
        bg_tex = arcade.load_texture('Assets/png/panel.png')

        #Création d'une zone de texte scrollable
        self.misc_title = UITextArea(
            x= 479,
            y= 750, 
            width =130,
            height= 50, 
            font_size=20, 
            text_color=(242, 243, 244)
        )
        #Ajout du fond pour la zone de texte
        self.manager.add(
            UITexturePane(
                self.misc_title.with_space_around(),
                tex= bg_tex,
                padding = (10,10,10,10)
            )
        )

        self.misc_description = UITextArea(
            x= 460,
            y= 340, 
            width =185,
            height= 400, 
            text_color=(242, 243, 244)
        )
        self.manager.add(
            UITexturePane(
                self.misc_description.with_space_around(right= 10, left= 25),
                tex= bg_tex,
                padding = (30,30,30,30)
            )
        )
        self.misc_effect = UITextArea(
            x= 730,
            y= 330, 
            width =190,
            height= 60, 
            text_color=(242, 243, 244)
        )
        self.manager.add(
            UITexturePane(
                self.misc_effect.with_space_around(right= 10, left= 25),
                tex= bg_tex,
                padding = (20,20,20,20)
            )
        )

        #Affiche les icônes pour chaque items dans la class 'misc'
        for i, misc in enumerate(miscs):
            tex= arcade.load_texture(misc.filename)
            tex_hovered= arcade.load_texture(misc.fileaname_hovered)
            x= 90+(i%4) *70
            y= 750 - (i//4)* 70
            button = UITextureButton(x, y, texture=tex, texture_hovered=tex_hovered,
            width=50, height=50)
            button.misc = misc
            button.on_click = self.misc_pressed
            
            self.manager.add(button)

    #Affiche la description, les effets et le titre pour chaque items dans la class 'misc' dans les zones prédéfinies 
    def misc_pressed (self,event):
        button = event.source
        self.misc_description.text = button.misc.description
        self.misc_effect.text = f"{button.misc.effect}\n cost :  {button.misc.cost} mana"
        self.misc_title.text = button.misc.name
        self.window.selected_misc = button.misc

    def on_show_view(self):
        self.manager.enable()
        self.armor_icon = arcade.load_texture(self.window.misc.filename)

    def on_hide_view(self):
        self.manager.disable()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)
    
    def back_button_clicked(self, event):
        self.window.show_view(self.window.inventory_view)

    def select_button_clicked(self, event):
        self.window.show_view(self.window.game_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text("Miscs",415,910,arcade.color.WHITE, 25)
        arcade.set_background_color(arcade.color.GRAY)


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        play = arcade.load_texture('Assets/png/buttons/play.png')
        play_hovered = arcade.load_texture('Assets/png/buttons/play_hovered.png')
        settings = arcade.load_texture('Assets/png/buttons/settings.png')
        settings_hovered = arcade.load_texture('Assets/png/buttons/settings_hovered.png')
        save = arcade.load_texture('Assets/png/buttons/save.png')
        save_hovered = arcade.load_texture('Assets/png/buttons/save_hovered.png')
        quit = arcade.load_texture('Assets/png/buttons/quit.png')
        quit_hovered = arcade.load_texture('Assets/png/buttons/quit_hovered.png')

        self.play_button = arcade.gui.UITextureButton(381,673,  texture= play, texture_hovered= play_hovered)
        self.settings_button = arcade.gui.UITextureButton(337,560,  texture= settings, texture_hovered= settings_hovered)
        self.save_button = arcade.gui.UITextureButton(381,437,  texture= save, texture_hovered= save_hovered)
        self.quit_button = arcade.gui.UITextureButton(381,314,  texture= quit, texture_hovered= quit_hovered)

        self.play_button.on_click = self.play_button_clicked
        self.manager.add(self.play_button)
        self.settings_button.on_click = self.settings_button_clicked
        self.manager.add(self.settings_button)
        self.save_button.on_click = self.quit_button_clicked
        self.manager.add(self.save_button)
        self.quit_button.on_click = self.quit_button_clicked
        self.manager.add(self.quit_button)

    def play_button_clicked(self, event):
        self.window.show_view(self.window.game_view)
    
    def settings_button_clicked(self, event):
        self.window.show_view(self.window.settings_view)

    def save_button_clicked(self, event):
        pass

    def quit_button_clicked(self, event):
        arcade.exit()

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.set_background_color(arcade.color.WHITE_SMOKE)


class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        back = arcade.load_texture('Assets/png/buttons/back.png')
        back_hovered = arcade.load_texture('Assets/png/buttons/back_hovered.png')
        bindings = arcade.load_texture('Assets/png/buttons/bindings.png')
        bindings_hovered = arcade.load_texture('Assets/png/buttons/bindings_hovered.png')

        self.back_button = arcade.gui.UITextureButton(381,320,  texture=back, texture_hovered= back_hovered)
        self.bindings_button = arcade.gui.UITextureButton(337,490,  texture=bindings, texture_hovered= bindings_hovered)

        self.back_button.on_click = self.back_button_clicked
        self.manager.add(self.back_button)
        self.bindings_button.on_click = self.bindings_button_clicked
        self.manager.add(self.bindings_button)
    #Fonction qui nous fait revenir dans la fenêtre correspondant à l'endroit où le joueur à utilisé le bouton 'settings'
    def back_button_clicked(self, event):
        global interface
        if interface == 0:
            self.window.show_view(self.window.start_view)
        elif interface == 1 :
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
        arcade.set_background_color(arcade.color.WHITE_SMOKE)      


class KeyBindingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        back = arcade.load_texture('Assets/png/buttons/back.png')
        back_hovered = arcade.load_texture('Assets/png/buttons/back_hovered.png')

        self.back_button = arcade.gui.UITextureButton(381,320,  texture=back, texture_hovered= back_hovered)

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

        #Ahout des contours d'un rectangle
        arcade.draw_rectangle_outline(480, 780, 200,200, arcade.color.BLACK, 3)
        #Ahout du texte autour et à l'interieur du rectangle
        arcade.draw_text("CONTROLS", 390, 895 , arcade.color.BLACK, font_size= 23,align="left")
        arcade.draw_text("Forward : Z", 390, 850 , arcade.color.BLACK, font_size= 15,align="left")
        arcade.draw_text("Backward: S", 390, 825 , arcade.color.BLACK, font_size= 15,align="left")
        arcade.draw_text("Left: Q", 390, 800, arcade.color.BLACK, font_size= 15,align="left")
        arcade.draw_text("Right: D ", 390, 775, arcade.color.BLACK, font_size= 15,align="left")
        arcade.draw_text("Crouch: Left ctrl", 390, 750, arcade.color.BLACK, font_size= 15,align="left")
        arcade.draw_text("Jump: Space", 390, 725, arcade.color.BLACK, font_size= 15,align="left")
        arcade.draw_text("test :i", 390, 700, arcade.color.BLACK, font_size= 15,align="left")

        arcade.set_background_color(arcade.color.WHITE_SMOKE)


#Classes qui definit le nom, la descrition, les effets et le prix de l'item
class Armor:
    def __init__(self, name, description, effect, cost):
        self.name = name
        self.description = description
        self.effect = effect
        self.cost = cost 
        self.filename = f"Assets/png/armors/{self.name}.png"
        self.fileaname_hovered = f"Assets/png/armors/{self.name}_hovered.png"

armors = [
    Armor(
        'confusion',
        'jsp',
        'stun enemies for 3 seconds',
        8,
    ),
    Armor(
        'confusion1',
        'jsp',
        'stun enemies for 3nds',
        2,
    ),
    Armor(
        'confusion2',
        'jsp',
        'stuc for 3 seconds',
        18,
    ),
    Armor(
        'confusion3',
        'jspjspjspjspjspjspjspjspjspjspjspjspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Armor(
        'confusion4',
        'jspjspjspjspjspjspjspjs',
        'stuc for 3 seconds',
        1,
    ),
    Armor(
        'confusion5',
        'jspjspjspjspjspjspjspjspjspjpjspjspjspjspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Armor(
        'confusion6',
        'jspjspjspjspjjspjspjspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Armor(
        'confusion7',
        'jspspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Armor(
        'confusion8',
        'jspjspjsspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Armor(
        'confusion9',
        'pezihjfeà',
        'stuc for 3 seconds',
        1,
    ),

]


class Weapon:
    def __init__(self, name, description, effect, cost):
        self.name = name
        self.description = description
        self.effect = effect
        self.cost = cost 
        self.filename = f"Assets/png/armors/{self.name}.png"
        self.fileaname_hovered = f"Assets/png/armors/{self.name}_hovered.png"


weapons = [
    Weapon(
        'confusion',
        'jsp',
        'stun enemies for 3 seconds',
        8,
    ),
    Weapon(
        'confusion1',
        'jsp',
        'stun enemies for 3nds',
        2,
    ),
    Weapon(
        'confusion2',
        'jsp',
        'stuc for 3 seconds',
        18,
    ),
    Weapon(
        'confusion3',
        'jspjspjspjspjspjspjspjspjspjspjspjspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Weapon(
        'confusion4',
        'jspjspjspjspjspjspjspjs',
        'stuc for 3 seconds',
        1,
    ),
    Weapon(
        'confusion5',
        'jspjspjspjspjspjspjspjspjspjpjspjspjspjspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Weapon(
        'confusion6',
        'jspjspjspjspjjspjspjspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Weapon(
        'confusion7',
        'jspspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Weapon(
        'confusion8',
        'jspjspjsspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Weapon(
        'confusion9',
        'pezihjfeà',
        'stuc for 3 seconds',
        1,
    ),

]


class Consumable:
    def __init__(self, name, description, effect, cost):
        self.name = name
        self.description = description
        self.effect = effect
        self.cost = cost 
        self.filename = f"Assets/png/armors/{self.name}.png"
        self.fileaname_hovered = f"Assets/png/armors/{self.name}_hovered.png"


consumables = [
    Consumable(
        'confusion',
        'jsp',
        'stun enemies for 3 seconds',
        8,
    ),
    Consumable(
        'confusion1',
        'jsp',
        'stun enemies for 3nds',
        2,
    ),
    Consumable(
        'confusion2',
        'jsp',
        'stuc for 3 seconds',
        18,
    ),
    Consumable(
        'confusion3',
        'jspjspjspjspjspjspjspjspjspjspjspjspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Consumable(
        'confusion4',
        'jspjspjspjspjspjspjspjs',
        'stuc for 3 seconds',
        1,
    ),
    Consumable(
        'confusion5',
        'jspjspjspjspjspjspjspjspjspjpjspjspjspjspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Consumable(
        'confusion6',
        'jspjspjspjspjjspjspjspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Consumable(
        'confusion7',
        'jspspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Consumable(
        'confusion8',
        'jspjspjsspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Consumable(
        'confusion9',
        'pezihjfeà',
        'stuc for 3 seconds',
        1,
    ),

]


class Misc:
    def __init__(self, name, description, effect, cost):
        self.name = name
        self.description = description
        self.effect = effect
        self.cost = cost 
        self.filename = f"Assets/png/armors/{self.name}.png"
        self.fileaname_hovered = f"Assets/png/armors/{self.name}_hovered.png"


miscs = [
    Misc(
        'confusion',
        'jsp',
        'stun enemies for 3 seconds',
        8,
    ),
    Misc(
        'confusion1',
        'jsp',
        'stun enemies for 3nds',
        2,
    ),
    Misc(
        'confusion2',
        'jsp',
        'stuc for 3 seconds',
        18,
    ),
    Misc(
        'confusion3',
        'jspjspjspjspjspjspjspjspjspjspjspjspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Misc(
        'confusion4',
        'jspjspjspjspjspjspjspjs',
        'stuc for 3 seconds',
        1,
    ),
    Misc(
        'confusion5',
        'jspjspjspjspjspjspjspjspjspjpjspjspjspjspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Misc(
        'confusion6',
        'jspjspjspjspjjspjspjspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Armor(
        'confusion7',
        'jspspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Misc(
        'confusion8',
        'jspjspjsspjsp',
        'stuc for 3 seconds',
        1,
    ),
    Misc(
        'confusion9',
        'pezihjfeà',
        'stuc for 3 seconds',
        1,
    ),

]


def main():
    window=GameWindow()
    arcade.run()


if __name__ == "__main__":
    main()



