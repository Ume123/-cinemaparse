from bs4 import BeautifulSoup
import lxml
import requests
class CinemaParser:
	def __init__(self,name):
		self.city=name
		if self.city=="Москва":
			url = 'https://msk.subscity.ru/'
		else:
			url='https://spb.subscity.ru/'
		page = requests.get(url)
		self.content  = BeautifulSoup(page.text, "html.parser")

	def print_raw_content(self):
		return self.content.prettify()

	def find(self):
		self.content.find_all('div')

a=CinemaParser('Москва')
print(a.print_raw_content())
print(a.find())
