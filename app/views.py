from django.shortcuts import render,HttpResponse,redirect
import requests
from .models import Savesearches,Email
import json
from django.conf import settings
from django.core.mail import send_mail
import datetime
from django.utils import timezone
import csv
from .models import Companies,UkCompanies
import pandas as pd

def home(request):
    if request.method == 'GET' and 'search_query' in request.GET:
        # Get the search query from the frontend form
        search_query = request.GET.get('search_query')
        api_key = 'x3DXCsAWpBjbry7LAzgRnA'
        headers = {'Authorization': 'Bearer ' + api_key}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        params = {
            'linkedin_profile_url':f'http://www.linkedin.com/in/{search_query}/',
        }
        response = requests.get(api_endpoint, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=4, separators=(',', ': ')))
            return render(request , 'index.html', {'linkedin_data': data})
        else:
            return HttpResponse('Failed to fetch data from API')
    else:
        return render(request , 'index.html')      
          
def fetch_all_results(api_endpoint, params, headers):
    all_results = []
    while api_endpoint:
        response = requests.get(api_endpoint, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            employees = data.get('employees', [])
            all_results.extend(employees)
            api_endpoint = data.get('next_page')
        else:
            print(f"Error fetching data: {response.status_code}")
            break
    return all_results

def filter(request):
    send_daily_email()
    if request.method == 'POST' and 'company_name' in request.POST:
        compani = request.POST.get('company_name')
        companies = compani.split(',')
        job_title = request.POST.get('job_title')  
        job_titles_list = job_title.split(',')

        api_key = 'x3DXCsAWpBjbry7LAzgRnA'
        headers = {'Authorization': 'Bearer ' + api_key}
        company_data_list = []
        for company in companies:
            api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/company/resolve'
            params = { 'company_name': company }
            response = requests.get(api_endpoint, params=params, headers=headers)
            data = response.json()
            company_data_list.append(data)

        api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/company/employees/'
        temp_data = []
        employee_data_list = []
        for company_data in company_data_list:
            url = company_data.get('url')
            for job_title in job_titles_list:
                params = {
                    'url': url,
                    'role_search': job_title,
                    'country': '',
                    'enrich_profiles': 'enrich',
                    'page_size': '10',
                    'employment_status': 'all',
                    'resolve_numeric_id': 'false',
                }
                employee_data = fetch_all_results(api_endpoint, params, headers)
                temp_data.append(employee_data) 
            for data in temp_data:
                employee_data_list.append(data)            
            # print(employee_data_list)
            for employee_data in temp_data:
                for employee in employee_data:
                    # Get last updated timestamp
                    last_updated_timestamp = employee.get('last_updated')
                    print(last_updated_timestamp)
                    if last_updated_timestamp is not None:
                        # Convert last updated timestamp to datetime object
                        last_updated_datetime = datetime.datetime.strptime(last_updated_timestamp, "%Y-%m-%dT%H:%M:%SZ")
                        # Get current datetime
                        current_datetime = datetime.datetime.utcnow()                        
                        # Check if the profile was last updated today
                        if last_updated_datetime.year == current_datetime.year and last_updated_datetime.month == current_datetime.month and last_updated_datetime.day == current_datetime.day:
                            # Initialize variables to store the latest and second last job titles
                            latest_job_title = None
                            second_last_job_title = None  
                                                    
                            # Iterate through experiences
                            experiences = employee.get('profile').get('experiences')
                            if experiences:
                                for exp in experiences:
                                    if exp.get('ends_at') is None:
                                        latest_job_title = exp['title']
                                        latest_job_company = exp['company']
                                        print(latest_job_title)
                                        break 
                                for exp in experiences:
                                    if exp.get('ends_at') is not None:
                                        if exp['title'] != latest_job_title:
                                            second_last_job_title = exp['title']
                                            second_last_job_company = exp['company']
                                            print(second_last_job_title)
                                            break    # Stop searching once the second last job title is found               
                                     
                                # Check if both latest and second last job titles are found
                                if latest_job_title != second_last_job_title:
                                    subject = 'Job Title Change Alert'
                                    # message = f"The job title for {employee['profile']['full_name']} has changed from '{second_last_job_title}' to '{latest_job_title}'."
                                    message = f"This message is to inform you that {employee['profile']['full_name']} who was a {second_last_job_title} at {second_last_job_company} changed his job and now he is {employee['profile']['occupation']} "
                                    email_from = settings.EMAIL_HOST_USER
                                    recipient_list = ['azharyaseen871@gmail.com']  # Update with recipient email address
                                    send_mail(subject, message, email_from, recipient_list)
                                    
        results = sum(len(data) for data in employee_data_list)
        request.session['company_name'] = companies
        request.session['job_title'] = job_title
        request.session['results'] = results 
        current_url = request.build_absolute_uri()
        request.session['current_url'] = current_url 
    
        return render(request, 'filters.html', {'employee_data_list': employee_data_list,'companies':compani,'job_title':job_title})
    return render(request, 'filters.html')
 

def savesearches(request):
    if request.method == 'GET':
        companies = request.GET.get('company_name')
        job_title = request.GET.get('job_title')
        results = request.session.get('results', None)
        # print(companies,job_title)
        # current_url = request.session.get('current_url', None)
        current_url = request.build_absolute_uri()
        # request.session['current_url'] = current_url  
        search = Savesearches(companies=companies,job_title=job_title, results=results,current_url=current_url)
        search.save()
        return redirect('savedsearches')

def savedsearches(request):
    searches = Savesearches.objects.all()
    return render(request, 'savedsearches.html',{'searches':searches})

def delete_search(request,id):
    if request.method == 'GET':
        searches = Savesearches.objects.get(pk = id)
        searches.delete()
        return redirect('savedsearches')   
    
def dashboard(request):
    return render(request, 'dashboard.html')


def send_daily_email():
    # Get today's date
    present_date = datetime.date.today() 
    email = Email.objects.filter(date=present_date)                                        
    # print(email.date,present_date)
    if not email:
        company_data_list = ['https://www.linkedin.com/company/zebra-architects-limited/','https://www.linkedin.com/company/croydon-churches-housing-association']

        # ukcompanies = UkCompanies.objects.all()
        # for compani in ukcompanies:
        #     company_data_list.append(data)

        api_key = 'x3DXCsAWpBjbry7LAzgRnA'        
        headers = {'Authorization': 'Bearer ' + api_key}
        api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/company/employees/'
        temp_data = []
        employee_data_list = []
        for url in company_data_list:
                params = {
                        'url': url,
                        'enrich_profiles': 'enrich',
                        'page_size': '10',
                        'employment_status': 'all',
                        'resolve_numeric_id': 'false',
                    }
                employee_data = fetch_all_results(api_endpoint, params, headers)
                temp_data.append(employee_data) 
                for data in temp_data:
                    employee_data_list.append(data)            
                print(employee_data_list)
                for employee_data in temp_data:
                    for employee in employee_data:
                        # Get last updated timestamp
                        last_updated_timestamp = employee.get('last_updated')
                        print(last_updated_timestamp)
                        if last_updated_timestamp is not None:
                            # Convert last updated timestamp to datetime object
                            last_updated_datetime = datetime.datetime.strptime(last_updated_timestamp, "%Y-%m-%dT%H:%M:%SZ")
                            # Get current datetime
                            current_datetime = datetime.datetime.utcnow()                        
                            # Check if the profile was last updated today
                            if last_updated_datetime.year == current_datetime.year:
                                # Initialize variables to store the latest and second last job titles
                                latest_job_title = None
                                second_last_job_title = None                                                          
                                # Iterate through experiences
                                experiences = employee.get('profile').get('experiences')
                                if experiences:
                                    for exp in experiences:
                                        if exp.get('ends_at') is None:
                                            latest_job_title = exp['title']
                                            latest_job_company = exp['company']
                                            print(latest_job_title)
                                            break 
                                    for exp in experiences:
                                        if exp.get('ends_at') is not None:
                                            if exp['title'] != latest_job_title:
                                                second_last_job_title = exp['title']
                                                second_last_job_company = exp['company']
                                                print(second_last_job_title)
                                                break    # Stop searching once the second last job title is found               
                                    # Check if both latest and second last job titles are found
                                    if latest_job_title != second_last_job_title:
                                        subject = 'Job Title Change Alert'
                                        # message = f"The job title for {employee['profile']['full_name']} has changed from '{second_last_job_title}' to '{latest_job_title}'."
                                        message = f"This message is to inform you that {employee['profile']['full_name']} who was a {second_last_job_title} at {second_last_job_company} changed his job and now he is {employee['profile']['occupation']} "
                                        email_from = settings.EMAIL_HOST_USER
                                        recipient_list = ['Dawarsardar786@gmail.com']  # Update with recipient email address
                                        send_mail(subject, message, email_from, recipient_list)
                                        email_obj = Email()
                                        email_obj.save()
                                        print('email sended and saved date ') 
                                        
               
    return HttpResponse('It is not time to send the email yet.')

def read_and_save_companies(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    # Extract the company names from the DataFrame
    company_names = df['Name of Company']
    
    # Save company names into the model
    for name in company_names:
        Companies.objects.create(company=name.strip())
csv_file_path = r'F:\falconxoft internship\project2\linkedin_dataset_project\nm\linkedin_dataset\Organisation Linkedin Names for proxycurl.xlsx'
# read_and_save_companies(csv_file_path)


# def uk_based_company():    
#     company_data_list = []
#     companies = [
#     ]
#     # my_companies = Companies.objects.all()
#     # for my_companies in my_companies:
#     #     cleaned_company_name = my_companies.company.strip('"')
#     #     companies.append(cleaned_company_name)  

#     api_key = 'x3DXCsAWpBjbry7LAzgRnA'
#     headers = {'Authorization': 'Bearer ' + api_key}  
#     for company in companies:
#             api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/company/resolve'
#             params = {
#                 'company_name': company ,
#                 'company_location': 'GB',
#                 }
#             response = requests.get(api_endpoint, params=params, headers=headers)
#             data = response.json()
#             company_data_list.append(data)
    
#     print(company_data_list)

#     api_key = 'x3DXCsAWpBjbry7LAzgRnA'
#     headers = {'Authorization': 'Bearer ' + api_key}
#     api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/company'
#     for company_data in company_data_list:
#                 url = company_data.get('url')
#                 print(url)
#                 # company profile    
#                 params = {
#                     'url': url,
#                     'resolve_numeric_id': 'true',
#                     'categories': 'include',
#                     'funding_data': 'include',
#                     'exit_data': 'include',
#                     'acquisitions': 'include',
#                     'extra': 'include',
#                     'use_cache': 'if-present',
#                     'fallback_to_cache': 'on-error',
#                 }
#                 response = requests.get(api_endpoint,
#                                         params=params,
#                                         headers=headers)
#                 data = response.json()
#                 # print(data)

#                 # Extract the headquarters location
#                 headquarters = data.get("hq")

#                 if headquarters:
#                     country = headquarters.get("country")
#                     print(country)
#                     if country != None and country.lower() == 'gb':
#                         uk_companies = UkCompanies(linkedin_profile_link=url, country=country)
#                         uk_companies.save()
#                         print("data saved successfully")
#                     else:
#                         print(f"cannot save the company because comapnies is from {country} not uk")
# # uk_based_company()