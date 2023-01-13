import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import utils
import time
from collections import deque

def bfs(grid):
  start_pos = None
  end_pos = None
  # find start and end positions
  for i in range(len(grid)):
    for j in range(len(grid[i])):
      if grid[i][j] == "s":
        start_pos = (i, j)
      elif grid[i][j] == "e":
        end_pos = (i, j)
  if not start_pos or not end_pos:
      return None
  # Visualize init
  clock = pygame.time.Clock()
  screen = pygame.display.set_mode((
      len(grid[0]) * (utils.tile_size + utils.tile_border_size),
      len(grid) * (utils.tile_size + utils.tile_border_size),
  ))
  pygame.display.set_caption("Breadth First Search")


  # BFS algorithm
  queue = deque([(start_pos, [])])
  while queue:
    # Pygame exit handling
    for event in pygame.event.get(): 
      if event.type == pygame.QUIT:
        print("Aborting search...")
        exit(1)

    # sleep(0.1)
    (i, j), path = queue.popleft()
    
    # visualize
    utils.render(grid, screen, clock)

    # calculate
    if (i, j) == end_pos:
      return path + [(i, j)]
    for x, y in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
      if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] not in ["b", "v"]:
        if grid[i][j] not in ["s", "e"]:
          grid[i][j] = "v"
        queue.append(((x, y), path + [(i, j)]))
    time.sleep(0.15)

  return None
