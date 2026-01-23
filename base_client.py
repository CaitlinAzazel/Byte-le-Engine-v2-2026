from game.client.user_client import UserClient
from game.common.enums import ObjectType, ActionType

class Client(UserClient):

    def __init__(self):
        super().__init__()

    def team_name(self):
        """
        Allows the team to set a team name.
        :return: Your team name
        """
        return "William Afton"

    def take_turn(self, turn, actions, world, avatar):
        """
        This is where your AI will decide what to do.
        :param turn:        The current turn of the game.
        :param actions:     This is the actions object that you will add effort allocations or decrees to.
        :param world:       Generic world information
        """
        current = avatar.position
        if current is None:
            return []

        # Get all coins on the board
        coins = world.get_objects(ObjectType.COIN)
        if not coins:
            return []  # No coins, do nothing

        # Choose the closest coin (Manhattan distance)
        goal = min(coins.keys(), key=lambda v: abs(v.x - current.x) + abs(v.y - current.y))

        # Decide move toward the coin
        move = self.step_toward(world, current, goal)
        if move:
            return [move]

        return []

    def step_toward(self, world, current, goal):
        best_move = None
        best_dist = abs(current.x - goal.x) + abs(current.y - goal.y)

        # Check adjacent tiles
        directions = [
            (ActionType.MOVE_UP, 0, -1),
            (ActionType.MOVE_DOWN, 0, 1),
            (ActionType.MOVE_LEFT, -1, 0),
            (ActionType.MOVE_RIGHT, 1, 0),
        ]

        for action, dx, dy in directions:
            nx, ny = current.x + dx, current.y + dy

            # Skip tiles with walls
            blocked = any(obj.x == nx and obj.y == ny for obj in world.get_objects(ObjectType.WALL))
            if blocked:
                continue

            blocked = any(obj.x == nx and obj.y == ny for obj in world.get_objects(ObjectType.GENERATOR))
            if blocked:
                continue
            # Skip out-of-bounds tiles
            if nx < 0 or nx >= world.map_size.x or ny < 0 or ny >= world.map_size.y:
                continue

            # Check if this move reduces distance
            dist = abs(nx - goal.x) + abs(ny - goal.y)
            if dist < best_dist:
                best_dist = dist
                best_move = action

        return best_move

