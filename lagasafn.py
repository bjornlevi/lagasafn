import requests
from bs4 import BeautifulSoup
import os

def get_lagalisti():
	# Fetch the webpage content
	url = 'https://www.althingi.is/lagasafn/' 
	response = requests.get(url)
	html_content = response.text

	# Parse the HTML content
	soup = BeautifulSoup(html_content, 'html.parser')

	# Find the <ul> tag with id="lagalisti"
	ul_tag = soup.find('ul', id='lagalisti')

	# Extract the <li> tags from the <ul> tag
	li_tags = ul_tag.find_all('li')

	# Create a list to store the extracted data
	lagalisti = []

	# Extract the name and URL from each <li> tag
	for li_tag in li_tags:
	    a_tag = li_tag.find('a')
	    name = a_tag.text
	    url = 'https://www.althingi.is' + a_tag['href']
	    
	    # Create a dictionary and append it to the list
	    lagalisti.append({'name': name, 'url': url})

	return lagalisti

lagalisti = get_lagalisti()

def get_law_text(url):
	# Fetch the webpage content
	response = requests.get(url)
	html_content = response.text

	# Create a BeautifulSoup object and specify the parser
	soup = BeautifulSoup(html_content, 'html.parser')

	unclean_text = soup.find('div', {"class":"article box login"})

	# Find all the <p> and <br> tags and remove them
	for tag in unclean_text.find_all(['p', 'br']):
	    tag.decompose()

	# Get the remaining text
	clean_text = unclean_text.get_text().strip()
	clean_text.replace('&nbsp;', '')
	clean_text.replace('   ', '')
	

	# Print the cleaned text
	return clean_text

for l in lagalisti:
	print(l)
	try:
		file_name = 'data/'+l['name']+'.txt'
		with open(file_name, 'w') as file:
			text = get_law_text(l['url'])
			file.write(text)
	except:
		print('failed')