# a5_unogamestate.py
# skeleton by:
#     Anthony Poon (ATP65)
#     Lillian Lee (LJL2) - simple edits
# April 27, 2018

"""
This module contains UnoGameState class for keeping track of game state for Uno.
"""

class UnoGameState():
    """
    An UnoGameState keeps track of state (data) that the game stores across all player turns and
    is constantly modified during the play of the game.  This object may be passed to UnoCards
    and other classes that may affect the game state.  The particular data in the game state
    is listed below as attributes.

    Instance Attributes:
        nextPlayer [int]: A position representing the next player.  This is updated to reflect who
            the next player is, allowing for players to be skipped by changing this number.  This
            value can be treated as an index to the player list, but may have values that are
            larger or smaller than the player list size.

        isReversed [bool]: A boolean representation of whether the play order is normal or
            reversed.  If normal, the nextPlayer number should be incremented after each turn.  If
            reversed, the nextPlayer number is decremented after each turn.

        numExtraCardDraw [int]: A non-negative integer describing how many cards (if any) the next
            player must draw before the start of their next turn.
    """

    def __init__(self):
        """
        Initialize a game state as it should be at the start of a new game.  This means the
        first player in the list is the next player, the play order is not reversed, and no one
        is drawing extra cards yet.
        """
        self.nextPlayer = 0
        self.isReversed = False
        self.numExtraCardDraw = 0

    def updateNextPlayer(self):
        """
        Increment the nextPlayer attribute or decrement it, depending on whether isReversed is
        True or False.  If isReversed is False, this method increments nextPlayer.  If True,
        nextPlayer is decremented.
        """
        if self.isReversed:
            self.nextPlayer -= 1
        else:
            self.nextPlayer += 1

    def __str__(self):
        """
        Returns a string representation of the game state.
        """
        return self.__repr__()

    def __repr__(self):
        """
        Returns a string representation of the game state.
        """
        outstring = "UnoGameState"
        outstring += "( nextPlayer=" + str(self.nextPlayer)
        outstring += ", isReversed=" + str(self.isReversed)
        outstring += ", numExtraCardDraw=" + str(self.numExtraCardDraw) + ")"
        return outstring
