# Topic 1, Day 2 Homework
# Applied mini-task: Login gate with PIN validation
# Goal: combine validation loop, truthiness/short-circuit conditions, and string methods

username = input("Enter username: ")
while True:
    pin = input("Enter pin (or 'quit' to exit): ")
    if pin == "quit":
        break
    if pin.isdigit() and len(pin) == 4:
        break
    else:
        print("Invalid Pin, try again")

if pin != "quit":
    print("Welcome", username)
    print("Access granted.")
