import csv
from os import name
from bs4 import BeautifulSoup
import requests
import pandas as pd

def extract(skill,page):
    source = 'https://in.indeed.com/jobs?q={}&start={}'
    url = source.format(skill,page)
    response = requests.get(url)
    print(response)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def transform(soup,skill):
    link = soup.find_all('a', 'fs-unmask')
    cards = soup.find_all('div', 'job_seen_beacon')
    job_url =[]
    for url in link:
        l= url.get('href')
        job_url.append(l)
    
    print(len(job_url))

    i=0
    for item in cards:
        title = item.find('div', class_ = 'singleLineTitle').text
        company = item.find('span', class_ = 'companyName').text
        location = item.find('div', class_ ='companyLocation').text
        url = 'in.indeed.com' + job_url[i]
        i+=1
        try:
            salary = item.find('div', class_ = 'salary-snippet').text
        except:
            salary ='Not Specified'

        job ={
            'Title' : title,
            'Skill' : skill.strip(),
            'Company' : company,
            'Location' : location,
            'Salary' : salary,
            'Link' : url
        }
        jobListing.append(job)
    return

jobListing = []
with open('skills.txt') as file:
    for skill in file:
        for i in range(0,40,10):
            c = extract(skill,i)
            transform(c,skill)

        print(len(jobListing))

    df = pd.DataFrame(jobListing)
    print(df.head())
    df.to_csv('output_21_Dec.csv')

file.close()
