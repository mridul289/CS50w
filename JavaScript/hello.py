number_1 = int(input("Tell me the first number: "))

operation = input("What do you want to do?" )

number_2 = int(input("Tell me the second number: "))

if operation == "add":
    print( number_1 + number_2 )
    
elif operation == "substract":
    print( number_1 - number_2 )

elif operation == "multiply":
    print( number_1 * number_2 )

elif (operation == "divide"):
    print( number_1 / number_2 )

else :
    print("This is a wrong operation")
    
