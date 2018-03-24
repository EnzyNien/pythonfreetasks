import re
from collections import Counter
import random 

#1
class FindEntryPerc():

	def calcWords(self, text, cmp):
		returnlist = []
		result = self.pattern.findall(text)
		for i in result:
			returnlist += [j.lower() for j in list(i)]
		len_ = len(returnlist)
		resultdict = Counter(returnlist)
		return resultdict.get(cmp,0)/len_*100
			

	def Find(self):
		if self.filename is None:
			raise ValueError('filename error')
			return
		with open(self.filename, 'r') as f:
			C = f.readline().replace('\n','').lower()
			rows = [(idx,self.calcWords(row,C)) for idx, row in enumerate(f)]
			rows = sorted(list(filter(lambda x: x[1] > 0, rows)),key=lambda x:x[0])

		if rows:
			print(round(rows[0][1],0),rows[0][0])
		else:
			print('Nothing found')

	def __init__(self, filename=None):
		self.filename = filename
		self.pattern = re.compile('\w+')

#2
class Blackjack():

	class Deck():
		def __init__(self):
			ranks = "23456789TJQKA"
			suits = "DCHS"
			self.cards = [Blackjack.Card(r,s) for r in ranks for s in suits]
			random.shuffle(self.cards)

		def deal_card(self):
			return self.cards.pop()

	class Card():

		def card_value(self):
			if self.rank in "TJQK":
				return 10
			else:
				return " A23456789".index(self.rank)

		def get_rank(self):
			return self.rank
		def __init__(self, rank, suit):
			self.rank = rank
			self.suit = suit

		def __str__(self):
			return "{}{}".format(self.rank, self.suit)

	class Hand():
		def add_card(self, card):
			self.cards.append(card)

		def get_value(self):
			result = 0
			aces = 0
			for card in self.cards:
				result += card.card_value()
				if card.get_rank() == "A":
					aces += 1
			if result + aces * 10 <= 21:
				result += aces * 10
			return result

		def __str__(self):
			text = "{}'s contains:\n".format(self.name)
			for card in self.cards:
				text += str(card) + " "
			text += "\nHand value: " + str(self.get_value())
			return text
		def __init__(self, name):
			self.name = name
			self.cards = []

	def new_game(self):
		d = self.Deck()
		player_hand = self.Hand("Player")
		dealer_hand = self.Hand("Dealer")

		player_hand.add_card(d.deal_card())
		player_hand.add_card(d.deal_card())

		dealer_hand.add_card(d.deal_card())
		print(dealer_hand)
		print("=" * 20)
		print(player_hand)

		in_game = True

		while player_hand.get_value() < 21:
			ans = input("Hit or stand? (h/s) ")
			if ans == "h":
				player_hand.add_card(d.deal_card())
				print(player_hand)

				if player_hand.get_value() > 21:
					print("You lose")
					in_game = False
			else:
				print("You stand!")
				break
		print("=" * 20)
		if in_game:
			# По правилам дилер обязан набирать карты пока его счет меньше 17
			while dealer_hand.get_value() < 17:
				dealer_hand.add_card(d.deal_card())
				print(dealer_hand)
				if dealer_hand.get_value() > 21:
					print("Dealer bust")
					in_game = False
		if in_game:
			if player_hand.get_value() > dealer_hand.get_value():
				print("You win")
			else:
				print("Dealer win")

#FindEntryPerc('sometext.txt').Find()
#Blackjack().new_game()
