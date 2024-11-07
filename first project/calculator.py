

# creates the funtion startup which initiates the program through a call
def startup():
    print("Would you like to Start Yes or No? \n")
    #basic input that allows to see if the user wants to continue
    sinput = str(input())
    #checks if the input says yes or no
    if sinput == "Yes":
        calculator()
    else:
        return ["No workie"]

# The actual calculator funtion does all the functionality.
def calculator():
    # asks for the leading number
    print("first Number: \n")
    a = float(input())
    #asks for the trailing number
    print("second Number: \n")
    b = float(input())
    #asks for user input for the opperation they want to do
    print("what would you like to do. Multiply, Add, Subtract, or Divide,")
    Uinput = str(input())
    # checks what oppperation they want to do and then prints the the solution and then asks for startup.
    if Uinput == "Add":
        print(a+b)
        startup()
    elif Uinput == "Multiply":
        print(a*b)
        startup()
    elif Uinput == "Subtract":
        print(a-b)
        startup()
    else:
        print(a/b)
        startup()


startup()
