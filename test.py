import pygame
from environment.world import World
from environment.camera import Camera
from environment.animal import Animal, Rabbit, Fox
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

pygame.init()
pygame.surfarray.use_arraytype('numpy')

# Window Setup
canvas: pygame.Surface = pygame.display.set_mode((960, 540))
pygame.display.set_caption("EnvSim")

# Simulation Setup
exit: bool = False
world: World = World(8)
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

rabbit_history = []
fox_history = []
plot_cooldown = 0

plt.ion()
fig, ax = plt.subplots()
rabbit_data, = ax.plot([], [], label="Rabbit Population", color='brown')
fox_data, = ax.plot([], [], label="Fox Population", color='orange')
ax.legend()

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

    if plot_cooldown < 0:
        rabbit_history.append(Rabbit.count)
        fox_history.append(Fox.count)
        plot_cooldown = 1
        rabbit_data.set_data(range(len(rabbit_history)), rabbit_history)
        fox_data.set_data(range(len(fox_history)), fox_history)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()
    else:
        plot_cooldown -= delta_time

    canvas.fill((0, 0, 0))
    world.tick(delta_time)
    main_camera.tick(delta_time, controls)
    world.render(main_camera)
    pygame.display.flip()

    # Debug FPS
    #print(int(clock.get_fps()))