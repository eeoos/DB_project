from requests import get
from bs4 import BeautifulSoup

def extract_languageList():
    url = "https://survey.stackoverflow.co/2023/#technology-most-popular-technologies"
    response = get(url)

    result = []

    if response.status_code != 200:
        print("Can't request website")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        languages =soup.select('#languageere2c > tr')

        for language_section in languages:
            language = language_section.select_one('td')                    
            result.append(language.text)

    c_index = result.index('C')
    result[c_index] = 'C%BE%F0%BE%EE' # C언어의 인코딩

    go_index = result.index('Go')
    result[go_index] = 'Golang'

    htmlcss_index = result.index('HTML/CSS')
    result[htmlcss_index] = 'HTML CSS'

    bashshell_index = result.index('Bash/Shell (all shells)')
    result[bashshell_index] = 'Bash Shell'

    return result[:20]

