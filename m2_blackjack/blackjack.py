### IMPORTS
import random
#from IPython.display import clear_output  #jupyter notebook only


###CARD ATTRIBUTES
#tuples of suits and ranks
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')

ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

#dictionary of card values; Ace = 11 points
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}


MINIMUM_BET = 1


#### CLASS DEFINITIONS
class Card:
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:
    def __init__(self):
        self.all_cards = [] #initially empty, stores card objects

    #nested for loop, create standard 52 card deck
        for suit in suits:
            for rank in ranks:
                created_card = Card(rank, suit)
                self.all_cards.append(created_card)

    #shuffle method
    def shuffle(self):
        random.shuffle(self.all_cards)
    
    #print method
    def __str__(self):
        return f'The deck has {len(self.all_cards)} cards.'

class Player:
    def __init__(self, name, bankroll):
        self.name = name #For print statements, expects string
        self.hand = [] #initially empty, stores card objects
        self.bankroll = bankroll #unique to player, expects integer

    def get_a_card(self,deck, discard_pile):
        #deck = primary source
        #if deck empty, transfer from discard pile, shuffle, then draw
        card_to_add = deal_a_card(deck, discard_pile)
        self.hand.append(card_to_add)

    #Face down draw an important attribute? Seems like not...

    def bet_chips(self,bet_amt):
        if bet_amt > self.bankroll:
            print(f'Cant bet more than bankroll value of ${self.bankroll}!')
        else:
            self.bankroll -=  bet_amt
    
    def add_chips(self,add_amt):
        self.bankroll += add_amt

    def score_hand(self):

        '''
        Totals values of cards in a player hand, and tallies the number of Aces
        being scored as 11s If total is over 22 and an Ace-as-11 remains, counts
        the Ace as a 1 instead.
        '''
        hand_score = 0
        num_aces = 0
        aces_as_ones = 0
        
        for card in self.hand:
            hand_score += card.value
            if card.rank == 'Ace':
                num_aces += 1
    
        #If score is a bust, and Aces in hand, recount them as 1s
        #Stops if non-bust score reached, or all Aces recounted
        for i in range(num_aces):
            if hand_score >= 22:
                hand_score -= 10
                aces_as_ones += 10
    
        return hand_score
        #    print(f'{aces_as_ones} Ace cards scored as 1s') #sanity check print statement
  
    def display_hand(self):
        for card in self.hand:
            print(card)

    def discard_hand(self, destination):
        '''
        Transfer entirety of a player hand to other player hand
        Can use to transfer to discard pile.
        Cant use to transfer to the Deck!
        '''
        destination.hand.extend(self.hand)
        self.hand = []
        
        def __str__(self):
            return f'{self.name} has {len(self.hand)} cards and ${self.bankroll}.'

#### FUNCTIONS - post discard_pile as player change
def ask_for_bet(player):
    '''
    Asks for player input of a bet amount. Validates for an integer.
    Validates to confirm bet amount does not exceed bankroll.
    Returns bet amount, but does not place the bet.
    '''
    
    bet_valid = False
    while bet_valid == False:
        try:
            print(f'You have ${player.bankroll} in chips.')
            print(f'Minimum bet is ${MINIMUM_BET}')
            bet_amt = int(input('How much do you want to bet? $'))
            if bet_amt > player.bankroll:
                #clear_output()
                print('Cant bet that much, ya wise guy!')
            elif bet_amt < MINIMUM_BET:
                #clear_output()
                print('Cant bet less than the minimum, ya cheapskate!')
            
            else:
                bet_valid = True
                return bet_amt
                
        except:
            #clear_output()
            print('Sorry I need a number of dollars you want to place as a bet.')
            

def place_a_bet(bet_amt, player, dealer, discard):
    '''
    Expects validated bet amount. Transfers that amount from player bankroll
    and from dealer bankroll to the 'pot' (Discard Pile bankroll).
    '''

    player.bet_chips(bet_amt)
    dealer.bet_chips(bet_amt)
    discard.add_chips(bet_amt*2)


def deal_hands(deck, discard, player, dealer):
    '''
    Deals cards one at a time from the deck, two to the player and two to the dealer.
    If the deck is depleted, refresh from discard pile.
    Deal: player/dealer/player/dealer (facedown)
    '''

    for cards_to_deal in range(0,2):
       
        #Deal player a card (pop from deck, append to hand)
        player.get_a_card(deck, discard)
       
        #Deal dealer a card (pop from deck, append to hand)  
        dealer.get_a_card(deck, discard)

    #Recite last cards dealt
    #Negative indexing allows for serial deal calls to sanity check
    print(f'You were dealt {player.hand[-2]} and {player.hand[-1]}.')
    print(f'{dealer.name} was dealt {dealer.hand[-2]} and a facedown card.')


def check_card_total(player, dealer, deck, discard):
    '''
    Error checking function
    Sums up list length of hands (player, dealer and discard) and the deck.
    Useful for sanity checking gamestate; should find 52 cards throughout.
    '''
    card_total = len(discard.hand) + len(deck.all_cards) + len(player.hand) + len(dealer.hand)
    if card_total == 52:
        print(f'{card_total} cards found in total.')

def check_chip_total(player, dealer, discard):
    '''
    Error checking function.
    Sums up bankrolls of discard, player and dealer.
    Useful for sanity checking gamestate, should be constant throughout.
    '''
    chip_total = player.bankroll + dealer.bankroll + discard.bankroll
    print(f'${chip_total} found in total.')
   


def deal_a_card(deck, discard):
    '''
    Draws a card from the deck.
    If no cards available, the discard pile is added to the deck, and the deck is shuffled.
    Called inside player class get a card method
    '''

    if len(deck.all_cards) == 0:
        print('Deck is empty. Shuffling...')

        deck.all_cards = discard.hand
        discard.hand = []
        deck.shuffle()


    return deck.all_cards.pop(0)


def ask_if_hitting(player):
    '''
    Displays cards in player hand and current score.
    Asks if player wants to hit (draw a card) with input command.
    Validates for answers starting y/yes as hit, or n/no as call (stop drawing cards).
    Returns True or False
    '''
    #placeholder value of user response to trigger while loop
    player_hitting = 'not given'
    #validates user input for Yes or Y (case-insenstivie) = True, No/N = False
    while player_hitting == 'not given':
        #clear_output()
        player.display_hand()
        print(f'You have {player.score_hand()}')
        hit_choice = input('Want to hit? (Y/N) ')
        if hit_choice[0].upper() == 'Y':
            player_hitting = True
            #clear_output()
        elif hit_choice[0].upper() == 'N':
            player_hitting = False
            #clear_output()
        else: 
            print('Sorry, I dont understand. Please enter Yes or No.')

    return player_hitting

def player_turn(player, deck, discard):
    ''' Asks if player wants to hit on start of turn.
        Checks if player busted, if so turn ends.
        If not busted, ask if player wants to hit.
        If yes, get a card and check score. If not, call and end turn.

    '''  
    player_hitting = ask_if_hitting(player) # initial fencepost bug ask, skip hit loop if false
    
    #hit loop, escape if busted or if not hitting
    while player_hitting == True:
        print('Hit! Dealing a card...')
        player.display_hand()
        player.get_a_card(deck, discard)
        print(f'You are dealt: {player.hand[-1]}.')
        print(f'You have {player.score_hand()}.')
        if player.score_hand() >= 22:
            #clear_output()          
            print(f'You are dealt: {player.hand[-1]}.')
            print(f'You have {player.score_hand()}.')
            print('Oh no, you busted! Dealer wins this hand.')
            break
        else:
            player_hitting = ask_if_hitting(player)  #displays hand + score, and asks if hitting

    if player_hitting == False:
        #clear_output()
        print('Call! No more cards.')
        print(f'You have {player.score_hand()}.')

def dealer_turn(dealer, deck, discard):
    print('\n--- DEALER TURN ---')
    dealer.display_hand()
    print(f'Dealer has {dealer.score_hand()}.')
    while dealer.score_hand() <= 16:
        dealer.get_a_card(deck, discard)
        print(f'Dealer draws {dealer.hand[-1]}.')
        print(f'Dealer has {dealer.score_hand()}.')

    if dealer.score_hand() >= 22:
        print('Dealer busts. Congratulations!')



def resolve_round(player, dealer):
    '''Compareres player and dealer hands to determine win/lose/push.
        Returns round outcome as a string.
    '''
    #Check if anybody busted
    if player.score_hand() >= 22:
        return 'lose'
    elif dealer.score_hand() >= 22:
        return 'win'

    #Highest score wins if nobody busted
    #Tie = push
    elif  player.score_hand() > dealer.score_hand():
        return 'win'
    elif player.score_hand() < dealer.score_hand():
        return 'lose'
    elif player.score_hand() == dealer.score_hand():
        return 'push'


def resolve_pot(result, player, dealer, discard):
    '''
    Moves money from the discar pile bankroll (pot)
    to the winning player, or keeps it if
    the round was a push.
    '''
    
    pot = discard.bankroll
    
    if result == 'win':
        print(f'You won the round and get ${pot}!')
        player.add_chips(pot)
        discard.bankroll = 0

    elif result == 'lose':
        print(f'You lost the round. Pot resets from ${pot}.')
        dealer.add_chips(pot)
        discard.bankroll = 0

    elif result == 'push':
        print(f'Push! ${pot} stays in the pot.')
    else:
        print('Error - did not recognize result')

def discard_hands(player, dealer, discard):
    '''
    Players discard hands to discard pile using the discard_hand method.
    '''
    player.discard_hand(discard)
    dealer.discard_hand(discard)

def ask_if_playing(player):
    '''
    Asks if player for a yes or no and validates input.
    Returns True for yes/y, and False for no/n
    '''
    #placeholder value of user response to trigger while loop
    player_response = 'not given'
    #validates user input for Yes or Y (case-insenstivie) = True, No/N = False
    while player_response == 'not given':
        print(f'You have ${player.bankroll} in chips.')
        hit_choice = input('Want to play again? (Y/N) ')
        if hit_choice[0].upper() == 'Y':
            player_response = True
            #clear_output()
        elif hit_choice[0].upper() == 'N':
            player_response = False
            #clear_output()
        else:
            print('Sorry, I dont understand. Please enter Yes or No.')

    return player_response



    #Game setup

my_deck = Deck()
my_deck.shuffle()


#initialize players and bankroll amounts
#dealer bankroll is arbitrarily high
#discard_pile will be table pot, must start at 0

player = Player('Player',100)
dealer = Player('Dealer',1000)
discard_pile = Player('Discard Pile',0)

game_on = True

#Turn loop

while game_on == True:
   
    #Initial bet + cards dealt
    bet_amt = ask_for_bet(player)
    place_a_bet(bet_amt, player, dealer, discard_pile)    
    deal_hands(my_deck, discard_pile, player, dealer)

    #PLAYER TURN
    #Ends if busted or call
    player_turn(player, my_deck, discard_pile)
    
    #DEALER TURN
    #Skips if player busted
    if player.score_hand() <= 21: #only have dealer take a turn if player didnt bust
        dealer_turn(dealer, my_deck, discard_pile)
    else:
        print('You busted, so the dealer wont take a turn.')

    #Compare hands for win/lose/push"
    #Push = pot remiains, win = player gets pot, lose = dealer gets pot
    result = resolve_round(player, dealer)
    resolve_pot(result, player, dealer, discard_pile)
    discard_hands(player, dealer, discard_pile)
    
    if player.bankroll == 0:
        game_on = False
    else:
        game_on = ask_if_playing(player) 

## ENDGAME###
if player.bankroll == 0:
    print('Uh-oh, out of money. Better luck next time!')

elif player.bankroll <= 100:
    print(f'You ended the game with ${player.bankroll}. Could have been worse!')

else: 
    print(f'You ended the game with ${player.bankroll}. Congratulations!')

