import pygame
from gravity import *


class Window:
    def __init__(self):
        # Graphic Startup
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(NAME)
        self.colors = create_colors()

        # Create System
        self.system = System()
        self.scale = 0
        self.min_scope = 0
        self.set_scale()

        # self.set_custom_colors()
        return

    def set_custom_colors(self):
        for index, b in enumerate(BODIES):
            if len(b) > 5:
                self.colors[index] = b[-1]
        return

    def set_scale(self):
        b_pos = self.system.bodies[0].location.pos()
        farthest_num = max(abs(b_pos[0]), abs(b_pos[1]))
        # average all locations and center from that not 0, 0
        for body in self.system.bodies:
            body_x, body_y = body.location.pos()

            farthest_num = max(farthest_num, abs(body_x), abs(body_y))
        """
        //

        farthest_num = max(list(map(max, map(lambda p: map(abs, p), [b.location.pos() for b in self.system.bodies]))))
        """
        if self.scale == 0:
            self.min_scope = farthest_num * SCOPE_SCALE

        if self.min_scope > farthest_num:
            farthest_num = self.min_scope

        screen_min = min(SCREEN_SIZE) / 2
        self.scale = screen_min / (farthest_num + farthest_num * SCALE_BUFFER)
        """
        self.min_scope, self.scale = (((max(list(map(max, map(lambda p: map(abs, p), [b.location.pos() for b in
                                                                                      self.system.bodies]))) * SCOPE_SCALE) if not self.scale else self.min_scope),
                                       (min(SCREEN_SIZE) / 2) / ((max(list(map(max, map(lambda p: map(abs, p),
                                                                                        [b.location.pos() for b in
                                                                                         self.system.bodies]))) + [
                                                                          self.min_scope])) + (max(list(map(max,
                                                                                                            map(lambda
                                                                                                                    p: map(
                                                                                                                abs, p),
                                                                                                                [
                                                                                                                    b.location.pos()
                                                                                                                    for
                                                                                                                    b in
                                                                                                                    self.system.bodies]))) + [
                                                                                                       self.min_scope])) * SCALE_BUFFER)))
        """
        return

    def scale_position(self, pos) -> tuple:
        return (pos[0] * self.scale) + SCREEN_SIZE[0] / 2, (pos[1] * self.scale) + SCREEN_SIZE[1] / 2

    def draw_background(self):
        self.screen.fill(BACKGROUND_COLOR)
        return

    def draw_history(self):
        for index, b_history in enumerate(self.system.movement_history):
            for past_pos in b_history:
                pygame.draw.circle(self.screen, self.colors[index], self.scale_position(past_pos.pos()), HISTORY_R)
        return

    def draw_bodies(self):
        for body_index in range(len(self.system.bodies)):
            body_pos = self.system.bodies[body_index].location.x, self.system.bodies[body_index].location.y
            body_pos = self.scale_position(body_pos)
            pygame.draw.circle(self.screen, self.colors[body_index], body_pos, BODY_R)
        return

    def draw_all(self):
        # Update Scale
        self.draw_background()
        if RECORD_MOVEMENT:
            self.draw_history()
        self.draw_bodies()
        return

    def run(self):
        # Initial Setup
        running = True
        paused = False
        clock = pygame.time.Clock()
        self.draw_all()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        paused = not paused
                    elif event.key == pygame.K_r:
                        self.system = System()
                        self.colors = create_colors()
                        paused = False
                    elif event.key == pygame.K_TAB:
                        self.colors = create_colors()

            if not paused:
                # Update Gravity
                self.system.compute_gravity()
                self.set_scale()

                # Draw
                self.draw_all()
                pygame.display.update()
            else:
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(10, 10, 20, 60))
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(40, 10, 20, 60))
                pygame.display.flip()

            # Maintain Frames
            clock.tick(FPS)

        pygame.quit()
        return


def create_colors() -> list:
    colors = []
    for b in range(len(BODIES)):
        colors.append((random.randint(20, 255), random.randint(20, 255), random.randint(20, 255)))
    return colors


if __name__ == '__main__':
    Window().run()
