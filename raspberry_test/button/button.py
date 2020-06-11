from gpiozero import Button

button = Button(2)

while True:
    if button.is_pressed:
        print("按钮已经按下")
    else:
        print("按钮没有被按下")
