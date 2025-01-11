# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 12:07:12 2025

@author: Oreoluwa
"""

#Import dependencies
import requests
from bs4 import BeautifulSoup



#title = input("What job are you looking for? ")  # Job title
#location = input("Where do you want to work? ")  # Job location


def linkedln(title,location):
    start = 0  # Starting point for pagination
    # Construct the URL for LinkedIn job search
    list_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={title}&location={location}&start={start}"
    
    # Send a GET request to the URL and store the response
    response = requests.get(list_url)
    
    #Get the HTML, parse the response and find all list items(jobs postings)
    list_data = response.text
    list_soup = BeautifulSoup(list_data, "html.parser")
    page_jobs = list_soup.find_all("li")
        
        
    #Create an empty list to store the job postings
    id_list = []
    #Itetrate through job postings to find job ids
    try:
        for job in page_jobs:
            base_card_div = job.find("div", {"class": "base-card"})
            job_id = base_card_div.get("data-entity-urn").split(":")[3]
            id_list.append(job_id)
    except:
        pass
        
        
    # Initialize an empty list to store job information
    job_list = []
    
    # Loop through the list of job IDs and get each URL
    for job_id in id_list:
        # Construct the URL for each job using the job ID
        job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        
        # Send a GET request to the job URL and parse the reponse
        job_response = requests.get(job_url)
        job_soup = BeautifulSoup(job_response.text, "html.parser")
        
         # Create a dictionary to store job details
        job_post = {}
        
        # Try to extract and store the job title
        try:
            job_post["job_title"] = job_soup.find("h2", {"class":"top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"}).text.strip() + " at " + job_soup.find("a", {"class": "topcard__org-name-link topcard__flavor--black-link"}).text.strip()
        except:
            continue
            
        
       
        # Try to extract and store the number of applicants
        try:
            job_post["Location"] = location
        except:
            continue
            
            
        try:
            job_post["Link"] = job_url
        except:
            continue
        
            
        # Append the job details to the job_list
        job_list.append(job_post)
    return job_list
        
    '''counter = 1    
    for job in job_list:
        print("JOB " + str(counter))
        counter += 1
        
        for k,v in job.items():
            print(k, ": ",v)
            print("\n")'''    
    


    