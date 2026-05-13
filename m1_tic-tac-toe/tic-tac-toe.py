####Imports

#from IPython.display import clear_output
#Jupyter notebook only, comment out for .py file
import random

###Initial variables



def tic_tac_toe():

    #Initial variables

    replay_on = True
    game_on = True
    board_state = ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    ref_board = ['#', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    player_one_score = 0
    player_two_score = 0
    number_games = 0
    game_won = False
    game_tied = False

    # Pregame Setup
    welcome()
    (player_one_mark,player_two_mark) = xo_assign()
    (current_player) = coin_toss()
    (current_mark) = set_first_mark(current_player, player_one_mark, player_two_mark)

    # Game Loop
    while game_on == True:
        #player takes a turn, check if space is free, update board
        print(f'Player {current_player}s turn. Place your {current_mark.upper()}!')
        display_board(board_state)
        display_board(ref_board)
        space = space_choice(board_state, 0) #calls space_check within to validate
        board_state = update_board(board_state, current_mark, space)
        #clear_output()

        #check if placed mark results in endgame (win or tie)
        game_won = win_check(board_state, current_mark)
        game_tied = tied_check(board_state)

        if game_won:
            (player_one_score, player_two_score) = update_score(player_one_score, player_two_score, current_player)
            number_games += 1
            print(f'3-in-a-row!  Team {current_mark.upper()} wins. Congratulations Player {current_player}! \n')
            display_board(board_state)


            print(f'Player 1: {player_one_score}\nPlayer 2: {player_two_score}  \nTotal # games: {number_games}')
            game_on = ask_play_again(game_on)
            #clear_output()
            board_state = ['#',' ',' ',' ',' ',' ',' ',' ',' ',' ']

        elif game_tied:
            number_games += 1
            print(f'Stalemate! No open spaces remain. \n')
            display_board(board_state)
            print(f'Player 1: {player_one_score}\nPlayer 2: {player_two_score}  \nTotal # games: {number_games}')
            game_on = ask_play_again(game_on)
            board_state = ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            #clear_output()

        (current_player, current_mark) = advance_turn(current_player, current_mark)
        
    #Post-game
    #Final score report, exit game
    goodbye(player_one_score, player_two_score)





###Function library###################################

def welcome():
    #prints message with game instructions and board layout

            print('''
Welcome to Tic-Tac-Toe!

Two Players take turns placing X or O into empty
baord spaces using the number system shown below.
Player 1 chooses to be 'X' or 'O'.
Player 2 calls a coin toss to decide who goes first.
First to get three-in-a-row wins. Good luck!
            ''')
            print(' 1 | 2 | 3 \n---|---|---\n 4 | 5 | 6 \n---|---|---\n 7 | 8 | 9 \n')
            print('Game on!')

def xo_assign():
    #returns p1/p2  x/o assignments
    #assigns marker identity (X or O) to player 1 or player 2
    
    init_choice = 'wrong'
    valid_list = ['X', 'x', 'O', 'o']
    
    while init_choice not in valid_list:
        init_choice = input('Player 1, choose your fighter: X or O   ')
        if init_choice not in valid_list:
            print('Creative, but no. Please enter either X or O   ')
        elif 'X' == init_choice.upper():
            player_one_mark = 'x'
            player_two_mark = 'o'
            print('Huzzah! Player 1 has chosen X!')
            return player_one_mark, player_two_mark
        elif 'O' == init_choice.upper():
            player_one_mark = 'o'
            player_two_mark = 'x'
            print('Huzzah! Player 1 has chosen O!')
            return player_one_mark, player_two_mark


            
       
def coin_toss():
    #Player 2 calls a virtual coin toss, correct call -->  p2 is first, incorrect call --> p1 is first
    #Returns 1 or 2 denoting the first player to take a turn
    p2_call = 'undecided'
    valid_list = ['head', 'heads', 'h', 'tails', 'tail', 't']
    first_player = 0
    while p2_call.lower() not in valid_list:
        p2_call = input('Player 2, call the coin toss: Heads (H) or Tails (T)?    ')
        if p2_call.lower() not in valid_list:
            print('What? I didnt understand. Player 2, pick heads or tails: ')
        elif p2_call.lower() in valid_list:
            coin_toss = random.choice(['h', 't'])
            coin_dict = {'h':'Heads', 't':'Tails'} #converts single-character coin-toss to printable string
            coin_result = coin_dict[coin_toss]
            if coin_result == 'Heads':            #Prints coin-toss result, independent of call
                print('\n(H)     (^_^)')
            elif coin_result == 'Tails':
                print('\n(T)     (_x_) ')  
            if coin_toss == p2_call.lower()[0]:   #compares coin toss to Player 2's call
                first_player = 2
                print(f'\n{coin_result}!  Player {first_player} won the toss and will go first!')
                
            else:
                first_player = 1
                print(f'\n{coin_result}!  Player {first_player} won the toss and will go first!')
                
            return (first_player)

def set_first_mark(current_player, player_one_mark, player_two_mark):
    #sets the first turn mark based on first player
    if current_player == 1:
        first_mark = player_one_mark
    if current_player == 2:
        first_mark = player_two_mark
    return first_mark

def display_board(gm): 
    #prints game map from gamestate string
    #run as display_board(g)
    drawn_board = f' {gm[1]} | {gm[2]} | {gm[3]} \n---|---|---\n {gm[4]} | {gm[5]} | {gm[6]} \n---|---|---\n {gm[7]} | {gm[8]} | {gm[9]} \n'
    print(drawn_board)





######## GAME FUNCTION LIBRARY

def space_choice(board_state, player_input):
    #gets player's choice of space to fill (1-9)
    #calls collision_check to see if space is available
    #returns user input after validating
    player_input = '0'
    valid_inputs = ['#', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    while player_input not in valid_inputs:
        user_input = input('Choose a space to mark:    ')    
        if user_input in valid_inputs:
            if collision_check(board_state, int(user_input)):  
                print(f'Space {user_input} is free. Nice move!')
                checked_input = int(user_input)
                return checked_input
            else:
                print(f'Uh-oh! Space {user_input} is taken. Pick another.')
                display_hint(board_state)
        elif user_input not in valid_inputs:
            print('I dont understand. Enter a valid space number 1-9:  ')

def collision_check(board_state, space):
    #returns boolean, True if empty
    #checks if a chosen space is already filled in the current gamestate
    if board_state[space] == ' ':
        return True
    else:
        return False


def update_board(board_state, mark, space):
    #adds declared marker to delcared space
    # run as var = place(var, mark, space)
    board_state[space] = mark.upper()
    return board_state

def display_hint(board_state):
        spacestate = []
        empties = []
        for i, space in enumerate(board_state):
            if space == ' ':
                spacestate.append(i)
                empties.append(i)
            else:
                spacestate.append(' ')
        print('Available spaces:', empties)

def advance_turn(current_player, current_mark):
    if current_player == 1:
        current_player = 2
    else:
        current_player = 1
    if current_mark == 'x':
        current_mark = 'o'
    else:
        current_mark = 'x'
    return (current_player, current_mark)


def win_check(board_state, mark):
    #Check if specified marker one

    #Creates a set of space #s for the specified mark- X or O
    check_set = set([i for i, m in enumerate(board_state) if m.upper() == mark.upper()])

    #Winning trios of spaces, list of endgame sets
    win_setlist= [{1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {1, 4, 7}, {2, 5, 8}, {3, 6, 9}, {1, 5, 9}, {3, 5, 7}]

    #check for endgame set in the check set
    win_status = any(endgame <= check_set for endgame in win_setlist)

    return win_status

def tied_check(board_state):
    """
    Returns True if no empty spaces remain on the board, indicating a draw condition.
    Returns False if at least one empty space exists.
    """
    free_space = board_state.count(' ')
    if free_space == 0:
        return True
    else:
        return False

def update_score(player_one_score, player_two_score, current_player):
    if current_player == 1:
        player_one_score += 1
    else:
        player_two_score += 1
    return (player_one_score, player_two_score)

def ask_play_again(game_on):
    #Validates for yes/no input, retruns True if yes and False if no
    init_choice = 'wrong'
    valid_list = ['Y', 'Yes', 'yes', 'y', 'N', 'No', 'no', 'n']
    
    while init_choice not in valid_list:
        init_choice = input('Want to play again? (Y/N)  ')
        if init_choice not in valid_list:
            print('I love how you just say anything. But please - say either Yes/Y or No/N')
        elif 'y' in init_choice.lower():
            game_on = True
            return game_on
        elif 'n' in init_choice.lower():
            game_on = False
            return False



def goodbye(player_one_score, player_two_score):
    
    if player_one_score > player_two_score:
        print('\nPlayer 1 wins!. Congratulations!')
    elif player_two_score > player_one_score:
        print('\nPlayer 2 wins! Congratulations!')
    elif player_one_score == player_two_score:
        print('\nThe set was tied overall!  Everybody wins!')
    
    print('\nThanks for playing, see you next time!')



#### RUN THE PROGRAM#####

if __name__ == '__main__':
	tic_tac_toe()

