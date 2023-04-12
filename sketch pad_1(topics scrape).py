from bs4 import BeautifulSoup
import requests,openpyxl
import pandas as pd


excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'IMDB top rated movies data'
sheet.append(['TOPIC NAME', 'TOPIC DESCRIPTION', 'TOPIC URL'])


# variables
url = "https://github.com/topics"
topic_name_class = "f3 lh-condensed mb-0 mt-1 Link--primary"
topic_desc_class = "f5 color-fg-muted mb-0 mt-1"
topic_url_class = "no-underline flex-grow-0"
topic_body_class = "col-lg-9 position-relative pr-lg-5 mb-6 mr-lg-5"
url_pre =  "https://github.com" 
# extracting the data
source = requests.get(url)
#source.raise_for_status()
soup = BeautifulSoup(source.text,'html.parser')

# searching for the data

topics = soup.find("div", class_= topic_body_class).find("div")

for topic in topics:
    name = topics.find_all("p", class_=topic_name_class)
    desc  = topics.find_all("p", class_=topic_desc_class)
    link = topics.find_all("a", class_=topic_url_class)
  
topic_titles = []  
for topic in name:
   topic_titles.append(topic.text)
#print(topic_titles)

topic_descs = []  
for topic in desc:
   topic_descs.append(topic.text.strip())
#print(topic_descs)

topic_urls = []  
for topic in link:
   topicurl = url_pre + topic['href']
   topic_urls.append(topicurl)
#print(topic_urls)

topic_dict = {
    'TOPIC TITLE': topic_titles,
    'TOPIC DESC' : topic_descs,
    'TOPIC URLS' : topic_urls
}
topics_df = pd.DataFrame(topic_dict)
#print(topics_df)

topics_df.to_excel(r'C:\Users\chide\Desktop\GITHUBWEBSCRAPER.xlsx', sheet_name='GITHUB TOPICS', index=True)




print(topics_df)








