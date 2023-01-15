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

algorithms = {
  "bfs": ("Breadth First Search", solve.bfs)
}

def get_args() -> dict:
  parser = argparse.ArgumentParser()
  parser.add_argument("-c", "--columns", type=int, default=9)
  parser.add_argument("-r", "--rows", type=int, default=6)
  parser.add_argument("-i", "--import", type=str)
  parser.add_argument("-e", "--export", type=str, default="output.txt")
  parser.add_argument("-a", "--algorithm", type=str, default="bfs", choices=algorithms.keys())
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
    maze, screen = utils.load_maze(args["import"])
  else:
    screen = pygame.display.set_mode((
        args["columns"] * (utils.tile_size + utils.tile_border_size),
        args["rows"] * (utils.tile_size + utils.tile_border_size),
    ))
    maze = draw.draw_maze(args["columns"], args["rows"], screen)

  # Solve
  original = copy.deepcopy(maze)
  algorithm = algorithms[args["algorithm"]]
  path = algorithm[1](maze, on_update=lambda M: utils.render(M, screen, algorithm[0]))

  print(f"Solution found in {len(path)} steps")
  
  # Visualize path
  maze_visualize = maze.copy()
  for x, y in path:
    if maze_visualize[x][y] not in ["s", "e"]:
      maze_visualize[x][y] = "p"
    utils.render(maze_visualize, screen, "Final Path")
    time.sleep(utils.cycle_time)

  # Export
  utils.export_maze(args["export"], original)
  name = os.path.basename(args["export"]).replace(".txt", "")
  pygame.image.save(screen, os.path.join(utils.root_path, f'{name}.png'))


if __name__ == "__main__":
  exit(main())
