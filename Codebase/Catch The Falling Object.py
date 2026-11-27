"""PS 65 - Catch the Falling Objects (Python 3 + Pygame)"""
import random
import pygame

WIDTH, HEIGHT = 500, 600
BASKET_W, BASKET_H, BASKET_Y, BASKET_SPEED = 90, 32, 548, 10
OBJ_SIZE, OBJ_SPEED = 20, 5
START_LIVES = 3
WHITE, BLACK = (255, 255, 255), (20, 20, 20)
BLUE, DARK_BLUE = (50, 120, 220), (25, 75, 180)
RED, ORANGE = (220, 50, 50), (255, 150, 50)


def move_basket(basket_x, key):
    """LEFT/RIGHT move basket by 10 px and keep it inside window; other keys are ignored."""
    if key == pygame.K_LEFT:
        basket_x -= BASKET_SPEED
    elif key == pygame.K_RIGHT:
        basket_x += BASKET_SPEED
    return max(0, min(WIDTH - BASKET_W, basket_x))


def new_object():
    """Create a 20x20 object at a random x at the top of the screen."""
    return pygame.Rect(random.randint(0, WIDTH - OBJ_SIZE), 0, OBJ_SIZE, OBJ_SIZE)


def update_object(obj, basket, score, lives):
    """Move object down 5 px. Catch = +1 score (Rect collision), miss = -1 life."""
    obj.y += OBJ_SPEED
    result = None
    if obj.colliderect(basket):
        score += 1
        result = "Object caught"
    elif obj.y > HEIGHT:
        lives -= 1
        result = "Object missed"
    if result:
        obj = new_object()
    return obj, score, lives, result


def draw_text(screen, font, text, pos, color=BLACK):
    screen.blit(font.render(text, True, color), pos)


def draw_basket(screen, basket_x):
    """Draw a trapezoid basket with a solid blue rim, instead of a flat blue line."""
    rim_y = BASKET_Y
    basket_shape = [
        (basket_x + 8, rim_y + 7),
        (basket_x + BASKET_W - 8, rim_y + 7),
        (basket_x + BASKET_W - 18, rim_y + BASKET_H),
        (basket_x + 18, rim_y + BASKET_H),
    ]
    pygame.draw.polygon(screen, BLUE, basket_shape)
    pygame.draw.polygon(screen, DARK_BLUE, basket_shape, 3)
    pygame.draw.line(
        screen,
        DARK_BLUE,
        (basket_x, rim_y),
        (basket_x + BASKET_W, rim_y),
        8,
    )


def draw_ball(screen, obj):
    """Draw the falling object as a round ball."""
    center = (obj.x + OBJ_SIZE // 2, obj.y + OBJ_SIZE // 2)
    pygame.draw.circle(screen, RED, center, OBJ_SIZE // 2)
    pygame.draw.circle(
        screen,
        ORANGE,
        (center[0] - 5, center[1] - 5),
        OBJ_SIZE // 6,
    )


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Catch the Falling Objects")
    pygame.key.set_repeat(100, 30)  # holding a key keeps moving the basket
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 56)

    basket_x, score, lives = (WIDTH - BASKET_W) // 2, 0, START_LIVES
    obj = new_object()
    running = True

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and lives > 0:
                basket_x = move_basket(basket_x, event.key)

        basket = pygame.Rect(basket_x, BASKET_Y, BASKET_W, BASKET_H)
        if lives > 0:
            obj, score, lives, result = update_object(obj, basket, score, lives)
            if result:
                print(f"{result} | Score: {score} | Lives: {lives}")
                if lives == 0:
                    print(f"Game Over | Final Score: {score}")

        screen.fill(WHITE)
        draw_basket(screen, basket_x)
        if lives > 0:
            draw_ball(screen, obj)
        draw_text(screen, font, f"Score: {score}", (10, 10))
        draw_text(screen, font, f"Lives: {lives}", (WIDTH - 100, 10))
        if lives == 0:
            draw_text(screen, big_font, "Game Over", (130, 230), RED)
            draw_text(screen, font, f"Final Score: {score}", (170, 290))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()