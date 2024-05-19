import requests
from bs4 import BeautifulSoup

url = "https://www.genesisptwellness.com/contact"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')
cf_email = soup.find('span',{'class':'__cf_email__'})
cf_mail = cf_email.get('data-cfemail')


def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email

cfDecodeEmail(cf_mail)







