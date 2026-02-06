from copy import deepcopy
from dataclasses import dataclass
import dataclasses
import random

from game.common.action import Action
from game.common.avatar import Avatar
from game.common.enums import *
from game.common.player import Player
import game.config as config   # this is for turns
from game.common.stations.refuge import Refuge
from game.controllers import refuge_controller
from game.controllers.attack_controller import Attack_Controller
from game.controllers.bot_movement_controller import BotMovementController
from game.controllers.bot_vision_controller import BotVisionController
from game.controllers.point_controller import PointController, PointData
from game.controllers.power_controller import PowerController
from game.controllers.refuge_controller import RefugeController
from game.fnaacm.bots.bot import Bot
from game.fnaacm.bots.crawler_bot import CrawlerBot
from game.fnaacm.bots.dumb_bot import DumbBot
from game.fnaacm.bots.ian_bot import IANBot
from game.fnaacm.bots.jumper_bot import JumperBot
from game.fnaacm.bots.support_bot import SupportBot
from game.utils.thread import CommunicationThread
from game.controllers.movement_controller import MovementController
from game.controllers.controller import Controller
from game.controllers.interact_controller import InteractController
from game.common.map.game_board import GameBoard
from game.config import MAX_NUMBER_OF_ACTIONS_PER_TURN
from game.utils.vector import Vector 


class MasterController(Controller):
    """
    `Master Controller Notes:`

        Give Client Objects:
            Takes a list of Player objects and places each one in the game world.

        Game Loop Logic:
            Increments the turn count as the game plays (look at the engine to see how it's controlled more).

        Interpret Current Turn Data:
            This accesses the gameboard in the first turn of the game and generates the game's seed.

        Client Turn Arguments:
            There are lines of code commented out that create Action Objects instead of using the enum. If your project
            needs Actions Objects instead of the enums, comment out the enums and use Objects as necessary.

        Turn Logic:
            This method executes every movement and interact behavior from every client in the game. This is done by
            using every other type of Controller object that was created in the project that needs to be managed
            here (InteractController, MovementController, other game-specific controllers, etc.).

        Create Turn Log:
            This method creates a dictionary that stores the turn, all client objects, and the gameboard's JSON file to
            be used as the turn log.

        Return Final Results:
            This method creates a dictionary that stores a list of the clients' JSON files. This represents the final
            results of the game.
    """
    def __init__(self):
        super().__init__()
        self.game_over: bool = False
        # self.event_timer = GameStats.event_timer   # anything related to events are commented it out until made
        # self.event_times: tuple[int, int] | None = None
        self.turn: int = 1
        self.current_world_data: dict = None
        self.movement_controller: MovementController = MovementController()
        self.interact_controller: InteractController = InteractController()
        self.bot_movement_controller: BotMovementController = BotMovementController()
        self.bot_vision_controller: BotVisionController = BotVisionController()
        self.bot_attack_controller: Attack_Controller = Attack_Controller()
        self.bots: dict[ObjectType, Bot] = {}
        self.refuge_controller: RefugeController = RefugeController()
        self.point_controller: PointController = PointController()
        self.power_controller: PowerController = PowerController()
        self.point_data = PointData()

    # Receives all clients for the purpose of giving them the objects they will control
    def give_clients_objects(self, clients: list[Player], world: dict):
        # starting_positions = [[3, 3], [3, 9]]   # would be done in generate game
        gb: GameBoard = world['game_board']
        avatars: dict[Vector, list[Avatar]] = gb.get_objects(ObjectType.AVATAR)
        for (pos, avatars_at_pos), client in zip(avatars.items(), clients):
            assert len(avatars_at_pos) == 1
            avatars_at_pos[0].position = pos
            client.avatar = avatars_at_pos[0]

    # Generator function. Given a key:value pair where the key is the identifier for the current world and the value is
    # the state of the world, returns the key that will give the appropriate world information
    def game_loop_logic(self, start=1):
        self.turn = start

        # Basic loop from 1 to max turns
        while True:
            # Wait until the next call to give the number
            yield str(self.turn)
            # Increment the turn counter by 1
            self.turn += 1

    # Receives world data from the generated game log and is responsible for interpreting it
    def interpret_current_turn_data(self, clients: list[Player], world: dict, turn):
        self.current_world_data = world

        if turn == 1:
            random.seed(world['game_board'].seed)
            # self.event_times = random.randrange(162, 172), random.randrange(329, 339)

        # cache references to every bot
        gb: GameBoard = world['game_board']
        for obj_type in BOT_OBJECT_TYPES:
            if obj_type == ObjectType.BOT:
                continue
            # FIXME: just look at it
            game_objects = list(gb.get_objects(obj_type).values())[0]
            self.bots[obj_type] = game_objects[0]

    # Receive a specific client and send them what they get per turn. Also obfuscates necessary objects.
    def client_turn_arguments(self, client: Player, turn):
        client.actions = []

        # Create deep copies of all objects sent to the player
        current_world = deepcopy(self.current_world_data["game_board"])    # what is current world and copy avatar
        copy_avatar = deepcopy(client.avatar)
        # Obfuscate data in objects that that player should not be able to see
        # Currently world data isn't obfuscated at all
        args = (self.turn, current_world, copy_avatar)
        return args

    # Perform the main logic that happens per turn
    def turn_logic(self, clients: list[Player], turn: int):
        if self.game_over:
            return

        game_board: GameBoard = self.current_world_data["game_board"]

        for battery in game_board.battery_spawners:
            battery.tick()
        for scrap_spawner in game_board.scrap_spawners:
            scrap_spawner.tick()
        for coin_spawner in game_board.coin_spawners:
            coin_spawner.tick()

        for client in clients:
            for i in range(MAX_NUMBER_OF_ACTIONS_PER_TURN):
                try:
                    self.movement_controller.handle_actions(client.actions[i], client, game_board)
                    self.interact_controller.handle_actions(client.actions[i], client, game_board)
                except IndexError:
                    pass
            self.interact_controller.handle_implicit_interactions(client.avatar, game_board)

        # pve game so only one client
        player = clients[0]
        assert player.avatar is not None

        self.refuge_controller.handle_actions(ActionType.NONE, player, game_board)

        support_bot: SupportBot | None = self.bots.get(ObjectType.SUPPORT_BOT)
        assert support_bot is not None
        assert isinstance(support_bot, SupportBot)
        for bot in self.bots.values():
            bot.stunned()

            if isinstance(bot, SupportBot):
                bot.tick()

            self.bot_vision_controller.handle_actions(player.avatar, bot, game_board)

            if bot.can_move(turn):
                moves = self.bot_movement_controller.calc_next_moves(bot, player.avatar, game_board, turn)
                assert not moves is None, f'{bot.__class__}\'s next move was... None?'
                for move in moves:
                    self.bot_movement_controller.handle_actions(move, bot, game_board, self.turn)

            attack = self.bot_attack_controller.calculate_attack_action(bot, player.avatar)
            self.bot_attack_controller.handle_actions(attack, player, game_board, bot, support_bot)

            if not player.avatar.is_alive:
                self.game_over = True
                break

        self.power_controller.handle_actions(ActionType.NONE, player, game_board)
        if player.avatar.power <= 0:
            self.game_over = True
        self.point_data = self.point_controller.handle_actions(player.avatar, game_board)

        # checks event logic at the end of round
        # self.handle_events(clients)

    # comment out for now, nothing is in place for event types yet
    # def handle_events(self, clients):
        # If it is time to run an event, master controller picks an event to run
        # if self.turn == self.event_times[0] or self.turn == self.event_times[1]:
        #    self.current_world_data["game_map"].generate_event(EventType.example, EventType.example)
        # event type.example is just a placeholder for now

    # Return serialized version of game
    def create_turn_log(self, clients: list[Player], turn: int):
        data = dict()
        data['tick'] = turn
        data['clients'] = [client.to_json() for client in clients]
        # Add things that should be thrown into the turn logs here
        data['game_board'] = self.current_world_data["game_board"].to_json()
        data['point_data'] = dataclasses.asdict(self.point_data)
        data['points_awarded'] = self.point_data.point_award

        return data

    # Gather necessary data together in results file
    def return_final_results(self, clients: list[Player], turn):
        data = dict()

        data['players'] = list()
        # Determine results
        for client in clients:
            data['players'].append(client.to_json())

        return data
