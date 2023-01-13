import pygame
import utils
from enum import Enum

TILE_SIZE = 40  # pixels
BORDER_COLOR = (128, 128, 128)  # rgb
BORDER_SIZE = 2  # pixels


class State(Enum):
  NONE = "n"
  BLOCKED = "b"
  START = "s"
  END = "e"
  VISITED = "v"
  ACTIVE = "a"


colors = {
    State.NONE: (255, 255, 255),
    State.BLOCKED: (0, 0, 0),
    State.START: (0, 255, 0),
    State.END: (255, 0, 0)
}


class Tile():
  def __init__(self, col: int, row: int):
    self._col = col
    self._row = row
    self.state = State.NONE
    self._border_rect = pygame.Rect(
        self._col, self._row, TILE_SIZE + BORDER_SIZE, TILE_SIZE + BORDER_SIZE)
    self._inner_rect = pygame.Rect(
        self._col + BORDER_SIZE, self._row + BORDER_SIZE, TILE_SIZE, TILE_SIZE)

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
    self._start = None  # (row, col)
    self._end = None  # (row, col)

    if not grid:
      for rows in range(self._rows):
        self._grid.append([])
        for cols in range(self._cols):
          self._grid[rows].append(Tile(
              cols * (TILE_SIZE + BORDER_SIZE),
              rows * (TILE_SIZE + BORDER_SIZE)
          ))

  def set_start(self, row: int, col: int):
    if isinstance(self._start, tuple):
      self._grid[self._start[0]][self._start[1]].set_state(State.NONE)
    self._grid[row][col].set_state(State.START)
    self._start = (row, col)

  def set_end(self, row: int, col: int):
    if isinstance(self._end, tuple):
      self._grid[self._end[0]][self._end[1]].set_state(State.NONE)
    self._grid[row][col].set_state(State.END)
    self._end = (row, col)

  def render(self, screen):
    for row in range(self._rows):
      for col in range(self._cols):
        self._grid[row][col].render(screen)

  def export(self):
    with open(utils.export_path, "w+", encoding="utf-8") as f:
      f.write(str(self))

  def __str__(self) -> str:
    output = f"{self._rows} {self._cols}\n"
    for row in self._grid:
      output = output + " ".join([v.state.value for v in row]) + "\n"
    return output
