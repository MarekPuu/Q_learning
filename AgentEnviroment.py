
import random

class Environment:
    def __init__(self,board,agentO,agentX = None):
        self.board = board
        self.agentX = agentX
        self.agentO = agentO
        self.initialize()
        self.test_results = {'wins_x': 0, 'wins_o': 0, 'draws': 0}

    def initialize(self):
        print("Initializing Environment")

    def play(self):
        print(self.board)
        self.board.make_new_board()
        current_player = random.choice(['O', 'X'])
        next_player = 'O' if current_player == 'X' else 'X'

        for i in range(len(self.board.board)):

            print("Current player", current_player)
            self.board.print_board()
            
            if(current_player == 'O'):
                state = self.agentO.get_state(self.board.board) 
                ag1_action = self.agentO.choose_action(state,False)
                self.board.board[ag1_action] = current_player
                print("Agent O action: ",ag1_action)

            elif(current_player == 'X'):
                action = self.board.player_move()
                self.board.board[action] = current_player

            game_over = self.board.check_for_winner(current_player)

            if(game_over):
                if(game_over == 'draw'):
                    print("Draw")
                    break   
                print("Winner is:",game_over)
                break

            current_player, next_player = next_player, current_player          


    def train(self,epochs,save_interval):
        for epoch in range(epochs):
            self.play_training()
            if (epoch + 1) % save_interval == 0:
                self.agentX.save_q_table()
                self.agentO.save_q_table()
                print(f"Epoch {epoch + 1}/{epochs}")
                print(f"Q-table length O: {len(self.agentO.q_table)}, Q-table length X: {len(self.agentX.q_table)}")

        print(f"Training finished: epoch {epoch + 1}/{epochs}")        
        
  
    def play_training(self):
        self.board.make_new_board()
        current_player = random.choice(['O', 'X'])
        next_player = 'O' if current_player == 'X' else 'X'

        ag1_action = -1
        ag2_action = -1

        for i in range(len(self.board.board)):
            if(current_player == 'O'):
                state_ag1 = self.agentO.get_state(self.board.board) 
                ag1_action = self.agentO.choose_action(state_ag1,True)
                self.board.board[ag1_action] = current_player

            elif(current_player == 'X'):
                state_ag2 = self.agentX.get_state(self.board.board) 
                ag2_action = self.agentX.choose_action(state_ag2,True)
                self.board.board[ag2_action] = current_player

            game_over = self.board.check_for_winner(current_player)

            if(not game_over and ag1_action != -1 ):
                self.agentO.learn(state_ag1, self.agentO.get_state(self.board.board), ag1_action, 0)
            if(not game_over and ag2_action != -1 ):
                self.agentX.learn(state_ag2, self.agentX.get_state(self.board.board), ag2_action, 0)

            if(game_over):
                if(game_over == 'O'):
                    self.agentO.learn(state_ag1, self.agentO.get_state(self.board.board), ag1_action, 1)
                    self.agentX.learn(state_ag2, self.agentX.get_state(self.board.board), ag2_action, -1)
                elif(game_over == 'X'):
                    self.agentO.learn(state_ag1, self.agentO.get_state(self.board.board), ag1_action, -1)
                    self.agentX.learn(state_ag2, self.agentX.get_state(self.board.board), ag2_action, 1)
                elif (game_over == 'draw'):
                    self.agentO.learn(state_ag1, self.agentO.get_state(self.board.board), ag1_action, 0.5)
                    self.agentX.learn(state_ag2, self.agentX.get_state(self.board.board), ag2_action, 0.5)

            if(game_over):
                break

            current_player, next_player = next_player, current_player 

    def test(self,epochs=100000, print_interval=10000, play_random = False):
        self.test_results = {'wins_x': 0, 'wins_o': 0, 'draws': 0}

        for epoch in range(epochs):
                self.play_test(play_random)
                if print_interval > 0 and (epoch + 1) % print_interval == 0:
                    print(f"Epoch {epoch + 1}/{epochs}")
                    print(f"X wins: {self.test_results['wins_x']}, O wins: {self.test_results['wins_o']}, draws: {self.test_results['draws']}")

        total_games = epochs
        x_wins_percentage = (self.test_results['wins_x'] / total_games) * 100
        o_wins_percentage = (self.test_results['wins_o'] / total_games) * 100
        draws_percentage = (self.test_results['draws'] / total_games) * 100

        if(play_random == True):
            print(f"Test finished: Random wins: {x_wins_percentage:.2f}%, O wins: {o_wins_percentage:.2f}%, draws: {draws_percentage:.2f}%")
            return
        print(f"Test finished: X wins: {x_wins_percentage:.2f}%, O wins: {o_wins_percentage:.2f}%, draws: {draws_percentage:.2f}%")


    def play_test(self,play_random):
        self.board.make_new_board()
        current_player = random.choice(['O', 'X'])
        next_player = 'O' if current_player == 'X' else 'X'
        board_moves = []
        ag1_action = -1
        ag2_action = -1

        for i in range(len(self.board.board)):
            if(current_player == 'O'):
                state_ag1 = self.agentO.get_state(self.board.board) 
                ag1_action = self.agentO.choose_action(state_ag1)
                self.board.board[ag1_action] = current_player
                board_moves.append(f"O: {ag1_action}")
            elif(current_player == 'X'):
                if(play_random == True):
                    action = random.choice([i for i, x in enumerate(self.board.board) if x == ' '])
                    self.board.board[action] = current_player
                    board_moves.append(f"X: {action}")
                else:
                    state_ag2 = self.agentX.get_state(self.board.board) 
                    ag2_action = self.agentX.choose_action(state_ag2)
                    self.board.board[ag2_action] = current_player
                    board_moves.append(f"X{ag2_action}")

            game_over = self.board.check_for_winner(current_player)

            if(game_over):
                if(game_over == 'O'):
                    self.test_results['wins_o'] += 1
                elif(game_over == 'X'):
                    print("Test failed: ",board_moves)
                    self.test_results['wins_x'] += 1
                elif (game_over == 'draw'):
                    self.test_results['draws'] += 1

            if(game_over):
                break

            current_player, next_player = next_player, current_player 

