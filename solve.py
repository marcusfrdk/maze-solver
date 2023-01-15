import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import utils
import time
from typing import Callable

def bfs(maze: list[list[str]], on_update: Callable = None):
  """ Breadth first search """
  
  start_pos, end_pos = utils.get_pos(maze)
  queue = [(start_pos, [])]
  visited = []

  while queue:
    (r, c), path = queue.pop(0)
    
    if (r, c) == end_pos:
      return path + [(r, c)]

    for row, col in ((r+1, c), (r-1, c), (r, c+1), (r, c-1)):
      if maze[r][c] not in ["s", "e"]:
        maze[r][c] = "v"

      if 0 <= row < len(maze) and 0 <= col < len(maze[0]):
        if (row, col) not in visited and maze[row][col] not in ["b", "v"]:
          visited.append((row, col))
          queue.append(((row, col), path + [(row, col)]))

    if on_update:
      on_update(maze)

    if len(queue) == 0:
      print("No path found")
      exit(1)

    cycle_time = utils.cycle_time / len(queue)
    time.sleep(cycle_time)

def dfs(maze: list[list[str]], on_update: Callable = None):
  """ 
  Depth first search 
  Note: DFS does not always generate the shortest path, it only
        returns the first found path.
  """

  rows, cols = len(maze), len(maze[0])
  start_pos, end_pos = utils.get_pos(maze)

  stack = [(start_pos, [])]
  visited = set()

  while stack:
    (r, c), path = stack.pop()
    if (r, c) == end_pos:
      return path + [(r, c)]

    if maze[r][c] not in ["s", "e"]:
      maze[r][c] = "v"

    for row, col in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
      if 0 <= row < rows and 0 <= col < cols:
        if (row, col) not in visited and maze[row][col] not in ["b", "v"] and (row, col) != start_pos:
          visited.add((row, col))
          stack.append(((row, col), path + [(row, col)]))

    if on_update:
      on_update(maze)

    if len(stack) == 0:
      print("No path found")
      exit(1)

    cycle_time = utils.cycle_time / len(stack)
    time.sleep(cycle_time)
