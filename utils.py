import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

root_path = os.path.abspath(os.path.dirname(__file__))

tile_size = 40  # pixels
tile_border_size = 2  # pixels

colors = {
    "border": (224, 224, 224),
    "background": (255, 255, 255),
    "tile_none": (255, 255, 255),
    "tile_blocked": (0, 0, 0),
    "tile_start": (0, 255, 0),
    "tile_end": (255, 0, 0),
    "tile_visited": (255, 0, 255),
    "tile_path": (0, 255, 255),
}

state_colors = {
    "n": colors["tile_none"],
    "b": colors["tile_blocked"],
    "s": colors["tile_start"],
    "e": colors["tile_end"],
    "v": colors["tile_visited"],
    "p": colors["tile_path"]
}

def print_maze(maze: list[list[str]]) -> None:
  for row in maze:
    print(" ".join(row))

def render(grid: list[list[str]], screen: pygame.Surface, clock: pygame.time.Clock) -> None:
  screen.fill((255, 255, 255))
  for row in range(len(grid)):
    for col in range(len(grid[0])):
      max_size = tile_size + tile_border_size
      min_size = tile_size
      border_rect = pygame.Rect(
          col * max_size,
          row * max_size,
          max_size,
          max_size
      )
      inner_rect = pygame.Rect(
          col * max_size + tile_border_size,
          row * max_size + tile_border_size,
          min_size,
          min_size
      )
      pygame.draw.rect(screen, colors["border"], border_rect)
      pygame.draw.rect(screen, state_colors[grid[row][col]], inner_rect)
  pygame.display.flip()
  clock.tick(60)