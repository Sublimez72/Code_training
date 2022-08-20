# Drive around a virtual car in a 2d grid

class Car:

    locationX = 0
    locationY = 0

    def moveRight():
        if Car.locationX > 9:
            Car.locationX = -10
        else:
            Car.locationX += 1

    def moveLeft():
        if Car.locationX < -9:
            Car.locationX = 10
        else:
            Car.locationX -= 1

    def moveUp():
        if Car.locationY > 9:
            Car.locationY = -10
        else:
            Car.locationY += 1

    def moveDown():
        if Car.locationY < -9:
            Car.locationY = 10
        else:
            Car.locationY -= 1

    def showLocation():
        print("The coordinates of the car are: ",
              Car.locationX, ",", Car.locationY)

    def help():
        print("Welcome to Virtual car driver!".upper())
        print("-" * 50)
        print("\nControls: \n Up = w \n Down = s \n Left = a \n Right = d \n To see where the car is = f \n Controls/Help = h\n Quit = q")


Car.help()
while True:
    command = input("Command: ")

    if command.lower() == "s":
        Car.moveDown()
    elif command.lower() == "w":
        Car.moveUp()
    elif command.lower() == "d":
        Car.moveRight()
    elif command.lower() == "a":
        Car.moveLeft()
    elif command.lower() == "f":
        Car.showLocation()
    elif command.lower() == "h":
        Car.help()
    elif command.lower() == "q":
        break
    else:
        Car.help()
