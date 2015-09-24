#!/usr/bin/python

import urllib2
import json
import random
import sys


BASE_URL = 'http://lcboapi.com'
STORE_ID = 511
ACCESS_KEY = 'MDozNmE3MTlhYy01ZTcxLTExZTUtYWY4NC1jNzg2ZmY0MDQ2YzY6Y043aHpoamdUZk1uR0JYUmhTZ1VBeWF0TFdBRUtnQTdQZUJ0'


class BeerSnob():
	def __init__(self, filename):
		global BASE_URL
		global STORE_ID
		global ACCESS_KEY
		
		self.storeId = STORE_ID
		self.baseUrl = BASE_URL
		self.accessKey = ACCESS_KEY
		self.beers = {}
		self.availableBeers = []
		self.selectedBeers = []

		self.loadFromFile(filename)
		self.populateAvailableBeers()


	def loadFromFile(self, filename):
		try:
			with open(filename, 'r') as f:
				self.beers = json.load(f)
		except IOError as e:
			# file does not exist
			# fetch data from LCBO API
			self.getBeerProductIds()
			self.saveToFile(filename)
		except Exception as e:
			raise e

	def saveToFile(self, filename):
		try:
			with open(filename, 'w') as f:
				json.dump(self.beers, f, indent=4)
		except Exception as e:
			raise e


	def storeProductIdsFromJson(self, data):
		for product in data['result']:
			if product['primary_category'] == "Beer" and \
			   product["inventory_count"] > 0:
				self.beers[product['id']] = {'name': product['name']}

	
	def getBeerProductIds(self):
		MAX_PER_PAGE = 100

		url = self.baseUrl + '/products?store_id=' + str(self.storeId) + '&per_page=' + str(MAX_PER_PAGE)

		req = urllib2.Request(url)
		req.add_header('Authorization', 'Token ' + self.accessKey)

		data = json.load(urllib2.urlopen(req))

		self.storeProductIdsFromJson(data)

		pager_data = data['pager']
		while not pager_data['is_final_page']:
			next_page = pager_data['next_page']
			paged_url = url + "&page=" + str(next_page)

			req = urllib2.Request(paged_url)
			req.add_header('Authorization', 'Token ' + self.accessKey)

			data = json.load(urllib2.urlopen(req))
			pager_data = data['pager']

			self.storeProductIdsFromJson(data)

		# sort the ids
		#self.beers.sort(key=lambda x: x['id'])


	def populateAvailableBeers(self):
		for beer in self.beers:
			self.availableBeers.append(beer)


	def randomlySelectBeer(self):
		if len(self.availableBeers) > 0:
			idx = random.randint(0, len(self.availableBeers)-1)

			product_id = self.availableBeers[idx]

			self.selectedBeers.append(product_id)

			self.availableBeers.remove(product_id)

			return self.beers[product_id]['name']
		
		return None





if __name__ == '__main__':
	module = BeerSnob("beers.json")

	while len(module.availableBeers) > 0:
		beer = module.randomlySelectBeer()

		print "selected " + str(beer)




