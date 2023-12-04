from requests import get
from bs4 import BeautifulSoup

def get_page_count(keyword):
    base_url = "https://search.incruit.com/list/search.asp?col=job&kw="
    
    response = get(f"{base_url}{keyword}")
    if response.status_code != 200:
        print("Can't request website")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        pagination = soup.find("p", class_="sqr_paging")
        
        if pagination is None:
            return None

        pages = pagination.find_all("a", recursive=False)

        if not pages:
            return 1
        
        count = len(pages)
        if count >= 2:
            return 1
        else:
            return count
        
    
def extract_incruit_jobs(keyword):
    print(f"Searching {keyword}")
    results = []
    pages = get_page_count(keyword)
    if pages == None: #
        print("Data not found.") #
        return None #
    
    print("Found", pages, "pages (incruit)")
    
    for page in range(pages):
        
        base_url = "https://search.incruit.com/list/search.asp?col=job"
        final_url = f"{base_url}&kw={keyword}&startno={page*30}"
        response = get(final_url)
        print("Requesting", final_url)

        if response.status_code != 200:
            print("Can't request website")
        else:
            
            soup = BeautifulSoup(response.text, "html.parser")

            jobs = soup.find_all('div', class_="cBbslist_contenst")

            for job_section in jobs:
                job_posts = job_section.find_all('li')

                for post in job_posts:
                    
                    cell_first = post.find("div", class_="cell_first")
                    anchor = cell_first.select_one("div a")
                    title = anchor.get_text()
                    #link = anchor['href']

                    cell_mid = post.find("div", class_="cell_mid")
                    cl_top = cell_mid.find("div", class_="cl_top").select_one("a")
                    position = cl_top.get_text()
                    link = cl_top['href'] ## 


                    cell_mid = post.find("div", class_="cell_mid")
                    cl_md = cell_mid.find("div", class_="cl_md")
                    spans = cl_md.find_all("span")
                    career = spans[0].string
                    education = spans[1].string
                    location = spans[2].string
                    employment_type = spans[3].string

                    if link == "#":
                        link = "None"
                    # 왜 #가 뜨는지?

                    job_data = {
                                'link': f"{link}",
                                'company':title.replace(",", " "),
                                'location':location.replace(",", " "),
                                'position':position.replace(",", " "),
                                'career':career.replace(","," "),
                                'education':education.replace(","," "),
                                'employment_type':employment_type.replace(",", " ")
                            }
                    results.append(job_data)
    return results