import pygame
import os

root_path = os.path.abspath(os.path.dirname(__file__))

tile_size = 40  # pixels
tile_border_size = 2  # pixels

cycle_time = 0.1 # seconds between renders

colors = {
    "border": (180, 180, 180),
    "background": (255, 255, 255),
    "tile_none": (255, 255, 255),
    "tile_blocked": (28, 28, 28),
    "tile_start": (143, 240, 164),
    "tile_end": (246, 97, 81),
    "tile_visited": (220, 220, 220),
    "tile_path": (153, 193, 241),
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

def load_maze(fp: str) -> tuple[int, int, list[list[str]]]:
  with open(fp, "r", encoding="utf-8") as f:
    grid = []
    for line in [line.strip() for line in f.readlines()]:
      grid.append(line.split(" "))
    return grid

def export_maze(fp: str, maze: list[list[str]]) -> None:
  with open(fp, "w+", encoding="utf-8") as f:
    output = ""
    for row in maze:
      output = f"{output}{' '.join(row)}\n"
    f.write(output)

def get_screen(maze: list[list[str]]) -> pygame.Surface:
  return pygame.display.set_mode((
      len(maze[0]) * (tile_size + tile_border_size),
      len(maze) * (tile_size + tile_border_size),
  ))

def render(grid: list[list[str]], screen: pygame.Surface, clock: pygame.time.Clock) -> None:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      print("Aborting path visualization...")
      exit(1)

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