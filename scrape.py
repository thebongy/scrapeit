Symbol = str          # A Scheme Symbol is implemented as a Python str
List   = list         # A Scheme List is implemented as a Python list
Number = (int, float) # A Scheme Number is implemented as a Python int or float\
class ScrapeIt:
	def __init__(self,cfile):
		print self.parseit(open(cfile))
	def tokenize(self,char):
		return char.split()
	def parseit(self,code):
		return [[self.atom(token) for token in self.tokenize(line)] for line in code.readlines()]
	def atom(self,token):
	    "Numbers become numbers; every other token is a symbol."
	    try: return int(token)
	    except ValueError:
	        try: return float(token)
	        except ValueError:
	            return Symbol(token)
ScrapeIt("pokemonscraper.scrape")