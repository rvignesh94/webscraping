# Importing requried libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

# User input data
req_skill = input("Enter the skill you want to search:")
req_loc = input("Enter the location you want to search:")
exp = input("Enter the experience you want to search:")

# Getting data from the source urls
page = requests.get(f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={req_skill}&txtLocation={req_loc}&cboWorkExp1={exp}").text

# Creating lists of colomns
job_title = []
job_company = []
max_experience = []
job_location = []
skills = []
links = []
posted_date = []

# Creating instance of beautiful soup
soup = BeautifulSoup(page, "lxml")
jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')


#To find No of pages
count_per_page=(len(jobs))
total_count=int(soup.find('span', id='totolResultCountsId').text)
no_of_pages = (round(total_count/count_per_page))

# Filtering the data
for i in range(no_of_pages):
    for job in jobs:
        title = job.find('h2').text.strip()
        job_title.append(title)
        company = job.find('h3', class_= 'joblist-comp-name').text.strip()
        job_company.append(company)
        experience = job.find("ul", class_='top-jd-dtl clearfix').li.text.strip().split('-')[1]
        max_experience.append(experience)
        location = job.find("ul", class_='top-jd-dtl clearfix').span.text.strip()
        job_location.append(location)
        skill = job.find('span', class_='srp-skills').text.replace(' ','').strip()
        skills.append(skill)
        link = job.header.h2.a["href"]
        links.append(link)
        posted_on = job.find("span", class_='sim-posted').text.strip()
        posted_date.append(posted_on)
    print(f"{i} pages done.")


# Exporing to dataframe and to excel file format
data = pd.DataFrame({
    "job_title":job_title,
    "job_company":job_company,
    "job_location":job_location,
    "skills":skills,
    "links":links,
    "posted_on": posted_date
})

data.to_excel("data.xlsx")