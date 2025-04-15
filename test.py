import pygame
from environment.world import World
from rendering.camera import Camera
from agent.animal import Animal

pygame.init()
pygame.surfarray.use_arraytype('numpy')

# Window Setup
canvas: pygame.Surface = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("EnvSim")

# Simulation Setup
exit: bool = False
world: World = World(32)
main_camera: Camera = Camera(canvas)
clock: pygame.time.Clock = pygame.time.Clock()
controls: dict[str, bool] = {
    "up": False,
    "left": False,
    "down": False,
    "right": False,
    "zoom_in": False,
    "zoom_out": False,
    "speed": False,
}
FPS: int = 60
# test_animal: Animal = Animal(256, 256)

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

    # Controls
    keys = pygame.key.get_pressed()
    controls["up"] = keys[pygame.K_UP] or keys[pygame.K_w]
    controls["left"] = keys[pygame.K_LEFT] or keys[pygame.K_a]
    controls["right"] = keys[pygame.K_RIGHT] or keys[pygame.K_d]
    controls["down"] = keys[pygame.K_DOWN] or keys[pygame.K_s]
    controls["zoom_in"] = keys[pygame.K_e]
    controls["zoom_out"] = keys[pygame.K_q]
    controls["speed"] = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

    # Simulation
    delta_time: float = clock.tick(FPS) / 1000
    canvas.fill((0, 0, 0))
    world.tick(delta_time)
    main_camera.tick(delta_time, controls)
    world.render(main_camera)
    pygame.display.flip()

    # Debug FPS
    print(int(clock.get_fps()))