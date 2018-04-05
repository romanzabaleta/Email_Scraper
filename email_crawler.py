from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re
import pandas as pd

########################
########################

#Function for errors
def a_filter(a_entry,a_line):
        if a_entry in str(a_line):
                return True
        else:
                return False

########################
########################

#Input commands, sets, lists, & variables
UrL = str(input('Enter a URL:'))
edocn = input('Name of Excel Doc:')
lng = input('Number of pages to visit:')
look = input('Keyterm to avoid:')

# Queue of urls
new_urls = deque([UrL])
# URLs already crawled
processed_urls = set()
# List of emails found
emails = []

#######################
#######################

# Process URL's on Queue
for i in range(0,int(lng)):
    print(i)
    # deque: move next url from queue to processed urls set
    url = new_urls.popleft()
    processed_urls.add(url)
    # extract base url to resolve relative links
    parts = urlsplit(url)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url[:url.rfind('/')+1] if '/' in parts.path else url
    # get url's content
    print("Processing "+ str(url))
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        # ignore page errors
        continue 
    # get all email addresses and add to set
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
    print(new_emails)
    emails.append(new_emails)
    # create a beautiful soup for the html document
    soup = BeautifulSoup(response.text)
    # find and process all the anchors in the document
    for anchor in soup.find_all("a"):
        # extract link url from the anchor
        link = anchor.attrs["href"] if "href" in anchor.attrs else ''
        issue = ['.jpg', 'facebook', '.png', '.pdf', '.doc']
        # resolve relative links
        for i in range(0, len(issue)):
                if a_filter(issue[i], link) is True:
                        link = UrL
        if link.startswith('/'):
                link = base_url + link
        elif not link.startswith('http'):
                link = path + link
        # add the new url to the queue if it was not enqueued nor processed yet
        if not link in new_urls and not link in processed_urls:
                new_urls.append(link)
###########################
###########################     
email_list = pd.DataFrame(emails,processed_urls)
print(email_list)
##########################
##########################
# Convert the dataframe to an XlsxWriter Excel object.
writer = pd.ExcelWriter(str(edocn)+'.xlsx', engine='xlsxwriter')
email_list.to_excel(writer, sheet_name='Emails')
writer.save()
##########################
##########################
#End option
for i in range(0,10):
        ans = input("Type 'y' to exit:_")
        if ans is 'y':
                break
        else:
                print('Invalid input')
                continue
        
        
