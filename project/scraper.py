import os
import csv
import requests
from bs4 import BeautifulSoup


def latest_news_update(page):
    """
    Latest news article on website.

    Parameters:
        page : bs4.BeautifulSoup

    Returns:
        lastestNewsUpdate : str, str
            latest title and link of updated news
    """
    dax_latest = page.find(id='dax-latest-index-update')
    if dax_latest is not None:
        dax_table = dax_latest.find(id='categorieId')   
        if dax_table is not None:
            href_tag = dax_table.find(href=True)
            if href_tag is not None:
                link = href_tag['href']
                title = href_tag.text
            else:
                print('Not tags found.\n')
        else:
            print('No table body found.\n')
    else:
        print('No update table found.\n')    
    return title, link


def run_news_scrape(url, headers=None):
    """
    Get more recent news data.

    Parameters:
        url : str

        headers : dict, optional

    Returns:
        run_scrape : dict
            Dictionary of latest title and article link
    """
    with requests.Session() as s:
        if headers is not None:
            r = s.get(url, headers=headers)
        else:
            r = s.get(url)
        page = BeautifulSoup(r.content, 'html.parser')
        l_title, l_link = latest_news_update(page)
        l_link = l_link.replace(' ', '%20')
    news_data = {'title': l_title, 'link': l_link}
    return news_data
   
 
def initial_scrape(url, headers={'Accept-Language': 'en-US,en;q=0.9'}):
    """
    First web scrape on url to compare future runs.

    Parameters:
        url : str

        headers : dict, optional

    Returns:
        initial_scrape : 
            Write most recent news update to disk in data path. 

    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir_path = dir_path + '\\data'
    f_path = data_dir_path + '\\last_index_update.csv'
    news_data = run_news_scrape(url, headers)
    fieldnames = ['title', 'link']
    if os.path.isdir(data_dir_path):  
        if not os.listdir(data_dir_path):
            print(f'Fetching initial scrape to {data_dir_path}')
            with open(f_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(news_data)
        else:
            print('Initial scrape unsuccesful. Directory is not empty')
    else:
        print('Creating given directory.')
        os.mkdir(data_dir_path)
        with open(f_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(news_data)


def update_scrape(url, headers={'Accept-Language': 'en-US,en;q=0.9'}):
    """
    Update file with latest news update.

    Parameters:
    
        url : str
        
        headers : dict
    
    Returns:
        update_scrape :
            write new updates to stored file.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir_path = dir_path + '\\data'
    f_path = data_dir_path + '\\last_index_update.csv'
    news_data = run_news_scrape(url, headers)
    fieldnames = ['title', 'link']
    if os.path.isdir(data_dir_path):    
        if not os.listdir(data_dir_path):
            print('\nDirectory is empty')
        else:
            with open(f_path, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow(news_data)
    else:
        print('\nGiven directory does not exist')

