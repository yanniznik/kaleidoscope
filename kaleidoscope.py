import pygame
import sys
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def main():
    restart_requested = False

    # Initialize Pygame
    pygame.init()

    # Set up the drawing window
    screen_size = (750, 750)
    screen_width, screen_height = screen_size
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Meditation Pattern")

    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Initialize variables
    rad = 10
    rad_chg = 0.25  # Half the original speed
    min_rad = 10
    max_rad = (screen_width / 3) / 2  # Maximum radius to keep circles within cell

    # Watchdog Setup
    class WatchdogHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.src_path.endswith(sys.argv[0]):
                nonlocal restart_requested
                print("File changed, restarting...")
                restart_requested = True

    event_handler = WatchdogHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    running = True
    clock = pygame.time.Clock()

    cell_width = screen_width // 3
    cell_height = screen_height // 3

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if restart_requested:
            running = False
            continue

        # Clear the screen
        screen.fill(BLACK)

        # Update radius
        rad += rad_chg
        if rad < min_rad or rad > max_rad:
            rad_chg = -rad_chg

        # Draw the 3x3 grid
        for i in range(3):
            for j in range(3):
                cell_origin_x = i * cell_width
                cell_origin_y = j * cell_height

                # Draw the border of each cell
                pygame.draw.rect(screen, WHITE, (cell_origin_x, cell_origin_y, cell_width, cell_height), 2)

                # Draw circles in each cell

                # Circle Set A
                pygame.draw.circle(screen, WHITE, (cell_origin_x + cell_width//2, cell_origin_y + cell_height//2), int(rad), 2)
                pygame.draw.circle(screen, WHITE, (cell_origin_x + cell_width, cell_origin_y + cell_height//2), int(rad), 2)
                pygame.draw.circle(screen, WHITE, (cell_origin_x, cell_origin_y + cell_height//2), int(rad), 2)
                pygame.draw.circle(screen, WHITE, (cell_origin_x + cell_width//2, cell_origin_y), int(rad), 2)
                pygame.draw.circle(screen, WHITE, (cell_origin_x + cell_width//2, cell_origin_y + cell_height), int(rad), 2)

                # Circle Set B
                pygame.draw.circle(screen, WHITE, (cell_origin_x + cell_width//4, cell_origin_y + cell_height//4), int(rad), 2)
                pygame.draw.circle(screen, WHITE, (cell_origin_x + cell_width//4, cell_origin_y + 3*cell_height//4), int(rad), 2)
                pygame.draw.circle(screen, WHITE, (cell_origin_x + 3*cell_width//4, cell_origin_y + cell_height//4), int(rad), 2)
                pygame.draw.circle(screen, WHITE, (cell_origin_x + 3*cell_width//4, cell_origin_y + 3*cell_height//4), int(rad), 2)

                # Circle Set C
                pygame.draw.circle(screen, WHITE, (cell_origin_x, cell_origin_y), int(rad), 2)
                pygame.draw.circle(screen, WHITE, (cell_origin_x, cell_origin_y + cell_height), int(rad), 2)
                pygame.draw.circle(screen, WHITE, (cell_origin_x + cell_width, cell_origin_y), int(rad), 2)
                pygame.draw.circle(screen, WHITE, (cell_origin_x + cell_width, cell_origin_y + cell_height), int(rad), 2)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    # Clean up
    observer.stop()
    observer.join()
    pygame.quit()

    if restart_requested:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    else:
        sys.exit()

if __name__ == "__main__":
    main()
