import random
import turtle
from unittest import case
import time



def register_callback(callback):
    global my_handler
    my_handler = callback

def save_the_turtles(mode="manual"):
    # Initializing the Window
    window = turtle.Screen()
    window.screensize(400, 400)
    window.bgcolor('white')
    unit=15
    frametime=10 # milliseconds
    dt=frametime/1000.0
    turtle.delay(0)
    turtle.tracer(0)
    turtle.title("Save the Turtles "+mode.capitalize())

    static_turtle = turtle.Turtle()
    static_turtle.ht()
    static_turtle.pensize(unit)    
    static_turtle.shapesize(unit/20) # 8 pixels wide
    static_turtle.shape('square')
    static_turtle.speed(0)

    dynamic_turtle = turtle.Turtle()
    dynamic_turtle.ht()
    dynamic_turtle.pensize(unit)    
    dynamic_turtle.shapesize(unit/20) # 8 pixels wide
    dynamic_turtle.shape('turtle')
    dynamic_turtle.speed(0)


    text_turtle = turtle.Turtle()
    text_turtle.ht()
    text_turtle.pensize(unit)    
    text_turtle.shapesize(unit/20) # 8 pixels wide
    text_turtle.speed(0)
    text_turtle.color('black')

    # draw floor
    static_turtle.penup()
    static_turtle.pencolor('red')
    static_turtle.color('red')
    static_turtle.goto(-9*unit,-10*unit)
    static_turtle.pendown()
    static_turtle.stamp()
    static_turtle.goto(10*unit, -10*unit)
    static_turtle.stamp()
    # Initializing the Window
    window = turtle.Screen()
    window.screensize(400, 400)
    window.bgcolor('white')
    unit=15
    frametime=5 # milliseconds
    dt=frametime/1000.0
    turtle.delay(0)
    turtle.tracer(0)

    static_turtle = turtle.Turtle()
    static_turtle.ht()
    static_turtle.pensize(unit)    
    static_turtle.shapesize(unit/20) # 8 pixels wide
    static_turtle.shape('square')
    static_turtle.speed(0)

    dynamic_turtle = turtle.Turtle()
    dynamic_turtle.ht()
    dynamic_turtle.pensize(unit)    
    dynamic_turtle.shapesize(unit/20) # 8 pixels wide
    dynamic_turtle.shape('turtle')
    dynamic_turtle.speed(0)


    text_turtle = turtle.Turtle()
    text_turtle.ht()
    text_turtle.pensize(unit)    
    text_turtle.shapesize(unit/20) # 8 pixels wide
    text_turtle.speed(0)
    text_turtle.color('black')

    # draw floor
    static_turtle.penup()
    static_turtle.pencolor('red')
    static_turtle.color('red')
    static_turtle.goto(-9*unit,-10*unit)
    static_turtle.pendown()
    static_turtle.stamp()
    static_turtle.goto(10*unit, -10*unit)
    static_turtle.stamp()

    static_turtle.penup()

    # Contains the coordinate and colour
    paddle = 0         
    paddle_velocity=0
    paddle_acceleration=0
    user_acceleration=0
    game_running = True
    WAIT=30
    TURTLE_COUNT=10
    TURTLE_VEL=-1
    w=0
    if mode=="basic":
        TURTLE_COUNT=30
        TURTLE_VEL=-2
    elif mode=="challenge":
        TURTLE_COUNT=60
        TURTLE_VEL=-4
        w=1100
    turtlex = 0
    turtley = 8*unit
    turtle_color='black'

    turtlexvel=0

    def paddle_left():
        nonlocal user_acceleration
        user_acceleration = -2000
    def paddle_right():
        nonlocal user_acceleration
        user_acceleration = 2000
    def paddle_release():
        nonlocal user_acceleration
        user_acceleration = 0
    def restart():
        nonlocal turtle_count, wait, score, turtle_state
        random.seed(42)
        score = 0
        turtle_state = "Start"
        turtle_count=TURTLE_COUNT
        wait = WAIT
    def quit():
        nonlocal game_running
        game_running = False

    if (mode=="manual"):
        window.onkeypress(paddle_left, "a")
        window.onkeypress(paddle_right, "d")
        window.onkeyrelease(paddle_release, "a")
        window.onkeyrelease(paddle_release, "d")
    window.onkeypress(restart, "r")
    window.onkeypress(quit, "q")
    window.listen() # Start listening for key events

    restart()
    while (game_running):
        start_time = time.perf_counter()

        paddle_acceleration=0
        if (mode!="manual"):
            paddle_acceleration += my_handler(paddle,turtlex)        
        paddle_acceleration+=user_acceleration
        paddle_acceleration = max(-5000, min(5000, paddle_acceleration))  
        total_acceleration = paddle_acceleration + w

        paddle_velocity += (total_acceleration)*dt
        paddle += paddle_velocity*dt

        dynamic_turtle.clear() # clear the screen to redraw everything
        if (paddle_acceleration>10):
            maxdraw=min(paddle_acceleration, 1500)
            dynamic_turtle.color('red')
            dynamic_turtle.shape('arrow')
            dynamic_turtle.goto(paddle-unit*1-maxdraw*0.005, -8*unit)
            dynamic_turtle.setheading(180)
            dynamic_turtle.stamp()
        elif (paddle_acceleration<-10):
            maxdraw=max(paddle_acceleration, -1500)
            dynamic_turtle.color('red')
            dynamic_turtle.goto(paddle+unit*1-maxdraw*0.005, -8*unit)
            dynamic_turtle.shape('arrow')
            dynamic_turtle.setheading(0)
            dynamic_turtle.stamp()

        dynamic_turtle.penup()
        dynamic_turtle.goto(paddle-unit*1, -8*unit)
        dynamic_turtle.color('black')
        dynamic_turtle.pendown()
        dynamic_turtle.goto(paddle+unit*1, -8*unit)
        dynamic_turtle.penup()



        # draw turtle
        dynamic_turtle.penup()
        dynamic_turtle.shape('turtle')
        dynamic_turtle.setheading(90)
        dynamic_turtle.goto(turtlex, turtley)
        dynamic_turtle.color(turtle_color)
        dynamic_turtle.stamp()

        match(turtle_state):
            case "MOVING":
                turtlex+=turtlexvel
                turtley += turtleyvel
                if turtley < -9*unit:
                    turtle_state="Lava"
                elif turtley < -7*unit and turtley >-8*unit and abs(turtlex-paddle) <= 2*unit:
                    turtle_state="Catch"           
            case "Catch":
                score += 1              
                wait=WAIT
                turtlexvel=paddle_velocity*dt
                turtle_state = "Start"
            case "Lava":
                turtley+=turtleyvel
                turtleyvel = 0
                turtle_color='red'
                score -= 1
                wait=WAIT          
                turtle_state = "Start"                
            case "Start":

                if wait <= 0:
                    turtlex = random.uniform(-8*unit, 8*unit)
                    turtley = 8*unit
                    turtleyvel = TURTLE_VEL
                    turtlexvel = 0
                    turtle_count-=1
                    turtle_state = "MOVING"
                elif wait>=WAIT:
                    turtleyvel=0
                    turtle_color='black'
                    text_turtle.clear()
                    text_turtle.penup()
                    text_turtle.goto(-9*unit, 12*unit)
                    text_turtle.write("SCORE: "+str(score), move=False, align="left", font=("Arial", 40, "normal"))
                if turtle_count>0:
                    #turtlex+=turtlexvel
                    wait-=1

        turtle.update()
        elapsed = time.perf_counter() - start_time
        sleep_time = max(0, 0.01 - elapsed)
        time.sleep(sleep_time)
    turtle.done()

#save_the_turtles()