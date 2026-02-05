from game.client.user_client import UserClient
from game.common.enums import ObjectType, ActionType, BOT_OBJECT_TYPES


class Client(UserClient):

    def __init__(self):
        super().__init__()
        self.path = []
        self.current_goal = None
        self.goal_type = None
        self.next_generator_cost = 1
        self.last_battery_turn = 0
        self.hiding_in_refuge = False
        self.refuge_turns_left = 0
        self.bot_positions = []  # Cache bot positions

    def team_name(self):
        return "E-Bibby"

    def take_turn(self, turn, world, avatar):
        current = avatar.position
        if current is None:
            return []

        # Cache bot positions once per turn
        self.bot_positions = self.get_all_bot_positions(world)

        # Handle refuge hiding
        if self.hiding_in_refuge:
            self.refuge_turns_left -= 1
            if self.refuge_turns_left <= 0:
                self.hiding_in_refuge = False
                self.path = []
                self.current_goal = None
            return []

        # Check if we're adjacent to a generator with enough scrap
        scrap_count = avatar.get_quantity_of_item_type(ObjectType.SCRAP)
        if scrap_count >= self.next_generator_cost:
            interaction = self.try_interact_generator(world, current)
            if interaction:
                self.next_generator_cost += 1
                self.path = []
                self.current_goal = None
                return [interaction]

        # Check if adjacent to a coin - step on it
        coin_action = self.step_on_adjacent_coin(world, current)
        if coin_action:
            return [coin_action]

        # Check for nearby bots (using cached positions)
        bot_nearby = self.is_bot_within_3_tiles(current)
        battery_low = avatar.power < 50

        # If bot nearby and battery NOT low, flee to refuge
        if bot_nearby and not battery_low:
            refuge = self.find_nearest_refuge(world, current)
            if refuge:
                self.path = self.a_star(world, current, refuge)
                if self.path:
                    self.current_goal = refuge
                    self.goal_type = 'refuge'
                    next_pos = self.path.pop(0)
                    return [self.get_action_for_move(current, next_pos)]

        # Check if we just entered refuge
        on_tile = world.get_top(current)
        if on_tile and on_tile.object_type == ObjectType.REFUGE and self.goal_type == 'refuge':
            self.hiding_in_refuge = True
            self.refuge_turns_left = 4
            return []

        # Continue existing path
        if self.path:
            if len(self.path) > 0:
                next_pos = self.path[0]
                if self.can_move_to(world, next_pos):
                    self.path.pop(0)
                    return [self.get_action_for_move(current, next_pos)]
                else:
                    self.path = []
                    self.current_goal = None

        # Decide new goal
        goal = None

        # Priority 1: Battery if haven't collected in 30 turns OR battery is low
        if turn - self.last_battery_turn >= 30 or battery_low:
            batteries = [s.position for s in world.battery_spawners]
            if batteries:
                goal = self.find_closest(current, batteries)
                if goal:
                    self.goal_type = 'battery'
                    self.last_battery_turn = turn
                    self.path = self.a_star(world, current, goal)

        # Priority 2: Generator if we have enough scrap
        if not goal and scrap_count >= self.next_generator_cost and self.next_generator_cost <= 5:
            gen_adjacent = self.find_generator_adjacent_tile(world, current, self.next_generator_cost)
            if gen_adjacent:
                goal = gen_adjacent
                self.goal_type = 'generator'
                self.path = self.a_star(world, current, goal)

        # Priority 3: Scrap if we need more for next generator
        if not goal and self.next_generator_cost <= 5:
            scrap_spawners = [s.position for s in world.scrap_spawners]
            if scrap_spawners:
                goal = self.find_closest(current, scrap_spawners)
                if goal:
                    self.goal_type = 'scrap'
                    self.path = self.a_star(world, current, goal)

        # Execute new path
        if self.path:
            next_pos = self.path.pop(0)
            return [self.get_action_for_move(current, next_pos)]

        return []

    def get_all_bot_positions(self, world):
        """Cache all dangerous bot positions for this turn"""
        dangerous_bots = BOT_OBJECT_TYPES - {ObjectType.SUPPORT_BOT}
        positions = []

        for bot_type in dangerous_bots:
            bots = world.get_objects(bot_type)
            positions.extend(bots.keys())

        return positions

    def try_interact_generator(self, world, current):
        """Try to interact with adjacent generator"""
        directions = [
            (0, -1, ActionType.INTERACT_UP),
            (0, 1, ActionType.INTERACT_DOWN),
            (-1, 0, ActionType.INTERACT_LEFT),
            (1, 0, ActionType.INTERACT_RIGHT)
        ]

        for dx, dy, action in directions:
            pos = type(current)(current.x + dx, current.y + dy)
            if not world.is_valid_coords(pos):
                continue

            top = world.get_top(pos)
            if top and top.object_type == ObjectType.GENERATOR:
                if hasattr(top, 'active') and not top.active and hasattr(top, 'cost'):
                    if top.cost == self.next_generator_cost:
                        return action

        return None

    def step_on_adjacent_coin(self, world, current):
        """Move onto an adjacent coin spawner if there is one"""
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            pos = type(current)(current.x + dx, current.y + dy)
            if not world.is_valid_coords(pos):
                continue

            top = world.get_top(pos)
            if top and top.object_type == ObjectType.COIN:
                if self.can_move_to(world, pos):
                    return self.get_action_for_move(current, pos)

        return None

    def is_bot_within_3_tiles(self, current):
        """Check if any bot is within 3 tiles (uses cached positions)"""
        for bot_pos in self.bot_positions:
            dist = abs(bot_pos.x - current.x) + abs(bot_pos.y - current.y)
            if dist <= 3:
                return True
        return False

    def find_nearest_refuge(self, world, current):
        """Find closest refuge"""
        refuges = world.get_objects(ObjectType.REFUGE)
        if not refuges:
            return None

        return self.find_closest(current, list(refuges.keys()))

    def find_generator_adjacent_tile(self, world, current, cost):
        """Find a walkable tile adjacent to the target generator"""
        generators = world.get_objects(ObjectType.GENERATOR)
        candidates = []

        for pos, gen_list in generators.items():
            for gen in gen_list:
                if hasattr(gen, 'active') and not gen.active and hasattr(gen, 'cost'):
                    if gen.cost == cost:
                        # Find adjacent tiles
                        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                            adj = type(pos)(pos.x + dx, pos.y + dy)
                            if world.is_valid_coords(adj) and self.can_move_to(world, adj):
                                candidates.append(adj)

        if not candidates:
            return None

        return self.find_closest(current, candidates)

    def find_closest(self, current, positions):
        """Find closest position by Manhattan distance"""
        if not positions:
            return None

        return min(positions, key=lambda p: abs(p.x - current.x) + abs(p.y - current.y))

    def a_star(self, world, start, goal):
        """Lightweight A* pathfinding"""

        def heuristic(pos):
            return abs(pos.x - goal.x) + abs(pos.y - goal.y)

        open_list = [[heuristic(start), start, []]]
        closed = set()
        iterations = 0
        max_iterations = 200  # Reduced from 400

        while open_list and iterations < max_iterations:
            iterations += 1

            # Simple linear search for min (faster for small lists)
            min_idx = 0
            min_score = open_list[0][0]
            for i in range(1, len(open_list)):
                if open_list[i][0] < min_score:
                    min_score = open_list[i][0]
                    min_idx = i

            _, current, path = open_list.pop(min_idx)

            curr_tuple = (current.x, current.y)
            if curr_tuple in closed:
                continue
            closed.add(curr_tuple)

            # Goal check
            if current.x == goal.x and current.y == goal.y:
                return path

            # Explore neighbors
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                neighbor = type(current)(current.x + dx, current.y + dy)

                if not world.is_valid_coords(neighbor):
                    continue
                if (neighbor.x, neighbor.y) in closed:
                    continue
                if not self.can_move_to(world, neighbor):
                    continue

                new_path = path + [neighbor]
                f_score = len(new_path) + heuristic(neighbor)
                open_list.append([f_score, neighbor, new_path])

        return []

    def can_move_to(self, world, pos):
        """Check if position is walkable"""
        if not world.is_valid_coords(pos):
            return False

        top = world.get_top(pos)
        if top is None:
            return True

        obj_type = top.object_type

        # Can't move through
        if obj_type in [ObjectType.WALL, ObjectType.GENERATOR]:
            return False

        # Closed doors block
        if obj_type == ObjectType.DOOR:
            if hasattr(top, 'open') and not top.open:
                return False

        # Can move through
        if obj_type in [ObjectType.VENT, ObjectType.REFUGE]:
            return True

        return world.is_occupiable(pos)

    def get_action_for_move(self, current, target):
        """Convert position to movement action"""
        dx = target.x - current.x
        dy = target.y - current.y

        if dx == 1:
            return ActionType.MOVE_RIGHT
        elif dx == -1:
            return ActionType.MOVE_LEFT
        elif dy == 1:
            return ActionType.MOVE_DOWN
        elif dy == -1:
            return ActionType.MOVE_UP

        return None