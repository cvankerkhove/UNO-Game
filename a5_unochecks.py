# a5_unochecks.py
# skeleton by:
#     Anthony Poon (ATP65)
# April 27, 2018

"""
This module contains some light tests for the Uno game and related classes.
"""

import unittest
import sys
import a5_player as player
import a5_uno as uno
import a5_unocard as unocard

from a5_card import Card
from a5_unogamestate import UnoGameState


class AbstractTestUnoCard(unittest.TestCase):
    """
    Provides helper methods specific to testing UnoCards.
    """

    def assert_unocard_init(self, card, expected_suit, expected_rank,
                            expected_specialName):
        """
        Helper method that provides common asserts for init methods of
        UnoCard sub-classes.
        """
        self.assertTrue(isinstance(card, Card))
        self.assertEqual(expected_suit, card.suit)
        self.assertEqual(expected_rank, card.rank)
        self.assertEqual(expected_specialName, card.specialName)


class TestReverseActionCard(AbstractTestUnoCard):
    """
    Tests for a5_unocard.ReverseActionCard.
    """

    def test_init(self):
        """
        Tests the init method of ReverseActionCard.
        """
        card = unocard.ReverseActionCard(1)
        self.assert_unocard_init(card, 1, 10, "Reverse")

    def test_performAction(self):
        """
        Tests the performAction method of ReverseActionCard.
        """
        card = unocard.ReverseActionCard(0)
        gameState = UnoGameState()
        card.performAction(gameState)
        self.assertEqual(True, gameState.isReversed)
        card.performAction(gameState)
        self.assertEqual(False, gameState.isReversed)


class TestSkipActionCard(AbstractTestUnoCard):
    """
    Tests for a5_unocard.SkipActionCard.
    """

    def test_init(self):
        """
        Tests the init method of SkipActionCard.
        """
        card = unocard.SkipActionCard(3)
        self.assert_unocard_init(card, 3, 11, "Skip")

    def test_performAction(self):
        """
        Tests the performAction method of SkipActionCard.
        """
        card = unocard.SkipActionCard(0)
        gameState = UnoGameState()
        card.performAction(gameState)
        self.assertEqual(1, gameState.nextPlayer)

        # Reverse and try again.
        gameState.isReversed = True
        card.performAction(gameState)
        self.assertEqual(0, gameState.nextPlayer)

        # Make sure it goes negative.
        card.performAction(gameState)
        self.assertEqual(-1, gameState.nextPlayer)


class TestDrawTwoActionCard(AbstractTestUnoCard):
    """
    Tests for a5_unocard.DrawTwoActionCard.
    """

    def test_init(self):
        """
        Tests the init method of DrawTwoActionCard.
        """
        card = unocard.DrawTwoActionCard(2)
        self.assert_unocard_init(card, 2, 12, "Draw Two")

    def test_performAction(self):
        """
        Tests the performAction method of DrawTwoActionCard.
        """
        card = unocard.DrawTwoActionCard(0)
        gameState = UnoGameState()
        card.performAction(gameState)
        self.assertEqual(2, gameState.numExtraCardDraw)

        # This should set and not increment the value, check when the initial
        # value is not zero.
        gameState.numExtraCardDraw = 1
        card.performAction(gameState)
        self.assertEqual(2, gameState.numExtraCardDraw)


class TestWildUnoCard(AbstractTestUnoCard):
    """
    Tests for a5_unocard.WildUnoCard.
    """

    def test_init(self):
        """
        Tests the init method of WildUnoCard.
        """
        card = unocard.WildUnoCard(0)
        self.assert_unocard_init(card, 0, 13, "Wild")

    def test_performAction(self):
        """
        Tests the performAction method of WildUnoCard.
        """
        card = unocard.WildUnoCard(0)
        gameState = UnoGameState()

        # The perform action should have been a no-op.
        card.performAction(gameState)
        self.assertEqual(0, gameState.nextPlayer)
        self.assertEqual(False, gameState.isReversed)
        self.assertEqual(0, gameState.numExtraCardDraw)

    def test_isPlaceableOnTop(self):
        """
        Test the isPlaceableOnTop method of WildUnoCard.
        """
        card = unocard.WildUnoCard(0) # Wild clubs
        gameState = UnoGameState()

        # Is placeable on top of miss-matching suit.
        topCard = Card(alt="KD")
        self.assertTrue(card.isPlaceableOnTop(topCard))

        # Is placeable on top of miss-matching rank.
        topCard = Card(alt="3C")
        self.assertTrue(card.isPlaceableOnTop(topCard))

        # Is placeable on top of matching suit and rank.
        topCard = Card(alt="KC")
        self.assertTrue(card.isPlaceableOnTop(topCard))


class TestWildDrawFourActionCard(AbstractTestUnoCard):
    """
    Tests for a5_unocard.WildDrawFourActionCard.
    """

    def test_init(self):
        """
        Tests the init method of WildDrawFourActionCard.
        """
        card = unocard.WildDrawFourActionCard(0)
        self.assert_unocard_init(card, 0, 1, "Wild Draw Four")
        self.assertTrue(isinstance(card, unocard.WildUnoCard))

    def test_performAction(self):
        """
        Tests the performAction method of WildDrawFourActionCard.
        """
        card = unocard.WildDrawFourActionCard(0)
        gameState = UnoGameState()
        card.performAction(gameState)
        self.assertEqual(4, gameState.numExtraCardDraw)

        # This should set and not increment the value, check when the initial
        # value is not zero.
        gameState.numExtraCardDraw = 1
        card.performAction(gameState)
        self.assertEqual(4, gameState.numExtraCardDraw)

    def test_isPlaceableOnTop(self):
        """
        Test the isPlaceableOnTop method of WildDrawFourActionCard.
        """
        card = unocard.WildUnoCard(0) # Wild clubs
        gameState = UnoGameState()

        # Is placeable on top of miss-matching suit.
        topCard = Card(alt="KD")
        self.assertTrue(card.isPlaceableOnTop(topCard))

        # Is placeable on top of miss-matching rank.
        topCard = Card(alt="3C")
        self.assertTrue(card.isPlaceableOnTop(topCard))

        # Is placeable on top of matching suit and rank.
        topCard = Card(alt="KC")
        self.assertTrue(card.isPlaceableOnTop(topCard))


class TestRankThenSuitAiPlayer(unittest.TestCase):
    """
    Tests for the a5_player.RankThenSuitAiPlayer.
    """

    def test_suggestACard(self):
        """
        Tests the suggestACard method of RankThenSuitAiPlayer.
        """
        p = player.RankThenSuitAiPlayer("Test Player")
        c_8ofDiamonds = unocard.UnoCard(1, 8)
        c_7ofHearts = unocard.UnoCard(2, 7)
        c_KofDiamonds = unocard.WildUnoCard(1)
        c_AofDiamonds = unocard.WildDrawFourActionCard(1)
        p.setStartingHand([c_8ofDiamonds, c_7ofHearts])

        # Tests than any card is suggested when there is none in the pile.
        card = p.suggestACard(None, 5)
        self.assertTrue(card != None)
        self.assertEqual(2, len(p.hand)) # Card should not have been removed.

        # This matches two cards, but should favor the matching rank.
        topCard = Card(alt="7D") # 7 of Diamonds
        card = p.suggestACard(topCard, 5)
        self.assertEqual(c_7ofHearts, card) # Should be 7 of Hearts
        self.assertEqual(2, len(p.hand)) # Card should not have been removed.

        # This matches three cards, but should favor one non-wild.
        p.setStartingHand([c_KofDiamonds, c_AofDiamonds, c_8ofDiamonds, c_7ofHearts])
        topCard = Card(alt="5D") # 5 of Diamonds
        card = p.suggestACard(topCard, 5)
        self.assertEqual(c_8ofDiamonds, card) # Should be 8 of Diamonds
        self.assertEqual(4, len(p.hand)) # Card should not have been removed.

        # This matches only the wild card.
        p.setStartingHand([c_8ofDiamonds, c_KofDiamonds, c_7ofHearts])
        topCard = Card(alt="2C") # 2 of Clubs
        card = p.suggestACard(topCard, 5)
        self.assertEqual(c_KofDiamonds, card) # Should be K of Diamonds
        self.assertEqual(3, len(p.hand)) # Card should not have been removed.

        # This matches only the wild draw four card.
        p.setStartingHand([c_8ofDiamonds, c_AofDiamonds, c_7ofHearts])
        topCard = Card(alt="2C") # 2 of Clubs
        card = p.suggestACard(topCard, 5)
        self.assertEqual(c_AofDiamonds, card) # Should be A of Diamonds
        self.assertEqual(3, len(p.hand)) # Card should not have been removed.

        # This matches nothing, but some card should be suggested.
        p.setStartingHand([c_8ofDiamonds, c_7ofHearts])
        topCard = Card(alt="2C") # 2 of Clubs
        card = p.suggestACard(topCard, 5)
        self.assertTrue(card != None)
        self.assertEqual(2, len(p.hand)) # Card should not have been removed.


class TestUno(unittest.TestCase):
    """
    Tests for the a5_uno.Uno class and the main game logic inside.
    """

    def test_drawHand(self):
        """
        Tests for drawing hands from full to empty decks.
        """
        u = uno.Uno([player.RandomAiPlayer("Player A"),
                     player.RandomAiPlayer("Player B"),
                     player.RandomAiPlayer("Player C")])

        self.assertEqual(5, uno.Uno.STARTING_HAND_SIZE)
        startDeckLen = len(u.deck)
        self.assertTrue(startDeckLen > 5)

        # Check 5 cards are drawn and removed from deck
        hand = u._drawHand()
        self.assertEqual(5, len(hand))
        for c in hand:
            self.assertTrue(isinstance(c, unocard.UnoCard))
        self.assertEqual(startDeckLen - 5, len(u.deck))

        # Check only 3 cards are drawn when deck only contains 3.
        u.deck = hand[:3]
        hand = u._drawHand()
        self.assertEqual(3, len(hand))
        self.assertEqual(0, len(u.deck))

        # Check hand contains zero cards when deck is empty.
        u.deck = []
        hand = u._drawHand()
        self.assertEqual(0, len(hand))
        self.assertEqual(0, len(u.deck))

    def test_play_normalRounds(self):
        """
        Tests for the play method in a normal game that last 4 rounds.
        """
        pa = player.RandomAiPlayer("Player A")
        pb = player.RandomAiPlayer("Player B")
        pc = player.RandomAiPlayer("Player C")

        u = uno.Uno([pa, pb, pc])
        pa.hand = [unocard.UnoCard(1, 7), unocard.UnoCard(1, 7)] # 7 of Diamonds
        pb.hand = [unocard.UnoCard(1, 8), unocard.UnoCard(1, 8)] # 8 of Diamonds
        pc.hand = [unocard.UnoCard(1, 9), unocard.UnoCard(1, 9)] # 9 of Diamonds
        u.play()

        # This game should have resulted in 4 cards played, in order:
        self.assertEqual(4, len(u.pile))
        self.assertEqual(7, u.pile[0].rank)
        self.assertEqual(8, u.pile[1].rank)
        self.assertEqual(9, u.pile[2].rank)
        self.assertEqual(7, u.pile[3].rank)

    def test_play_reversed(self):
        """
        Tests for a game which reverses the order into negative numbers.
        """
        pa = player.RandomAiPlayer("Player A")
        pb = player.RandomAiPlayer("Player B")
        pc = player.RandomAiPlayer("Player C")

        u = uno.Uno([pa, pb, pc])
        pa.hand = [unocard.UnoCard(1, 7), unocard.UnoCard(1, 7), unocard.UnoCard(1, 7)] # 7 of Diamonds
        pb.hand = [unocard.ReverseActionCard(1), unocard.ReverseActionCard(1)] # 10 of Diamonds
        pc.hand = [unocard.UnoCard(1, 9), unocard.UnoCard(1, 9)] # 9 of Diamonds
        u.play()

        # This game should have resulted in 5 cards played, in order:
        self.assertEqual(5, len(u.pile))
        self.assertEqual(7, u.pile[0].rank)
        self.assertEqual(10, u.pile[1].rank)
        self.assertEqual(7, u.pile[2].rank)
        self.assertEqual(9, u.pile[3].rank)
        self.assertEqual(10, u.pile[4].rank)

    def test_play_drawExtraCards(self):
        """
        Tests for a game where a player has to draw extra cards.
        """
        pa = player.RandomAiPlayer("Player A")
        pb = player.RandomAiPlayer("Player B")
        pc = player.RandomAiPlayer("Player C")

        u = uno.Uno([pa, pb, pc])
        pa.hand = [unocard.UnoCard(1, 7)] # 7 of Diamonds
        pb.hand = [unocard.DrawTwoActionCard(1), unocard.DrawTwoActionCard(1)] # Q of Diamonds
        pc.hand = [unocard.UnoCard(1, 9), unocard.UnoCard(1, 9)] # 9 of Diamonds

        # The deck will start with certain cards meant to be drawn by certain players.
        u.deck[0] = unocard.UnoCard(1, 7)
        u.deck[1] = unocard.UnoCard(1, 7)
        u.deck[2] = unocard.UnoCard(1, 7)
        u.deck[3] = unocard.UnoCard(1, 7)
        u.deck[4] = unocard.UnoCard(1, 9)
        u.deck[5] = unocard.UnoCard(1, 9)
        u.deck[6] = unocard.UnoCard(0, 2) # 2 of Clubs should not be drawn

        u.gameState.numExtraCardDraw = 4 # Start with drawing 4 cards.
        u.play()

        # This game should have resulted in 5 cards played, in order:
        self.assertEqual(5, len(u.pile))
        self.assertEqual(7, u.pile[0].rank)
        self.assertEqual(12, u.pile[1].rank)
        self.assertEqual(9, u.pile[2].rank)
        self.assertEqual(7, u.pile[3].rank)
        self.assertEqual(12, u.pile[4].rank)

        # Top card of deck should be 2 of clubs.
        self.assertEqual(2, u.deck[0].rank)

        # Player A and C should both end with 3 cards.
        self.assertEqual(3, len(pa.hand))
        self.assertEqual(3, len(pc.hand))




"""
This sets up and runs all the test functions for Uno.
"""
if __name__ == '__main__':

    # Suppress print statements made within the Uno game.
    original_stdout = sys.stdout
    #sys.stdout = None # Comment out this line to allow print statements.

    try:
        unittest.main(verbosity=2)
    finally:
        # Restore standard out even if tests fail.
        sys.stdout = original_stdout
