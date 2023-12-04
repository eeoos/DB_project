from requests import get
from bs4 import BeautifulSoup

import mysql.connector
import MySQLdb

from languageList import extract_languageList
from incruit import extract_incruit_jobs
from companySize import get_companySize



# 데이터베이스 연결 생성
conn = MySQLdb.connect(
        user="crawl_usr",
        passwd="Test001",
        host="localhost",
        db="crawl_data"
        # charset="utf-8"
    )

mycursor = conn.cursor()

def insert_jobPosting():
    

    companySizeList = get_companySize()
    languageList = extract_languageList()

    for companySize in companySizeList: #companySize 테이블에 데이터 삽입
        sql = "INSERT INTO companySize (companySizeName) VALUES (%s)"
        val = (companySize,)
        mycursor.execute(sql, val)
    #jobPostingID = 1

    urls = []
    jobposting_company_name = []
    for keyword in languageList: #language 테이블에 데이터 삽입
        sql = "INSERT INTO language (languageID, languageName) VALUES (%s, %s)"
        val = (languageList.index(keyword), keyword)
        mycursor.execute(sql, val)

        if keyword == 'Bash Shell': # bash와 shell 따로 검색 후 합치기
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

    return urls, languageList, companySizeList
    


company_datas = []

def insert_company():
    urls, languageList, companySizeList = insert_jobPosting()
    
    for url in urls:
        print("Searching company information")

        
        response = get(url)
        print("Requesting", url)

        if response.status_code != 200:
            print("Can't request weibsite")
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            
            
            company_section = soup.select_one('.mid_company_info')
            
            
            # 기업 정보 부분이 있는 경우
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
                
                for i, size in enumerate(companySizeList, start=1):  # 인덱스는 1부터 시작
                    if size in company_size: 
                        company_sizeID = i
                        break

                company_data = {
                    'link' : f"{company_url}",
                    'company_name' : company_name,
                    'establishment_date' : establishment_date,
                    'company_sizeID' : company_sizeID,
                    'company_sector' : company_sector
                }

                # company_name 중복 방지
                if not any(data['company_name'] == company_name for data in company_datas):
                    company_datas.append(company_data)
    
            else: # 기업 정보 부분이 없는 경우 
                sub_company_name = soup.select_one('.job_info_detail > h2 > em')
                if sub_company_name is not None:

                   

                    company_data = {
                        'link' : None,
                        'company_name' : sub_company_name.text,
                        'establishment_date' : None,
                        'company_sizeID' : companySizeList.index('무입력'),
                        'company_sector' : None
                    }

                    # company_name 중복 방지
                    if not any(data['company_name'] == sub_company_name.text for data in company_datas):
                        company_datas.append(company_data)

    # company 테이블에 데이터 추가
    for company_data in company_datas:

        sql = "INSERT INTO company (companyName, establishmentDate, companySizeID, sector, companyURL) VALUES (%s, %s, %s, %s, %s)"
        val = (company_data['company_name'], company_data['establishment_date'], company_data['company_sizeID'], company_data['company_sector'], company_data['link'])
        mycursor.execute(sql, val)
    
    # companySize 테이블의 companySizeID로 jobPosting 테이블의 Company 컬럼 업데이트
    for company_data in company_datas:
        sql = "UPDATE jobPosting SET Company = (SELECT companySizeID FROM company WHERE companyName = %s) WHERE Company = %s"
        val = (company_data['company_name'], company_data['company_name'])
        mycursor.execute(sql, val)
        
    conn.commit()

insert_company()


#python 내부에서 인덱스를 넣지 않은 db 테이블은 어떻게 처리해야하는지 검색 후 처리 
