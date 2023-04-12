# GITHUB-WEBSCRAPER
This code scrapes information about various topics on GitHub, including the titles, descriptions, and URLs of those topics, and then scrapes information about repositories for each topic. Here are the steps and functions involved:

Import the required libraries: BeautifulSoup, requests, os, and pandas.
Define a variable "topic_url" with the URL of the main topics page on GitHub.
Define a function "get_topic_titles" that accepts an HTML document as input, searches for all the topic titles on that page using the specified CSS class, and returns a list of those titles.
Define a function "get_topic_desc" that accepts an HTML document as input, searches for all the topic descriptions on that page using the specified CSS class, and returns a list of those descriptions.
Define a function "get_topic_url" that accepts an HTML document as input, searches for all the topic URLs on that page using the specified CSS class, and returns a list of those URLs.
Define a function "get_topics" that accepts a topic URL as input, sends a request to that URL to get the corresponding HTML page, and then calls the three functions defined above to extract the titles, descriptions, and URLs of the topics on that page. These values are stored in a dictionary and returned as a pandas dataframe.
Call the "get_topics" function with the main topic URL to get information about all the topics on GitHub.
Define a function "stars_count_int" that accepts a string representing a number of stars on a repository and converts it to an integer. If the string ends with a "k", it is treated as thousands and the value is multiplied by 1000 before conversion.
Define a function "topic_page_raw" that accepts a topic URL as input, sends a request to that URL to get the corresponding HTML page, and returns the BeautifulSoup object representing that page.
Define a function "topic_repo" that accepts a BeautifulSoup object representing a topic page as input, searches for all the repository names and star counts on that page using the specified CSS classes, and returns lists of those names and counts.
Define a function "get_repo_info" that accepts a single repository name and star count along with the corresponding BeautifulSoup object representing a topic page as input. It extracts the username, repository name, repository URL, and star count from the input and stores them in a dictionary, which is returned.
Define a function "get_all_repo_info" that accepts a topic URL as input, calls the "topic_page_raw" function to get the corresponding BeautifulSoup object, calls the "topic_repo" function to get lists of all the repository names and star counts on that page, and then calls the "get_repo_info" function for each repository to extract its information and store it in a list of dictionaries. The final list is then converted to a pandas dataframe and returned.
Define a function "scrape_topic" that accepts a topic URL and topic name as input, calls the "get_all_repo_info" function to get a dataframe of all the repositories for that topic, and then saves that dataframe to an Excel file with the topic name as the sheet name.
Define a function "scrape_all" that first calls the "get_topics" function to get information about all the topics on GitHub, and then iterates over each row in that dataframe, calling the "scrape_topic" function for each topic URL to scrape repository information and save it to an Excel file.
Call the "scrape_all" function to execute the entire scraping process.
