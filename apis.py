from os import read
import requests, json


def getApiData():
  api_key = 'x3DXCsAWpBjbry7LAzgRnA'
  headers = {'Authorization': 'Bearer ' + api_key}
  api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
  params = {
      # 'twitter_profile_url': 'https://twitter.com/johnrmarty/',
      # 'facebook_profile_url': 'https://facebook.com/johnrmarty/',
      'linkedin_profile_url': 'https://linkedin.com/in/subuktageenfarooqi/',
      # 'extra': 'include',
      # 'github_profile_id': 'include',
      # 'facebook_profile_id': 'include',
      # 'twitter_profile_id': 'include',
      # 'personal_contact_number': 'include',
      # 'personal_email': 'include',
      # 'inferred_salary': 'include',
      # 'skills': 'include',
      # 'use_cache': 'if-present',
      # 'fallback_to_cache': 'on-error',
  }
  response = requests.get(api_endpoint, params=params, headers=headers)
  #print(response)
  data = response.json()
  #print(data)
  myValues = []
  myValues.append([data])
  print(json.dumps(data, indent=4, separators=(',', ': ')))

def getPeopleApiData():
  api_key = 'x3DXCsAWpBjbry7LAzgRnA'
  headers = {'Authorization': 'Bearer ' + api_key}
  api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
  params = {
    'linkedin_profile_url': 'https://linkedin.com/in/johnrmarty/',
  }
  response = requests.get(api_endpoint, params=params, headers=headers)
  print(response)
  data = response.json()
  print(data)
  myValues = []
  myValues.append([data['public_identifier']])
  print(myValues)

# Search Api - Person Search Endpoint
def getSearchApiData():
  api_key = 'x3DXCsAWpBjbry7LAzgRnA'
  headers = {'Authorization': 'Bearer ' + api_key}
  api_endpoint = 'https://nubela.co/proxycurl/api/v2/search/person/'
  params = {
    'country': 'PK',
    'first_name': 'Subuktageen',
    #'enrich_profiles': 'enrich',
  }
  response = requests.get(api_endpoint, params=params, headers=headers)
  data = response.json()
  print(json.dumps(data, indent=4, separators=(',', ': ')))
  return data['results']

def getPeopleApiData():
  api_key = 'x3DXCsAWpBjbry7LAzgRnA'
  headers = {'Authorization': 'Bearer ' + api_key}
  api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/profile/resolve'
  params = {
    'company_domain': 'gatesfoundation.org',
    'first_name': 'Bill',
    'similarity_checks': 'include',
    'enrich_profile': 'enrich',
    'location': 'Seattle',
    'title': 'Co-chair',
    'last_name': 'Gates',
  }
  response = requests.get(api_endpoint, params=params, headers=headers)
  data = response.json()
  print(json.dumps(data, indent=4, separators=(',', ': ')))
  return data


  
  
  
def companyLookupEndpoint():
  companies = input("company name")
  api_key = 'x3DXCsAWpBjbry7LAzgRnA'
  headers = {'Authorization': 'Bearer ' + api_key}
  api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/company/resolve'
  company_data_list = []
  for company in companies:
    print(company)
    params = { 'company_name': company }
    response = requests.get(api_endpoint, params=params, headers=headers)
    try:
      data = response.json()
      print(data)
    except json.decoder.JSONDecodeError:
          print(f"Failed to decode JSON response for company: {company}")
          print("Response content:", response.content)
          continue
    company_data_list.append(data)
  print('api request completed')
  with open("some_companies_urls.txt", "w") as f:
    for data in company_data_list:
      f.write(json.dumps(data['url'], indent=4, separators=(',', ': ')))
      f.write('\n')  # Add a newline between each company's data
  return data
  
def employee_listing_endpoint(company_urls):
  api_key = 'x3DXCsAWpBjbry7LAzgRnA'
  headers = {'Authorization': 'Bearer ' + api_key}
  api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/company/employees/'
  employee_data_list = []
  # company_urls = ["https://www.linkedin.com/company/abri-group"]
  company_urls = [url.strip('""') for url in company_urls]

  for url in company_urls:
    print(url) 
    params = {
      'url': url,
      'country': 'uk',
      'role_search': r'(?:estate\s*surveyor|GP\s*surveyor|General\s*Practice\s*surveyor|landlord\s+and\s+tenant|L&T\s*surveyor|planning\s+enforcement|planning\s+policy|planning\s+obligations|cil\s+officer|dm\s+planner|development\s+management|head\s+of\s+planning|development\s+manager|land\s+manager|development\s+project\s+manager|new\s+business\s+manager|estates\s+regeneration|town\s+centre\s+regeneration|regeneration\s+manager|development\s+surveyor|asset\s+manager|director\s+of\s+regeneration|head\s+of\s+development|head\s+of\s+regeneration|Planning\s+officer)',
      'employment_status': 'current',
      'enrich_profiles': 'enrich',
    }
    response = requests.get(api_endpoint, params=params, headers=headers)
    try:
      data = response.json()
    except json.decoder.JSONDecodeError:
      print(f"Failed to decode JSON response for employee: {url}")
      print("Response content:", response.content)
      continue
    employee_data_list.append(data)
  print('api request completed')
  with open("employee_data.txt", "w") as f:
    for data in employee_data_list:
      f.write(json.dumps(data, indent=4, separators=(',', ': ')))
      f.write('\n')  # Add a newline between each company's data
  return data


def read_txt(filename):
  items = []
  with open(filename, 'r') as f:
    lines = f.readlines()
    for item in lines:
        items.append(item.strip())    
    f.close()
    #print(items)
    return items
  
if __name__=='__main__':
  #getApiData()   # Task 01 - Get Api Data
  # getSearchApiData()   # Task 02 - Test Api Endpoint Search Api Person Profile Endpoint
  #getPeopleApiData()   # Task 02 - Test Api Endoint
  #getCompanyApiData()  # Task 03 - Get Company Employees
  # companiesList = read_txt('some_companies_names.txt')
  companyLookupEndpoint()
  # companies_url_list = read_txt('some_companies_urls.txt')
  # employee_listing_endpoint()