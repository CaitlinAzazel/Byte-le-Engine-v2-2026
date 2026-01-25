from game.common.avatar import Avatar
from game.common.enums import *
from game.constants import INTERACT_TO_DIRECTION
from game.controllers.controller import Controller
from game.common.player import Player
from game.common.stations.station import Station
from game.common.map.game_board import GameBoard


class InteractController(Controller):
    """
    `Interact Controller Notes:`

        The Interact Controller manages the actions the player tries to execute. As the game is played, a player can
        interact with surrounding, adjacent stations and the space they're currently standing on.

        Example:
        ::
            x x x x x x
            x         x
            x   O     x
            x O A O   x
            x   O     x
            x x x x x x

        The given visual shows what players can interact with. "A" represents the avatar; "O" represents the spaces
        that can be interacted with (including where the "A" is); and "x" represents the walls and map border.

        These interactions are managed by using the provided ActionType enums in the enums.py file.
    """

    def __init__(self):
        super().__init__()

    def handle_implicit_interactions(self, avatar: Avatar, world: GameBoard) -> None:
        """
        handle things the player interacts with without needing an "INTERACT_*" action
        """
        for battery_spawner in world.battery_spawners:
            battery_spawner.handle_turn(avatar)
        for scrap_spawner in world.scrap_spawners:
            scrap_spawner.handle_turn(avatar)
        for coin_spawner in world.coin_spawners:
            coin_spawner.handle_turn(avatar)

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard) -> None:
        """
        Given the ActionType for interacting in a direction, the Player's avatar will engage with the object.
        :param action:
        :param client:
        :param world:
        :return: None
        """
        if action not in INTERACT_TO_DIRECTION:
            return
        direction = INTERACT_TO_DIRECTION[action]
            
        # find result in interaction
        target = client.avatar.position + direction
        stat: Station = world.get_top(target)

        if stat is not None and isinstance(stat, Station):
            stat.take_action(client.avatar)
