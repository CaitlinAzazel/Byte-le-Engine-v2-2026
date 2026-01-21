import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from typing import Callable, Any

from game.config import MAX_TICKS
from game.utils.vector import Vector
from game.common.enums import ObjectType

from visualizer.bytesprites.bytesprite import ByteSprite
from visualizer.bytesprites.tileBS import TileBS
from visualizer.bytesprites.wallBS import WallBS
from visualizer.bytesprites.scrapBS import ScrapBS
from visualizer.bytesprites.ventBS import VentBS
from visualizer.bytesprites.generatorBS import GeneratorBS
from visualizer.bytesprites.coinBS import CoinBS
from visualizer.bytesprites.avatarBS import AvatarBS
from visualizer.bytesprites.botBS import MovingBotBS
from visualizer.bytesprites.boosterbotBS import BoosterBotBS
from visualizer.bytesprites.doorBS import DoorBS
from visualizer.bytesprites.safeSpotBS import SafeSpotBS
from visualizer.bytesprites.batteryBS import BatteryBS

from visualizer.templates.menu_templates import Basic, MenuTemplate
from visualizer.templates.playback_template import PlaybackTemplate, PlaybackButtons
from visualizer.templates.game_frame import GameFrame
from visualizer.templates.scoreboard_template import ScoreboardTemplate


class Adapter:
    """
    The Adapter class can be considered the "Master Controller" of the Visualizer; it works in tandem with main.py.
    Main.py will call many of the methods that are provided in here to keep the Visualizer moving smoothly.
    """

    def __init__(self, screen: pygame.Surface):
        self.screen: pygame.Surface = screen
        self.bytesprites: list[ByteSprite] = []
        self.populate_bytesprite: pygame.sprite.Group = pygame.sprite.Group()
        self.menu: MenuTemplate = Basic(screen, 'Five Nights at The ACM')
        self.playback: PlaybackTemplate = PlaybackTemplate(screen)
        self.turn_number: int = 0
        self.turn_max: int = MAX_TICKS
        self.game_frame = GameFrame(self.screen)

        # Fixed: scoreboard using self.surface from InfoTemplate
        self.scoreboard = ScoreboardTemplate(
            self.screen,
            Vector(0, 0),       # top-left position
            Vector(1200, 200),  # size
            font="Arial",        # font
            color="#FFFFFF"      # font color
        )

    # ---------------- Start Menu Methods ----------------
    def start_menu_event(self, event: pygame.event) -> Any:
        """
        Handle events in the start menu.
        """
        return self.menu.start_events(event)

    def start_menu_render(self) -> None:
        """
        Render the start menu.
        """
        self.menu.start_render()

    # ---------------- Playback / Runtime Methods ----------------
    def on_event(self, event) -> PlaybackButtons:
        """
        Handle playback events.
        """
        return self.playback.playback_events(event)

    def prerender(self) -> None:
        """
        Handle any pre-animation updates per frame.
        """
        ...

    def continue_animation(self) -> None:
        """
        Used after main.py continue_animation()
        """
        ...

    def recalc_animation(self, turn_log: dict) -> None:
        """
        Called every time the turn changes.
        Updates the turn number and scoreboard.
        """
        self.turn_number = turn_log['tick']
        self.scoreboard.recalc_animation(turn_log)

    # ---------------- Bytesprite Factories ----------------
    def populate_bytesprite_factories(self) -> dict[int, Callable[[pygame.Surface], ByteSprite]]:
        return {
            # ---- Static tiles ----
            ObjectType.TILE.value: TileBS.create_bytesprite,
            ObjectType.WALL.value: WallBS.create_bytesprite,
            ObjectType.SCRAP_SPAWNER.value: ScrapBS.create_bytesprite,
            ObjectType.VENT.value: VentBS.create_bytesprite,
            ObjectType.GENERATOR.value: GeneratorBS.create_bytesprite,
            ObjectType.COIN.value: CoinBS.create_bytesprite,
            ObjectType.REFUGE.value: SafeSpotBS.create_bytesprite,
            ObjectType.BATTERY.value: BatteryBS.create_bytesprite,

            # ---- Avatar ----
            ObjectType.AVATAR.value: AvatarBS.create_bytesprite,

            # ---- Moving bots ----
            ObjectType.IAN_BOT.value: lambda screen: MovingBotBS.create_bytesprite(screen, "IanBot.png"),
            ObjectType.JUMPER_BOT.value: lambda screen: MovingBotBS.create_bytesprite(screen, "JumperBot.png"),
            ObjectType.DUMB_BOT.value: lambda screen: MovingBotBS.create_bytesprite(screen, "DumbBot.png"),
            ObjectType.CRAWLER_BOT.value: lambda screen: MovingBotBS.create_bytesprite(screen, "CrawlerBot.png"),

            # ---- Booster bot ----
            ObjectType.SUPPORT_BOT.value: BoosterBotBS.create_bytesprite,

            # ---- Door ----
            ObjectType.DOOR.value: DoorBS.create_bytesprite,
        }

    # ---------------- Render Methods ----------------
    def render(self) -> None:
        """
        Render game frame, scoreboard, and playback UI.
        """
        # Draw the game background as transparent black outside the frame
        frame_rect = self.game_frame.get_rect()
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))  # semi-transparent black
        overlay.fill((0, 0, 0, 0), frame_rect)  # clear out game area
        self.screen.blit(overlay, (0, 0))

        # Draw the border
        self.game_frame.render()

        # Draw the scoreboard (turns + scores)
        self.scoreboard.render()

        # Draw playback buttons/UI
        self.playback.playback_render()

    def clean_up(self) -> None:
        """
        Cleanup after rendering each frame.
        """
        ...

    # ---------------- Results / End Screen ----------------
    def results_load(self, results: dict) -> None:
        """
        Load the end screen for the visualizer.
        """
        self.menu.load_results_screen(results)

    def results_event(self, event: pygame.event) -> Any:
        """
        Handle events on the end screen.
        """
        return self.menu.results_events(event)

    def results_render(self) -> None:
        """
        Render the results / end screen.
        """
        self.menu.results_render()
