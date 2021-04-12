import os
import csv
import requests
import re
from bs4 import BeautifulSoup


def get_last_page(URL):
  result= requests.get(URL)
  soup= BeautifulSoup(result.text,"html.parser" )
  jobs_count=soup.find(class_='jobCount').text
  pages=int(re.findall('\d+', jobs_count)[0])/50+1
  return int(pages)



def get_alba_info(URL):
  job_info=[]
  result= requests.get(URL)
  soup= BeautifulSoup(result.text,"html.parser" )
  infos=soup.find_all('tr')
  for info in infos:
    if info.find('td',class_='local first'):
        loc = info.find('td',class_='local first').text
        company =info.find('span', class_='company').text
        data =info.find('td',class_='data').text
        pay =info.find('td',class_='pay').get_text()
        regDate=info.find('td',class_='regDate last').text
        job_info.append({'location': loc ,'company': company,'time': data,'pay': pay,regDate: regDate})
  return job_info


def save_to_file(key, values):
  file= open(f"{key}.csv", mode="w")
  writer= csv.writer(file)
  writer.writerow(["place","title","time","pay","date"])
  for value in values:
    writer.writerow(list(value.values()))
  return f"{key}.csv"


os.system("clear")
alba_url = "http://www.alba.co.kr"

alba_request=requests.get(alba_url)
alba_soup=BeautifulSoup(alba_request.text,"html.parser")
links=alba_soup.find_all(class_='impact'or'first impact')

jobs_infos={}

for i, link in enumerate(links):
  try:
    job_infos=[]
    company_name=link.find('span',class_='company').text
    filename = re.sub('[\/:*?"<>|]','',company_name)
    if os.path.isfile(f"{filename}.csv")==False:
      url=link.find('a')['href']+"job/brand/"
      result= requests.get(url)
      last_page=get_last_page(url)
      
      for page in range(last_page):
        job_infos=job_infos+(get_alba_info(url+f"?page={page+1}&pagesize=50"))

      jobs_infos[filename]=job_infos
      print(f"#{i}: "+filename+" ok")
    else:
      print(f"#{i}: "+filename+" file already exists")

  except AttributeError:
    print(f"#{i}: "+company_name+" don't have text")
    

for key, values in jobs_infos.items():
  save_to_file(key, values)
