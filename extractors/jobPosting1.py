from requests import get
from bs4 import BeautifulSoup

import mysql.connector
import MySQLdb

from languageList import extract_languageList
from incruit import extract_incruit_jobs

def insert_jobPosting():
    # 데이터베이스 연결 생성
    conn = MySQLdb.connect(
        user="crawl_usr",
        passwd="Test001",
        host="localhost",
        db="crawl_data"
        # charset="utf-8"
    )

    mycursor = conn.cursor()

    languageList = extract_languageList()

    #jobPostingID = 1

    urls = []
    for keyword in languageList:
        sql = "INSERT INTO language (languageID, languageName) VALUES (%s, %s)"
        val = (languageList.index(keyword), keyword)
        mycursor.execute(sql, val)
        
        if keyword == 'Bash Shell':
            bash = extract_incruit_jobs('bash')
            shell = extract_incruit_jobs('shell')
            incruit = bash + shell
            keyword = "Bash Shell"
        else:
            incruit = extract_incruit_jobs(keyword)

        if incruit is not None:
            for job in incruit:
                if job['link'] not in urls:
                # SQL INSERT 문을 실행
                
                #sql = "INSERT INTO jobPosting (JobPostingID,Position, Company, Career, Education, Location, EmploymentType, URL, LanguageID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                #val = (jobPostingID,job['position'], job['company'], job['career'], job['education'], job['location'], job['employment_type'], job['link'], languageList.index(keyword))
                #mycursor.execute(sql, val)
                    urls.append(job['link'])
                    sql = "INSERT INTO jobPosting (Position, Company, Career, Education, Location, EmploymentType, URL, LanguageID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (job['position'], job['company'], job['career'], job['education'], job['location'], job['employment_type'], job['link'], languageList.index(keyword))
                    mycursor.execute(sql, val)
                #jobPostingID += 1

    # 변경사항을 데이터베이스에 적용
    conn.commit()

    return urls
    


company_datas = []

def insert_company():
    urls = insert_jobPosting()
    
    for url in urls:
        print("Searching company information")

        
        response = get(url)
        print("Requesting", url)

        if response.status_code != 200:
            print("Can't request weibsite")
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            
            company_section = soup.select_one('.mid_company_info')
            
            # 기업 정보 부분이 없는 경우 제외
            if company_section is not None:
                conts_box = company_section.select_one('.conts_box')

                
                #company_url
                jcinfo_logo = conts_box.select_one('.jcinfo_logo')
                company_url = jcinfo_logo.select_one("a")['href']
                
                #company_name
                jcinfo_logo_cpname = jcinfo_logo.select_one('.jcinfo_logo_cpname')
                company_name = jcinfo_logo_cpname.select_one("a").text
                



                jcinfo_list = conts_box.select('.jcinfo_list > li')
                establishment_date = jcinfo_list[0].select_one('.txt > em').text
                company_size = jcinfo_list[1].select_one('.txt > em').text
                company_sector = jcinfo_list[2].select_one('.txt > em').text
                
                company_data = {
                    'link' : f"{company_url}",
                    'company_name' : company_name,
                    'establishment_date' : establishment_date,
                    'company_size' : company_size,
                    'company_sector' : company_sector
                }

                # company_name 중복 방지
                if not any(data['company_name'] == company_name for data in company_datas):
                    company_datas.append(company_data)
    
    for company_data in company_datas:
        sql = "INSERT INTO jobPosting (Position, Company, Career, Education, Location, EmploymentType, URL, LanguageID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    
        sql = "INSERT INTO company (companyName, establishmentDate, sector) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (job['position'], job['company'], job['career'], job['education'], job['location'], job['employment_type'], job['link'], languageList.index(keyword))
        mycursor.execute(sql, val)

insert_jobPosting()
