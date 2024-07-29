import requests
import pandas as pd
from bs4 import BeautifulSoup
from colorama import Fore
from unidecode import unidecode
import time
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import psycopg2

page_website = 'https://quotes.toscrape.com/page/'
about_website = 'https://quotes.toscrape.com/author/'

load_dotenv()

USERNAME = os.getenv('USERNAME')
PWD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')

# ------------------------- DATABASE CONNECTION
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=DATABASE,
            user=USERNAME,
            password=PWD,
            host=HOST,
            port=PORT
        )
        print(f"{Fore.CYAN}🎉Successfully connected to DB🎉{Fore.RESET}")
        conn.close()
    except Exception as e:
        print(f"{Fore.RED}Connection failed due to: {e}{Fore.RESET}")

# ------------------------- AUTHOR DETAILS
def get_author_details(author_url):
    url = f'{about_website}{author_url}'
    print(f"{Fore.GREEN}Fetching page for author: {url}{Fore.RESET}")
    
    response = requests.get(url)
    
    if response.status_code == 404:
        print(f"Page for {author_url} not found (404). Skipping.")
        return None  
    elif response.status_code != 200:
        print(f"Error fetching page for {author_url}. Status code: {response.status_code}. Skipping.")
        return None  

    soup = BeautifulSoup(response.text, 'html.parser')
    
    author_details_div = soup.find('div', {'class': 'author-details'})
    if not author_details_div:
        print(f"{Fore.YELLOW}No author details found for {author_url}. Skipping.{Fore.RESET}")
        return None

    author_name = author_details_div.find('h3', {'class': 'author-title'})
    author_born_date = author_details_div.find('span', {'class': 'author-born-date'})
    author_born_location = author_details_div.find('span', {'class': 'author-born-location'})
    author_description = author_details_div.find('div', {'class': 'author-description'})

    # check for None and provide default values
    author_info = {
        'author': author_name.text.strip() if author_name else 'Unknown',
        'born_date': author_born_date.text.strip() if author_born_date else 'Unknown',
        'born_location': author_born_location.text.strip() if author_born_location else 'Unknown',
        'description': author_description.text.strip() if author_description else 'No description'
    }

    return author_info


# ------------------------- TOTAL DATA SCRAPING
def page_scraping():
    quote_data = []
    page_number = 1
    while True:
        website = f'{page_website}{page_number}'
        print(f"{Fore.MAGENTA}Downloading page {page_number}: {website}{Fore.RESET}")
        
        try:
            response = requests.get(website)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"{Fore.RED}Error: {e}{Fore.RESET}")
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes_divs = soup.findAll('div', class_='quote')
        
        if not quotes_divs:
            print(f"{Fore.YELLOW}No more data found. Exiting.{Fore.RESET}")
            break
        
        for div in quotes_divs:
            quote = div.find('span', class_='text').text.strip()
            author = div.find('small', class_='author').text.strip()
            tags = [tag.text for tag in div.findAll('a', class_='tag')]

            author_url = unidecode(author)
            author_url = author_url.replace(' ', '-').replace('.', '-').replace('--', '-').replace("'", '').rstrip('-')

            author_details = get_author_details(author_url)
            if not author_details:
                continue
            
            dictionary= {
                'quote': quote, 
                'author': author, 
                'tags': ', '.join(tags),
                'born_date': author_details['born_date'],
                'born_location': author_details['born_location'],
                'description': author_details['description']
            }
            quote_data.append(dictionary)
        
        page_number += 1
        # time.sleep(2)

    df = pd.DataFrame(quote_data)
    return df

# ------------------------- SAVE DATA IN DATABASE
def save_to_db(df):
    connection_string = f'postgresql://{USERNAME}:{PWD}@{HOST}:{PORT}/{DATABASE}'
    engine = create_engine(connection_string)
    table_name = 'all_quotes_data'
    
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"{Fore.CYAN}DataFrame sent to the table {table_name} in the database {DATABASE}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Error sending DataFrame to the database: {e}{Fore.RESET}")

if __name__ == "__main__":
    connect_to_db()
    df_final = page_scraping()
    save_to_db(df_final)
