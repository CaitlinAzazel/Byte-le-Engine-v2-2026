from game.fnaacm.game_object_list import GameObjectList
from game.fnaacm.stations.scrap_spawner import ScrapSpawner


class ScrapSpawnerList(GameObjectList[ScrapSpawner]):
    def __init__(self):
        super().__init__('scrap_spawners', ScrapSpawner)
