class fight():
    def __init__(self):
        self.dead_player = False
        self.enemy = None
        self.dead_enemy = False
        self.turn = 0
        self.boost = {"Atk": False, "Def": False}
        self.action = 0
        self.object = 0

    def fight_enemy(self):
        if self.player.health == 0 and not self.dead_player:
            self.dead_player = True

        elif self.enemy.health == 0 and not self.dead_enemy:
            self.dead_enemy = True

        if self.player.velocity >= self.enemy.velocity:
            self.turn = 1
            # Action
            if self.action == 0:
                print("Attaque")
                print("Inventaire")

            if self.action == 1:
                print("Player attaque")
                amount_dealt = int(self.player.attack + self.player.attack_boost - self.enemy.defence)

                if amount_dealt < 0:
                    amount_dealt = 0
                self.enemy.damage(amount_dealt)
                print("T'as infligé tel montant de degats")
            self.action = 0
            self.turn = 2

            if self.action == 2:

                if self.object == 0:
                    print("Fonction pour ouvrir l'inventaire")

        else:
            self.turn = 2
            amount_received = int(self.enemy.attack - self.player.defence)
            if amount_received < 0:
                amount_received = 0
            self.player.damage(amount_received)
            print("T'as reçu tel montant de degats")

        if self.dead_enemy:
            self.player.xp += self.enemy.xp
            self.player.level_update()
            if self.player.level_up:
                print("T'as augmenté de level")
                self.player.level_up = False

        if self.dead_player:
            print("Vous etes mort . Retour au menu.")
            self.enemy_hp = self.enemy_max_hp