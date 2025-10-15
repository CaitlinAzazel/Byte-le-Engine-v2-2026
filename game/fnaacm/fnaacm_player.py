from game.common.enums import ActionType, ObjectType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.common.avatar import Avatar

class FNAACMPlayer(Player):
    def __init__(self, code: object | None = None, team_name: str | None = None, actions: list[ActionType] = [],
                 avatar: Avatar | None = None):
        super().__init__(code, team_name, actions, avatar)
        self.health = 3
        self.tempPower = 0
        self.pointsTotal = 0

    # def moveLeft(self):
    #     MovementController.handle_actions(self.movement_controller, ActionType(4), self.player, self.gameboard)
    #
    # def moveUp(self):
    #     MovementController.handle_actions(self.movement_controller, ActionType(2), self.player, self.gameboard)
    #
    # def moveRight(self):
    #     MovementController.handle_actions(self.movement_controller, ActionType(5), self.player, self.gameboard)
    #
    # def moveDown(self):
    #     MovementController.handle_actions(self.movement_controller, ActionType(3), self.player, self.gameboard)
    #
    # def hit(self):
    #     stun()
    #     self.health -= 1
    #     self.tempPower = player.power(self) - 50
    #     if self.tempPower < 0:
    #         self.tempPower = 0
    #     player.power(self, self.tempPower)
    #     if self.health <= 0:
    #         MasterController.game_over = True

    def addPoint(self):
        if not self.in_refuge:
            self.pointsTotal += 1
        else:
            self.pointsTotal += 0

    def action(self):
        self.addPoint()

    def in_refuge(self) -> bool:
        # FIXME: replace with real check
        return False

    def in_vent(self, gameboard: GameBoard) -> bool:
        return gameboard.object_is_found_at(self.avatar.position, ObjectType.VENT)

        # get the tile the player is standing on
        # look for a vent
        # return whether or not vent is found
