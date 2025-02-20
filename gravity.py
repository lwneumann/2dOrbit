"""
gravity.py holds classes that create a system, which is also held within this file.
"""
from config import *
import math
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        return

    def pos(self) -> tuple:
        return self.x, self.y

    def __repr__(self) -> str:
        return f'Point({self.x}, {self.y})'

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __add__(self, other) -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y


class Body:
    def __init__(self, x: int, y: int, velocity_x: float, velocity_y: float, mass: float):
        self.location = Point(x, y)
        self.velocity = Point(velocity_x, velocity_y)
        self.mass = mass
        return

    def __str__(self) -> str:
        return f'{self.location}, {self.mass}'

    def __repr__(self) -> str:
        return f'Body({self.location}, {self.velocity}, {self.mass})'


class System:
    def __init__(self):
        # Create bodies
        self.bodies = []
        if MODE == "Random":
            self.bodies = random_bodies()
        else:
            for body in BODIES:
                self.bodies.append(make_listed_body(body))

        # Other Data
        self.movement_history = [[]*b for b in range(len(BODIES))]
        self.update_order = list(range(len(BODIES)))
        return

    def calculate_acceleration(self, body_index: int) -> Point:
        """
        returns the acceleration of a single body in the system
        """
        acceleration = Point(0, 0)
        body = self.bodies[body_index]

        # Apply force from all bodies
        for index, other_body in enumerate(self.bodies):
            if index != body_index:
                r = (body.location.x - other_body.location.x) ** 2 + \
                    (body.location.y - other_body.location.y) ** 2
                r = math.sqrt(r)
                g_force = G_CONST * other_body.mass / r**2
                acceleration.x += g_force * (other_body.location.x - body.location.x)
                acceleration.y += g_force * (other_body.location.y - body.location.y)

        return acceleration

    def calculate_velocity(self):
        """
        Updates the velocity of the bodies
        """
        if SHUFFLE_UPDATE_ORDER:
            random.shuffle(self.update_order)

        for body_index in self.update_order:
            acceleration = self.calculate_acceleration(body_index)
            self.bodies[body_index].velocity.x += acceleration.x * TIME_STEP
            self.bodies[body_index].velocity.y += acceleration.y * TIME_STEP
        return

    def update_location(self):
        """
        Moves all the bodies
        """
        for index, body in enumerate(self.bodies):
            body.location.x += body.velocity.x * TIME_STEP
            body.location.y += body.velocity.y * TIME_STEP

            if RECORD_MOVEMENT:
                self.movement_history[index].append(Point(body.location.x, body.location.y))
                if BURN_HISTORY and len(self.movement_history[index]) > HISTORY_LEN:
                    self.movement_history[index].pop(0)
        return

    def compute_gravity(self):
        """
        Calls the appropriate functions to complete a step of gravity
        """
        self.calculate_velocity()
        self.update_location()
        return


def make_listed_body(body_list) -> Body:
    """
    Created a body from a given list. Namely to create bodies given from the config file.
    """
    return Body(body_list[0], body_list[1], body_list[2], body_list[3], body_list[4])


def random_bodies(body_count=BODE_COUNT) -> list:
    bodies = []
    for b in range(body_count):
        bodies.append(Body(random.randint(-RANDOM_BODY_RANGE, RANDOM_BODY_RANGE),
                           random.randint(-RANDOM_BODY_RANGE, RANDOM_BODY_RANGE),
                           random.randint(-RANDOM_VEL_RANGE, RANDOM_VEL_RANGE),
                           random.randint(-RANDOM_VEL_RANGE, RANDOM_VEL_RANGE), 9e11))
    return bodies
