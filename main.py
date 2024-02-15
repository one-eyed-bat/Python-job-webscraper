from bs4 import BeautifulSoup
import requests
import csv

class Work:
    def __init__(self, title, deet, skill):
        self.title = title
        self.deet = deet
        self.skill = skill

def single_page():
    work_list = []
    html_text = requests.get('https://www.freelancer.com/jobs/python/').text
    soup = BeautifulSoup(html_text, 'lxml')
    job_list = soup.find_all('div', class_="JobSearchCard-item")

    for job in job_list:
        job_skill = job.find('div', class_="JobSearchCard-primary-tags").text
        if 'Web Scraping' in job_skill:
            job_title = job.find('div', class_="JobSearchCard-primary-heading").a.text.replace('  ', '')
            job_deet = job.find('p', class_="JobSearchCard-primary-description").text.replace('  ', '')
            work = Work(job_title, job_deet, job_skill)
            work_list.extend([work.title, work.deet, work.skill])

    return work_list

def page_dict():
    nop = int(input("Please select number of pages to scrape (2-10): "))
    while not 2 <= nop <= 10:
        nop = int(input("Please select number of pages to scrape between 2 and 10: "))

    y = 2
    all_html = {}
    for _ in range(nop-1):
        z = f'https://www.freelancer.com/jobs/python/{y}'
        all_html[y] = z
        y += 1

    return all_html

def soup_func(all_html, max_jobs):
    work_list = []
    j = 0

    for url in all_html.values():
        html_text = requests.get(f'{url}').text
        soup = BeautifulSoup(html_text, 'lxml')
        job_list = soup.find_all('div', class_="JobSearchCard-item")

        for job in job_list:
            job_skill = job.find('div', class_="JobSearchCard-primary-tags").text
            if 'Web Scraping' in job_skill:
                job_title = job.find('div', class_="JobSearchCard-primary-heading").a.text.replace('  ', '')
                job_deet = job.find('p', class_="JobSearchCard-primary-description").text.replace('  ', '')
                work = Work(job_title, job_deet, job_skill)
                work_list.extend([work.title, work.deet, work.skill])

                j += 1
                if j == max_jobs:
                    print(f"Maximum number of jobs ({j}) reached.")
                    return work_list

    return work_list

def write_mult_files(work_list):
    print("Writing Multiple pages")
    for job in work_list:
        print(job)
        file.write(job + " working")

    exit("Multiple pages finished scraping")

def main():
    ans = input("Would you like to scrape multiple pages: ").lower()
    if ans not in ('y', 'yes', 'n', 'no'):
        ans = input("Please choose 'y', or 'n': ").lower()

    if ans == 'no' or ans == 'n':
        print("Writing single page.")
        work_l = single_page()
        for work in work_l:
            file.write(work)
        quit("Single page finished scraping")

    elif ans == 'yes' or ans == 'y':
        work_l = single_page()
        for work in work_l:
            file.write(work)

        all_html = page_dict()
        max_jobs = int(input("Choose the max number of job offers: "))
        work_list = soup_func(all_html, max_jobs)
        write_mult_files(work_list)
    else:
        quit("Stop messing around...")

if __name__ == "__main__":
    file = open("JobList.txt", "a")
    main()
