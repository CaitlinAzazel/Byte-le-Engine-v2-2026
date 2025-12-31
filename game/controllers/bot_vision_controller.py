from game.common.avatar import Avatar
from game.common.stations.refuge import Refuge
from game.fnaacm.bots.bot import Bot
from game.common.enums import ActionType, ObjectType
from game.common.map.occupiable import Occupiable
from game.controllers.controller import Controller
from game.common.map.game_board import GameBoard
from game.utils.vector import Vector


class BotVisionController(Controller):
    def __init__(self):
        super().__init__()

    def can_see_avatar(self, avatar: Avatar, bot: Bot, world: GameBoard) -> bool:
        assert avatar.position is not None
        distance_to_player: int = bot.position.distance(avatar.position)
        in_vision: bool = distance_to_player <= bot.get_current_vision_radius()
        if not in_vision:
            return False

        positions_between = Vector.get_positions_overlapped_by_line(bot.position, avatar.position)
        for position in positions_between:
            tile_objects = world.get(position)
            assert tile_objects is not None
            if not bot._is_tile_open(tile_objects):
                return False

        if Refuge.global_occupied:
            return False

        return True

    def handle_actions(self, avatar: Avatar, bot: Bot, world : GameBoard ):
        """
        Noah's Note: Calculate the Bot's desired position which should return a list of movement actions,
            and then validate and process each movement action

        Import the Position of the Bot on the Gameboard
        - Define movement vectors
        - set destination variable and combine movement vectors with the current position vector
        - validate that the bot can move into a space that is occupiable
        - validate that two bots don't share the same space
        """
        bot.can_see_player = self.can_see_avatar(avatar, bot, world)
