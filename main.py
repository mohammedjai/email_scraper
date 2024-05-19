import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

file_path = r'C:/Users\pc\Desktop\fes dent.xlsx'

df = pd.read_excel(file_path, sheet_name='Feuil1')

websites = df['website'].tolist()

def get_links():
    for website in websites:
        try:
            links = f'https://www.{website}'
            r = requests.get(links, headers=headers),
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, 'html.parser')
                href_html = soup.find_all('a')
                website_links = [link.get('href') for link in href_html]
                yield (website, website_links)
              
        except Exception as e:
            print(website, e)

def get_email(args):
    website, links = args
    for link in links:
        try:
            r = requests.get(link, headers=headers, verify=True)
            soup = BeautifulSoup(r.content, 'html.parser')
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.get_text())
            
            if not emails:
                cf_email = soup.find('span', {'class': '__cf_email__'})
                if cf_email:
                    cf_mail = [mail.get('data-cfemail') for mail in cf_email]
                    decoded_email = cfDecodeEmail(cf_mail)
                    if decoded_email:
                        print(f'Website: {website}, Email: {decoded_email}')
                        return website, decoded_email

            elif emails:
                first_email = emails[0]
                print(f'Website: {website}, Email: {first_email}')
                return website, first_email

        except Exception as e:
            print(f'{website}: {e}')

def cfDecodeEmail(encodedString):
    r = int(encodedString[:2], 16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email

def process_website(website):
    try:
        email_result = get_email((website, [f'https://{website}']))
        if email_result:
            return email_result
        else:
            return website, "No Email"
    except requests.exceptions.RequestException as req_error:
        print(f'{website}: Request Error - {req_error}')
        return website, "No Email"

all_emails = []

with ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(process_website, websites)

for website, email in results:
    all_emails.append((website, email))
    df.loc[df['website'] == website, 'emails'] = email

df.to_excel(file_path, index=False, sheet_name='Feuil1')
print("All Emails:", all_emails)
