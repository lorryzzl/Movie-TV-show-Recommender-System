from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

url = 'https://www.themoviedb.org/tv'
path = 'C:/Users/Lorry/Desktop/chromedriver.exe'
browser_locale = 'en'
options = Options()
options.add_argument("--lang={}".format(browser_locale))
driver = webdriver.Chrome(executable_path=path,
                           chrome_options=options)
driver.get(url)

load_more_butn = driver.find_element_by_xpath('(//a[@class="no_click load_more"])[2]')
load_more_butn.click()
for i in range(1000):
    driver.execute_script("window.scrollBy(0, 1000)","")

tv_names = []
img_links = []
descript_links = []

pages = driver.find_elements_by_xpath('//div[@class="page_wrapper"]')
for page in pages:
    cards = page.find_elements_by_xpath('./div[@class="card style_1"]')
    for card in cards:
        name_wrapper = card.find_element_by_tag_name('h2')
        name = name_wrapper.find_element_by_tag_name('a')
        name_text = name.text
        descript_link = name.get_attribute('href')
        try:
            img = card.find_element_by_tag_name('img')
        except NoSuchElementException:
            continue
        tv_names.append(name.text)
        descript_links.append(descript_link)
        img_links.append(img.get_attribute('src'))

descripts = []
for link in descript_links:
    driver.get(link)
    overview_wrapper = driver.find_element_by_xpath('//div[@class="overview"]')
    overview = overview_wrapper.find_element_by_tag_name('p')
    description = overview.text
    descripts.append(description)

#driver.quit()

print(tv_names[50])
print(descript_links[50])
print(img_links[50])
print(len(tv_names), len(descript_links), len(img_links), len(descripts))

df = pd.DataFrame({'Title': tv_names, 'Description': descripts, 'Img_Link': img_links})
df.to_csv(r'C:\Users\Lorry\Desktop\tv_shows.csv',index=False)

driver.quit()