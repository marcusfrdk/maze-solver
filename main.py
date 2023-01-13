import pygame
from grid import Grid, TILE_SIZE, BORDER_SIZE, State, Tile
from solve import bfs

fn = bfs


def main() -> int:
  pygame.init()
  pygame.display.set_caption("Maze Solver")

  WIDTH, HEIGHT = 5, 5  # number of tiles

  DONE = False
  SOLVING = False
  SCREEN = pygame.display.set_mode((
      WIDTH * (TILE_SIZE + BORDER_SIZE),
      HEIGHT * (TILE_SIZE + BORDER_SIZE)
  ))
  CLOCK = pygame.time.Clock()
  GRID = Grid(WIDTH, HEIGHT)

  while not DONE:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        DONE = True
      elif SOLVING:
        # run solving function here
        DONE = True
      elif event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        col = pos[0] // (TILE_SIZE + BORDER_SIZE)
        row = pos[1] // (TILE_SIZE + BORDER_SIZE)
        tile: Tile = GRID._grid[row][col]
        if event.button == 1:
          tile.toggle_block()
        elif event.button == 2:
          GRID.set_start(row, col)
        elif event.button == 3:
          GRID.set_end(row, col)
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        SOLVING = True

    SCREEN.fill((255, 255, 255))
    GRID.render(SCREEN)
    pygame.display.flip()
    CLOCK.tick(60)

  GRID.export()
  return 0


if __name__ == "__main__":
  exit(main())
