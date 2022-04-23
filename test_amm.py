import math
import numpy as np

class AMM:
	def __init__(self, initial_funding):
		self.invariant = None
		self.inventory = {
			"YES":0,
			"NO":0
		}
		self.pool_size = {
			"YES":0,
			"NO":0
		}
		self.mint(initial_funding)

	def mint(self, token):
		for obj in [self.inventory, self.pool_size]:
			obj["YES"] += token
			obj["NO"] += token

		if self.invariant is None:
			self.invariant = token * token

	def buy_yes_token(self, amount):
		self.mint(amount)
		NEW_INVARIANT = self.get_invariant()
		payout = self.inventory["YES"] * (1 - (self.invariant / (NEW_INVARIANT)))
		self.inventory["YES"] -= payout

		assert np.isclose(self.get_invariant(), self.invariant)

		return payout

	def buy_no_token(self, amount):
		self.mint(amount)
		NEW_INVARIANT = self.get_invariant()
		payout = self.inventory["NO"] * (1 - (self.invariant / (NEW_INVARIANT)))
		self.inventory["NO"] -= payout

		assert np.isclose(self.get_invariant(), self.invariant)

		return payout

	def odds(self, token):
		assert token in self.inventory
		odds_weight = math.prod(
			self.inventory[i] for i in self._get_all_other_tokens(token)
		)
		sum_inventory = sum([
			self.inventory[i] for i in self.inventory
		])
		return odds_weight / sum_inventory

	def get_withdraw_amount(self, winning_token):
		percentage = self.odds(winning_token)
		pool_size = sum(
			 self.pool_size[i] for i in	self._get_all_other_tokens(winning_token)
		)
		withdraw = pool_size * percentage

		return withdraw

	def _get_all_other_tokens(self, token):
		return [
			i for i in self.inventory if i != token
		]

	def get_invariant(self):
		return self.inventory["YES"] * self.inventory["NO"]

if __name__ == '__main__':
	amm = AMM(initial_funding=100)
	amm.buy_yes_token(50)
	amm.buy_no_token(20)

	print(amm.pool_size)
	print(amm.inventory)

	print(amm.get_withdraw_amount("YES"))
	print(amm.get_withdraw_amount("NO"))


