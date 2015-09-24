import random
import string

import cherrypy
from myserver import BeerSnob

class BeerSelection(object):
    def __init__(self):
        self.count = 0
        self.selectedBeers = []
        self.module = BeerSnob("beers.json")

    def generateHtml(self):
        html = """ \
          <html> \
          <head></head> \
          <body> \
            <form method="put" action="selectBeer"> \
              <button type="submit">Select a beer</button> \
            </form>"""

        for beer in self.selectedBeers:
          html += beer + "<br>"
        
        html += " \
        </body> \
        </html>"

        return html

    @cherrypy.expose
    def index(self):
        return self.generateHtml()

    @cherrypy.expose
    def selectBeer(self):
        beer = self.module.randomlySelectBeer()

        if beer:
            self.selectedBeers.append(beer)

        return self.generateHtml()


if __name__ == '__main__':
    cherrypy.quickstart(BeerSelection())
