from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

website = 'https://www.adamchoi.co.uk/overs/detailed'
path = r'C:\Users\HP\Documents\chromedriver-win64\chromedriver.exe'  

service = Service(executable_path=path)

driver = webdriver.Chrome(service=service)
driver.get(website)

all_matches_button = driver.find_elements(By.XPATH, '//label[@analytics-event="All matches"]')

if all_matches_button:
    all_matches_button[0].click()

matches = driver.find_elements(By.TAG_NAME,'tr')

date=[]
home_team= []
score= []
away_team=[]

for match in matches:
    try:

        tds = match.find_elements(By.TAG_NAME, 'td')
        if len(tds) >= 4:  # Ensure there are at least 4 columns in the row
            date_text = tds[0].text  # First td is the date
            home_text = tds[2].text  # Second td is the home team
            score_text = tds[3].text  # Third td is the score
            away_text = tds[4].text  # Fourth td is the away team

            date.append(date_text)
            home_team.append(home_text)
            score.append(score_text)
            away_team.append(away_text)


            print(f"Date: {date_text}, Home: {home_text}, Score:{score_text}, Away: {away_text}")
        else:
            print(f"Skipping row with insufficient data: {match.get_attribute('outerHTML')}")
    except Exception as e:
        print("Error while extracting data:", e)

driver.quit()

df = pd.DataFrame({'date':date,'home_team':home_team,'score':score,'away_team':away_team})
df.to_csv('football_data.csv', index= False)
print(df)
