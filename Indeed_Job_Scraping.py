# packages import
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# User inputs for job input
# position, city, state, radius, and pages
position = input("Enter position you are looking for: ")
city = input("Enter the city name: ")
state = input("Enter the state code of the city: ")
radius_distance = input("Enter the radius distance: ")
pages = input("Enter number of desire pages: ")

# Regular expression is needed here because of how Indeed format their url
position_replace = re.sub("\s+", '+', position)  # regular expression to replace space between position to plus sign, +
city_replace = re.sub("\s+", '+', city) # regular expression to replace space between city name tp plus sign, +  

# job list to store data
job_List = []


# job_ method
def job_():
    # for loop to iterate through the pages
    # Using range 0 up to the desire pages multiply by 10 with increments of 10
    for page in range(0, int(pages) * 10, 10):
        # url format with user inputs
        url = f"https://www.indeed.com/jobs?q={position_replace}&l={city_replace}%2C+{state}&radius={radius_distance}&start={page}"
        print(url)  # print out url indicating the scraping page
        r = requests.get(url)  # requests to obtain data from url
        bs = BeautifulSoup(r.content, 'html.parser')  # beautiful soup to parse html

        jobs = bs.find_all('div', class_='jobsearch-SerpJobCard')  # find all listed jobs in a page
        # for loop to iterate thru all jobs
        for each in jobs:
            title = each.find('a').text.strip()  # title of job
            company = each.find('span', class_='company').text.strip()  # company of the job

            # concatenate the indeed_link and job_link to create the full link of job
            link = 'https://www.indeed.com' + each.find('a', class_='jobtitle').attrs['href']

            # try and except for rating
            rating = each.find('span', class_='ratingsContent').text.strip() if (
                    each.find('span', class_='ratingsContent') != None) else "none"

            # location of job
            location = each.find(class_='location accessible-contrast-color-location').text.strip()

            # try and except for remote_option
            remote_options = each.find(class_='remote').text.strip() if (each.find(class_='remote') != None) else "none"

            date = each.find(class_='date').get_text().strip()  # date posted of job

            # try and except for salary
            salary = each.find('span', class_='salaryText').text.strip() if (
                        each.find('span', class_='salaryText') != None) else "none"

            # list job in json format
            job = {
                'title': title,
                'company': company,
                'rating': rating,
                'location': location,
                'remote_option': remote_options,
                'salary': salary,
                'date posted': date,
                'job link': link
            }

            job_List.append(job)  # append job to job_List


# job_save_to_csv method
def job_save_to_csv():
    job_naming = re.sub("\s+", '_', position)  # replace the empty space in position with an underscore
    df = pd.DataFrame(job_List)  # set up a pd dataframe tabular data format
    # Change the path directory to your desire saving directory
    path = 'C:\\Users\\Hubert\\Desktop\\'+f'jobs_{job_naming}.csv'
    # new line and print out the message of the path you save your csv file
    print(f"\nThis is where your saved csv file: {path}")
    df.to_csv(path, index=False)  # save df to_csv format with path and index equal false to not include index

# call out the method for data scraping
job_()
job_save_to_csv()
