from game.client.user_client import UserClient
from game.common.enums import ObjectType, ActionType, BOT_OBJECT_TYPES


class Client(UserClient):

    def __init__(self):
        super().__init__()
        self.path = []
        self.current_goal = None
        self.goal_type = None
        self.generators_activated = 0
        self.waiting_for_respawn = False
        self.wait_location = None
        self.last_scrap_pickup_turn = -10
        self.hiding_in_refuge = False
        self.refuge_turns_left = 0
        self.bot_positions = {}  # Changed to dict to track positions
        self.previous_bot_positions = {}

    def team_name(self):
        return "E-Bibby"

    def take_turn(self, turn, world, avatar):
        current = avatar.position
        if current is None:
            return []

        # Update bot tracking
        self.previous_bot_positions = self.bot_positions.copy()
        self.bot_positions = self.get_bot_positions_by_type(world)

        # Handle refuge hiding
        if self.hiding_in_refuge:
            self.refuge_turns_left -= 1
            if self.refuge_turns_left <= 0:
                self.hiding_in_refuge = False
                self.path = []
                self.current_goal = None
                self.waiting_for_respawn = False
            return []

        # CRITICAL: Check battery level first - below 35% is urgent
        if avatar.power < 35:
            battery = self.find_nearest_battery(world, current)
            if battery:
                self.waiting_for_respawn = False
                self.path = self.a_star_prefer_safe(world, current, battery)
                if self.path:
                    next_pos = self.path.pop(0)
                    move = self.get_action_for_move(current, next_pos)
                    if move:
                        return [move]

        # Check for approaching bots
        approaching_bots = self.get_approaching_bots(current, 4)
        crawler_approaching = self.is_crawler_approaching(current, 4)

        # Handle CrawlerBot - ALWAYS run, never hide
        if crawler_approaching:
            escape_pos = self.find_escape_position_from_crawler(world, current)
            if escape_pos:
                self.path = self.a_star_prefer_safe(world, current, escape_pos)
                if self.path:
                    next_pos = self.path.pop(0)
                    move = self.get_action_for_move(current, next_pos)
                    if move:
                        return [move]

        # Handle other bots - hide in refuge if not getting battery
        elif approaching_bots and avatar.power >= 35:
            refuge = self.find_nearby_refuge(world, current, 5)
            if refuge:
                self.path = self.a_star_prefer_safe(world, current, refuge)
                if self.path:
                    next_pos = self.path.pop(0)
                    move = self.get_action_for_move(current, next_pos)
                    if move:
                        # Check if we just entered refuge
                        on_tile = world.get_top(next_pos)
                        if on_tile and on_tile.object_type == ObjectType.REFUGE:
                            self.hiding_in_refuge = True
                            self.refuge_turns_left = 4
                        return [move]
            else:
                # No refuge, run away
                escape_pos = self.find_escape_position(world, current, approaching_bots)
                if escape_pos:
                    self.path = self.a_star_prefer_safe(world, current, escape_pos)
                    if self.path:
                        next_pos = self.path.pop(0)
                        move = self.get_action_for_move(current, next_pos)
                        if move:
                            return [move]

        # Check if we're adjacent to a generator and should activate it
        scrap_count = avatar.get_quantity_of_item_type(ObjectType.SCRAP)
        needed_scrap = self.generators_activated + 1

        if scrap_count >= needed_scrap and self.generators_activated < 5:
            interaction = self.try_interact_generator(world, current, needed_scrap)
            if interaction:
                self.generators_activated += 1
                self.path = []
                self.current_goal = None
                self.waiting_for_respawn = False
                return [interaction]

        # If waiting for respawn, check for nearby useful items or stay put
        if self.waiting_for_respawn:
            nearby_important = self.find_nearby_important_collectible(world, current, 5)
            if nearby_important:
                self.waiting_for_respawn = False
                self.path = self.a_star_prefer_safe(world, current, nearby_important)
                if self.path:
                    next_pos = self.path.pop(0)
                    move = self.get_action_for_move(current, next_pos)
                    if move:
                        return [move]

            if self.wait_location and current.x == self.wait_location.x and current.y == self.wait_location.y:
                if turn - self.last_scrap_pickup_turn >= 5:
                    self.waiting_for_respawn = False
                    self.path = []
                else:
                    return []
            elif self.wait_location:
                self.path = self.a_star_prefer_safe(world, current, self.wait_location)
                if self.path:
                    next_pos = self.path.pop(0)
                    move = self.get_action_for_move(current, next_pos)
                    if move:
                        return [move]

        # Continue existing path
        if self.path:
            if len(self.path) > 0:
                next_pos = self.path[0]
                if self.can_move_to(world, next_pos):
                    move = self.get_action_for_move(current, next_pos)
                    if move:
                        self.path.pop(0)
                        on_tile = world.get_top(current)
                        if on_tile and on_tile.object_type == ObjectType.SCRAP:
                            self.last_scrap_pickup_turn = turn
                        return [move]
                else:
                    self.path = []

        # Decide new goal based on current phase
        goal = None
        needed_scrap = self.generators_activated + 1

        # If we need more scrap for next generator
        if scrap_count < needed_scrap and self.generators_activated < 5:
            scrap_spawners = [s.position for s in world.scrap_spawners]
            if scrap_spawners:
                goal = self.find_closest(current, scrap_spawners)
                if goal:
                    self.goal_type = 'scrap'
                    self.path = self.a_star_prefer_safe(world, current, goal)

        # If we have enough scrap, go to next generator
        elif scrap_count >= needed_scrap and self.generators_activated < 5:
            gen_adjacent = self.find_generator_adjacent_tile(world, current, needed_scrap)
            if gen_adjacent:
                goal = gen_adjacent
                self.goal_type = 'generator'
                self.path = self.a_star_prefer_safe(world, current, goal)

        # Execute new path
        if self.path:
            next_pos = self.path.pop(0)
            move = self.get_action_for_move(current, next_pos)
            if move:
                return [move]

        # If we just picked up scrap and have no path, find safe spot to wait
        if self.goal_type == 'scrap' and scrap_count < needed_scrap and not self.waiting_for_respawn:
            safe_spot = self.find_nearby_safe_spot(world, current, 5)
            if safe_spot:
                self.waiting_for_respawn = True
                self.wait_location = safe_spot

        return []

    def get_bot_positions_by_type(self, world):
        """Get positions of all dangerous bots by type"""
        dangerous_types = BOT_OBJECT_TYPES - {ObjectType.SUPPORT_BOT}
        positions = {}

        for bot_type in dangerous_types:
            bots = world.get_objects(bot_type)
            for bot_pos in bots.keys():
                positions[bot_type] = positions.get(bot_type, [])
                positions[bot_type].append(bot_pos)

        return positions

    def get_approaching_bots(self, current, distance):
        """Get list of bot positions that are within distance AND getting closer"""
        approaching = []

        for bot_type, positions in self.bot_positions.items():
            if bot_type == ObjectType.CRAWLER_BOT:
                continue  # Handle crawler separately

            for bot_pos in positions:
                current_dist = abs(bot_pos.x - current.x) + abs(bot_pos.y - current.y)

                if current_dist <= distance:
                    # Check if it was farther away last turn (getting closer)
                    if bot_type in self.previous_bot_positions:
                        for prev_pos in self.previous_bot_positions[bot_type]:
                            prev_dist = abs(prev_pos.x - current.x) + abs(prev_pos.y - current.y)
                            if current_dist < prev_dist:
                                approaching.append(bot_pos)
                                break
                    else:
                        # First time seeing this bot, consider it approaching
                        approaching.append(bot_pos)

        return approaching

    def is_crawler_approaching(self, current, distance):
        """Check if CrawlerBot is within distance AND getting closer"""
        if ObjectType.CRAWLER_BOT not in self.bot_positions:
            return False

        for crawler_pos in self.bot_positions[ObjectType.CRAWLER_BOT]:
            current_dist = abs(crawler_pos.x - current.x) + abs(crawler_pos.y - current.y)

            if current_dist <= distance:
                # Check if getting closer
                if ObjectType.CRAWLER_BOT in self.previous_bot_positions:
                    for prev_pos in self.previous_bot_positions[ObjectType.CRAWLER_BOT]:
                        prev_dist = abs(prev_pos.x - current.x) + abs(prev_pos.y - current.y)
                        if current_dist < prev_dist:
                            return True
                else:
                    return True

        return False

    def find_escape_position_from_crawler(self, world, current):
        """Find escape position from CrawlerBot, avoiding paths back through it"""
        if ObjectType.CRAWLER_BOT not in self.bot_positions:
            return None

        # Get all crawler positions
        crawlers = self.bot_positions[ObjectType.CRAWLER_BOT]
        if not crawlers:
            return None

        nearest_crawler = min(crawlers, key=lambda p: abs(p.x - current.x) + abs(p.y - current.y))

        # Move in opposite direction
        dx = current.x - nearest_crawler.x
        dy = current.y - nearest_crawler.y

        if dx != 0:
            dx = dx // abs(dx)
        if dy != 0:
            dy = dy // abs(dy)

        # Try positions away from crawler
        for multiplier in range(5, 10):  # 5-9 tiles away
            escape_x = current.x + (dx * multiplier)
            escape_y = current.y + (dy * multiplier)
            escape_pos = type(current)(escape_x, escape_y)

            if world.is_valid_coords(escape_pos) and self.can_move_to(world, escape_pos):
                # Make sure escape position is farther from crawler than current
                escape_dist = abs(nearest_crawler.x - escape_x) + abs(nearest_crawler.y - escape_y)
                current_dist = abs(nearest_crawler.x - current.x) + abs(nearest_crawler.y - current.y)

                if escape_dist > current_dist:
                    return escape_pos

        return None

    def find_nearby_refuge(self, world, current, radius):
        """Find refuge within radius tiles"""
        refuges = world.get_objects(ObjectType.REFUGE)
        candidates = []

        for pos in refuges.keys():
            dist = abs(pos.x - current.x) + abs(pos.y - current.y)
            if dist <= radius:
                candidates.append(pos)

        if not candidates:
            return None

        return self.find_closest(current, candidates)

    def find_escape_position(self, world, current, approaching_bots):
        """Find a safe position away from approaching bots"""
        if not approaching_bots:
            return None

        nearest_bot = min(approaching_bots, key=lambda p: abs(p.x - current.x) + abs(p.y - current.y))

        dx = current.x - nearest_bot.x
        dy = current.y - nearest_bot.y

        if dx != 0:
            dx = dx // abs(dx)
        if dy != 0:
            dy = dy // abs(dy)

        for multiplier in range(3, 8):
            escape_x = current.x + (dx * multiplier)
            escape_y = current.y + (dy * multiplier)
            escape_pos = type(current)(escape_x, escape_y)

            if world.is_valid_coords(escape_pos) and self.can_move_to(world, escape_pos):
                # Make sure not near other bots
                too_close = False
                for bot_pos in approaching_bots:
                    if abs(bot_pos.x - escape_x) + abs(bot_pos.y - escape_y) <= 2:
                        too_close = True
                        break

                if not too_close:
                    return escape_pos

        return None

    def find_nearby_important_collectible(self, world, current, radius):
        """Find scrap or battery within radius"""
        collectibles = []

        for spawner in world.scrap_spawners:
            dist = abs(spawner.position.x - current.x) + abs(spawner.position.y - current.y)
            if dist <= radius and dist > 0:
                collectibles.append(spawner.position)

        for spawner in world.battery_spawners:
            dist = abs(spawner.position.x - current.x) + abs(spawner.position.y - current.y)
            if dist <= radius and dist > 0:
                collectibles.append(spawner.position)

        if not collectibles:
            return None

        return self.find_closest(current, collectibles)

    def find_nearby_safe_spot(self, world, current, radius):
        """Find a refuge or vent within radius tiles"""
        safe_spots = []

        refuges = world.get_objects(ObjectType.REFUGE)
        for pos in refuges.keys():
            dist = abs(pos.x - current.x) + abs(pos.y - current.y)
            if dist <= radius:
                safe_spots.append(pos)

        vents = world.get_objects(ObjectType.VENT)
        for pos in vents.keys():
            dist = abs(pos.x - current.x) + abs(pos.y - current.y)
            if dist <= radius:
                safe_spots.append(pos)

        if not safe_spots:
            return None

        return self.find_closest(current, safe_spots)

    def find_nearest_battery(self, world, current):
        """Find closest battery spawner"""
        batteries = [s.position for s in world.battery_spawners]
        if not batteries:
            return None
        return self.find_closest(current, batteries)

    def try_interact_generator(self, world, current, cost):
        """Try to interact with adjacent generator of specific cost"""
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
                    if top.cost == cost:
                        return action

        return None

    def find_generator_adjacent_tile(self, world, current, cost):
        """Find a walkable tile adjacent to generator with specific cost"""
        generators = world.get_objects(ObjectType.GENERATOR)
        candidates = []

        for pos, gen_list in generators.items():
            for gen in gen_list:
                if hasattr(gen, 'active') and not gen.active and hasattr(gen, 'cost'):
                    if gen.cost == cost:
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

    def a_star_prefer_safe(self, world, start, goal):
        """A* that prefers vents and refuges"""

        def heuristic(pos):
            return abs(pos.x - goal.x) + abs(pos.y - goal.y)

        def get_tile_cost(pos):
            top = world.get_top(pos)
            if top:
                if top.object_type in [ObjectType.VENT, ObjectType.REFUGE]:
                    return 0.3
            return 1.0

        open_list = [[heuristic(start), start, [], 0]]
        closed = set()
        iterations = 0
        max_iterations = 300

        while open_list and iterations < max_iterations:
            iterations += 1

            min_idx = 0
            min_score = open_list[0][0]
            for i in range(1, len(open_list)):
                if open_list[i][0] < min_score:
                    min_score = open_list[i][0]
                    min_idx = i

            _, current, path, g_score = open_list.pop(min_idx)

            curr_tuple = (current.x, current.y)
            if curr_tuple in closed:
                continue
            closed.add(curr_tuple)

            if current.x == goal.x and current.y == goal.y:
                return path

            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                neighbor = type(current)(current.x + dx, current.y + dy)

                if not world.is_valid_coords(neighbor):
                    continue
                if (neighbor.x, neighbor.y) in closed:
                    continue
                if not self.can_move_to(world, neighbor):
                    continue

                new_path = path + [neighbor]
                new_g = g_score + get_tile_cost(neighbor)
                f_score = new_g + heuristic(neighbor)
                open_list.append([f_score, neighbor, new_path, new_g])

        return []

    def can_move_to(self, world, pos):
        """Check if position is walkable"""
        if not world.is_valid_coords(pos):
            return False

        top = world.get_top(pos)
        if top is None:
            return True

        obj_type = top.object_type

        if obj_type in [ObjectType.WALL, ObjectType.GENERATOR]:
            return False

        if obj_type == ObjectType.DOOR:
            if hasattr(top, 'open') and not top.open:
                return False

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