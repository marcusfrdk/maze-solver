import pygame
from grid import Grid, TILE_SIZE, BORDER_SIZE, State, Tile


def main() -> int:
  pygame.init()
  pygame.display.set_caption("Maze Solver")

  WIDTH, HEIGHT = 10, 5  # number of tiles

  DONE = False
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
      elif event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        col = pos[0] // (TILE_SIZE + BORDER_SIZE)
        row = pos[1] // (TILE_SIZE + BORDER_SIZE)
        tile: Tile = GRID._grid[col][row]
        if event.button == 1:
          tile.toggle_block()
        elif event.button == 2:
          GRID.set_start(col, row)
        elif event.button == 3:
          GRID.set_end(col, row)

    SCREEN.fill((255, 255, 255))
    GRID.render(SCREEN)
    pygame.display.flip()
    CLOCK.tick(60)

  GRID.export()
  return 0


if __name__ == "__main__":
  exit(main())
