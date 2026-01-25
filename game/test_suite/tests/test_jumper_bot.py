import unittest

from game.common.avatar import Avatar
from game.common.enums import ActionType
from game.common.game_object import GameObject
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.fnaacm.bots.jumper_bot import JumperBot
from game.utils.vector import Vector
from game.controllers.movement_controller import MovementController
from game.controllers.bot_movement_controller import BotMovementController


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.jumpBot = JumperBot()
        self.movementController = MovementController()
        self.botController = BotMovementController()
        self.jumpBot.vector = Vector(3, 3)
        self.avatar_start_pos = self.jumpBot.vector.add_y(1)
        self.avatar = Avatar(position=self.avatar_start_pos)
        self.locations: dict[Vector, list[GameObject]] = {
            self.jumpBot.vector: [self.jumpBot],
            self.avatar_start_pos: [self.avatar],
        }
        self.game_board = GameBoard(0, Vector(5, 5), self.locations)
        self.player = Player(avatar=self.avatar)
        self.game_board.generate_map()

    def test_init(self):
        self.assertEqual(self.jumpBot.boosted, False)
        self.assertEqual(self.jumpBot.stun, False)
        self.assertEqual(self.jumpBot.cooldown, 0)
        self.assertEqual(self.jumpBot.vision, 2)

    def test_movement(self):
        action = self.botController.jumper_patrol()
        actionList = ([ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT], [ActionType.MOVE_DOWN, ActionType.MOVE_LEFT], [ActionType.MOVE_UP, ActionType.MOVE_RIGHT], [ActionType.MOVE_UP, ActionType.MOVE_LEFT])
        self.assertIn(action, actionList)

    def test_player_seen_movement_down(self):
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        actionList = ([ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT], [ActionType.MOVE_DOWN, ActionType.MOVE_LEFT])
        self.assertIn(action, actionList)

    def test_player_seen_movement_up(self):
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        actionList = ([ActionType.MOVE_UP, ActionType.MOVE_RIGHT], [ActionType.MOVE_UP, ActionType.MOVE_LEFT])
        self.assertIn(action, actionList)

    def test_player_seen_movement_right(self):
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        actionList = ([ActionType.MOVE_UP, ActionType.MOVE_RIGHT], [ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT])
        self.assertIn(action, actionList)

    def test_player_seen_movement_left(self):
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        actionList = ([ActionType.MOVE_UP, ActionType.MOVE_LEFT], [ActionType.MOVE_DOWN, ActionType.MOVE_LEFT])
        self.assertIn(action, actionList)

    def test_player_seen_movement_down_right(self):
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_DOWN, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        self.assertEqual(action, [ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT])

    def test_player_seen_movement_down_left(self):
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_DOWN, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        self.assertEqual(action, [ActionType.MOVE_DOWN, ActionType.MOVE_LEFT])

    def test_player_seen_movement_up_right(self):
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        self.assertEqual(action, [ActionType.MOVE_UP, ActionType.MOVE_RIGHT])

    def test_player_seen_movement_up_left(self):
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        self.assertEqual(action, [ActionType.MOVE_UP, ActionType.MOVE_LEFT])

    def test_boosted_on_cooldown_player_seen_movement_down(self):
        self.jumpBot.cooldown = 1
        self.jumpBot.boosted = True
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        actionList = ([ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT], [ActionType.MOVE_DOWN, ActionType.MOVE_LEFT])
        self.assertIn(action, actionList)

    def test_boosted_on_cooldown_player_seen_movement_up(self):
        self.jumpBot.cooldown = 1
        self.jumpBot.boosted = True
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        actionList = ([ActionType.MOVE_UP, ActionType.MOVE_RIGHT], [ActionType.MOVE_UP, ActionType.MOVE_LEFT])
        self.assertIn(action, actionList)

    def test_boosted_on_cooldown_player_seen_movement_right(self):
        self.jumpBot.cooldown = 1
        self.jumpBot.boosted = True
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        actionList = ([ActionType.MOVE_UP, ActionType.MOVE_RIGHT], [ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT])
        self.assertIn(action, actionList)

    def test_boosted_on_cooldown_player_seen_movement_left(self):
        self.jumpBot.cooldown = 1
        self.jumpBot.boosted = True
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        actionList = ([ActionType.MOVE_UP, ActionType.MOVE_LEFT], [ActionType.MOVE_DOWN, ActionType.MOVE_LEFT])
        self.assertIn(action, actionList)

    def test_boosted_on_cooldown_player_seen_movement_down_right(self):
        self.jumpBot.cooldown = 1
        self.jumpBot.boosted = True
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_DOWN, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        self.assertEqual(action, [ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT])

    def test_boosted_on_cooldown_player_seen_movement_down_left(self):
        self.jumpBot.cooldown = 1
        self.jumpBot.boosted = True
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_DOWN, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        self.assertEqual(action, [ActionType.MOVE_DOWN, ActionType.MOVE_LEFT])

    def test_boosted_on_cooldown_player_seen_movement_up_right(self):
        self.jumpBot.cooldown = 1
        self.jumpBot.boosted = True
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        self.assertEqual(action, [ActionType.MOVE_UP, ActionType.MOVE_RIGHT])

    def test_boosted_on_cooldown_player_seen_movement_up_left(self):
        self.jumpBot.cooldown = 1
        self.jumpBot.boosted = True
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        self.assertEqual(action, [ActionType.MOVE_UP, ActionType.MOVE_LEFT])

    def test_boosted_not_on_cooldown_player_seen_movement_down(self):
        self.jumpBot.cooldown = 0
        self.jumpBot.boosted = True
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        self.assertEqual(action, [ActionType.MOVE_DOWN, ActionType.MOVE_DOWN])

    def test_boosted_not_on_cooldown_player_seen_movement_up(self):
        self.jumpBot.cooldown = 0
        self.jumpBot.boosted = True
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        self.assertEqual(action, [ActionType.MOVE_UP, ActionType.MOVE_UP])

    def test_boosted_not_on_cooldown_player_seen_movement_right(self):
        self.jumpBot.cooldown = 0
        self.jumpBot.boosted = True
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        self.assertEqual(action, [ActionType.MOVE_RIGHT, ActionType.MOVE_RIGHT])

    def test_boosted_not_on_cooldown_player_seen_movement_left(self):
        self.jumpBot.cooldown = 0
        self.jumpBot.boosted = True
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        self.assertEqual(action, [ActionType.MOVE_LEFT, ActionType.MOVE_LEFT])

    def test_boosted_not_on_cooldown_player_seen_movement_down_right(self):
        self.jumpBot.cooldown = 0
        self.jumpBot.boosted = True
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_DOWN, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        self.assertEqual(action, [ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT, ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT])

    def test_boosted_not_on_cooldown_player_seen_movement_down_left(self):
        self.jumpBot.cooldown = 0
        self.jumpBot.boosted = True
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_DOWN, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        self.assertEqual(action, [ActionType.MOVE_DOWN, ActionType.MOVE_LEFT, ActionType.MOVE_DOWN, ActionType.MOVE_LEFT])

    def test_boosted_not_on_cooldown_player_seen_movement_up_right(self):
        self.jumpBot.cooldown = 0
        self.jumpBot.boosted = True
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_RIGHT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        self.assertEqual(action, [ActionType.MOVE_UP, ActionType.MOVE_RIGHT, ActionType.MOVE_UP, ActionType.MOVE_RIGHT])

    def test_boosted_not_on_cooldown_player_seen_movement_up_left(self):
        self.jumpBot.cooldown = 0
        self.jumpBot.boosted = True
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_LEFT, self.player, self.game_board)
        self.movementController.handle_actions(ActionType.MOVE_UP, self.player, self.game_board)
        action = self.botController.jumper_hunt(self.jumpBot, self.avatar)
        self.assertEqual(action, [ActionType.MOVE_UP, ActionType.MOVE_LEFT, ActionType.MOVE_UP, ActionType.MOVE_LEFT])

    # def test_action_player_seen(self):
    #     self.jumpBot.can_see_player()
    #
    # def test_action_player_unseen(self):
    #
    #     actionList = ([ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT], [ActionType.MOVE_DOWN, ActionType.MOVE_LEFT],
    #                   [ActionType.MOVE_UP, ActionType.MOVE_RIGHT], [ActionType.MOVE_UP, ActionType.MOVE_LEFT])
    #     self.assertIn(self.jumpBot.action(), actionList)