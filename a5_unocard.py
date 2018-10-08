# a5_unocard.py
# Chris VanKerkhove cjv47; Omar Rasheed oyr2
# None
# 5/9/2018
# skeleton by:
#     Anthony Poon (ATP65)
#     Victoria Litvinova (VL242) - simple edits
#     Lillian Lee (LJL2) - simple edits
# April 27, 2018

"""
This module contains the UnoCard class and sub-classes for the Uno game.
"""
from a5_card import Card
import a5_unogamestate

class UnoCard(Card):
    """
    An Uno card is an extension of the standard playing card that provide two 
    additional features. It is capable of determining whether it can be placed 
    on top of another card.  And also, it can define an optional action to take 
    on the game state when the card is played.
    
    Instance Attributes:
        specialName [str or None]: A short name of any special ability that this 
            UnoCard has or None if the card doesn't do anything special.
    """
    
    def __init__(self, suit, rank):
        """
        In addition to defining the suit and rank, also define the special name.
        By default, the special name is None.
        
        Preconditions:
            suit [int]: An int in 0..Card.NUM_SUITS-1.
        """
        super().__init__(suit, rank)
        self.specialName = None
    
    def __str__(self):
        """
        Override the parent str method to append the special name of this card, 
        if any.
        
        Returns:
            A string representation of an UnoCard.
        """
        output = super().__str__()
        if self.specialName != None:
            output = output + " (" + self.specialName + ")"
        return output
    
    def isPlaceableOnTop(self, c):
        """
        Determines if the self UnoCard can be placed on top of the given card, c.
        For example, if the given card is the top card of the pile, this method 
        returns True or False depending on whether this card can be added to the
        pile.
        
        The default implementation of this is that it returns True if the given 
        card is None or either the rank or suit of this card matches the given
        card.
        
        Preconditions:
            c [Card or None]: A card, which is typically the top card in the 
                game's pile, or None if the game's pile is empty.
                
        Returns:
            A boolean, True if this card can be placed on top of c or False if
            it cannot. 
        """
        if c == None:
            return True
        
        if self.rank == c.rank:
            return True
        
        if self.suit == c.suit:
            return True
        
        else:
            return False
        
    def performAction(self, gameState):
        """
        This method is invoked when the game has determined that this card has
        been played and so it must perform its action. The method allows the card
        to perform its action by modifying the provided game state.  By default,
        an UnoCard has a no-op action.
        
        Preconditions:
            gameState [UnoGameState]: A non-None game state for the currently 
                running game of Uno.
        """
        return


class ReverseActionCard(UnoCard):
    """
    Cards with the 10 rank are considered Reverse cards, which reverse the order
    of play.
    """
    
    def __init__(self, suit):
        """
        Override the parent init method so that the rank is always 10 and the
        specialName attribute is set to "Reverse".  Inside, this should call
        an init method from a parent class.
        
        Requirement: Call a parent class's init method.
        
        Preconditions:
            suit [int]: An int in 0..Card.NUM_SUITS-1.
        """
        super().__init__(suit, 10)
        self.specialName = 'Reverse'

    
    def performAction(self, gameState):
        """
        Modify the game state to reverse the order of play.
        
        Preconditions:
            Same preconditions as the parent definition of this method.
        """
        print(">> Play order has been reversed!")
        gameState.isReversed = not gameState.isReversed


class SkipActionCard(UnoCard):
    """
    Cards with the 11th rank (Jacks) are considered Skip cards, which skip the 
    next player.
    """
    
    def __init__(self, suit):
        """
        Override the parent init method so that the rank is always 11 and the
        specialName attribute is set to "Skip".  Inside, this should call
        an init method from a parent class.
        
        Requirement: Call a parent class's init method.
        
        Preconditions:
            suit [int]: An int in 0..Card.NUM_SUITS-1.
        """
        super().__init__(suit, 11)
        self.specialName = 'Skip'
        

    def performAction(self, gameState):
        """
        Modify the game state to increment past the next player without actually
        allowing that player to take their turn.
        
        Preconditions:
            Same preconditions as the parent definition of this method.
        """
        print(">> Next player has been skipped!")
        if gameState.isReversed:
            gameState.nextPlayer -= 1
        else:
            gameState.nextPlayer += 1
    
    
class DrawTwoActionCard(UnoCard):
    """
    Cards with the 12th rank (Queens) are Draw-Two cards, which force the next 
    player to draw two cards.  Note that in this version of the game, we do not 
    skip the next player even though they are forced to draw two cards.
    """
    
    def __init__(self, suit):
        """
        Override the parent init method so that the rank is always 12 and the
        specialName attribute is set to "Draw Two".  Inside, this should call
        an init method from a parent class.
        
        Requirement: Call a parent class's init method.
        
        Preconditions:
            suit [int]: An int in 0..Card.NUM_SUITS-1.
        """
        super().__init__(suit, 12)
        self.specialName = "Draw Two"

        
    def performAction(self, gameState):
        """
        Modify the game state to force the next player to draw two cards.  Do 
        NOT skip the next player.
        
        Preconditions:
            Same preconditions as the parent definition of this method.
        """
        print(">> Next player must draw two cards!")
        gameState.numExtraCardDraw = 2
    
    
class WildUnoCard(UnoCard):
    """
    Cards in the 13th Rank (Kings) are Wild cards.  They can be played on top of
    any card and force the suit to change to this card's suit.
    """
    
    def __init__(self, suit):
        """
        Override the parent init method so that the rank is always 13 and the
        specialName attribute is set to "Wild".  Inside, this should call
        an init method from a parent class.
        
        Requirement: Call a parent class's init method.
        
        Preconditions:
            suit [int]: An int in 0..Card.NUM_SUITS-1.
        """
        super().__init__(suit, 13)
        self.specialName = "Wild"

        
    def isPlaceableOnTop(self, c):
        """
        As wild cards can be placed on top of any card, overwrite the parent 
        implementation so that this card is always playable on top of any card
        regardless of what that card is.
        
        Preconditions:
            Same preconditions as the parent definition of this method.
            
        Returns:
            A boolean, True if this card can be placed on top of c or False if
            it cannot. 
        """
        return True


class WildDrawFourActionCard(WildUnoCard):
    """
    Cards in the 1st Rank (Aces) are Wild Draw Four cards.  They can be played 
    on top of any card, force the suit to change to this card's suit, and also 
    force the next player to draw four cards.
    
    Notice that this extends from WildUnoCard, and thus inherits its 
    isPlaceableOnTop behavior.
    """
    def __init__(self, suit):
        """
        Override the parent init method so that the rank is always 1 and the
        specialName attribute is set to "Wild Draw Four".  Inside, this should
        call an init method from a parent class.
        
        Requirement: Call a parent class's init method.
        Hint: There are ways to call the init of a specific parent class.  For
        example, super() can be called with arguments:
        https://docs.python.org/3/library/functions.html#super
        
        Preconditions:
            suit [int]: An int in 0..Card.NUM_SUITS-1.
        """
        super().__init__(suit)
        self.rank = 1
        self.specialName = "Wild Draw Four"

    
    def performAction(self, gameState):
        """
        Modify the game state to force the next player to draw four cards.  Do 
        NOT skip the next player.
        
        Preconditions:
            Same preconditions as the parent definition of this method.
        """
        print(">> Next player must draw four cards!")
        gameState.numExtraCardDraw = 4
        
        




def full_deck():
    """
    Returns a list of all 52 cards, where the 10s, Jacks, Queens, Kings, and 
    Aces are instantiated as instances of the appropriate UnoCard sub-type and 
    the remaining cards are provided as UnoCard instances.  The returned list is
    in ascending rank order and then suit order, with the 2 of Clubs first and 
    then the Ace of Spades last.
    
    Returns:
        A list of 52 UnoCards.
    """
    output = []
    
    # This includes ranks between 2 and 9, inclusive, which are created as normal
    # cards.
    for rank in range(2, 10):
        for suit in range(Card.NUM_SUITS):
            output.append(UnoCard(suit, rank))
    
    # Create reverse cards, which are 10s.
    for suit in range(Card.NUM_SUITS):
        output.append(ReverseActionCard(suit))
    
    # Create skip cards, which are Jacks.
    for suit in range(Card.NUM_SUITS):
        output.append(SkipActionCard(suit))
        
    # Create draw two cards, which are Queens.
    for suit in range(Card.NUM_SUITS):
        output.append(DrawTwoActionCard(suit))
        
    # Create wild cards, which are Kings.
    for suit in range(Card.NUM_SUITS):
        output.append(WildUnoCard(suit))
    
    # Create wild draw four cards, which are Aces.
    for suit in range(Card.NUM_SUITS):
        output.append(WildDrawFourActionCard(suit))
    
    return output
