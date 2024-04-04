import pygame
import numpy as np
import heapq

pygame.init()

WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
AGENT_COLOR = BLUE
GOAL_COLOR = RED
OBSTACLE_COLOR = (100, 100, 100)
FONT_SIZE = 24
BUTTON_COLOR = (0, 128, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Manual Gridworld Navigation")

def generate_random_maze(grid_width, grid_height, num_obstacles):
    grid = np.zeros((grid_width, grid_height))
    for _ in range(num_obstacles):
        x, y = np.random.randint(0, grid_width), np.random.randint(0, grid_height)
        grid[x, y] = 1
    return grid

def find_path(grid, start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {pos: float('inf') for pos in np.ndindex(grid.shape)}
    g_score[start] = 0

    while open_list:
        _, current = heapq.heappop(open_list)
        if current == goal:
            path = []
            while current in came_from:
                path.insert(0, current)
                current = came_from[current]
            return path

        for dx, dy in directions:
            x, y = current
            neighbor = x + dx, y + dy
            if 0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1]:
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor] and grid[neighbor] != 1:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    heapq.heappush(open_list, (tentative_g_score + heuristic(neighbor, goal), neighbor))

    return None

def heuristic(pos, goal):
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

def find_valid_start_goal(grid):
    while True:
        start = (np.random.randint(0, GRID_WIDTH), np.random.randint(0, GRID_HEIGHT))
        goal = (np.random.randint(0, GRID_WIDTH), np.random.randint(0, GRID_HEIGHT))
        if grid[start] != 1 and grid[goal] != 1:
            return start, goal

grid = generate_random_maze(GRID_WIDTH, GRID_HEIGHT, num_obstacles=100)
start, goal = find_valid_start_goal(grid)
path = None

game_over = False
message = ""
start_game = False

start_button_rect = pygame.Rect(150, 350, 100, 40)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not start_game:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button_rect.collidepoint(event.pos):
                    start_game = True
                    path = find_path(grid, start, goal)

    if start_game:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and start[1] > 0 and grid[start[0], start[1] - 1] != 1:
            start = (start[0], start[1] - 1)
        if keys[pygame.K_DOWN] and start[1] < GRID_HEIGHT - 1 and grid[start[0], start[1] + 1] != 1:
            start = (start[0], start[1] + 1)
        if keys[pygame.K_LEFT] and start[0] > 0 and grid[start[0] - 1, start[1]] != 1:
            start = (start[0] - 1, start[1])
        if keys[pygame.K_RIGHT] and start[0] < GRID_WIDTH - 1 and grid[start[0] + 1, start[1]] != 1:
            start = (start[0] + 1, start[1])

        if start == goal:
            game_over = True
            message = "Congratulations! You reached the goal."

    screen.fill(WHITE)

    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x, y] == 1:
                pygame.draw.rect(screen, OBSTACLE_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.draw.rect(screen, GOAL_COLOR, (goal[0] * GRID_SIZE, goal[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.draw.rect(screen, AGENT_COLOR, (start[0] * GRID_SIZE, start[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    if not start_game:
        pygame.draw.rect(screen, BUTTON_COLOR, start_button_rect)
        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render("Start Game", True, BUTTON_TEXT_COLOR)
        text_rect = text.get_rect(center=start_button_rect.center)
        screen.blit(text, text_rect)

    if game_over:
        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render(message, True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
