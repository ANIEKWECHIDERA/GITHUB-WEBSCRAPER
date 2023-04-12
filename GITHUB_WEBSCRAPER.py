#This code scrapes information about various topics on GitHub, including the titles, descriptions, and URLs of those topics, and then scrapes information about repositories for each topic.
#first i imported the required libraries for the project
from bs4 import BeautifulSoup
import requests, os
import pandas as pd

topic_url = "https://github.com/topics"
#then i started defining functions to scrape my reqired information from the prsed HTML
def get_topic_titles(html_doc):
    topic_name_class = "f3 lh-condensed mb-0 mt-1 Link--primary"
    name = html_doc.find_all("p", class_=topic_name_class)
    topic_titles = []  
    for topic in name:
        topic_titles.append(topic.text)
    return topic_titles

def get_topic_desc(html_doc):
    topic_desc_class = "f5 color-fg-muted mb-0 mt-1"
    desc  = html_doc.find_all("p", class_=topic_desc_class)
    topic_descs = []  
    for topic in desc:
        topic_descs.append(topic.text.strip())
    return topic_descs

def get_topic_url(html_doc):
    url_pre =  "https://github.com" 
    topic_url_class = "no-underline flex-grow-0"
    link = html_doc.find_all("a", class_=topic_url_class)
    topic_urls = []  
    for topic in link:
        topicurl = url_pre + topic['href']
        topic_urls.append(topicurl)
    return topic_urls
        
def get_topics(topic_url): 
    source = requests.get(topic_url)
    if source.status_code < 200 or source.status_code >= 300:
        raise Exception('failed to open page {}'.format(topic_url))
    html_doc = BeautifulSoup(source.text,'html.parser')
    topic_dict = {
        'TOPIC TITLE': get_topic_titles(html_doc),
        'TOPIC DESC' : get_topic_desc(html_doc),
        'TOPIC URLS' : get_topic_url(html_doc)
}
    return pd.DataFrame(topic_dict)
topic_df = get_topics(topic_url)


def stars_count_int(stars_str):
    stars_str = stars_str.strip()
    if stars_str[-1] == 'k':
        return int(float(stars_str[:-1]) * 1000)
    return int(stars_str)

def topic_page_raw(topic_url):
    response = requests.get(topic_url)
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception('failed to open page {}'.format(topic_url))
    topic_doc = BeautifulSoup(response.text, 'html.parser')
    return topic_doc

def topic_repo(topic_doc):
    repo_name_class = 'f3 color-fg-muted text-normal lh-condensed'
    h3 = topic_doc.find_all('h3', class_ = repo_name_class)
    star_count_class = 'Counter js-social-count'
    star_tags = topic_doc.find_all('span', star_count_class)
    return h3, star_tags

def get_repo_info(h3_obj, star_tags):
    url_pre =  "https://github.com" 
    h3_tags = h3_obj.find_all('a')
    user_name = h3_tags[0].text.strip()
    repo_name = h3_tags[1].text.strip()
    repo_url = url_pre + h3_tags[1]['href']
    stars = stars_count_int(star_tags.text.strip())
    
    repo_dict = {
        'username':user_name,
        'repo_name': repo_name,
        'stars': stars,
        'repo_url': repo_url
}
    return repo_dict
    
def get_all_repo_info(topic_url):
    topic_doc = topic_page_raw(topic_url)
    h3_tags, star_tags = topic_repo(topic_doc)

    repo_list = []
    for i in range(len(h3_tags)):
        repo_dict = get_repo_info(h3_tags[i], star_tags[i])
        repo_list.append(repo_dict)

    repo_df = pd.DataFrame(repo_list)
    return repo_df
 

def scrape_topic(topic_url, topic_name):
    file_path = r'C:\Users\chide\Documents\Web Scrape projexts\\'
    file_name = topic_name + '.xlsx'
    if os.path.exists(file_path + file_name):
        print('{} already exists!'.format(file_name))
        return
    repo = get_all_repo_info(topic_url)
    topic_repo_df = pd.DataFrame(repo)
    topic_repo_df.to_excel(file_path + file_name, sheet_name= topic_name , index=True)
    return topic_repo_df
 

def scrape_all():
    print('scraping topic list !')
    topic_df = get_topics(topic_url)
    for index, row in topic_df.iterrows():
        print('scraping repositories from "{}"'.format(row['TOPIC URLS'])) 
        scrape_topic(row['TOPIC URLS'], row['TOPIC TITLE'])

print(scrape_all())   

   


