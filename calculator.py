# Cribbage Calculator 
# Author: Mikayla Smith
# Last Modified: 27/03/2024

import itertools
import copy

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

#Get the value of a card for when counting to 15
def get_card_points_15(value):
    # Define the logic to calculate points for a card value here
    if value in ["K", "Q", "J"]:
        return 10
    elif value == "A":
        return 1
    else:
        return int(value)

#Getting a value for a card when evaluating runs
def get_card_points_runs(value):
    # Define the logic to calculate points for a card value here
    if value == "K": 
        return 13
    elif value == "Q":
        return 12
    elif value == "J":
        return 11
    elif value == "A":
        return 1
    else:
        return int(value)

#Finding Nibs  
def nibs(flipped):
    points = 0

    #For Nibs (flipping a jack)
    if flipped.value == "J":
        print("Nibs for 2")
        points += 2

    return points

#Finding Nobs
def nobs(hand, flipped):
    points = 0
    
    #For Nobs (suit of jack in hand matches the flipped suit)
    for card in hand:
        if card.suit == flipped.suit and card.value == "J":
            print("Nobs for 1")
            points += 1
            break

    return points

#Finding 15s
def find_15s(hand, flipped):
    hand = copy.copy(hand)
    hand.append(flipped)

    points = 0

    for subset_size in range(1, len(hand) + 1):
        for subset in itertools.combinations(hand, subset_size):
            subset_values = [card.value for card in subset]
            subset_sum = sum(get_card_points_15(value) for value in subset_values)

            if subset_sum == 15:
                points += 2
                subset_expression = " + ".join(f"{card.value} {card.suit}" for card in subset)
                print(f"{subset_expression} - 15 {points}.")
                
    return points

#Finding Pairs
def find_pairs(hand, flipped):
    hand = copy.copy(hand)
    hand.append(flipped)

    points = 0

    for card1, card2 in itertools.combinations(hand, 2):
        if card1.value == card2.value:
            points += 2
            print(f"Pair {card1.value} {card1.suit} / {card2.value} {card2.suit} for {points}")
            
    return points

#Finding Runs
def find_runs(hand, flipped):
    card_values = [get_card_points_runs(card.value) for card in hand]
    card_values.append(get_card_points_runs(flipped.value))

    card_values.sort(reverse=True)
    points = 0

    longest_run = None
    runs = []
    
    for run_length in range(len(card_values), 2, -1):  # Start with longest possible run length
        for run in itertools.permutations(card_values, run_length):
            if all(run[i] == run[i-1] + 1 for i in range(1, len(run))):
                longest_run = run
                break
        if longest_run:
            break  # Exit the loop if longest run is found

    if longest_run:
        # Filter out any shorter runs using the same numbers
        if len(longest_run) == 3:
            for run_length in range(3, len(card_values) + 1):
                for run in itertools.permutations(card_values, run_length):
                    if (all(run[i] == run[i-1] + 1 for i in range(1, len(run)))):
                        runs.append(run)
        elif len(longest_run) == 4:
            for run_length in range(4, len(card_values) + 1):
                for run in itertools.permutations(card_values, run_length):
                    if (all(run[i] == run[i-1] + 1 for i in range(1, len(run)))):
                        runs.append(run)
        else:
            runs = [longest_run]


    for run in runs:
        points += len(run)
        print(f"Run of {len(run)}{run} for {points}")

    return points

#Finding Flush
def find_flush(hand, flipped):
    points = 0
    first_suit = hand[0].suit

    if all(card.suit == flipped.suit for card in hand):
        points += len(hand) + 1
        print(f"Flush of {hand[0].suit} for {points}")
    elif all(card.suit == first_suit for card in hand):
        points += len(hand)
        print(f"Flush of {first_suit} for {points}")

    return points

#Calculate the score
def calculate():
    points = 0
    hand = []
    cut_card = 0
    flipped = 0

    print("Enter cards one by one until hand is represented.")
    print("Format for card as it is entered: value (A, K, Q, J, 2, 3 etc.) suit (diamonds, hearts, spades, clubs)")
    print("Ex: K clubs or A spades")
    print ("Enter 'done' when finished.")

    # card = Card("A", "hearts")
    # hand.append(card)
    # card = Card("2", "spades")
    # hand.append(card)
    # card = Card("3", "clubs")
    # hand.append(card)
    # card = Card("4", "hearts")
    # hand.append(card)

    # flipped = Card("K", "clubs")

    # card = Card("J", "hearts")
    # hand.append(card)
    # card = Card("Q", "spades")
    # hand.append(card)
    # card = Card("Q", "clubs")
    # hand.append(card)
    # card = Card("10", "hearts")
    # hand.append(card)

    # flipped = Card("5", "hearts")
    while True:
        card = input("Card: ")
        if card == "done":
            cut_card = input("Flipped Card: ")
            value, suit = cut_card.split()
            flipped = Card(value, suit)
            points += nibs(flipped)
            break
        else:
            value, suit = card.split()
            card = Card(value, suit)
            hand.append(card)

    #Organize the hand
    hand = sorted(hand, key=lambda x: x.value)
    
    for card in hand:
        print(f"{card.value} {card.suit}")
    
    print("------------------------")

    #Calculate points
    points += find_15s(hand, flipped)
    points += find_pairs(hand, flipped)
    points += find_runs(hand, flipped)
    points += find_flush(hand, flipped)
    points += nobs(hand, flipped)

    print("------------------------")
    print(f'Total points: {points}')
    return points

calculate()