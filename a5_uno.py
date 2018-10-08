# a5_uno.py
# Chris VanKerkhove cjv47; Omar Rasheed oyr2
# None
# 5/9/2018
# skeleton by:
#     Anthony Poon (ATP65)
#     Victoria Litvinova (VL242) - simple edits
#     Lillian Lee (LJL2) - simple edits
# April 27, 2018

"""
This module contains an implementation of an Uno-like game using standard 
52-card playing cards.
"""
import random
import a5_player
import a5_unocard
from a5_card import Card
from a5_unocard import UnoCard
from a5_unocard import WildUnoCard
from a5_unogamestate import UnoGameState

class Uno():
    """
    Uno is a game where players take turns attempting to get rid of the cards in 
    their hand by adding them to a shared pile.  The first player with no cards in
    his/her hand wins.  This is a version of Uno with a few simplified rules and 
    using a standard 52-card deck rather than a specialized deck.
    
    This class maintains the game state, defines and enforces rules for player 
    actions, and evaluates and declares a winner.  More detailed rules will be 
    listed in the method specifications of the appropriate method.
    
    Instance Attributes:
        players [list of Players]: A list of players in this game, in play order.
        deck [list of UnoCards, may be empty]: A list of remaining cards to draw 
                from.
        pile [list of UnoCards, may be empty]: A list of cards in the shared pile in
                the order added.
        gameState [UnoGameState]: Stores the state of the game between player turns.
    """
    
    STARTING_HAND_SIZE = 5 # How many cards to give each player at the beginning of the game.
    NUM_ATTEMPTS_BEFORE_DRAW = 5 # How many attempts we give a player before forcing them to draw a card.
    
    def __init__(self, p):
        """
        Creates a new game of Uno and sets it up.  In doing this, we create a new, 
        shuffled deck, deal out the players, and set up a default play order.
        
        One way that this implementation of Uno differs from the normal game is that
        we're using the suits and ranks of standard playing cards.  Because a 
        standard playing card deck has only 52 cards (without Jokers) and a standard
        Uno deck has 108 cards, we will instead use three copies of a standard card 
        deck to make sure we have enough cards.
        
        Preconditions:
            p [list of Players]: A list of players for this game, in play order, where
                the first player is at index 0.  This list must be non-empty and contain
                only Player instances and have at least 2 players. 
        """
        # Create a deck combining three decks of standard cards and shuffle it.
        self.deck = a5_unocard.full_deck() + a5_unocard.full_deck() + a5_unocard.full_deck()
        random.shuffle(self.deck)
        self.pile = [] # The pile starts empty.
        
        # Set the players and draw out a starting hand for each player.
        self.players = p
        for player in self.players:
            player.setStartingHand(self._drawHand())
        
        # This object models the game state between player turns.  Create one in 
        # default state.
        self.gameState = UnoGameState()
        
        
    def _drawHand(self):
        """
        A helper method that creates and returns a list of cards drawn from the
        deck.  Cards should be drawn from the front of the deck (at index 0) and 
        removed from the deck.  The returned hand is a list of the cards removed 
        from the deck.  The size of the hand should not be larger than 
        self.STARTING_HAND_SIZE or however many cards are remaining in the deck, 
        whichever is smaller.
        
        Requirement: This should be implemented using a while loop.  You are not
            required to include loop invariant comments.
        
        Returns:
            A list of cards drawn from the deck.
        """
        playerhand = []
        if self.STARTING_HAND_SIZE < len(self.deck):
            while len(playerhand) < self.STARTING_HAND_SIZE:
                playerhand.append(self.deck.pop(0))
        else:
            l = len(self.deck)
            while len(playerhand) < l:
                playerhand.append(self.deck.pop(0))
        return playerhand
    
    
    def play(self):
        """
        Start and execute the game of Uno.  This method does not end until a winner
        is declared and the game is over.  This method controls the flow of the game,
        following and updating the between-player state that is stored in
        self.gameState.
        
        The general flow of the game should look like this:
            1. Determine who the next player is from the self.gameState.nextPlayer 
                attribute and the list of players.
            2. If the previous player played a card that caused this player to draw 
                extra cards (as seen in the self.gameState.numExtraCardDraw attribute), 
                as long as there are that many cards remaining in the deck, draw and 
                remove them from the front of the deck and add them to the next player's 
                hand.
            3. Allow the next player to perform their turn.
            4. Update the game state for the next player.
        
        Requirement: This should be implemented using a while loop.  You are not
            required to include loop invariant comments.
        Hint: When finding the next Player instance in the list of players, the
            gameState.nextPlayer pointer can exceed the length of the list of players.
            You need to calculate the remainder of places by which the pointer exceeds
            the length of the list to find the appropriate player.
        Hint: Make use of the helper functions below.
        
        Preconditions:
            Game has not yet been played.
        """

        while self._isGameOver() == False and self.deck != []:
            if self.gameState.numExtraCardDraw > 0:
                for each in range(self.gameState.numExtraCardDraw):
                    currentPlayer = self.gameState.nextPlayer % len(self.players)
                    self.players[currentPlayer].addCardToHand(self.deck.pop(0))
                self.gameState.numExtraCardDraw = 0
            self._performPlayerTurn(self.players[self.gameState.nextPlayer % 3])
            self.gameState.updateNextPlayer()
    
    
    def _printStartMessage(self):
        """
        A helper method that just prints out the start message at the beginning
        of the game.
        """
        print("Welcome to CS 1110 Uno using regular playing cards.")
        print()
        print("Rules:")
        print("\t* Take turns removing cards from your hand and adding them to the " +
                "pile.")
        print("\t* Added cards must match either the suit or the rank of the top " +
                "card of the pile.")
        print("\t* Tens reverse the play order.")
        print("\t* Jacks skip the next player.")
        print("\t* Queens force the next player to draw two cards (if available in " +
                "the deck).")
        print("\t* Kings are wild cards.")
        print("\t* Aces are wild cards that also force the next player to draw four" + 
                " cards.")
        print("\t* Cards that force players to draw cards do not chain and do not " +
                "cause turn to be skipped.")
        print("\t* First player with no cards in hand wins the game!")
        print()
        print("Starting game with " + str(len(self.players)) + " players: " + 
                str([p.name for p in self.players]))
    
    
    def _isGameOver(self):
        """
        A helper method that checks to see if the game is over.  The game is over 
        when there is a player with zero cards in their hand.  Returns True if the 
        game is over, False otherwise.
        """
        for player in self.players:
            # This is the first player with a zero-length hand; declare them the winner.
            if len(player.hand) == 0:
                print()
                print("The game is over!  " + player.name + " won!")
                for player in self.players:
                    print(player.name + " had ending hand: " + str(list(map(str, player.hand))))
                return True
            
        # Otherwise, we've gone through the entire list of players and no one has 
        # won yet.
        return False
    
    
    def _performPlayerTurn(self, player):
        """
        A helper method that attempts to execute the turn for a particular player.  
        The player has up to self.NUM_ATTEMPTS_BEFORE_DRAW to pick a card that can 
        actually be placed on top of the pile.  The player can also choose to return
        None to draw a card immediately.  If a good card is chosen, then the card is 
        removed from the hand, placed on the pile, and any action associated is 
        performed.  if not, then the player draws a new card and their turn ends.
        
        Preconditions:
            player [Player]: A non-None player object, whose turn is the current turn.
        """
        # Determine what is the top card on the pile; either None if the pile is 
        # empty or the last thing in the list.
        if len(self.pile) == 0:
            topCardInPile = None
        else:
            topCardInPile = self.pile[len(self.pile) - 1]
        
        # We'll perform this loop up to a maximum of NUM_ATTEMPTS_BEFORE_DRAW times
        for i in range(self.NUM_ATTEMPTS_BEFORE_DRAW):
            
            # Ask the player to give us a card to try to play.
            card = player.suggestACard(topCardInPile, self.NUM_ATTEMPTS_BEFORE_DRAW - i - 1)
            
            # If the card is None, no need to try further.
            if card == None:
                break
            
            # If the card is playable on top of the pile, do so and return without 
            # drawing a card.
            if card.isPlaceableOnTop(topCardInPile):
                
                # Move the card to the pile.
                player.removeCardFromHand(card)
                self.pile.append(card)
                
                # Perform any action that the card has on the game state.
                card.performAction(self.gameState)
                
                # Return so that the player does not draw a card.
                return
            
            # If the card was not playable, we notify the player, and try again.
            else:
                player.notifyNotAcceptableCard(card)
        
        # We got here because either the player ran out of attempts or chose to draw
        # explicitly. Draw a card, so long as the deck has more cards.
        if len(self.deck) > 0:
            player.addCardToHand(self.deck.pop(0))




"""
This sets up and starts a game of Uno.
"""
if __name__ == '__main__': 
    p = []
    p.append(a5_player.HumanConsolePlayer())
    p.append(a5_player.RandomAiPlayer("HAL 9000"))
    p.append(a5_player.RandomAiPlayer("WOPR"))
    p.append(a5_player.RandomAiPlayer("Skynet"))
    p.append(a5_player.RankThenSuitAiPlayer("lil hoe"))
    
    # TODO: Students, after you implement the RankThenSuitAiPlayer, add a 5th
    # player to the game using your new RankThenSuitAiPlayer implementation.  This
    # should result in one human player, three random AI players and one "smarter"
    # rank-then-suit AI player.
    
    u = Uno(p)
    u.play()
