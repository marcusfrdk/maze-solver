import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import utils
import time
from typing import Callable

def bfs(maze: list[list[str]], on_update: Callable = None):
  start_pos = None
  end_pos = None

  # find start position
  for i in range(len(maze)):
    for j in range(len(maze[i])):
      if maze[i][j] == "s":
        start_pos = (i, j)
      elif maze[i][j] == "e":
        end_pos = (i, j)
  if not start_pos or not end_pos:
    return None

  # visualize init
  # screen, clock = utils.get_visualization(maze, "Breadth First Search")

  queue = [(start_pos, [])]
  visited = []

  while queue:
    # Pygame exit handling
    for event in pygame.event.get(): 
      if event.type == pygame.QUIT:
        print("Aborting search...")
        exit(1)
    
    # visualize
    if on_update:
      on_update(maze)

    # calculate
    (i, j), path = queue.pop(0)

    if (i, j) == end_pos:
      return path + [(i, j)]

    for x, y in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
      if maze[i][j] not in ["s", "e"]:
        maze[i][j] = "v"

      if 0 <= x < len(maze) and 0 <= y < len(maze[0]):
        if (x, y) not in visited and maze[x][y] not in ["b", "v"]:
          visited.append((x, y))
          queue.append(((x, y), path + [(i, j)]))

    if len(queue) == 0:
      print("No path found")
      exit(1)

    cycle_time = utils.cycle_time / len(queue)
    time.sleep(cycle_time)

  return None
