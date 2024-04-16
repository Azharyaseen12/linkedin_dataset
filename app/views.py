from django.shortcuts import render,HttpResponse,redirect
import requests
from .models import Savesearches
import json
from django.conf import settings
from django.core.mail import send_mail
import datetime




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
            
            for employee_data in temp_data:
                for employee in employee_data:
                    last_updated_timestamp = employee.get('last_updated')
                    last_updated_datetime = datetime.datetime.strptime(last_updated_timestamp, "%Y-%m-%dT%H:%M:%SZ")
                    current_datetime = datetime.datetime.utcnow()
                    time_difference = current_datetime - last_updated_datetime
                    threshold = datetime.timedelta(days=3)
                    # print(last_updated_datetime,last_updated_timestamp,current_datetime,time_difference,threshold)
                    if time_difference <= threshold:
                        subject = 'Profile Update Alert'
                        message = f"The profile for {employee['profile']['full_name']} is updated recently."
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

