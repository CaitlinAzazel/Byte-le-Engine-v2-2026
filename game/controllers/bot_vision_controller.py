from game.common.avatar import Avatar
from game.common.map.game_object_container import GameObjectContainer
from game.common.stations.refuge import Refuge
from game.fnaacm.bots.bot import Bot
from game.common.enums import ActionType, ObjectType
from game.common.map.occupiable import Occupiable
from game.controllers.controller import Controller
from game.common.map.game_board import GameBoard
from game.utils.vector import Vector


class BotVisionController(Controller):
    """
    responsible for updating `Bot.can_see_player` every turn
    """

    def is_tile_open(self, bot: Bot, tile_data: GameObjectContainer) -> bool:
        """
        determines if a tile "blocks" this bot's line of sight or not
        """
        for game_object in tile_data:
            # "see through" other bots and players
            if isinstance(game_object, Bot):
                continue
            if isinstance(game_object, Avatar):
                continue

            # crawler can occupy vents, so it can see into them; other bots cannot
            # works for everything besides things like windows (cannot stand in them, but you can see through them)
            if isinstance(game_object, Occupiable) and not game_object.can_be_occupied_by(bot):
                return False

        return True

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
            if not self.is_tile_open(bot, tile_objects):
                return False

        if Refuge.global_occupied:
            return False

        return True

    def handle_actions(self, avatar: Avatar, bot: Bot, world : GameBoard ):
        bot.can_see_player = self.can_see_avatar(avatar, bot, world)
