#import libraries for webscraping

from bs4 import BeautifulSoup
import requests,openpyxl
import pandas as pd

#variables
url = 'https://github.com/topics/3d'
repo_name_class = 'f3 color-fg-muted text-normal lh-condensed'
star_count_class = 'Counter js-social-count'
url_pre =  "https://github.com" 
#request for page html content

page = requests.get(url)
#print(page.status_code) #check for response code (200 - 299)
page_doc = BeautifulSoup(page.text, 'html.parser')

#search for information
#repository names and topics
h3 = page_doc.find_all('h3', class_ = repo_name_class)

user_name = h3[0].find_all('a')[0].text.strip()
repo_name = h3[0].find_all('a')[1].text.strip()
user_name_url = h3[0].find_all('a')[0]['href']
repo_url = url_pre + h3[0].find_all('a')[1]['href']

#repository star count

star_tags = page_doc.find_all('span', star_count_class)

star_count =star_tags[0].text.strip()
#CONVERT Stars into a number by defining a function
def stars_count_int(stars_str):
    stars_str = stars_str.strip()
    if stars_str[-1] == 'k':
        return int(float(stars_str[:-1]) * 1000)
    return int(stars_str)

#getting all information
def get_repo_info(h3_obj, star_tags):
    h3_tags = h3_obj.find_all('a')
    user_name = h3_tags[0].text.strip()
    repo_name = h3_tags[1].text.strip()
    repo_url = url_pre + h3_tags[1]['href']
    stars = stars_count_int(star_tags.text.strip())
    return user_name, repo_name, stars, repo_url
#create a dictionary
repo_dict = {
    'username':[],
    'repo_name': [],
    'stars': [],
    'repo_url': []
}

#printing the information
for a in range(len(h3)):
    repo_info = get_repo_info(h3[a], star_tags[a])
    repo_dict['username'].append(repo_info[0])
    repo_dict['repo_name'].append(repo_info[1])
    repo_dict['stars'].append(repo_info[2])
    repo_dict['repo_url'].append(repo_info[3])
#repodf = pd.DataFrame(repo_dict)
#saving the file to excel workbook
#repodf.to_excel(r'C:\Users\chide\Desktop\TOP_REPOSITORY_INFO_GITHUB.xlsx', sheet_name='TOP REPOSITORY INFO', index=True)


#parsing the code into functions
#CONVERT Stars into a number by defining a function
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


repo_df = get_all_repo_info('https://github.com/topics/ansible')
print(repo_df)







