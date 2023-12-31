import MySQLdb
import mysql.connector

conn = MySQLdb.connect(
    user="crawl_usr",
    passwd="Test001",
    host="localhost",
    db="crawl_data"
    # charset="utf-8"
)
print(type(conn))
# <class 'MySQLdb.connections.Connection'>
cursor = conn.cursor()
print(type(cursor))
# <class 'MySQLdb.cursors.Cursor'>

# CREATE TABLE 쿼리 실행 # insertData.py에서 company 엔트리는 companyID로 바뀜
create_JobPosting_table_query = """ 
CREATE TABLE jobPosting (
    
    JobPostingID INT AUTO_INCREMENT,
    Position VARCHAR(100),
    Company VARCHAR(100),
    Career VARCHAR(100),
    Education VARCHAR(100),
    Location VARCHAR(100),
    EmploymentType VARCHAR(100),
    URL VARCHAR(255),
    LanguageID INT,
    PRIMARY KEY (JobPostingID),
    FOREIGN KEY (LanguageID) REFERENCES language(languageID)
)
"""
create_company_table_query = """
CREATE TABLE company (
    
    companyID INT AUTO_INCREMENT,
    companyName VARCHAR(100),
    establishmentDate VARCHAR(100), 
    companySizeID INT,
    sector VARCHAR(100),
    companyURL VARCHAR(100),
    PRIMARY KEY (companyID),
    FOREIGN KEY (companySizeID) REFERENCES companySize(companySizeID)
)
"""
create_companySize_table_query = """
CREATE TABLE companySize (

    companySizeID INT AUTO_INCREMENT,
    companySizeName VARCHAR(100),
    PRIMARY KEY (companySizeID)
)
"""
create_language_table_query = """
CREATE TABLE language (

    languageID INT,
    languageName VARCHAR(100),
    PRIMARY KEY (languageID)
)
"""
create_User_table_query = """
CREATE TABLE user (

    userID INT AUTO_INCREMENT,
    userName VARCHAR(100),
    userAddress VARCHAR(100),
    userPhoneNum VARCHAR(100),
    userEmail VARCHAR(100),
    userMainLanguageID INT,
    PRIMARY KEY (userID),
    FOREIGN KEY (userMainLanguageID) REFERENCES language(languageID)
)
"""

cursor.execute(create_language_table_query)
cursor.execute(create_companySize_table_query)
cursor.execute(create_company_table_query)
cursor.execute(create_User_table_query)
cursor.execute(create_JobPosting_table_query)
print("Table creation complete")

conn.commit()
#cursor.close()
#conn.close()