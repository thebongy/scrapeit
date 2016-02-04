Symbol = str          # A Scheme Symbol is implemented as a Python str
List   = list         # A Scheme List is implemented as a Python list
Number = (int, float) # A Scheme Number is implemented as a Python int or float\
Env = dict

class DOMParser:
	def __init__(self,parse,parent):
		self.parser = parse
		self.parsed = ""
		self.data = []
		if parent.__class__.__name__ == "URL":
			self.parent = parent
		else:
			raise ValueError("Parent of Parser Object should be valid URL.")
	def parse(self,attr="default", strict=True):
		from bs4 import BeautifulSoup
		import urlparse
		if self.parsed == "":
		  soup = BeautifulSoup(self.parent.getsource())
		  self.parsed = soup.select(self.parser)
		if attr == "default":
		  return self.parsed
		elif attr == "text":
		  return [parse.getText() for parse in self.parsed]
		else:
		  for parse in self.parsed:
		    try:
		      self.data.append(parse[attr])
		    except KeyError:
		      if strict:
		        raise ValueError("[FATAL] Attribute " + str(attr) + " not found in data: " + str(parse))
		      else:
		        print "[IGNORE] Attribute " + str(attr) + " not found in data: " + str(parse)
		  return self.data
		
class URL:
	def __init__(self,url):
		self.url = url
		self.source = ""
	def getsource(self):
		import requests
		if self.source == "":
			self.source = requests.get(self.url).text.encode('utf-8')
		return self.source

def run(cfile):
	for line in open(cfile).readlines():
		print parse(line)
		print eval(parse(line))

def tokenize(char):
	return char.split()

def parse(code):
	i = 0
	# Count number of tabs.
	if code[0] == "\t":
		while code[i] == "\t":
			i += 1
	# Set parser ahead of tabs
	j = i
	# Check for url parsers
	if code[j] == "(":
		try:
			while code[j] != ")":
				j += 1
		except IndexError:
			raise SyntaxError(") expected after (")
		return [i,code[i:j+1]]
	if len(tokenize(code)) == 1:
		return [i,tokenize(code)[0]]
	else:
		return [i,tokenize(code)]

def atom(token):
	"Numbers become numbers; every other token is a symbol."
	try: return int(token)
	except ValueError:
	    try: return float(token)
	    except ValueError:
	        return Symbol(token)

def environment():
	envir = Env()
	envir.update({
		"levels":{}
		})
	return envir

global_env = environment()

def eval(x,env=global_env):
	if x[1][:4] == "http":
		env["levels"].update({x[0]:URL(x[1])})
	elif x[1][0] == "(":
		try:
			x[1] = x[1].replace("(","")
			x[1] = x[1].replace(")","")
			env["levels"].update({x[0]:DOMParser(x[1],env["levels"][x[0]-1])})
		except KeyError:
			raise ValueError("Parser expects URL declaration.")
	elif x[1][0] == "store":
	  if x[1].count("in") == 0:
	    raise SyntaxError("'in' expected for store statement")
	  if env["levels"][x[0]-1].__class__.__name__ == "DOMParser":
	    env.update({x[1][3]:env["levels"][x[0]-1].parse(x[1][1].replace("*","").replace(".",""),x[1][1].endswith("*"))})
	  elif env["levels"][x[0]-1].__class__.__name__ == "URL":
	     env.update({x[1][3]:DOMParser("html",env["levels"][x[0]-1]).parse(x[1][1].replace("*","").replace(".",""),x[1][1].endswith("*"))})
	return env
run("pokemonscraper.scrape")