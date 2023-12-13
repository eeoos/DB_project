from requests import get
from bs4 import BeautifulSoup

import mysql.connector
import MySQLdb

import sys
sys.path.append('D:\Programs\GitHub\DB_project\extractors')

from language1 import extract_languageList
from incruit import extract_incruit_jobs
from companySize import get_companySize
from user import extract_userList

# 데이터베이스 연결 생성
conn = MySQLdb.connect(
        user="crawl_usr",
        passwd="Test001",
        host="localhost",
        db="crawl_data"
        # charset="utf-8"
    )

mycursor = conn.cursor()

def insert_Data():
    

    companySizeList = get_companySize()
    languageList = extract_languageList()

    for companySize in companySizeList: #companySize 테이블에 데이터 삽입
        sql = "INSERT INTO companySize (companySizeName) VALUES (%s)"
        val = (companySize,)
        mycursor.execute(sql, val)
    #jobPostingID = 1

    urls = []
    #jobposting_company_name = []

    for idx, keyword in enumerate(languageList):  # language 테이블에 데이터 삽입
        sql = "INSERT INTO language (languageID, languageName) VALUES (%s, %s)"
        val = (idx, keyword)
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
                    #url을 따로 저장
                    urls.append(job['link'])
                    
                    # SQL INSERT 문을 실행
                    sql = "INSERT INTO jobPosting (Position, Company, Career, Education, Location, EmploymentType, URL, LanguageID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (job['position'], job['company'], job['career'], job['education'], job['location'], job['employment_type'], job['link'], idx)
                    mycursor.execute(sql, val)
                #jobPostingID += 1

    # 변경사항을 데이터베이스에 적용
    conn.commit()

    return urls, languageList, companySizeList
    


company_datas = []

def insert_company():
    urls, languageList, companySizeList = insert_Data()
    print("Searching company information")
    for url in urls:
        
 
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

    
    # 찾을 수 없는 게시물의 회사 정보       
    company_data = {
                        'link' : None,
                        'company_name' : "없음",
                        'establishment_date' : None,
                        'company_sizeID' : companySizeList.index('무입력'),
                        'company_sector' : None
                    }
    company_datas.append(company_data)
    
    print(f'Found {len(company_datas)} company datas')

    # company 테이블에 데이터 추가
    for company_data in company_datas:

        sql = "INSERT INTO company (companyName, establishmentDate, companySizeID, sector, companyURL) VALUES (%s, %s, %s, %s, %s)"
        val = (company_data['company_name'], company_data['establishment_date'], company_data['company_sizeID'], company_data['company_sector'], company_data['link'])
        mycursor.execute(sql, val)
    conn.commit()

    # jobposting 테이블의 company 컬럼을 companyID 컬럼으로 수정하고 그에 맞게 작업
    match_jobposting_company()

    # user 테이블에 데이터 삽입
    insert_user()

companyIDList = []

# 함수 이름 바꾸기
def match_jobposting_company():
    mycursor.execute("SELECT companyID, companyName FROM company")
    company_data = mycursor.fetchall()
    company_id_dict = {row[1]: row[0] for row in company_data}

    mycursor.execute("SELECT company FROM jobposting")
    company_data = mycursor.fetchall()
 
    # 가져온 데이터 출력
    for row in company_data:
        company = row[0]
        if company in company_id_dict:
            company = company_id_dict[company]
        else:
            company = company_id_dict["없음"]
        companyIDList.append(company)

    # 기존 데이터 삭제 (선택 사항)
    mycursor.execute("UPDATE jobposting SET company = NULL")

    # ALTER TABLE 문 실행하여 컬럼 이름 변경 및 데이터 타입 변경
    # companyID 컬럼을 company 테이블의 외래 키로 설정
    mycursor.execute("ALTER TABLE jobposting CHANGE company companyID INT")
    mycursor.execute("ALTER TABLE jobposting ADD FOREIGN KEY (companyID) REFERENCES company(companyID)")

    # 데이터 입력
    for companyID in companyIDList:
        # jobposting 테이블에 데이터 추가하는 코드
        sql = "UPDATE jobposting SET companyID = %s WHERE companyID IS NULL LIMIT 1"
        val = (companyID,)
        mycursor.execute(sql, val)
        conn.commit()


def insert_user():
    userList = extract_userList()

    for user in userList:

        sql = "INSERT INTO user (userName, userAddress, userPhoneNum, userEmail, userMainLanguageID) VALUES (%s, %s, %s, %s, %s)"
        val = (user[0], user[1], user[2], user[3], user[4])
        mycursor.execute(sql, val)
    conn.commit()

