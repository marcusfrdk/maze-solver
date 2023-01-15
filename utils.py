import pygame
import os

root_path = os.path.abspath(os.path.dirname(__file__))

tile_size = 40  # pixels
tile_border_size = 2  # pixels
tile_full_size = tile_size + tile_border_size

cycle_time = 0.1 # seconds between renders

colors = {
    "border": (200, 200, 200),
    "background": (255, 255, 255),
    "tile_none": (255, 255, 255),
    "tile_blocked": (28, 28, 28),
    "tile_start": (28, 204, 66),
    "tile_end": (220, 32, 12),
    "tile_visited": (139, 139, 139),
    "tile_path": (201, 75, 203),
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

def load_maze(fp: str) -> tuple[tuple[int, int, list[list[str]]], pygame.Surface]:
  with open(fp, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines()]
    rows, cols = len(lines), len(lines[0].split(" "))

    screen = pygame.display.set_mode((cols * tile_full_size, rows * tile_full_size))

    grid = []
    for line in lines:
      grid.append(line.split(" "))

    return grid, screen

def export_maze(fp: str, maze: list[list[str]]) -> None:
  with open(fp, "w+", encoding="utf-8") as f:
    output = ""
    for row in maze:
      output = f"{output}{' '.join(row)}\n"
    f.write(output)

def render(grid: list[list[str]], screen: pygame.Surface, title: str) -> None:
  clock = pygame.time.Clock()
  pygame.display.set_caption(title)

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