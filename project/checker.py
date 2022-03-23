import os
import argparse
import csv
import smtplib
import sched, time

from translate import Translator

from scraper import run_news_scrape, update_scrape, initial_scrape


def prev_state():
    """
    Previous state of webpage
    
    Returns:
        prev_state : list
            Last news update entry recorded
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir_path = dir_path + '\\data' 
    
    if os.path.isdir(data_dir_path):
        
        f_path = data_dir_path + '\\last_index_update.csv'

        if not os.listdir(data_dir_path):
            print('\nDirectory is empty')

        else:
            data = []
            with open(f_path, mode='r', encoding='utf-8' ) as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    if row: 
                        data.append(row) 
            return data[-1]

    else:
        print('\nGiven directory does not exist')

def check_state(url):
    """Check webpage status
    
    Parameters:
        url : str
        
    Returns:
        check_state : None or dict
            If there is a difference in state a dict is returned.
            Otherwise None.
    """
    
    # read in the last news update from data directory
    # this contains the last headline from the site
    prev_data = prev_state()

    latest_data = run_news_scrape(url)

    # fetch last headline which can either be
    # the same headline, no email is needed
    plink = prev_data[-1]
    nlink = latest_data['link']
    
    if plink == nlink:
        return None
    else:
        # a different headline, email is needed 
        return latest_data

def email_messanger(username, password, news_data, recpients):
    """
    Notifiy receipent of news update
    
    Parameters:
        username : str

        password : str

        news_data : dict

        recpients : list

    Returns:
        email_messanger : 
            Sends news alert update to recipients.
        
    """

    gmail_user = username
    gmail_password = password

    sent_from = gmail_user
    subject = 'Subject: Alert - dax index update'

    translator = Translator(from_lang='german', to_lang='english')

    news_title = translator.translate(news_data['title'])
    news_link = news_data['link']

    email_text = u'\n'.join((subject, news_title, news_link)).encode('utf-8').strip()

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, recpients, email_text)
        server.close()

        print ('\nEmail sent!')
    except Exception as e:
        print(e)
        print ('\nSomething went wrong...')
    

scheduler = sched.scheduler(time.time, time.sleep)
  
def run_alert(sender, password, receivers):
    """
    Run alert checking process

    Parameters:

        sender : str

        password : str

        receivers : str

        time_delay : int
    
    Returns:
        run_alert:
            Alert checking process on webpage.
    """
    
    url = 'https://www.dax-indices.com/news'
    
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir_path = dir_path + '\\data'
    
    if os.path.isdir(data_dir_path):

        if not os.listdir(data_dir_path):
            print(f'Populating folder with initial data.\n')
            initial_scrape(url)
    else:
        print(f'Directory not found. Creating and retrieving data.\n')
        os.mkdir(data_dir_path)
        initial_scrape(url)

    
    site_state = check_state(url)

    if site_state is not None:
        print('\nNew update.')
        email_messanger(sender, password, site_state, receivers)
        update_scrape(url)
    else:
        print('\nNo update.')



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Alert Messanger for dax-index')
    parser.add_argument('email', help='email address for sender of email alert',
                        type=str)
    parser.add_argument('password', help='password for sender email login',
                        type=str)
    parser.add_argument('recepients', nargs='+', help='list of people receiving the update alert',
                        type=list)
    parser.add_argument('delay', help='second delay between successive runs of process',
                        type=int)
    
    args = parser.parse_args()
    
    
    print('Start Event: ')
    # set to True to run forever
    attempts = 0
    while attempts < 15:

        scheduler.enter(args.delay, 1, run_alert(args.email, args.password, args.recepients))
        attempts += 1

    