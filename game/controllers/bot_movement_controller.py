from logging import warning
import random
from typing import Optional
from game.common.avatar import Avatar
from game.controllers.pathfind_controller import a_star_path
from game.fnaacm.bots.bot import Bot
from game.common.enums import ActionType, ObjectType
from game.common.map.occupiable import Occupiable
from game.controllers.controller import Controller
from game.common.map.game_board import GameBoard
from game.fnaacm.bots.crawler_bot import CrawlerBot
from game.fnaacm.bots.dumb_bot import DumbBot
from game.fnaacm.bots.ian_bot import IANBot
from game.fnaacm.bots.jumper_bot import JumperBot
from game.fnaacm.bots.support_bot import SupportBot
from game.utils.vector import Vector


class BotMovementController(Controller):
    def __init__(self):
        super().__init__()

    def random_horizontal_move(self) -> ActionType:
        return random.choice([ActionType.MOVE_RIGHT, ActionType.MOVE_LEFT,])

    def random_vertical_move(self) -> ActionType:
        return random.choice([ActionType.MOVE_UP, ActionType.MOVE_DOWN,])

    def random_move(self) -> ActionType:
        return random.choice([ActionType.MOVE_UP, ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT, ActionType.MOVE_LEFT])

    @staticmethod
    def vector_to_action(delta: Vector) -> Optional[ActionType]:
        if delta.x == 0 and delta.y == -1:
            return ActionType.MOVE_UP
        if delta.x == 0 and delta.y == 1:
            return ActionType.MOVE_DOWN
        if delta.x == -1 and delta.y == 0:
            return ActionType.MOVE_LEFT
        if delta.x == 1 and delta.y == 0:
            return ActionType.MOVE_RIGHT
        return None

    def dumb_patrol(self) -> list[ActionType]:
        return [self.random_move()]

    def dumb_hunt(self, dumb_bot: DumbBot, avatar: Avatar) -> list[ActionType]:
        player_pos = avatar.position
        direction_to_player = (player_pos - dumb_bot.position)
        playerX = direction_to_player.x
        playerY = direction_to_player.y
        if playerX > 0 and playerY == 0:
            return [ActionType.MOVE_RIGHT]
        elif playerX < 0 and playerY == 0:
            return [ActionType.MOVE_LEFT]
        elif playerX == 0 and playerY > 0:
            return [ActionType.MOVE_DOWN]
        elif playerX == 0 and playerY < 0:
            return [ActionType.MOVE_UP]
        elif playerX > 0 and playerY > 0:
            if playerY > playerX:
                return [ActionType.MOVE_DOWN]
            else:
                return [ActionType.MOVE_RIGHT]
        elif playerX < 0 and playerY < 0:
            if playerY < playerX:
                return [ActionType.MOVE_UP]
            else:
                return [ActionType.MOVE_LEFT]
        elif playerX > 0 and playerY < 0:
            if abs(playerY) > playerX:
                return [ActionType.MOVE_UP]
            else:
                return [ActionType.MOVE_RIGHT]
        elif playerX < 0 and playerY > 0:
            if playerY > abs(playerX):
                return [ActionType.MOVE_DOWN]
            else:
                return [ActionType.MOVE_LEFT]
        else:
            return self.dumb_patrol()

    def crawler_patrol(self) -> list[ActionType]:
        return []

    def crawler_hunt(self, crawler_bot: CrawlerBot, avatar: Avatar, world: GameBoard) -> list[ActionType]:
        bot_pos = crawler_bot.position
        player_pos = avatar.position

        path = a_star_path(
            start=bot_pos,
            goal=player_pos,
            world=world,
            allow_vents=True,  # crawler special rule
        )

        if not path or len(path) < 2:
            warning(f'could not find a valid path')
            return []

        next_step: Vector = path[1]
        direction = next_step - bot_pos
        action = self.vector_to_action(direction)
        if not action:
            return []

        return [action, action] if crawler_bot.boosted else [action]

    def ian_patrol(self) -> list[ActionType]:
        return []

    def ian_hunt(self, ian_bot: IANBot, avatar: Avatar, world: GameBoard) -> list[ActionType]:
        path = a_star_path(
            start=ian_bot.position,
            goal=avatar.position,
            world=world,
            allow_vents=False
        )

        if not path or len(path) < 2:
            return []

        next_step = path[1]
        delta = next_step - ian_bot.position
        action = self.vector_to_action(delta)
        if not action:
            return []

        return [action, action] if ian_bot.boosted else [action]

    def jumper_patrol(self) -> list[ActionType]:
        return [self.random_vertical_move(), self.random_horizontal_move()]

    def jumper_hunt(self, jumper_bot: JumperBot, avatar: Avatar) -> list[ActionType]:
        player_pos = avatar.position
        direction_to_player = (player_pos - jumper_bot.position)
        playerX = direction_to_player.x
        playerY = direction_to_player.y
        if jumper_bot.boosted:
            if jumper_bot.cooldown != 0:
                jumper_bot.cooldown -= 1
                if playerX > 0 and playerY == 0:
                    randomvar = random.choice([ActionType.MOVE_UP, ActionType.MOVE_DOWN])
                    return [randomvar, ActionType.MOVE_RIGHT]
                elif playerX < 0 and playerY == 0:
                    randomvar = random.choice([ActionType.MOVE_UP, ActionType.MOVE_DOWN])
                    return [randomvar, ActionType.MOVE_LEFT]
                elif playerX == 0 and playerY > 0:
                    randomvar = random.choice([ActionType.MOVE_LEFT, ActionType.MOVE_RIGHT])
                    return [ActionType.MOVE_DOWN, randomvar]
                elif playerX == 0 and playerY < 0:
                    randomvar = random.choice([ActionType.MOVE_LEFT, ActionType.MOVE_RIGHT])
                    return [ActionType.MOVE_UP, randomvar]
                elif playerX > 0 and playerY > 0:
                    return [ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT]
                elif playerX < 0 and playerY < 0:
                    return [ActionType.MOVE_UP, ActionType.MOVE_LEFT]
                elif playerX > 0 and playerY < 0:
                    return [ActionType.MOVE_UP, ActionType.MOVE_RIGHT]
                elif playerX < 0 and playerY > 0:
                    return [ActionType.MOVE_DOWN, ActionType.MOVE_LEFT]
            elif jumper_bot.cooldown == 0:
                jumper_bot.cooldown = random.randint(1,3)
                if playerX > 0 and playerY == 0:
                    return [ActionType.MOVE_RIGHT, ActionType.MOVE_RIGHT]
                elif playerX < 0 and playerY == 0:
                    return [ActionType.MOVE_LEFT, ActionType.MOVE_LEFT]
                elif playerX == 0 and playerY > 0:
                    return [ActionType.MOVE_DOWN, ActionType.MOVE_DOWN]
                elif playerX == 0 and playerY < 0:
                    return [ActionType.MOVE_UP, ActionType.MOVE_UP]
                elif playerX > 0 and playerY > 0:
                    return [ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT, ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT]
                elif playerX < 0 and playerY < 0:
                    return [ActionType.MOVE_UP, ActionType.MOVE_LEFT, ActionType.MOVE_UP, ActionType.MOVE_LEFT]
                elif playerX > 0 and playerY < 0:
                    return [ActionType.MOVE_UP, ActionType.MOVE_RIGHT, ActionType.MOVE_UP, ActionType.MOVE_RIGHT]
                elif playerX < 0 and playerY > 0:
                    return [ActionType.MOVE_DOWN, ActionType.MOVE_LEFT, ActionType.MOVE_DOWN, ActionType.MOVE_LEFT]
        elif not jumper_bot.boosted:
            if jumper_bot.cooldown != 0:
                jumper_bot.cooldown -= 1
                return []
            if playerX > 0 and playerY == 0:
                randomvar = random.choice([ActionType.MOVE_UP, ActionType.MOVE_DOWN])
                return [randomvar, ActionType.MOVE_RIGHT]
            elif playerX < 0 and playerY == 0:
                randomvar = random.choice([ActionType.MOVE_UP, ActionType.MOVE_DOWN])
                return [randomvar, ActionType.MOVE_LEFT]
            elif playerX == 0 and playerY > 0:
                randomvar = random.choice([ActionType.MOVE_LEFT, ActionType.MOVE_RIGHT])
                return [ActionType.MOVE_DOWN, randomvar]
            elif playerX == 0 and playerY < 0:
                randomvar = random.choice([ActionType.MOVE_LEFT, ActionType.MOVE_RIGHT])
                return [ActionType.MOVE_UP, randomvar]
            elif playerX > 0 and playerY > 0:
                return [ActionType.MOVE_DOWN, ActionType.MOVE_RIGHT]
            elif playerX < 0 and playerY < 0:
                return [ActionType.MOVE_UP, ActionType.MOVE_LEFT]
            elif playerX > 0 and playerY < 0:
                return [ActionType.MOVE_UP, ActionType.MOVE_RIGHT]
            elif playerX < 0 and playerY > 0:
                return [ActionType.MOVE_DOWN, ActionType.MOVE_LEFT]

        return self.jumper_patrol()

    def calc_next_moves(self, bot: Bot, avatar: Avatar, world: GameBoard, turn: int) -> list[ActionType]:
        """
        :return: moves `bot` should take to get wherever it wants to go
        """
        moves = []
        if bot.is_stunned:
            return moves
        if turn % bot.turn_delay != 0:
            return moves
        if isinstance(bot, SupportBot):
            return moves

        if bot.can_see_player:
            if isinstance(bot, CrawlerBot):
                moves = self.crawler_hunt(bot, avatar, world)
            elif isinstance(bot, DumbBot):
                moves = self.dumb_hunt(bot, avatar)
            elif isinstance(bot, IANBot):
                moves = self.ian_hunt(bot, avatar, world)
            elif isinstance(bot, JumperBot):
                moves = self.jumper_hunt(bot, avatar)
        else:
            if isinstance(bot, CrawlerBot):
                moves = self.crawler_patrol()
            elif isinstance(bot, DumbBot):
                moves = self.dumb_patrol()
            elif isinstance(bot, IANBot):
                moves = self.ian_patrol()
            elif isinstance(bot, JumperBot):
                moves = self.jumper_patrol()

        return moves

    def handle_actions(self, action: ActionType, bot: Bot, world: GameBoard, turn: int = 0):
        """
        Noah's Note: Calculate the Bot's desired position which should return a list of movement actions,
            and then validate and process each movement action

        Import the Position of the Bot on the Gameboard
        - Define movement vectors
        - set destination variable and combine movement vectors with the current position vector
        - validate that the bot can move into a space that is occupiable
        - validate that two bots don't share the same space
        """
        direction: Vector
        match action:
            case ActionType.MOVE_UP:
                direction = Vector(x=0, y=-1)
            case ActionType.MOVE_DOWN:
                direction = Vector(x=0, y=1)
            case ActionType.MOVE_LEFT:
                direction = Vector(x=-1, y=0)
            case ActionType.MOVE_RIGHT:
                direction = Vector(x=1, y=0)
            case _:  # default case
                return

        destination: Vector = bot.position + direction

        if not world.can_object_occupy(destination, bot):
            return

        world.update_object_position(destination, bot)

