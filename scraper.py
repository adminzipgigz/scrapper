import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd

def extract(postion,location,page):
    source = 'https://in.indeed.com/jobs?q={}&l={}&start={}'
    url = source.format(postion,location,page)
    response = requests.get(url)
    print(response)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def transform(soup):
    cards = soup.find_all('div', 'job_seen_beacon')
    for item in cards:
        title = item.find('div', class_ = 'singleLineTitle').text
        company = item.find('span', class_ = 'companyName').text
        location = item.find('div', class_ ='companyLocation').text

        try:
            salary = item.find('div', class_ = 'salary-snippet').text
        except:
            salary ='Not Specified'

        job ={
            'title' : title,
            'company' : company,
            'location' : location,
            'salary' : salary
        }
        jobListing.append(job)
    return

jobListing = []
for i in range(0,40,10):
    c = extract('software engineer', 'Bengaluru',i)
    transform(c)

print(len(jobListing))

df = pd.DataFrame(jobListing)
print(df.head())
df.to_csv('jobs.csv')