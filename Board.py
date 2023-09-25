

class Board:
    def __init__(self,board_size = 3, winning_length = 3):
        self.board_size = board_size
        self.winning_length = winning_length
        self.board = []
        self.winning_combinations = []
        self.initialize()

    def initialize(self):
        print("Initializing Board")
        self.make_new_board()
        self.generate_win_configurations()
        print(self.winning_combinations)
        

    def make_new_board(self):
        self.board = [' '] * self.board_size  * self.board_size

    def generate_win_configurations(self):
        board_size = self.board_size
        winning_length = self.winning_length
        combinations = []

        # Generate horizontal winning combinations
        for row in range(board_size):
            for start_col in range(board_size - winning_length + 1):
                combination = [row * board_size + col for col in range(start_col, start_col + winning_length)]
                combinations.append(combination)

        # Generate vertical winning combinations
        for col in range(board_size):
            for start_row in range(board_size - winning_length + 1):
                combination = [row * board_size + col for row in range(start_row, start_row + winning_length)]
                combinations.append(combination)

        # Generate diagonal winning combinations (top-left to bottom-right)
        for row in range(board_size - winning_length + 1):
            for col in range(board_size - winning_length + 1):
                combination = [row * board_size + col + i * (board_size + 1) for i in range(winning_length)]
                if all(0 <= idx < board_size * board_size for idx in combination):
                    combinations.append(combination)    

        # Generate diagonal winning combinations (top-right to bottom-left)
        for row in range(board_size - winning_length + 1):
            for col in range(board_size - winning_length + 1):
                combination = [i * board_size + (board_size - 1 - i) for i in range(board_size)]
                if all(0 <= idx < board_size * board_size for idx in combination):
                    combinations.append(combination)

        self.winning_combinations = combinations




    # def print_board(self):
    #     GREEN = '\033[92m'
    #     RED = '\033[91m'
    #     END = '\033[0m'

    #     max_width = len(str(len(self.board) - 1))  

    #     for i in range(0, len(self.board), self.board_size):
    #         row = []
    #         for j in range(self.board_size):
    #             position = i + j
    #             if self.board[position] == ' ':
    #                 string = " " + str(position) + " " if position < 10 else str(position) + " "
    #                 formatted_number = GREEN + string + END
    #             else:
    #                 formatted_number = RED + " " +  self.board[position]  + " " +  END
    #             row.append(formatted_number)
    #         print("|".join(row))
    #         if i < len(self.board) - self.board_size:
    #             print("-" * (self.board_size * 3 + self.board_size - 1))

    def print_board(self):
        max_width = len(str(len(self.board) - 1))
        for i in range(0, len(self.board), self.board_size):
            row = []
            for j in range(self.board_size):
                position = i + j
                if self.board[position] == ' ':
                    string = "[" + str(position) + "]" if position < 10 else str(position) + " "
                    formatted_number = string
                else:
                    formatted_number =  " " + self.board[position]+ " " 
                row.append(formatted_number)
            print("|".join(row))
            if i < len(self.board) - self.board_size:
                print("-" * (self.board_size * 3 + self.board_size - 1))


    def player_move(self):
        available_actions = [str(i) for i, x in enumerate(self.board) if x == ' ']
        action = -1
        while action not in available_actions:
            action = input(f"Your move ({', '.join(available_actions)}): ")
        return int(action)
   
    def check_for_winner(self, player):
        have_winner = any(all(self.board[idx] == player for idx in config) for config in self.winning_combinations)
    
        if have_winner:
            return player
        elif all(position != ' ' for position in self.board):
            return 'draw'
        
        return None