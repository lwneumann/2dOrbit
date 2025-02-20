import math

# Graphics
SCREEN_SIZE = 1920, 1080
NAME = 'Orbiter'
BACKGROUND_COLOR = 0, 0, 15
BODY_R = 5
HISTORY_R = 1

# Settings
G_CONST = 6.67408e-11  # m^3/(kg*s^2)

SCALE_BUFFER = .2
SCOPE_SCALE = 1.5

TIME_STEP = 1
FPS = 220

RECORD_MOVEMENT = True
HISTORY_LEN = 100
BURN_HISTORY = True

SHUFFLE_UPDATE_ORDER = False  # For a lot of bodies
RANDOM_BODY_RANGE = 1500
RANDOM_VEL_RANGE = 1

BODE_COUNT = 3
SPEED = 1
BODY_DICT = {"Solar System": (
    (0, 0, 0, 0, 2e30, (255, 255, 0)),  # Sun
    (0, 7e10, 47000, 0, 3.285e23, (102, 102, 102)),  # Mercury
    (0, 1.1e11, 35000, 0, 4.8e24, (161, 130, 92)),  # Venus
    (0, 1.5e11, 30000, 0, 6e24, (0, 255, 20)),  # Earth
    (0, 2.2e11, 24000, 0, 2.4e24, (163, 0, 0)),  # Mars
    (0, 7.7e11, 13000, 0, 1e28, (199, 199, 199)),  # Jupiter
    (0, 1.4e12, 9000, 0, 5.7e26, (115, 145, 148)),  # Saturn
    (0, 2.8e12, 6835, 0, 8.7e25, (47, 143, 120)),  # Uranus
    (0, 4.5e12, 5477, 0, 1e26, (0, 123, 255)),  # Neptune
    (0, 3.7e12, 4748, 0, 1.3e22, (169, 3, 252))),  # Pluto
    "Symmetry": (
    (-100, 0, 0, -SPEED, 9e10),
    (100, 0, 0, SPEED, 9e10),
    (0, -100, SPEED, 0, 9e10),
    (0, 100, -SPEED, 0, 9e10)),
    "Random": [
        []*i for i in range(BODE_COUNT)]
}

MODE = "Random"
BODIES = BODY_DICT[MODE]
