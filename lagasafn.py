import requests
from bs4 import BeautifulSoup
import os

ALTHINGI_BASE: str = 'https://www.althingi.is/'
LAGALISTI_URL: str = 'https://www.althingi.is/lagasafn/' 

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
	if not os.path.exists('data'):
		os.mkdir('data')
	
	# Get list of laws
	lagalisti = get_lagalisti()

	# Downloads every law in Iceland
	for l in lagalisti:
		print(l)
		try:
			# Use os.path.join to make it Windows friendly
			file_name = os.path.join('data', l['name'] + '.txt')
			with open(file_name, 'w') as file:
				text = get_law_text(l['url'])
				file.write(text)
		except:
			print('failed')

# If we run this file directly, then we update laws data
# If imported to another file, then it will not run automatically
if __name__ == '__main__':
	update_laws_data()