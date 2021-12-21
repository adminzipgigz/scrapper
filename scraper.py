import csv
from os import name
from bs4 import BeautifulSoup
import requests
import pandas as pd

def extract(postion,page):
    source = 'https://in.indeed.com/jobs?q={}&start={}'
    url = source.format(postion,page)
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
            'Title' : title,
            'Company' : company,
            'Location' : location,
            'Salary' : salary
        }
        jobListing.append(job)
    return

with open('skills.txt') as file:
    for skill in file:
        jobListing = []
        for i in range(0,40,10):
            c = extract(skill,i)
            transform(c)

        print(len(jobListing))

        df = pd.DataFrame(jobListing)
        print(df.head())
        name = skill.strip()
        df.to_csv(f'{name}.csv')

file.close()
