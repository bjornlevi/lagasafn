import requests
from bs4 import BeautifulSoup
import os
import cache
import platform

ALTHINGI_BASE: str = 'https://www.althingi.is'
LAGALISTI_URL: str = 'https://www.althingi.is/lagasafn/' 

LAWS_PATH: list[str] = ['laws']
INFO_PATH: list[str] = ['info']

def get_lagalisti() -> list[dict[str,str]]:
	# Fetch the webpage content
	response = requests.get(LAGALISTI_URL)
	html_content = response.text

	# Parse the HTML content
	soup = BeautifulSoup(html_content, 'html.parser')

	# Find the <ul> tag with id="lagalisti"
	ul_tag = soup.find('ul', id='lagalisti')

	# Extract the <li> tags from the <ul> tag
	li_tags = ul_tag.find_all('li')

	# Create a list to store the extracted data
	lagalisti: list[dict[str,str]] = []

	# Extract the name and URL from each <li> tag
	for li_tag in li_tags:
	    a_tag = li_tag.find('a')
	    name = a_tag.text
	    url = ALTHINGI_BASE + a_tag['href']
	    
	    # Create a dictionary and append it to the list
	    lagalisti.append({'name': name, 'url': url})

	return lagalisti

def get_law_text(url: str) -> str:
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

# Update our data/ folder
def update_laws_data() -> None:
	#prepare_dir(LAWS_PATH)

	
	# Get list of laws
	lagalisti = get_lagalisti()

	# Downloads every law in Iceland
	for l in lagalisti:
		print(l)
		#try:
		# Unix-like systems do not support having charachter '/' in a filename.
		if '/' in l['name'] and platform.system().lower() != 'windows':
			l['name'] = l['name'].replace('/', ' ')

		# If filename is too long, then shorten it
		if len(bytes(l['name'], encoding='utf-8')) >= 255:
			byterow = bytes(l['name'], encoding='utf-8')
			byterow = byterow[:250] #Leave space for .txt in the end
			l['name'] = str(byterow, encoding='utf-8') 
		
		file_path = LAWS_PATH + [l['name'] + '.txt']
		law_text = get_law_text(l['url'])
		cache.save_cache(file_path, law_text)
		#except Exception as e:
		#	print('failed')

# If we run this file directly, then we update laws data
# If imported to another file, then it will not run automatically
if __name__ == '__main__':
	update_laws_data()