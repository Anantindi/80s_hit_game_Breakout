import turtle
import time

# Screen setup
screen = turtle.Screen()
screen.title("Breakout Game")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# Paddle
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -250)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0, -230)
ball.dx = 3   # faster ball
ball.dy = 3

# Bricks
bricks = []
colors = ["red", "orange", "yellow", "green"]
def create_bricks():
    for y in range(4):
        for x in range(-350, 400, 70):
            brick = turtle.Turtle()
            brick.speed(0)
            brick.shape("square")
            brick.color(colors[y])
            brick.shapesize(stretch_wid=1, stretch_len=3)
            brick.penup()
            brick.goto(x, 250 - y * 30)
            bricks.append(brick)

create_bricks()

# Score and lives
score = 0
lives = 3

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write(f"Score: {score}  Lives: {lives}", align="center", font=("Courier", 18, "normal"))

# Paddle movement
def paddle_right():
    x = paddle.xcor()
    if x < 350:
        paddle.setx(x + 40)

def paddle_left():
    x = paddle.xcor()
    if x > -350:
        paddle.setx(x - 40)

screen.listen()
screen.onkeypress(paddle_right, "Right")
screen.onkeypress(paddle_left, "Left")

# Restart function
def restart():
    global score, lives, bricks
    score = 0
    lives = 3
    ball.goto(0, -230)
    ball.dx, ball.dy = 3, 3

    for b in bricks:
        b.hideturtle()
    bricks.clear()
    create_bricks()
    update_score()

screen.onkeypress(restart, "r")

def update_score():
    pen.clear()
    pen.write(f"Score: {score}  Lives: {lives}", align="center", font=("Courier", 18, "normal"))

# Game loop
while True:
    screen.update()
    time.sleep(0.01)  # slightly faster refresh than before

    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Wall collisions
    if ball.xcor() > 390 or ball.xcor() < -390:
        ball.dx *= -1
    if ball.ycor() > 290:
        ball.dy *= -1

    # Paddle collision
    if (paddle.ycor() - 10 < ball.ycor() < paddle.ycor() + 10) and (paddle.xcor() - 50 < ball.xcor() < paddle.xcor() + 50):
        ball.dy *= -1

    # Brick collision
    for brick in bricks:
        if brick.isvisible() and abs(ball.xcor() - brick.xcor()) < 35 and abs(ball.ycor() - brick.ycor()) < 15:
            ball.dy *= -1
            brick.hideturtle()
            score += 10
            update_score()

    # Missed ball
    if ball.ycor() < -290:
        lives -= 1
        update_score()
        if lives == 0:
            pen.clear()
            pen.write("GAME OVER! Press R to Restart", align="center", font=("Courier", 20, "normal"))
            ball.goto(1000, 1000)  # hide ball
            while lives == 0:
                screen.update()
                time.sleep(0.05)
        else:
            ball.goto(0, -230)
            ball.dy *= -1
