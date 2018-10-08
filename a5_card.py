# a5_card.py --- no changes from card_lab12.py in CS1110 Spring 2018
# L. Lee (LJL2), S. Marschner (SRM2), and W. White (WMW2)
# Apr 24, 2018

"""Module providing a class for standard playing cards (no jokers).

Implementation adapted from chapter 18 of the course text,
_Think Python_, by Allen B. Downey.
"""

from functools import total_ordering  # for implementing comparisons in Python3


# decorator "fills in" missing comparisons, at the cost of speed
@total_ordering
class Card():
    """An instance is a standard playing card (no jokers).

    Class variables:
        SUIT_NAMES: list of valid suit names:
            ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        NUM_SUITS (int): number of valid suits: 4
        RANK_NAMES: list representing translations of valid int ranks to names.
            0 is not a valid rank; do not reference RANK_NAME[0]
            RANK_NAME[1] is 'Ace',
            RANK_NAME[2] is '2',
           ...
            RANK_NAME[10] is '10',
            RANK_NAME[11] is 'Jack',
            RANK_NAME[12] is 'Queen',
            RANK_NAME[13] is 'King'
        NUM_RANKS (int): number of valid ranks: 13

    Instance Attributes:
        suit (int in 0..Card.NUM_SUITS-1): The suit encoding of this card.
            The *name* of this suit is given by `Card.SUIT_NAMES[suit]`.

        rank (int in 1..Card.NUM_RANKS): The rank encoding of this card.
            The *name* of this rank is given by `Card.RANK_NAMES[rank]`.

    For example, if we execute c = Card(0, 12), Card.SUIT_NAMES[c.suit] is
    'Clubs' and Card.RANK_NAMES[c.rank] is 'Queen', meaning c is the Queen of
    Clubs.
    """

    # class variable definitions.
    SUIT_NAMES = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    NUM_SUITS = len(SUIT_NAMES)
    # Halt execution if we have an unexpected number of suits
    assert NUM_SUITS == 4, 'instead of 4 suits, there are' + str(NUM_SUITS)

    # Starts at None so that we can treat RANK_NAMES as a translation table:
    # RANK_NAME[1] is 'Ace', RANK_NAME[13] is 'King', etc.
    RANK_NAMES = [None, 'Ace', '2', '3', '4', '5', '6', '7',
                  '8', '9', '10', 'Jack', 'Queen', 'King']
    NUM_RANKS = len(RANK_NAMES) - 1
    # Halt execution if we have an unexpected number of suits
    assert NUM_RANKS == 13, 'instead of 13 ranks, there are' + str(NUM_RANKS)

    def __init__(self, s=0, r=1, alt=None):
        """Initializer: A new Card with the given suit and rank.

        If `alt` is None, the Card has suit encoding s and rank encoding r.
        Otherwise, the suit and rank are given by `alt` as described below.

        Preconditions:
           s in 0..self.NUM_SUITS-1
           r in 1..self.NUM_RANKS
           If alt is not None, then it is length-2 string, where:
              * alt[0] in 'A23456789TJQK' represents the rank:
                A for ace, 2 for 2, 3 for 3, ...
                9 for 9, T for ten, J for Jack, Q for Queen, K for King
              * alt[1] in 'CDHS' represents the suit:
                C for clubs, D for diamonds, H for hearts, S for spades
              * s and r, even if given, are overridden by alt.

        """
        # We've written self.NUM_SUITS instead of Card.NUM_SUITS and
        # self.NUM_RANKS instead of Card.NUM_RANKS in the preconditions
        # to allow for sub-classing of the class Card
        # where there can be more suits or ranks than in the usual Card class.
        if alt:
            s = 'CDHS'.index(alt[1])
            r = ' A23456789TJQK'.index(alt[0])
        self.suit = s
        self.rank = r

    def __str__(self):
        """Returns: Readable string representation of this card.
        Example: '2 of Hearts'
        """
        return self.RANK_NAMES[self.rank] + ' of ' + self.SUIT_NAMES[self.suit]

    def __repr__(self):
        """Returns: Unambiguous string representation of this card.
        Example: 'Card(3,2): 2 of Spades'
        """
        outstring = 'Card'
        outstring += '(' + str(self.suit) + ',' + str(self.rank) + ')'
        outstring += ': ' + str(self)
        return outstring

    def __eq__(self, other):
        """Returns: True if `other` is a Card that has the same suit and rank as
        this Card;
        False if `other` is a Card that doesn't have the same suit and rank as
        this Card;
        and NotImplemented if `other` is not a Card."""
        if not isinstance(other, Card):
            return NotImplemented
        else:
            return (self.suit, self.rank) == (other.suit, other.rank)

    def __ne__(self, other):
        """Returns: True if `other` is a Card and does not have the same suit
        and rank as this Card, False otherwise."""
        return not self == other

    def __gt__(self, other):
        """Returns:
        True if `other` is a Card and either:
            * the rank of this Card is greater than the rank of `other`, or
            * this Card has the same rank as `other` but a suit that is greater
                than the suit of `other`;
        False if `other` is a Card and neither *'d condition above holds;
        NotImplemented if `other` is not a Card"""
        if not isinstance(other, Card):
            return NotImplemented
        else:
            return (self.rank > other.rank or
                    (self.rank == other.rank and self.suit > other.suit))

    def __hash__(self):
        """Returns a so-called 'hash' of this object, which is necessary to
        allow Cards to be keys in dictionaries.  We make the 'hash' of a Card
        be a tuple of its suit and rank.
        """
        # In Python 3, if you override __eq__, __hash__ will be set to None
        # unless __hash__ is defined
        return hash((self.suit, self.rank))


def full_deck():
    """Returns: list of the standard 52 Cards.
        The list is in ascending suit then rank order:
        Ace of Clubs first, King of Spades last."""
    output = []  # list of cards so far to be returned
    for suit in range(Card.NUM_SUITS):
        # range(n) creates the list [0,1,2,...,n-1]
        for rank in range(1, Card.NUM_RANKS+1):
            # range(1,n) creates the list [1,2,...,n-1]
            # skip the None value
            output.append(Card(suit, rank))
    return output


def print_cards(clist):
    """Print cards in list clist as a human-readable sequence of lines.

    Example printout:
    Queen of Clubs
    2 of Spades

    Precondition: clist is a (possibly empty) list of Cards."""
    for c in clist:
        print(c)  # `print` calls the __str__ function.


def cardlist_str(clist):
    """Returns: human_friendly string (no newlines) representing the
    cards in clist.
    Precondition: clist is a (possibly empty) list of Cards."""
    return ', '.join(map(str, clist))
