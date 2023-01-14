import pygame
import utils

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
        print("Exiting...")
        exit(1)
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
        pygame.draw.rect(screen, utils.colors["border"], border_rect)
        pygame.draw.rect(screen, utils.state_colors[grid[row][col]], inner_rect)

    pygame.display.flip()
    clock.tick(60)

  return grid