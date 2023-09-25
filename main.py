from QLearningAgent import QLearningAgent as QLA
from Board import Board
from AgentEnviroment import Environment


def define_enviroment(board_size,winning_length,version, version2 = None):
    board = Board(board_size,winning_length)
    version = f"_v{version}"
    agent1 = QLA(f"{board_size}x{board_size}_O{version}", board_size * board_size)

    if(version2 != None):
        print("Training against another agent")
        version2 = f"_v{version2}"
        agent2 = QLA(f"{board_size}x{board_size}_X{version2}",board_size * board_size)
    else:
        agent2 = QLA(f"{board_size}x{board_size}_X{version}",board_size * board_size)
        
    environment = Environment(board,agent1,agent2)
    return environment

if __name__ == "__main__":

    #Pakotetaan 3 
    environment_size = 3
    # environment_size = int(input("Enter the environment size (3x3 enviroment = 3): "))
    winning_length = environment_size
    version = input("Enter the version: ")

    print("By default the agent will train against itself")
    train_against_other_agent = input("Train against other version agent? (y/n): ")

    if(train_against_other_agent == "y"):
        version2 = input("Enter the version of the other agent: ")
        Environment = define_enviroment(environment_size,winning_length,version,version2)
    else:
        Environment = define_enviroment(environment_size,winning_length,version)

    while True:
        print("\nMenu:")
        print("1. Train AI (AI vs AI)")
        print("2. Play against AI")
        print("3. Test AI (AI vs AI)")
        print("4. Test AI (AI vs Random)")
        print("5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            training_epochs = int(input("Enter the number of training epochs: (0 for 1,000,000) "))
            training_epochs = 1000000 if training_epochs == 0 else training_epochs
            Environment.train(training_epochs,100000)
        elif choice == "2":
             Environment.play()
        elif choice == "3":
            Environment.test(10000,0)     
        elif choice == "4":
            Environment.test(100000,0,True)     
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

