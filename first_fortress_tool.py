# This is the first tool for my CyberTech Fortress!
# A simple Python script to greet the user.

def greet_fortress_commander(name):
    return f"Greetings, Commander {name}! Your Tech Fortress is online."

if __name__ == "__main__":
    commander_name = input("Enter your commander name: ")
    message = greet_fortress_commander(commander_name)
    print(message)
