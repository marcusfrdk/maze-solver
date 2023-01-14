import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import argparse
import copy
import time
import utils
import solve

pygame.init()

colors = {
    "border": (224, 224, 224),
    "background": (255, 255, 255),
    "tile_none": (255, 255, 255),
    "tile_blocked": (28, 28, 28),
    "tile_start": (143, 240, 164),
    "tile_end": (246, 97, 81),
    "tile_visited": (220, 138, 221),
    "tile_path": (249, 240, 107),
}

state_colors = {
    "n": colors["tile_none"],
    "b": colors["tile_blocked"],
    "s": colors["tile_start"],
    "e": colors["tile_end"],
    "v": colors["tile_visited"],
    "p": colors["tile_path"]
}


def get_args() -> dict:
  parser = argparse.ArgumentParser()
  parser.add_argument("-c", "--columns", type=int, default=9)
  parser.add_argument("-r", "--rows", type=int, default=6)
  parser.add_argument("-i", "--import", type=str)
  parser.add_argument("-e", "--export", type=str, default="output.txt")
  args = vars(parser.parse_args())

  if args["import"] and not os.path.isfile(args["import"]):
    print("Import file does not exist.")
    exit(1)

  if args["export"] and not args["export"].endswith(".txt"):
    print("Invalid export location.")
    exit(1)

  return args


def draw_maze(cols: int, rows: int) -> list[list[str]]:
  tile_size = 40  # pixels
  tile_border_size = 2  # pixels

  pygame.display.set_caption("Draw Maze")
  done = False
  clock = pygame.time.Clock()
  screen = pygame.display.set_mode((
      cols * (tile_size + tile_border_size),
      rows * (tile_size + tile_border_size),
  ))

  start = None
  end = None

  grid = []
  for row in range(rows):
    grid.append([])
    for col in range(cols):
      grid[row].append(f"n")

  while not done:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        done = True
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        if not start:
          print("Missing start")
        elif not end:
          print("Missing end")
        else:
          done = True
      elif event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        col = pos[0] // (tile_size + tile_border_size)
        row = pos[1] // (tile_size + tile_border_size)
        tile = grid[row][col]

        if event.button == 1:
          if tile == "n":
            grid[row][col] = "b"
          elif tile == "b":
            grid[row][col] = "n"
        elif event.button == 2:
          if isinstance(start, tuple):
            grid[start[0]][start[1]] = "n"
          grid[row][col] = "s"
          start = (row, col)
        elif event.button == 3:
          if isinstance(end, tuple):
            grid[end[0]][end[1]] = "n"
          grid[row][col] = "e"
          end = (row, col)

        # print(row, col, grid[row][col])

    screen.fill((255, 255, 255))

    for row in range(rows):
      for col in range(cols):
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

  return grid

def main() -> int:
  args = get_args()

  # Load
  if args["import"]:
    maze = utils.load_maze(args["import"])
  else:
    maze = draw_maze(args["columns"], args["rows"])

  # Solve
  original = copy.deepcopy(maze)
  path = solve.bfs(maze)
  
  # Visualize path
  maze_visualize = maze.copy()
  clock = pygame.time.Clock()
  screen = pygame.display.set_mode((
      len(maze[0]) * (utils.tile_size + utils.tile_border_size),
      len(maze) * (utils.tile_size + utils.tile_border_size),
  ))
  pygame.display.set_caption("Final Path")
  for x, y in path:
    if maze_visualize[x][y] not in ["s", "e"]:
      maze_visualize[x][y] = "p"
    utils.render(maze_visualize, screen, clock)
    time.sleep(utils.cycle_time)

  # Export
  utils.export_maze(args["export"], original)
  name = os.path.basename(args["export"]).replace(".txt", "")
  pygame.image.save(screen, os.path.join(utils.root_path, f'{name}.png'))


if __name__ == "__main__":
  exit(main())
