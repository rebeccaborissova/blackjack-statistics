import random
import pygame as pg
from itertools import zip_longest
import sys
import time

# creates a new deck to play with
def shuffle():
    # 1 = ace(worth 11); 11 = jack(worth 10); 12 = queen(worth 10); 13 = king(worth 10), makes it easier for images
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 7,
            8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
def pick_card(card_list):
    # starts a new deck if empty
    if len(card_list) == 0:
        return pick_card(shuffle())
    # randomize a card from the deck
    choice = random.choice(card_list)
    card_list.remove(choice)
    return choice

def pick_bet():
    # randomizes a bet for the player to place
    bet_options = [10, 20, 30, 40, 50]
    bet_choice = random.choice(bet_options)
    return bet_choice

def pick_bet_with_card_counting(running_count):
    bet_options = [10, 20, 30, 40, 50]
    weights = []
    if running_count >= 2:
        weights = [0, 0, 0, 0.5, 0.5]
    elif running_count < 2:
        weights = [0.5, 0.3, 0.2, 0, 0]
    return random.choices(bet_options, weights)[0]
def change_card_value(card):
    # changes card values based on image numbers to what the value of the card holds
    if card == 1:
        return 11
    elif card == 11:
        return 10
    elif card == 12:
        return 10
    elif card == 13:
        return 10
    else:
        return card

def get_score(card_list):
    # instead of sum() function, has to run through to know card's true value (numbered by image value)
    sum_list = 0
    for card in card_list:
        new_card = change_card_value(card)
        sum_list += new_card
    return sum_list

def determine_win(dealer_score, player_score):
    # determines winner based on comparing hand values
    if dealer_score == player_score:
        return 0
    elif dealer_score == 21:
        return 1
    elif player_score == 21:
        return 2
    elif player_score > 21:
        return 1
    elif dealer_score > 21:
        return 2
    elif dealer_score > player_score:
        return 1
    elif player_score > dealer_score:
        return 2


def player_should_continue(player_score):
    global player_actions
    # if player score is 21 or over, they cannot hit
    if player_score == 21:
        player_actions.append("Player holds")
        return False
    elif player_score < 17:
        # if player score is under 17, they should hit
        player_actions.append("Player hits")
        return True
    elif player_score > 21:
        player_actions.append("Player holds")
        return False

def dealer_should_continue(dealer_score):
    global dealer_actions
    # if dealer score is 21 or over, they cannot hit
    if dealer_score == 21:
        dealer_actions.append("Dealer holds")
        return False
    if dealer_score < 17:
        # if dealer score is under 17, they should hit
        dealer_actions.append("Dealer hits")
        return True
    elif dealer_score > 21:
        dealer_actions.append("Dealer holds")
        return False

def player_should_continue_advanced(player_score, dealer_card):
    # depending on what player and dealer scores are, this function determines if they should hit or hold
    if player_score == 21:
        player_actions.append("Player holds")
        return False
    elif player_score > 21:
        player_actions.append("Player holds")
        return False
    elif (17 <= player_score <= 21):
        player_actions.append("Player holds")
        return False
    elif (13 <= player_score <= 16 and 2 <= dealer_card <= 6):
        player_actions.append("Player holds")
        return False
    elif (13 <= player_score <= 16 and 7 <= dealer_card <= 13):
        player_actions.append("Player hits")
        return True
    elif (12 == player_score and 4 <= dealer_card <= 6):
        player_actions.append("Player holds")
        return False
    elif (12 == player_score and (2 <= dealer_card <= 3 or 7 <= dealer_card <= 13)):
        player_actions.append("Player hits")
        return True
    else:
        player_actions.append("Player hits")
        return True

#creates global variables in order to use in functions above and the running loops below in pygame
dealer_total_wins = 0
player_total_wins = 0
player_bet = 0
player_balance = 0

dealer_final_hands = []
player_final_hands = []

player_actions = []
dealer_actions = []

# starts the running count for counting cards, and a special deck to be used when counting cards (doesn't get reshuffled every new game)
running_count_i = 0
running_deck = shuffle()
# determines whether or not to display the statistics screen
show_stat_bool = False
# will eventually hold all the stats after running 1000 times
stats_1000 = []
stats_1000_basic = []
stats_1000_advanced = []
stats_1000_card_counting = []

# final_balance is to keep track when running 1000+ runs, in_game_balance is to accumulate bets every game
final_balances = []
in_game_balance = 0

def play_game(deck):
    # creates decks for dealer and player
    dealer_cards = [pick_card(deck), pick_card(deck)]
    player_cards = [pick_card(deck), pick_card(deck)]
    player_turn = True
    dealer_turn = False
    global player_bet, final_balances, in_game_balance
    # sets a bet for the player
    player_bet = pick_bet()

    # while the game is continued
    while player_turn or dealer_turn:
        dealer_score = get_score(dealer_cards)
        player_score = get_score(player_cards)

        if dealer_turn:
            if dealer_should_continue(dealer_score):
                dealer_cards.append(pick_card(deck))
            else:
                # set to False if they should hold
                dealer_turn = False

        if player_turn:
            if player_should_continue(player_score):
                player_cards.append(pick_card(deck))
            else:
                player_turn = False
                dealer_turn = True

    # adds up their score and determines the winner based on card value
    dealer_score = get_score(dealer_cards)
    player_score = get_score(player_cards)
    result = determine_win(dealer_score, player_score)

    dealer_win = False
    player_win = False

    global player_balance
    player_balance = 0

    # if dealer won, player loses their bet
    if result == 1:
        dealer_win = True
        global dealer_total_wins
        dealer_total_wins += 1
        print("Dealer win")
        in_game_balance -= player_bet
        player_balance -= player_bet
    # if player won, player wins back their bet
    elif result == 2:
        player_win = True
        global player_total_wins
        player_total_wins += 1
        print("Player win")
        # player_balance is for statistics, gets added to a list of 1000 balances
        player_balance += player_bet
        # in_game_balance is to be displayed on screen when running GUI, it doesn't get reset every time so it accumulates
        in_game_balance += player_bet
    final_balances.append(player_balance)

    # gets final hand, score, and who won
    dealer_final_hands.append((dealer_cards, dealer_score, dealer_win))
    player_final_hands.append((player_cards, player_score, player_win))

# source: wikipedia blackjack page
def play_game_with_strategy(deck):
    # same idea as play_game, just using player_should_contine_advanced
    dealer_cards = [pick_card(deck), pick_card(deck)]
    player_cards = [pick_card(deck), pick_card(deck)]
    global player_bet, final_balances, in_game_balance
    player_bet = pick_bet()

    player_turn = True
    dealer_turn = False

    while player_turn or dealer_turn:
        dealer_score = get_score(dealer_cards)
        player_score = get_score(player_cards)

        if dealer_turn:
            if dealer_should_continue(dealer_score):
                dealer_cards.append(pick_card(deck))
            else:
                dealer_turn = False

        if player_turn:
            if player_should_continue_advanced(player_score, dealer_cards[0]):
                player_cards.append(pick_card(deck))
            else:
                player_turn = False
                dealer_turn = True

    dealer_score = get_score(dealer_cards)
    player_score = get_score(player_cards)

    result = determine_win(dealer_score, player_score)

    dealer_win = False
    player_win = False

    global player_balance
    player_balance = 0

    if result == 0:
        print("Tie")
    elif result == 1:
        dealer_win = True
        global dealer_total_wins
        dealer_total_wins += 1
        print("Dealer win")
        player_balance -= player_bet
        in_game_balance -= player_bet
    elif result == 2:
        player_win = True
        global player_total_wins
        player_total_wins += 1
        print("Player win")
        player_balance += player_bet
        in_game_balance += player_bet

    final_balances.append(player_balance)

    dealer_final_hands.append((dealer_cards, dealer_score, dealer_win))
    player_final_hands.append((player_cards, player_score, player_win))

#source for how card counting works: https://www.blackjackapprenticeship.com/how-to-count-cards/
def play_game_with_card_counting(deck, running_count):
    # same idea as play_game, just using player_should_contine
    dealer_cards = [pick_card(deck), pick_card(deck)]
    player_cards = [pick_card(deck), pick_card(deck)]
    global player_bet, final_balances, in_game_balance
    player_bet = pick_bet_with_card_counting(running_count)

    player_turn = True
    dealer_turn = False

    while player_turn or dealer_turn:
        dealer_score = get_score(dealer_cards)
        player_score = get_score(player_cards)

        if dealer_turn:
            if dealer_should_continue(dealer_score):
                dealer_cards.append(pick_card(deck))
            else:
                dealer_turn = False

        if player_turn:
            if player_should_continue_advanced(player_score, dealer_cards[0]):
                player_cards.append(pick_card(deck))
            else:
                player_turn = False
                dealer_turn = True

    dealer_score = get_score(dealer_cards)
    player_score = get_score(player_cards)

    result = determine_win(dealer_score, player_score)

    # where the card counting is implemented
    for dealer_card in dealer_cards:
        if dealer_card < 7:
            running_count += 1
        elif 10 <= dealer_card <= 11:
            running_count -= 1

    for player_card in player_cards:
        if player_card < 7:
            running_count += 1
        elif 10 <= player_card <= 11:
            running_count -= 1


    dealer_win = False
    player_win = False

    global player_balance
    player_balance = 0


    if result == 1:
        dealer_win = True
        global dealer_total_wins
        dealer_total_wins += 1
        player_balance -= player_bet
        in_game_balance -= player_bet
        print("Dealer win")
    elif result == 2:
        player_win = True
        global player_total_wins
        player_total_wins += 1
        player_balance += player_bet
        in_game_balance += player_bet
        print("Player win")

    final_balances.append(player_balance)
    dealer_final_hands.append((dealer_cards, dealer_score, dealer_win))
    player_final_hands.append((player_cards, player_score, player_win))

    return running_count

def run_simulation():
    # resets all global variables
    global dealer_total_wins, player_total_wins, player_balance, player_final_hands, dealer_final_hands, stats_1000_basic, final_balances
    dealer_total_wins = 0
    player_total_wins = 0
    player_balance = 0
    player_final_hands = []
    dealer_final_hands = []
    stats_1000_basic = []
    final_balances = []

    i = 0
    deck = shuffle()
    while i < 1000:
        play_game(deck)
        i += 1

    stats_1000_basic = get_1000_stats_advanced()

def run_simulation_with_strategy():
    global dealer_total_wins, player_total_wins, player_balance, player_final_hands, dealer_final_hands, stats_1000_advanced, final_balances
    dealer_total_wins = 0
    player_total_wins = 0
    player_balance = 0
    player_final_hands = []
    dealer_final_hands = []
    stats_1000_advanced = []
    final_balances = []

    i = 0
    deck = shuffle()
    while i < 1000:
        play_game_with_strategy(deck)
        i += 1

    stats_1000_advanced = get_1000_stats_advanced()

def run_simulation_with_card_counting():
    global dealer_total_wins, player_total_wins, player_balance, player_final_hands, dealer_final_hands, stats_1000_card_counting, final_balances
    dealer_total_wins = 0
    player_total_wins = 0
    player_balance = 0
    player_final_hands = []
    dealer_final_hands = []
    running_count = 0
    stats_1000_card_counting = []
    final_balances = []

    i = 0
    deck = shuffle()
    while i < 1000:
        running_count = play_game_with_card_counting(deck, running_count)
        i += 1
    stats_1000_card_counting = get_1000_stats_advanced()

def get_1000_stats_advanced():
    global final_balances
    average_balance = sum(final_balances) / len(final_balances)
    return (round(player_total_wins / (dealer_total_wins + player_total_wins), 2), average_balance)

def run_1000():
    # resets the global statistics
    global stats_1000, stats_1000_basic, stats_1000_advanced, stats_1000_card_counting, dealer_total_wins, player_total_wins
    stats_1000 = []
    dealer_total_wins = 0
    player_total_wins = 0

    # runs the game 1000 times, with advanced strategy
    i = 0
    deck = shuffle()
    while i < 1000:
        play_game(deck)
        i += 1
    # takes in the amount of player and dealer wins first
    stats_1000.append(dealer_total_wins)
    stats_1000.append(player_total_wins)

    # dont take in these stats for visualization
    first_card_stats = []
    for i in range(2, 12):
        totals = []
        total = 0
        total_wins = 0

        for hand in player_final_hands:
            if hand[0][0] == i:
                totals.append(hand)
                total += 1
                if hand[2] == True:
                    total_wins += 1
        chance = total_wins / total
        first_card_stats.append(chance)

    # then takes in the first_card_stats: "chances of playing winning if their first card is a 2, 3, 4, etc"
    stats_1000.append(first_card_stats)

    second_card_stats = []
    for i in range(2, 12):
        totals = []
        total = 0
        total_wins = 0

        for hand in player_final_hands:
            if hand[0][1] == i:
                totals.append(hand)
                total += 1
                if hand[2] == True:
                    total_wins += 1
        chance = total_wins / total
        second_card_stats.append(chance)

    # then takes in the second_card_stats: "chances of playing winning if their second card is a 2, 3, 4, etc"
    stats_1000.append(second_card_stats)

    total_bust = 0
    total_hands = 0
    for hand in player_final_hands:
        if hand[1] > 21:
            total_bust += 1
        total_hands += 1

    print(f"\nChance of player bust: ", total_bust / total_hands)
    # takes in chances of player bust as last item in stats_1000 list
    stats_1000.append(total_bust / total_hands)

    # running all modes 10000 times for balance and winnning chances ----------------------------------------------------------------------
    run_simulation_with_strategy() # gets in form of (chance of winning, final balance)
    run_simulation_with_card_counting()
    run_simulation()


class Card:
    # initialzier for the class, value is the card number, position is the x,y coord
    def __init__(self, value, position):
        image_value = f"{value}image.png"
        self.value = value
        self.image = pg.image.load(image_value)
        self.position = position

    def image_return(self):
        # scales the original card image to the specified factor
        scale_factor = 0.6
        scaled_image = pg.transform.scale(self.image, (int(self.image.get_width() * scale_factor), int(self.image.get_height() * scale_factor)))
        return scaled_image

    def position_return(self):
        # returns x, y coordinates for where to put the image onto the pygame screen
        return self.position

def display_text(screen, text, position, font, font_color):
    rendered_text = font.render(text, True, font_color)
    screen.blit(rendered_text, position)
    updated_position = (position[0], position[1] + font.get_height() + 5)  # Adjust the 5 for spacing
    return updated_position

def print_winner(dealer_hand, dealer_score, player_hand, player_score, verdict):
    # smaller font size for the small labels at the top to show dealers/players side
    hand_font = pg.font.Font(None, 25)

    # sets new image as the background: "playing_screen.jpg"
    playing_image = pg.image.load("playing_screen.jpg")
    screen_width, screen_height = pg.display.get_surface().get_size()

    # scales the background image to fit the screen
    scaled_background_image = pg.transform.scale(playing_image, (screen_width, screen_height))
    screen.blit(scaled_background_image, (0, 0))

    # displays "Dealer's hand" at the top left to show their side
    dealer_text = hand_font.render(f"Dealer's hand:", True, (255, 255, 255))
    screen.blit(dealer_text, (20, 10))  # Adjusted Y-coordinate

    # creates Card instances for each card in the dealer's hand
    classed_dealer_cards = [Card(value, (100 + i * 90, 50)) for i, value in enumerate(dealer_hand)]

    # displays "Player's hand" at the bottom left of the screen
    player_text = hand_font.render(f"Player's hand:", True, (255, 255, 255))
    screen.blit(player_text, (20, 560))  # Adjusted Y-coordinate

    # creates Card instances for each card in the player's hand
    classed_player_cards = [Card(value, (100 + i * 90, 400)) for i, value in enumerate(player_hand)]

    # prints Player's bet amount at the top right of the screen
    player_bet_text = hand_font.render(f"Player's bet: ${player_bet}", True, (255, 255, 255))
    screen.blit(player_bet_text, (screen_width - player_bet_text.get_width() - 20, 10))

    # sets the font size for the text of player wins, dealer wins, or tie
    verdict_font = pg.font.Font(None, 60)

    # if the user chose to run 1000 times, it will display "Running 1000 times" on screen while running one game
    global show_stat_bool
    if show_stat_bool:
        running_text = verdict_font.render("Running 1000 times...", True, (255, 215, 0))
        statw, stath = running_text.get_size()
        # gets the center of the screen to put the text on
        statx = (screen_width - statw) // 2
        staty = (screen_height - stath) // 2
        screen.blit(running_text, (statx, staty))

    pg.display.flip()
    time.sleep(1)

    player_card_placed = 0
    dealer_card_placed = 0

    # Citation: Chatgpt helped me learn about zip_longest() when I was trying to iterate between player and dealer getting cards
    for player_card, dealer_card in zip_longest(classed_player_cards, classed_dealer_cards, fillvalue=None):
        if player_card is not None:
            if player_card_placed == 2 and not show_stat_bool:
                y_coordinate = 350
                # prints the player actions on the right side of the screen below dealer actions, after first 2 cards have been dealt
                for action in player_actions:
                    text = hand_font.render(action, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(screen_width - 75, y_coordinate))
                    screen.blit(text, text_rect)
                    y_coordinate += 30
                    pg.display.flip()
                    time.sleep(1)
            player_card_placed += 1
            screen.blit(player_card.image_return(), player_card.position_return())
            pg.display.flip()
            time.sleep(1)

        if dealer_card is not None:
            if dealer_card_placed == 2 and not show_stat_bool:
                y_coordinate = 250
                # prints the dealer actions on the right side of the screen above player actions, after first 2 cards have been dealt
                for action in dealer_actions:
                    text = hand_font.render(action, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(screen_width - 75, y_coordinate))
                    screen.blit(text, text_rect)
                    y_coordinate += 30
                    pg.display.flip()
                    time.sleep(1)

            dealer_card_placed += 1
            # displays card imaged 1 at a time
            screen.blit(dealer_card.image_return(), dealer_card.position_return())
            pg.display.flip()
            time.sleep(1)

    # adds the scores of the player and dealer to be displayed on screen to the top and bottom of the screen where "Player's Hand:" is
    player_text = hand_font.render(f"{player_score}", True, (255, 255, 255))
    screen.blit(player_text, (140, 560))
    dealer_text = hand_font.render(f"{dealer_score}", True, (255, 255, 255))
    screen.blit(dealer_text, (140, 10))

    # displays player's balance from betting after they won or loss
    global in_game_balance
    player_balance_text = hand_font.render(f"Player's balance: ${in_game_balance}", True, (255, 255, 255))
    screen.blit(player_balance_text, (screen_width - player_balance_text.get_width() - 20, 40))  # Below Player's bet

    verdict_text = verdict_font.render(verdict, True, (255, 215, 0))
    text_width, text_height = verdict_text.get_size()

    # gets center  of the screen to put the text on
    x = (screen_width - text_width) // 2
    y = (screen_height - text_height) // 2
    # displays the text in the middle of who won
    screen.blit(verdict_text, (x, y))

    pg.display.flip()

def run_game():
    deck = shuffle()

    if easy_or_hard_or_stat_or_card== 1:
        # if they chose "Easy Mode" from home screen, play_game regular
        play_game(deck)
        print(player_actions)
        print(dealer_actions)
    elif easy_or_hard_or_stat_or_card== 2:
        # if they chose "Hard Mode" from home screen, play_game_with_strategy
        play_game_with_strategy(deck)
        print(player_actions)
        print(dealer_actions)
    elif easy_or_hard_or_stat_or_card== 3:
        # if they chose "Run 1000 Times" from home screen
        play_game(deck)
        global stats_1000
        # takes in the stats after running 1000 times (player/dealer wins, player/dealer hands, etc)
        run_1000()
        global show_stat_bool
        # show the stat screen after running one time
        show_stat_bool = True
    elif easy_or_hard_or_stat_or_card == 4:
        # if they chose to play the game using card counting strategy
        global running_count_i, running_deck
        running_count_i = play_game_with_card_counting(running_deck, running_count_i)
        print(player_actions)
        print(dealer_actions)

    # takes in the statistics in the correct order from play_game to be run in print_winner()
    dealer_final_cards, dealer_final_score, dealer_win_bool = dealer_final_hands[0]
    player_final_cards, player_final_score, player_win_bool = player_final_hands[0]

    # gets the verdict statement from dealer/player_win_bool
    if dealer_win_bool:
        verdict = "DEALER WINS!"
    elif player_win_bool:
        verdict = "PLAYER WINS!"
    else:
        verdict = "ITS A TIE!"

    # displays the visualized game onto the pygame board
    print_winner(dealer_final_cards, dealer_final_score, player_final_cards, player_final_score, verdict)

def draw_button(screen, color, text, text_color, rect):
    # draws a button based on which screen, color, text, text_color, and coordinate/size (rect)
    pg.draw.rect(screen, color, rect)
    font = pg.font.Font(None, 36)
    button_text = font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
    screen.blit(button_text, text_rect)


def show_stat_screen():
    global stats_1000_basic, stats_1000_advanced, stats_1000_card_counting, stats_1000
    # takes in the chances of winning and final balances with each strategy

    basic_winning = stats_1000_basic[0]
    basic_balance = stats_1000_basic[1]

    advanced_winning = stats_1000_advanced[0]
    advanced_balance = stats_1000_advanced[1]

    counting_winning = stats_1000_card_counting[0]
    counting_balance = stats_1000_card_counting[1]

    # from the stats1000() list, it takes in the items in the order it was appended from run_1000()
    dealer_wins = stats_1000[0]
    player_wins = stats_1000[1]
    first_chances = stats_1000[2]
    bust_chance = stats_1000[4]

    # creates a new font size for the statistics to be printed
    stat_font = pg.font.Font(None, 20)
    title_font = pg.font.Font(None, 36)  # chose a larger font size for the title
    gold = (255, 215, 0)
    # makes the background of the screen gold
    screen.fill(gold)

    # render and center the title of the statistic display screen
    title_text = title_font.render("Statistics after 1000 Basic Strategy Games", True, (0, 0, 0))
    title_text_rect = title_text.get_rect(center=(screen.get_width() // 2, 30))
    screen.blit(title_text, title_text_rect)

    # calculate the y-coord for the statistics
    stats_start_y = title_text_rect.bottom + 20 # starts printing below the title text

    # displays basic statistics: Dealer wins, Player wins, Chance of player bust
    dealer_text = stat_font.render(f"Dealer total wins: {dealer_wins}", True, (0, 0, 0))
    dealer_text_rect = dealer_text.get_rect(topleft=(50, stats_start_y))
    screen.blit(dealer_text, dealer_text_rect)

    player_text = stat_font.render(f"Player total wins: {player_wins}", True, (0, 0, 0))
    player_text_rect = player_text.get_rect(topleft=(240, stats_start_y))
    screen.blit(player_text, player_text_rect)

    bust_text = stat_font.render(f"Chance of player bust: {bust_chance}", True, (0, 0, 0))
    bust_text_rect = bust_text.get_rect(topleft=(440, stats_start_y))
    screen.blit(bust_text, bust_text_rect)

# begins drawing the first table ----------------------------------------------------------------------------------------------------------------
    # display the chances of winning based on the first card as a table
    # all constants for how the table will be created
    table_start_x = 90
    table_start_y = stats_start_y + 80
    table_spacing = 40
    table_title_font = pg.font.Font(None, 22)

    # creates a title for the first card table
    first_table_title = table_title_font.render("Chances of player winning if their first card is a:", True, (0, 0, 0))
    first_table_title_rect = first_table_title.get_rect(center=(table_start_x + 100, table_start_y - 30))
    screen.blit(first_table_title, first_table_title_rect)
    add_text1 = stat_font.render("(With basic strategy)", True, (0, 0, 0))
    add_text_rect = add_text1.get_rect(center=(table_start_x + 100, table_start_y - 10))
    screen.blit(add_text1, add_text_rect)

    # draws lines to box the sides of the first card table
    pg.draw.line(screen, (0, 0, 0), (table_start_x, table_start_y),(table_start_x, table_start_y + len(first_chances) * table_spacing), 2)
    pg.draw.line(screen, (0, 0, 0), (table_start_x + 200, table_start_y),(table_start_x + 200, table_start_y + len(first_chances) * table_spacing), 2)

    # for each item in the first_chances card list, it spaces them accordingly in the first table
    for i, chance in enumerate(first_chances):
        # draws horizontal lines to separate each table cell
        pg.draw.line(screen, (0, 0, 0), (table_start_x, table_start_y + i * table_spacing),(table_start_x + 200, table_start_y + i * table_spacing), 2)

        # renders the numbers on the left side of the table (i+2 because the first i value is 0, the first card value is 2)
        number_text = stat_font.render(f"{i + 2}", True, (0, 0, 0))
        number_text_rect = number_text.get_rect(topleft=(table_start_x + 10, table_start_y + i * table_spacing + 15))
        screen.blit(number_text, number_text_rect)

        # renders the chances of winning data on the right side of the table
        chance_text = stat_font.render(f"{chance}", True, (0, 0, 0))
        chance_text_rect = chance_text.get_rect(topleft=(table_start_x + 50, table_start_y + i * table_spacing+ 15))
        screen.blit(chance_text, chance_text_rect)

        # draws a line to separate the card value number and chance of winning data
        pg.draw.line(screen, (0, 0, 0), (table_start_x + 45, table_start_y + i * table_spacing),(table_start_x + 45, table_start_y + (i + 1) * table_spacing), 2)

    # adds a bottom horizontal line to finish the end of the table
    pg.draw.line(screen, (0, 0, 0), (table_start_x, table_start_y + len(first_chances) * table_spacing),(table_start_x + 200, table_start_y +len(first_chances) * table_spacing), 2)

    # displays the chance of winning and final average balance for basic strategy
    basic_winning_text = stat_font.render(f"Chance of winning with basic strategy: {basic_winning}", True, (0, 0, 0))
    basic_winning_rect = basic_winning_text.get_rect(topleft=(screen.get_width() // 2 + 20, stats_start_y+80))
    screen.blit(basic_winning_text, basic_winning_rect)

    basic_balance_text = stat_font.render(f"Average Balance with basic strategy: ${round(basic_balance, 2)}", True, (0, 0, 0))
    basic_balance_rect = basic_balance_text.get_rect(topleft=(screen.get_width() // 2 + 20, stats_start_y + 110))
    screen.blit(basic_balance_text, basic_balance_rect)

    # displayss the chance of winning and final average balance for advanced strategy
    advanced_winning_text = stat_font.render(f"Chance of winning with advanced strategy: {advanced_winning}", True,
                                             (0, 0, 0))
    advanced_winning_rect = advanced_winning_text.get_rect(topleft=(screen.get_width() // 2 + 20, stats_start_y + 160))
    screen.blit(advanced_winning_text, advanced_winning_rect)

    advanced_balance_text = stat_font.render(f"Average Balance with advanced strategy: ${round(advanced_balance, 2)}", True,(0, 0, 0))
    advanced_balance_rect = advanced_balance_text.get_rect(topleft=(screen.get_width() // 2 + 20, stats_start_y + 190))
    screen.blit(advanced_balance_text, advanced_balance_rect)

    # displays the chance of winning and final average balance for card counting strategy
    counting_winning_text = stat_font.render(f"Chance of winning with card counting: {counting_winning}", True,
                                             (0, 0, 0))
    counting_winning_rect = counting_winning_text.get_rect(topleft=(screen.get_width() // 2 + 20, stats_start_y + 240))
    screen.blit(counting_winning_text, counting_winning_rect)

    counting_balance_text = stat_font.render(f"Average Balance with card counting: ${round(counting_balance, 2)}", True, (0, 0, 0))
    counting_balance_rect = counting_balance_text.get_rect(topleft=(screen.get_width() // 2 + 20, stats_start_y + 270))
    screen.blit(counting_balance_text, counting_balance_rect)

    see_more_text = stat_font.render("For more detailed statistics, see Jupyter notebook!", True, (0, 0, 0))
    see_more_rect = see_more_text.get_rect(topleft=(screen.get_width() // 2 + 20, stats_start_y + 350))
    screen.blit(see_more_text, see_more_rect)

    # sets and displays a button to return to home screen to select a new game mode
    stat_button_rect = (300, 500, 200, 50)

    draw_button(screen, BUTTON_COLOR, "Return to Start", BUTTON_TEXT_COLOR, stat_button_rect)

    pg.display.flip()


if __name__ == '__main__':
    pg.init()

    # constants (sets main screen width, height, and button colors)
    WIDTH = 800
    HEIGHT = 600
    FPS = 60
    BUTTON_COLOR = (50, 150, 255) # blue
    BUTTON_TEXT_COLOR = (255, 255, 255) # white

    # sets up the main screen where the game will be played and show cards
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Start Game Screen")
    clock = pg.time.Clock()

    # sets a background screen (for the start/home page)
    playing_image = pg.image.load("starting_screen.jpg")
    screen_width, screen_height = pg.display.get_surface().get_size()
    # scale the background image to fit the screen
    scaled_background_image = pg.transform.scale(playing_image, (screen_width, screen_height))
    # displays the background image onto the screen
    screen.blit(scaled_background_image, (0, 0))

    # if true, the start screen buttons will appear (checks if we are supposed to be on the home screen)
    mainButtonBool = True

    # sets running to true for main game play loop, will not be false unless they exit
    running = True
    # makes sure we don't run the game over and over while in the running loop
    game_played = False
    easy_or_hard_or_stat_or_card = 0 #easy = 1, hard = 2, stat = 3, card count = 4

    while running:
        # if we should be on the home screen (no buttons pressed yet)
        if mainButtonBool:
            # resets the bools so new cards appear and new instances of Card class can be made
            dealer_final_hands = []
            player_final_hands = []
            stats_1000 = []
            # keeps background image running
            screen.blit(scaled_background_image, (0, 0))
            # draws four buttons on start screen: Basic Game, advanced, card counting, run 1000 times
            easy_button_rect = (300, 250, 200, 50)
            hard_button_rect = (300, 320, 200, 50)
            run_times_rect = (300, 460, 200, 50)
            card_count_rect = (300, 390, 200, 50)

            draw_button(screen, BUTTON_COLOR, "Basic Game", BUTTON_TEXT_COLOR, easy_button_rect)
            draw_button(screen, BUTTON_COLOR, "Advanced Game", BUTTON_TEXT_COLOR, hard_button_rect)
            draw_button(screen, BUTTON_COLOR, "Run 1000 Times", BUTTON_TEXT_COLOR, run_times_rect)
            draw_button(screen, BUTTON_COLOR, "Card Counting", BUTTON_TEXT_COLOR, card_count_rect)

            # waiting for the user to press a button before it continues
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    if 300 <= x <= 500 and 250 <= y <= 300:
                        # print('EASY BUTTON PRESSED')
                        mainButtonBool = False
                        game_played = False
                        easy_or_hard_or_stat_or_card= 1
                    elif 300 <= x <= 500 and 320 <= y <= 370:
                        # print('HARD BUTTON PRESSED')
                        mainButtonBool = False
                        game_played = False
                        easy_or_hard_or_stat_or_card= 2
                    elif 300 <= x <= 500 and 460 <= y <= 510:
                        # print('RUN 1000 TIMES BUTTON PRESSED')
                        mainButtonBool = False
                        game_played = False
                        easy_or_hard_or_stat_or_card= 3
                    elif 300 <= x <= 500 and 390 <= y <= 440:
                        # print('CARD COUNTING PRESSED')
                        mainButtonBool = False
                        game_played = False
                        easy_or_hard_or_stat_or_card= 4

        # if a game mode has been chosen, and the game has not run
        elif not game_played and not mainButtonBool:
            # runs the game and displays the cards on screen (also calls print_winner())
            run_game()
            # sets to True so it won't infinitly run the game while in this loop)
            game_played = True
            # resets actions collected
            player_actions = []
            dealer_actions = []
            # creates buttons to exit or return home
            restart_button_rect = (550, 500, 200, 50)
            draw_button(screen, BUTTON_COLOR, "Restart Game", BUTTON_TEXT_COLOR, restart_button_rect)
            exit_button_rect = (550, 420, 200, 50)
            draw_button(screen, BUTTON_COLOR, "Exit Game", BUTTON_TEXT_COLOR, exit_button_rect)

        # if the game has been run, but no buttons have been pressed yet
        elif game_played and not mainButtonBool:
            # if the game mode was run_1000 times, waiting for exit button to be pressed
            if show_stat_bool:
                show_stat_screen()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        x, y = pg.mouse.get_pos()
                        if event.type == pg.MOUSEBUTTONDOWN:
                            if 300 <= x <= 500 and 500 <= y <= 550:
                                # EXIT STAT BUTTON PRESSED
                                show_stat_bool = False
                                mainButtonBool = True

            # if not stat screen, waiting for for exit / return home button to be pressed after game has ran
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if 550 <= x <= 750 and 420 <= y <= 470:
                            # EXIT BUTTON PRESSED
                            pg.quit()
                            sys.exit()
                        elif 550 <= x <= 750 and 500 <= y <= 550:
                            # RESTART BUTTON PRESSED
                            game_played = False
                            mainButtonBool = True
                            print("Restart button presssed")


        # Update the display
        pg.display.flip()
        clock.tick(FPS)

pg.quit()
sys.exit()
