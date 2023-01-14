import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import argparse
import copy
import draw
import solve
import time
import utils

pygame.init()

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


def main() -> int:
  args = get_args()

  # Load
  if args["import"]:
    maze = utils.load_maze(args["import"])
  else:
    maze = draw.draw_maze(args["columns"], args["rows"])

  # Solve
  original = copy.deepcopy(maze)
  path = solve.bfs(maze)

  print(path)
  
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
