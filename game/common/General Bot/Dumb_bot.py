import random

from General_Bot_Commands import *
from game.controllers.master_controller import MasterController

class Dumb_Bot:
    def __init__(self):
        super().__init__()
        self.vision = 1
        self.movement_controller: MovementController = MovementController()
        self.master_controller: MasterController = MasterController()

    def movement(self):
        while not self.master_controller.game_over:
            moveNum = random.randint(1,4)
            match moveNum:
                case 1:
                    moveUp(self)
                case 2:
                    moveRight(self)
                case 3:
                    moveDown(self)
                case 4:
                    moveLeft(self)

    def playerScanning(self):

