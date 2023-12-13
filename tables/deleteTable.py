import MySQLdb
import mysql.connector

conn = MySQLdb.connect(
    user="crawl_usr",
    passwd="Test001",
    host="localhost",
    db="crawl_data"
    # charset="utf-8"
)

cursor = conn.cursor()

delete_JobPosting_table_query = "DROP TABLE jobposting"

delete_language_table_query = "DROP TABLE language"

delete_companySize_table_query = "DROP TABLE companysize"

delete_company_table_query = "DROP TABLE company"

delete_User_table_query = "DROP TABLE user"

cursor.execute(delete_JobPosting_table_query)
cursor.execute(delete_company_table_query)
cursor.execute(delete_companySize_table_query)
cursor.execute(delete_User_table_query)
cursor.execute(delete_language_table_query)
print("Table deletion complete")

conn.commit()
#cursor.close()
#conn.close()