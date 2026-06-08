import turtle as t
import time

# 1. 배경화면
bg = t.Screen()
bg.title("Turtle Soccer Game")
bg.setup(width=1300, height=1000)
bg.tracer(0)  # 화면 깜빡거림 방지
bg.bgpic('images/gp.gif')
bg.bgcolor("lightgreen")

bg.addshape("images/gk.gif")
bg.addshape("images/ball.gif")

# 변수
score = 0      # 스코어
game = False   # 처음에 False로 시작

# 2. 점수판
sign = t.Turtle()
sign.speed(0)
sign.color("black")
sign.penup()
sign.hideturtle()
sign.goto(0,425)

# 3. 스페이스바 안내글(슛)
space = t.Turtle()
space.speed(0)
space.color("black")
space.penup()
space.hideturtle()
space.goto(0,-450)

# 4. 축구공 설정
ball = t.Turtle()
ball.speed(0)
ball.shape("images/ball.gif")
ball.penup()
ball.goto(0,-325)
ball_state = "ready"
ball_speed = 8   # 속도

# 5. 골키퍼 설정
gk = t.Turtle()
gk.speed(0)
gk.shape("images/gk.gif")
gk.penup()
gk.goto(0,30)
gk_dx = 4   # 속도

# 6. 안내글 설정
guide = t. Turtle()
guide.speed(0)
guide.color("black")
guide.penup()
guide.hideturtle()
guide.goto(0, 50)
guide.write("PRESS ENTER TO START", align="center", font=("Arial",30,"bold"))

# 함수
# (1) 스페이스바
def kick():
    global ball_state
    if game and ball_state == "ready":
        ball_state = "fire"

# (2) 엔터를 누르면 게임 시작
def start():
    global game
    if not game and score == 0:
        guide.clear()
        sign.write(f"Score: {score}", align="center", font=("Arial",28,'bold'))
        space.write("press SPACE to Kick!", align="center", font=("Arial",15,'bold'))
        game = True

# (3) 게임 오버에서 R을 누르면 새로 시작
def reset():
    global game, score, ball_state, gk_dx
    if not game:
        # 모든 변수 초기화
        score = 0
        ball_state = "ready"
        gk_dx = 4

        # 공, 골키퍼 위치 리셋
        ball.goto(0,-325)
        gk.goto(0,30)

        # 화면 글씨 재생성
        sign.clear()
        sign.goto(0,425)
        sign.color("black")
        sign.write("Score: 0", align="center", font=("Arial",28,'bold'))

        space.clear()
        space.color("black")
        space.write("Press SPACE to Kick!", align="center", font=("Arial",15,'bold'))

        game = True

# (4) 키보드 입력
bg.listen()
bg.onkeypress(kick, "space")
bg.onkeypress(start, "Return")
bg.onkeypress(reset, "r")
bg.onkeypress(reset, "R")

# 7. 메인 게임
try:
    while True:
        bg.update()
        time.sleep(0.01)

        # 게임 진행
        if game:
            # 골키퍼 좌우 이동
            gk.setx(gk.xcor() + gk_dx)
            if gk.xcor() > 170 or gk.xcor() < -170:
                gk_dx *= -1

            # 슈팅 움직임
            if ball_state == "fire":
                ball.sety(ball.ycor() + ball_speed)

            # 게임 오버 판정 (골키퍼가 막았을 때)
            x_diff = abs(ball.xcor() - gk.xcor())  # (축구공의 X좌표 - 골키퍼의 X좌표)
            y_diff = abs(ball.ycor() - gk.ycor())  # (축구공의 Y좌표 - 골키퍼의 Y좌표)

            if x_diff < 40 and y_diff < 30:
                game = False  # 게임 멈춤

                space.clear()  # 게임 오버 시 아래 안내글 지우고 재시작 안내 쓰기
                space.color("black")
                space.write("Press 'R' to Restart!", align="center", font=("Arial", 25, "bold"))

                sign.goto(0,0)
                sign.color("red")
                sign.write("GAME OVER", align="center", font=("Arial", 50, "bold"))

            # 골인
            elif ball.ycor() > 60 and -190 < ball.xcor() < 190:
                score += 1
                sign.clear()
                sign.write(f"Score: {score}", align="center", font=("Arial",28,"bold"))

                # 다음 슛을 위해 리셋
                time.sleep(0.5)
                ball.goto(0, -325)
                ball_state = "ready"

                # 성공할 때 마다 골키퍼 속도 증가
                # gk_dx = (무조건 속도 0.8씩 늘리기) * (오른쪽 방향이면 1, 왼쪽 방향이면 -1)
                gk_dx = (abs(gk_dx) + 0.8) * (1 if gk_dx > 0 else -1)

            # 노골 (리셋 처리)
            if ball.ycor() > 140:
                ball_state = "ready"
                ball.goto(0,-325)
except t.Terminator:
    pass
except Exception:
    pass

bg.mainloop()