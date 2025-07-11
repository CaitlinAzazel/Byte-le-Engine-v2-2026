from General_Bot_Commands import *
from game.common.avatar import Avatar
from game.controllers.master_controller import MasterController
from game.common.map.game_board import GameBoard


class IANBot:
    def __init__(self):
        super().__init__()
        self.vision = 1
        self.movement_controller: MovementController = MovementController()
        self.master_controller: MasterController = MasterController()
        self.game_board: GameBoard = GameBoard()
        self.player_seen : bool = False
        self.boosted : bool = False
        self.avatar: Avatar = Avatar()
        self.playerX: 0
        self.playerY: 0
        self.stun = False
        self.stun_counter = 0

    def movement(self):
        if not self.master_controller.game_over:
            """A* algorithm here mapping to the the coords of the player, MOVES EVERY TURN, IF BOOSTED MOVE 2 SPACES PER TURN"""

    def player_scan(self):
        if not self.master_controller.game_over and not self.stun:
            self.player_seen, self.playerX, self.playerY = playerScan(self, 100)

    def stunned(self):
        """do nothing"""
        self.stun_counter += 1
        if self.stun_counter == 10:
            self.stun = False
            self.stun_counter = 0

    def action(self):
        self.player_scan()
        self.movement()