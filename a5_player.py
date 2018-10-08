# a5_player.py
# Chris VanKerkhove cjv47, Omar Rasheed oyr2
# None
# 5/9/2018
# skeleton by:
#     Anthony Poon (ATP65)
#     Victoria Litvinova (VL242) - simple edits
#     Lillian Lee (LJL2) - simple edits
# April 27, 2018

"""
This module contains Player class and sub-classes for the Uno game.
"""
import random
import sys
from a5_unocard import WildUnoCard

class Player():
    """
    A player represents the state of one particular participant in an Uno game. 
    A player instance can attempt to play a card by suggesting a card to play.  
    A player has subclasses which may be human players or AI players.
    
    This is an abstract class.  An abstract class is a class, typically a
    parent of several subclasses, that doesn't have a lot of functionality
    on its own and is actually intended to be incomplete.  This incomplete
    functionality is caused by at least one abstract method, methods which are
    defined but have no implementation.  For Player, this class has one abstract
    method, suggestACard.  As an abstract class, the Player class should not be
    instantiated directly.
    
    Instance Attributes:
        name [str]: A non-blank name for this player for easy identification.
        hand [list of UnoCards, may be empty]: A list of cards currently in the 
            player's hand.
    """
    def __init__(self, name):
        """
        Create and set up a new player with the given name and an initially empty
        hand.
        
        Preconditions:
            name [str]: A non-None, non-blank string name for this player.
        """
        self.name = name
        self.hand = []
        
    def setStartingHand(self, h):
        """
        Set the hand that the player has, replacing entirely any hand that they 
        had before.
        
        Preconditions:
            h [list of UnoCards]: A list of only Cards.
        """
        self.hand = h
        
    def addCardToHand(self, c):
        """
        Add the given card to the hand.
        
        Preconditions:
            c [UnoCard]: A card which cannot be None not already in the player's hand.
        """
        self.hand.append(c)
        print(self.name + " drew a card and now has " + str(len(self.hand)) + " card(s).")
    
    def removeCardFromHand(self, c):
        """
        Remove the given card from the hand if the card exists in the hand.
        
        Preconditions:
            c [UnoCard]: A card which may exist in the Player's hand.
        """
        if c in self.hand:
            self.hand.remove(c)
            if len(self.hand) == 1:
                print(self.name + " played a card from hand, the " + str(c) + 
                    ", and now has " + str(len(self.hand)) + " card.  UNO!")
            else:
                print(self.name + " played a card from hand, the " + str(c) + 
                    ", and now has " + str(len(self.hand)) + " cards.")
    
    def suggestACard(self, topCardInPile, attemptsRemaining):
        """
        Returns a single card that will be played from the hand or None if
        the player will not play a card.  The card is NOT removed from the
        hand.  The player can decide to not play a card (for example if the
        player chooses to draw instead or cannot play a valid card).
        
        Preconditions:
            topCardInPile [Card or None]: The top card in the pile currently 
                before the player's turn.  Note that this may be None if there 
                are no cards in the pile.
            attemptsRemaining [int]: A non-negative number of attempts remaining
                after this method call if the card suggested could not be placed
                on the pile.  This is mostly passed for printing purposes.
                
        Returns:
            An UnoCard object in the player's hand or None.
        """
        pass
    
    def notifyNotAcceptableCard(self, suggestedCard):
        """
        The game can call this method to notify the player that their last card
        they attempted to play was not considered valid.  By default, the base
        implementation of this method does nothing.
        
        Preconditions:
            suggestedCard [UnoCard or None]: The card that was most-recently
                suggested by the player or None if the player suggested no card.
        """
        return


class RandomAiPlayer(Player):
    """
    An AI implementation of a player that attempts to make moves by suggesting a 
    card from the hand at random.
    """
    def suggestACard(self, topCardInPile, attemptsRemaining):
        """
        Suggest a card by picking randomly from the hand or None if the hand is 
        empty.
        
        Preconditions:
            Same preconditions as the parent definition of this method.
        
        Returns:
            A random UnoCard object in the player's hand.
        """
        if self.hand == []:
            return None
        else:
            return random.choice(self.hand)


class RankThenSuitAiPlayer(Player):
    """
    An improved AI implementation that attempts to find a card in the hand that 
    matches the rank of the card at the top of the pile first.  If that fails, 
    then attempts to find a card in the hand with a matching suit.
    """
    def suggestACard(self, topCardInPile, attemptsRemaining):
        """
        An improved AI that picks a card from the hand via the following rules:
            1. If the top card is None, picks a card randomly.
            2. Otherwise, picks the first non-wild card found in the hand
                matching the rank of the top card, if one exists.
            3. Otherwise, picks the first non-wild card found in the hand
                matching the suit of the top card, if one exists.
            4. Otherwise, picks the first wild card found in the hand, if one
                exists.
            5. Otherwise, picks a random card from the hand.
            
        Preconditions:
            Same preconditions as the parent definition of this method.
        
        Returns:
            A Card object in the player's hand.
        """
        if topCardInPile == None:
            return random.choice(self.hand)
        else:
            currentIndex = 0
            while currentIndex < len(self.hand):
                if self.hand[currentIndex].rank != 1 and self.hand[currentIndex].rank != 13:
                    if self.hand[currentIndex].rank == topCardInPile.rank:
                        return self.hand[currentIndex]
                currentIndex += 1
            currentIndex = 0
            while currentIndex < len(self.hand):
                if self.hand[currentIndex].rank != 1 and self.hand[currentIndex].rank != 13:
                    if self.hand[currentIndex].suit == topCardInPile.suit:
                        return self.hand[currentIndex]
                currentIndex += 1
            currentIndex = 0
            while currentIndex < len(self.hand):
                if self.hand[currentIndex].rank == 1 or self.hand[currentIndex].rank == 13:
                    return self.hand[currentIndex]
                currentIndex += 1
            return random.choice(self.hand)
    
    def _pickRandomCardHelper(self):
        """
        A little helper function to pick a card from the hand randomly or will 
        return None if the hand is empty.
        """
        if self.hand == []:
            return None
        else:
            return random.choice(self.hand)


class HumanConsolePlayer(Player):
    """
    An implementation of a player that is backed by a human.  In particular, it 
    asks the human to enter cards via the console.  In addition, this
    implementation overrides the add and remove card methods to print additional
    information to the console for the player.
    """
    def __init__(self):
        """
        Create a new human player.  Since this is the only player, we set the
        name to the string "You".
        """
        super().__init__("You")
    
    def addCardToHand(self, c):
        if c not in self.hand:
            self.hand.append(c)
            print("You drew a card, the " + str(c) + ", and now you have " +
                  str(len(self.hand)) + " card(s).")
    
    def removeCardFromHand(self, c):
        if c in self.hand:
            self.hand.remove(c)
            if len(self.hand) == 1:
                print("You played a card from hand, the " + str(c) +
                      ", and now have " + str(len(self.hand)) + " card.  UNO!")
            else:
                print("You played a card from hand, the " + str(c) +
                      ", and now have " + str(len(self.hand)) + " card(s).")
    
    def suggestACard(self, topCardInPile, attemptsRemaining):
        """
        Allows the human to select a card to suggest via the console by typing 
        in the index of the card in the hand.
        
        Preconditions:
            Same preconditions as the parent definition of this method.
        
        Returns:
            An UnoCard object in the player's hand or None.
        """
        print()
        print("It is now your turn!")
        print("You have " + str(attemptsRemaining) + 
            " remaining attempt(s) to choose a valid card.")
        
        if topCardInPile == None:
            print("The pile is currently empty.  You may play any card.")
        else:
            print("The top card in pile is currently the " + str(topCardInPile) 
                + ".")
        
        # Print each card in the hand on a separate line.
        handDict = {}
        print("Your hand is:")
        for i in range(len(self.hand)):
            print("\t" + str(i) + " - " + str(self.hand[i]))
        
        # Build the acceptable inputs as strings of the indexes.
        acceptableInputs = list(map(str, range(len(self.hand))))
        acceptableInputs.append('d')
        acceptableInputs.append('q')
        
        input = self._prompt_player("Type the index of the card to select, 'd' " +
            "to draw a card, or 'q' to quit the game: ", acceptableInputs)
        print()
        
        if input == 'd':
            return None
        elif input == 'q':
            print ("You quit the game.")
            sys.exit()
        else:
            return self.hand[int(input)]
    
    def _prompt_player(self, prompt, valid_responses):
        """
        Prompts the user with `prompt` and checks if the response is valid against
        a list of acceptable answers.  If it is not valid, it asks the question
        again. Otherwise, returns the player's answer.
        
        Preconditions:
            prompt is a string.
            valid_responses is a list of strings representing the valid responses.
        
        Returns:
            The choice of a player for a given prompt.
        
        Taken from blackjack.py in Lab 08, Spring 2018, CS 1110 by:
        L. Lee (LJL2), S. Marschner (SRM2), W. White (WMW2), A. Parkhurst (ANP56)
        """
        # Ask the question for the first time.
        # ri: input received from player
        ri = input(prompt)
    
        # Continue to ask while the response is not valid.
        while not (ri in valid_responses):
            print('Sorry, your response is invalid. It must be one of ' +
                  str(valid_responses))
            print()
            ri = input(prompt)
    
        return ri
    
    def notifyNotAcceptableCard(self, suggestedCard):
        """
        The HumanConsolePlayer subclass of Player simply prints a message to
        notify the human that their last card was rejected.
        """
        print("Your last card, " + str(suggestedCard) + ", was invalid and " +
            "not playable.  It must match either the suit or the rank or be a " +
            "wild card.")
