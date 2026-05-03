
import turtle
import time
import random

######################################################
#game settings(you can edit values)
worm_start_speed = 0.20 #0.20 recommended
worm_max_speed = 0.04 #0.04 recommended
obstacle_amount = 10 #10 recommended. 200MAX
######################################################

#pelin muuttujat
score = 0
highscore = 0
worm_speed = worm_start_speed
tick_time = 0

#pelin ikkuna
game_screen = turtle.Screen()
game_screen.title("Jarggon matopeli")
game_screen.bgcolor("black")
game_screen.setup(width=700, height=700)
game_screen.tracer(0)

#pelin visuaaliset seinät
wall = turtle.Turtle()
wall.color("#646E78")
wall.fillcolor("#2D3741")
wall.pensize(25)
wall.penup()
wall.goto(-300,-300)
wall.pendown()
wall.begin_fill()
for _ in range(4):
    wall.forward(600)
    wall.left(90)
wall.end_fill()
wall.hideturtle()

#pisteet visuaalit
points = turtle.Turtle()
points.color("white")
points.penup()
points.goto(-340,315)
points.write(f"SCORE: {score}      HIGHSCORE: {highscore}", font=("Courier New", 25, "normal"))
points.hideturtle()

#madon pää
head = turtle.Turtle()
head.speed(0)
head.shape("circle")
head.shapesize(1.2)
head.color("#C8CDD2")
head.goto(0,0)
head.penup()
head.direction = "stop"
head.turn_lock = False

#madon vartalo
worm_body_parts = []

#madon esteet
obstacles = []

#madon ruoka
food = turtle.Turtle()
food.shape("circle")
food.shapesize(0.8)
food.color("#32FFDC")
food.penup()
food.goto(0, 100)

#kultainen omena
golden_apple = turtle.Turtle()
golden_apple.hideturtle()
golden_apple.shape("circle")
golden_apple.shapesize(1.1)
golden_apple.color("#dea731")
golden_apple.penup()
golden_apple.goto(1000,1000)

def tick_timer():
    global tick_time
    tick_time += 1

def spawn_golden_apple():

        golden_apple.showturtle()
        safe_golden_apple_place = False
        while safe_golden_apple_place == False:

            x = random.randint(-14, 14) * 20
            y = random.randint(-14, 14) * 20
            golden_apple.goto(x, y)

            safe_golden_apple_place = True

            #tarkistetaan ettei spawnaa väärään paikkaan
            for part in worm_body_parts:
                if golden_apple.distance(part) < 20:
                    safe_golden_apple_place = False

            if golden_apple.distance(head) < 20 or golden_apple.distance(food) < 20:
                safe_golden_apple_place = False

            for obs in obstacles:
                if golden_apple.distance(obs) < 20:
                    safe_golden_apple_place = False

def despawn_golden_apple():

    golden_apple.hideturtle()
    golden_apple.goto(1000,1000)

def spawn_obstacle():

    new_obstacle = turtle.Turtle()
    new_obstacle.shape("square")
    new_obstacle.shapesize(1)
    new_obstacle.color("#646E78")
    new_obstacle.penup()

    #tarkistaa ettei este spawnaa väärään paikkaan
    safe_obstacle_place = False
    counter = 0

    while safe_obstacle_place == False and counter < 10:

        x = random.randint(-13, 13) * 20
        y = random.randint(-13, 13) * 20
        new_obstacle.goto(x, y)
        safe_obstacle_place = True

        if new_obstacle.distance(head) < 20 or new_obstacle.distance(food) < 20 or new_obstacle.distance(golden_apple) < 20:
            safe_obstacle_place = False

        for obs in obstacles:
            if new_obstacle.distance(obs) < 40:
                safe_obstacle_place = False

        for part in worm_body_parts:
            if new_obstacle.distance(part) < 20:
                safe_obstacle_place = False
        
        counter += 1

    if safe_obstacle_place == False:
        new_obstacle.goto(1000,1000)
        new_obstacle.hideturtle()
    else:
        obstacles.append(new_obstacle)

    #lisätään listaan        
    obstacles.append(new_obstacle)

#spawnataan asetettu määrä esteitä mutta minimissään 200
def spawn_all_obstacles():

    safe_amount = min(obstacle_amount, 200)

    for _ in range(safe_amount):
        spawn_obstacle()

#madon suunta
def go_up():
    if head.direction != "down" and head.turn_lock == False:
        head.direction = "up"
        head.turn_lock = True
def go_down():
    if head.direction != "up" and head.turn_lock == False:
        head.direction = "down"
        head.turn_lock = True

def go_left():
    if head.direction != "right" and head.turn_lock == False:
        head.direction = "left"
        head.turn_lock = True

def go_right():
    if head.direction != "left" and head.turn_lock == False:
        head.direction = "right"
        head.turn_lock = True

#madon liike
def move():
    
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

    tick_timer()

def update_scoreboard():
    global highscore

    if score > highscore:
        highscore = score
    points.clear()
    points.write(f"SCORE: {score}      HIGHSCORE: {highscore}", font=("Courier New", 25, "normal"))

def add_new_body_part():
    #lisätään uusi vartalopala
    new_body_part = turtle.Turtle()
    new_body_part.speed(0)
    new_body_part.shape("circle")
    new_body_part.color("#0096FF")
    new_body_part.penup()
    new_body_part.hideturtle()
    worm_body_parts.append(new_body_part)

def worm_speed_increase():
    global worm_speed
    if worm_speed > worm_max_speed:
        worm_speed -= 0.0012

#peli loppuu
def game_over():
    global score, worm_speed, tick_time

    game_screen.update()
    time.sleep(2)
    head.goto(0,0)
    food.goto(0, 100)
    head.direction = "stop"
    #piilottaa kuolleet madon palat peliruudun ulkopuolelle
    for part in worm_body_parts:
        part.goto(1000,1000)
        part.hideturtle()
    worm_body_parts.clear()
    #piilottaa esteet peliruudun ulkopuolelle
    for i in obstacles:
        i.goto(1000,1000)
        i.hideturtle()
    obstacles.clear()
    spawn_all_obstacles()
    despawn_golden_apple()

    print(f" you moved {tick_time} times")
    tick_time = 0
    worm_speed = worm_start_speed
    score = 0
    update_scoreboard()

#madon suunta näppäimet
game_screen.listen()
game_screen.onkeypress(go_up, "Up")
game_screen.onkeypress(go_down, "Down")
game_screen.onkeypress(go_left, "Left")
game_screen.onkeypress(go_right, "Right")

spawn_all_obstacles()

#pelin päivitys
while True:
    game_screen.update()

    #madon vartalopalat seuraa niskapalaa
    for i in range(len(worm_body_parts) - 1, 0, -1):
        x = worm_body_parts[i - 1].xcor()
        y = worm_body_parts[i - 1].ycor()
        worm_body_parts[i].goto(x,y)
        worm_body_parts[i].showturtle()

    #madon niskapala seuraa päätä
    if len(worm_body_parts) > 0:
        x = head.xcor()
        y = head.ycor()
        worm_body_parts[0].goto(x,y)
        worm_body_parts[0].showturtle()

    #mato liikkuu
    move()
    head.turn_lock = False
    time.sleep(worm_speed)

    #osuit seinään
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        game_over()

    #osuit itseesi
    for part in worm_body_parts:
        if head.distance(part) < 20:
            game_over()

    #osuit esteeseen
    for _ in obstacles:
        if head.distance(_) < 20:
            game_over()
    
    #spawnataan kultainen omena
    if tick_time % 100 == 0 and tick_time > 0 and score > 150:
        spawn_golden_apple()

    if tick_time % 50 == 0 and tick_time % 100 != 0:
        despawn_golden_apple()

    #jos söit kultaisen omenan
    if head.distance(golden_apple) < 20:

        #pisteen lisäys
        score += 50
        update_scoreboard()
        despawn_golden_apple()

        #madon nopeus kasvaa
        worm_speed_increase()
        add_new_body_part()
    
    #jos söit ruokaa
    if head.distance(food) < 20:

        #madon nopeus kasvaa
        worm_speed_increase()

        #pisteen lisäys
        score += 10
        update_scoreboard()
        
        safe_food_place = False
        while safe_food_place == False:

            #vaihdetaan ruuan paikka
            x = random.randint(-14, 14) * 20
            y = random.randint(-14, 14) * 20
            food.goto(x, y)
            safe_food_place = True

            #tarkistetaan ettei ruoka spawnaa madon tai kultaisen omenan sisään
            for part in worm_body_parts:
                if food.distance(part) < 20:
                    safe_food_place = False
            if food.distance(head) < 20 or food.distance(golden_apple) < 20:
                safe_food_place = False

            #tarkistetaan ettei ruoka spawnaa esteen sisään
            for obs in obstacles:
                if food.distance(obs) < 20:
                    safe_food_place = False
        add_new_body_part()            

