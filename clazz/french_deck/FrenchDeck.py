import collections
from random import choice

Card = collections.namedtuple('Card', ['rank', 'suits'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self.cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, action):
        return self.cards[action]


if __name__ == '__main__':
    beer_card = Card('7', 'diamonds')
    print(beer_card)
    deck = FrenchDeck()
    print('长度', len(deck))
    print('第一个元素', deck[0])
    print('随机元素', choice(deck))
    print('牌面数值', [rank for rank in FrenchDeck.ranks])
    print('牌面类型', [suit for suit in FrenchDeck.suits])
    print('slice 操作', deck[:3])
    print(deck[12::13])
    print(deck[-2:1])
    print(deck[2:1])
