from pygame.locals import *

def play_game():
    import pygame
    pygame.init()

    WIDTH, HEIGHT = 1000, 700
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ping Pong")

    FPS = 60
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLACK = (0,0,0)
    PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
    BALL_RADIUS = 7
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    REST = pygame.font.SysFont("comicsans",35)
    WINNING_SCORE = 5

    # background Image
    background_image = pygame.image.load('game_img/ping_pong_bg.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    class PingPong:
        class Paddle:
            COLOR = WHITE
            VEL = 4

            def __init__(self, x, y, width, height):
                self.x = self.original_x = x
                self.y = self.original_y = y
                self.width = width
                self.height = height

            def draw(self, win):
                pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

            def move(self, up=True):
                if up:
                    self.y -= self.VEL
                else:
                    self.y += self.VEL

            def reset(self):
                self.x = self.original_x
                self.y = self.original_y

        # Create ball
        class Ball:
            MAX_VEL = 6
            COLOR = YELLOW

            def __init__(self, x, y, radius):
                self.x = self.original_x = x
                self.y = self.original_y = y
                self.radius = radius
                self.x_vel = self.MAX_VEL
                self.y_vel = 0

            def draw(self, win):
                pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

            def move(self):
                self.x += self.x_vel
                self.y += self.y_vel

            def reset(self):
                self.x = self.original_x
                self.y = self.original_y
                self.radius = 7
                self.y_vel = 0
                self.x_vel *= -1

        # window objects define
        def draw(self, win, paddles, ball, left_score, right_score, game_over):
            win.blit(background_image, (0,0))
            left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
            right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
            win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
            win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

            for paddle in paddles:
                paddle.draw(win)
                
            # middle white line
            for i in range(10, HEIGHT, HEIGHT//20):
                if i % 2 == 1:
                    continue
                pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

            ball.draw(win)
            if not game_over:
                pygame.display.update()

        # ball collision control
        def handle_collision(self, ball, left_paddle, right_paddle):
            if ball.y + ball.radius >= HEIGHT:
                ball.y_vel *= -1
            elif ball.y - ball.radius <= 0:
                ball.y_vel *= -1

            if ball.x_vel < 0:
                # left_paddle collision
                if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
                    if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                        ball.x_vel *= -1

                        middle_y = left_paddle.y + left_paddle.height / 2
                        difference_in_y = middle_y - ball.y
                        reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                        y_vel = difference_in_y / reduction_factor
                        ball.y_vel = -1 * y_vel

            else:
                # right_paddle collision
                if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
                    if ball.x + ball.radius >= right_paddle.x:
                        ball.x_vel *= -1

                        middle_y = right_paddle.y + right_paddle.height / 2
                        difference_in_y = middle_y - ball.y
                        reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                        y_vel = difference_in_y / reduction_factor
                        ball.y_vel = -1 * y_vel

        # controls of paddle
        def handle_paddle_movement(self, keys, left_paddle, right_paddle):
            if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
                left_paddle.move(up=True)
            if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
                left_paddle.move(up=False)

            if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
                right_paddle.move(up=True)
            if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
                right_paddle.move(up=False)

        # initialize an object
        def mainloop(self):
            run = True
            clock = pygame.time.Clock()

            left_paddle = self.Paddle(10, HEIGHT//2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
            right_paddle = self.Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
            ball = self.Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

            left_score = 0
            right_score = 0
            game_over = False

            while run:
                clock.tick(FPS)
                self.draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score,game_over)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        break

                # actions
                keys = pygame.key.get_pressed()
                self.handle_paddle_movement(keys, left_paddle, right_paddle)

                ball.move()
                self.handle_collision(ball, left_paddle, right_paddle)

                # score management
                score_chg = False
                if ball.x < 0:
                    right_score += 1
                    p_text = "Point to Player 2"
                    score_chg = True if right_score <= 4 else None
                elif ball.x > WIDTH:
                    left_score += 1
                    p_text = "Point to Player 1"
                    score_chg = True if left_score <= 4 else None

                if score_chg:
                    text = SCORE_FONT.render(p_text,1,WHITE)
                    WIN.blit(text,(WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
                    ball.reset()
                    pygame.display.update()
                    pygame.time.delay(1500)
                
                # winner management
                won = False
                if left_score == WINNING_SCORE:
                    won = True
                    win_text = "Player 1 Won!"
                elif right_score == WINNING_SCORE:
                    won = True
                    win_text = "Player 2 Won!"

                if won:
                    text = SCORE_FONT.render(win_text, 1, WHITE)
                    WIN.blit(text, (WIDTH//2 - text.get_width() //2, HEIGHT//2 - text.get_height()//2))
                    restart = pygame.draw.rect(WIN, BLACK, (WIDTH //2 - 100, (HEIGHT//2 - 25) + 70,200,50 ))
                    text = REST.render("RESTART",1,WHITE)
                    WIN.blit(text,text.get_rect(center = restart.center))
                    ball.reset()
                    game_over = True

                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                        if restart.collidepoint(pygame.mouse.get_pos()) or event.key == pygame.K_RETURN:
                            left_paddle.reset()
                            right_paddle.reset()
                            left_score = 0
                            right_score = 0
                            game_over = False
                    pygame.display.update()
            pygame.quit()
    
    game_instance = PingPong()
    game_instance.mainloop()

if __name__ == "__main__":
    play_game()