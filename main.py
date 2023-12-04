from extractors.languageList import extract_languageList
from extractors.incruit import extract_incruit_jobs
#from creators.createTable

"""
keyword = input("What do you want to search for?")

incruit = extract_incruit_jobs(keyword)

file = open(f"{keyword}.csv", "w", encoding="utf-8")
file.write("Position,Company,Location,URL\n")

for job in incruit:
    file.write(f"{job['position']},{job['company']},{job['location']},{job['link']}\n")
file.close()
"""
"""
languageList = extract_languageList()


for keyword in languageList:

    if keyword == 'Bash Shell':
        bash = extract_incruit_jobs('bash')
        shell = extract_incruit_jobs('shell')
        incruit = bash + shell
        keyword = "bash shell"
        jobPosting = []
    else:
        incruit = extract_incruit_jobs(keyword)

    if keyword == "C%BE%F0%BE%EE":
        keyword = "C"

    
    file = open(f"{keyword}.csv", "w", encoding="utf-8")
    file.write("Position,Company,Career,Education,Location,URL\n")

    if incruit is None:
        pass

    else:
        for job in incruit:
            file.write(f"{job['position']},{job['company']},{job['career']},{job['education']},{job['location']},{job['employment_type']},{job['link']}\n")
        file.close()
"""


################### 파일 저장 코드 ##############################
""" 
languageList = extract_languageList()

file = open("jobPosting.csv", "w", encoding="utf-8")
file.write("Position,Company,Career,Education,Location,URL\n")

for keyword in languageList:
    if keyword == 'Bash Shell':
        bash = extract_incruit_jobs('bash')
        shell = extract_incruit_jobs('shell')
        incruit = bash + shell
        keyword = "Bash Shell"
    else:
        incruit = extract_incruit_jobs(keyword)

    #if keyword == "C%BE%F0%BE%EE":
    #    keyword = "C"




    if incruit is not None:
        for job in incruit:
            file.write(f"{job['position']},{job['company']},{job['career']},{job['education']},{job['location']},{job['employment_type']},{job['link']},{languageList.index(keyword)}\n")

file.close()
"""

languageList = extract_languageList()

url = []
for keyword in languageList:
    if keyword == 'Bash Shell':
        bash = extract_incruit_jobs('bash')
        shell = extract_incruit_jobs('shell')
        incruit = bash + shell
        keyword = "Bash Shell"
    else:
        incruit = extract_incruit_jobs(keyword)

    if incruit is not None:
        for job in incruit:
            url.append(job['link'])


print(url)