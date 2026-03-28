import random

suit_names = ('Spades', 'Hearts','Diamons', 'Clubs')
suit_values = (0, 1, 2, 3)

# Player class
class player_class:
    def __init__(self,name = "Name", hand = [], money = 0):
        self.hand = hand
        self.name = name
        self.fold = False
        self.money = money

# Card class   
class cards:
    def __init__(self, card_name = "", card_value = 0, suit_name = "", suit_value = 0):
        self.card_name = card_name
        self.card_value = card_value
        self.suit_name = suit_name
        self.suit_value = suit_value

# Creates suit   
def generate_suit(suit_name):
    suit = []
    
    for i in range(2,15):
        name = ""
    
        match i:
            case 11: name = f"Jack of {suit_name}"
            case 12: name = f"Queen of {suit_name}"
            case 13: name = f"King of {suit_name}"
            case 14: name = f"Ace of {suit_name}"
            case _: name = f"{i} of {suit_name}"

        suit.append(cards(name, i, suit_name))
    
    return suit

# Logic for making the deck 
def generate_deck():
    deck = []
    
    for i in suit_names:
        deck += generate_suit(i)
    
    return deck

# Give player the cards
def poker_private(deck, players):
    for i in range (0, 2):
        for p in players:
            top_card = len(deck) - 1
            p.hand.append(deck[top_card])
            del deck[top_card]
    
    # Print player cards. Checks if working
    for card in players[0].hand:
        print(card.card_name)
    
    print('\n')
    
    return players

# Validates player input.
def play_input(in_check = False):
    valid_moves = ["fold", "call", "raise"]
    
    if in_check:
        valid_moves[1] = "check"
    
    while True:
        print(f"{valid_moves[0]}, {valid_moves[1]}, {valid_moves[2]}")
        player_input = input()
        
        if player_input in valid_moves:
            return player_input
        
        else: print("\ninvalid\n")



# Betting rounds
def poker_bet(players, bet, check = False, play_index = 0, bet_raised = False):
    players_in_play = []
    player_index = len(players)

    # Player chooses their turn.
    for i in range(play_index, player_index):
        
        # Ignore if folded.
        if players[i].fold:
            continue
        players_in_play.append(players[i])
        # Actual choices
        print(players[i].name)
        player_input = play_input(check)

        if player_input.lower() == "raise":
            bet_raised = True
            player_raised = i
            bet += 10
            players[i].money -= bet
            play_index = 1
            break

        elif player_input.lower() == "fold":
            players[i].fold = True
            players_in_play.remove(players[i])
    
        elif player_input.lower() == "check":
                print("check")
        
        elif player_input.lower() == "call":
                players[i].money -= bet

    print('\n')
    print(len(players_in_play))
    if len(players_in_play) == 1:
        print("win Condition")
    
    # Reorganize player order if possible.
    try:
        if bet_raised:    
            players_ordered = players[player_raised:] + players[:player_raised]
    except UnboundLocalError: pass

    # Continue betting round if bets are raised.
    if bet_raised:
        players = poker_bet(players_ordered, bet, False, 1)

    return players

# Flop   
def poker_community(deck, draw = 1, table = []):
    for i in range (0, draw):
        top_deck = len(deck) - 1
        table.append(deck[top_deck])
        del deck[top_deck]
    
    print('\n')
    
    for i in table: print(i.card_name)

    return deck, table



# Main game.
def __main__():
    # Make the deck.
    deck = generate_deck()

    # Shuffle the deck.
    shuffle_amount = random.randint(1,5)
    
    for i in range (0, shuffle_amount):
        random.shuffle(deck)

    # Players.
    players = [player_class("P1",[], 100), player_class("P2",[], 100)]
    
    # Main game loop.
    players = poker_private(deck, players) # - Pre-flop
    players = poker_bet(players, 10)
    deck, table = poker_community(deck, 3) # - Flop
    print("Flop\n")
    players = poker_bet(players, 10, True)
    deck, table = poker_community(deck, 1, table) # - Turn
    print("Turn\n")
    players = poker_bet(players, 10, True)
    deck, table = poker_community(deck, 1, table) # - River
    print("River\n")
    players = poker_bet(players, 10, True)
    
    for i in table:
        print(i.card_name)
    
    print(players[0].money)

__main__()