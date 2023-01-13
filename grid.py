import pygame
from enum import Enum

TILE_SIZE = 40  # pixels
BORDER_COLOR = (128, 128, 128)  # rgb
BORDER_SIZE = 2  # pixels


class State(Enum):
  NONE = "n"
  BLOCKED = "b"
  START = "s"
  END = "e"


colors = {
    State.NONE: (255, 255, 255),
    State.BLOCKED: (0, 0, 0),
    State.START: (0, 255, 0),
    State.END: (255, 0, 0)
}


class Tile():
  def __init__(self, x: int, y: int):
    self._x = x
    self._y = y
    self.state = State.NONE
    self._border_rect = pygame.Rect(
        self._x, self._y, TILE_SIZE + BORDER_SIZE, TILE_SIZE + BORDER_SIZE)
    self._inner_rect = pygame.Rect(
        self._x + BORDER_SIZE, self._y + BORDER_SIZE, TILE_SIZE, TILE_SIZE)

  def render(self, screen):
    pygame.draw.rect(screen, BORDER_COLOR, self._border_rect)
    pygame.draw.rect(screen, colors[self.state], self._inner_rect)

  def toggle_block(self):
    self.state = State.BLOCKED if self.state == State.NONE else State.NONE

  def set_state(self, state: State):
    self.state = state


class Grid():
  def __init__(self, cols: int = 20, rows: int = 20, grid: list[list[int]] = []):
    self._cols = cols
    self._rows = rows
    self._grid = grid
    self._start = None  # (col, row)
    self._end = None  # (col, row)

    if not grid:
      for x_pos in range(self._cols):
        self._grid.append([])
        for y_pos in range(self._rows):
          self._grid[x_pos].append(Tile(
              x_pos * (TILE_SIZE + BORDER_SIZE),
              y_pos * (TILE_SIZE + BORDER_SIZE)
          ))

  def set_start(self, col: int, row: int):
    if isinstance(self._start, tuple):
      self._grid[self._start[0]][self._start[1]].set_state(State.NONE)
    self._grid[col][row].set_state(State.START)
    self._start = (col, row)

  def set_end(self, col: int, row: int):
    if isinstance(self._end, tuple):
      self._grid[self._end[0]][self._end[1]].set_state(State.NONE)
    self._grid[col][row].set_state(State.END)
    self._end = (col, row)

  def render(self, screen):
    for col in range(self._cols):
      for row in range(self._rows):
        self._grid[col][row].render(screen)

  def export(self):
    pass
