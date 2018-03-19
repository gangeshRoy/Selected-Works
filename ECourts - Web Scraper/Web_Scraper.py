from selenium import webdriver
import datetime
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd


def populate_page_for_a_court(court):
	'''Takes a given court, selects court part 11C, and populates the date information.
	If the court is Queens or New York, it will also select all judges from the next screen.'''

	# Select Court
	select_a_court_menu = driver.find_element_by_xpath('//*[@id="cboCourt"]')
	select_a_court_menu.click()

	# Enters the code specific to the court. 
	if court == 'Bronx County Civil Court':
	    court_option = '//*[@id="cboCourt"]/option[8]'
	elif court == 'New York County Civil Court':
	    court_option = '//*[@id="cboCourt"]/option[42]'
	else:
	    court_option = '//*[@id="cboCourt"]/option[56]'

	select_a_court_item = driver.find_element_by_xpath(court_option)
	select_a_court_item.click()

	# Select Court Part
	court_part_menu = driver.find_element_by_xpath('//*[@id="cboCourtPart"]')
	court_part_menu.click()

	# Depending on the court, there are different XPaths to get to 11C court_part_item.
	if court == 'Bronx County Civil Court':
	    court_part_item = driver.find_element_by_xpath('//*[@id="cboCourtPart"]/option[7]')
	    court_part_item.click()
	elif court == 'New York County Civil Court':
	    court_part_item = driver.find_element_by_xpath('//*[@id="cboCourtPart"]/option[21]')
	    court_part_item.click()
	else:
	    court_part_item = driver.find_element_by_xpath('//*[@id="cboCourtPart"]/option[4]')
	    court_part_item.click()

	# Entering Dates
	start_month = driver.find_element_by_xpath('//*[@id="f_monthcalFromDate"]')
	start_month.clear()
	start_month.send_keys(two_mondays_month)
	start_day = driver.find_element_by_xpath('//*[@id="f_datecalFromDate"]')
	start_day.clear()
	start_day.send_keys(two_mondays_day)
	start_year = driver.find_element_by_xpath('//*[@id="f_yearcalFromDate"]')
	start_year.clear()
	start_year.send_keys(two_mondays_year)
	end_month = driver.find_element_by_xpath('//*[@id="f_monthcalToDate"]')
	end_month.send_keys(two_fridays_month)
	end_day = driver.find_element_by_xpath('//*[@id="f_datecalToDate"]')
	end_day.send_keys(two_fridays_day)
	end_year = driver.find_element_by_xpath('//*[@id="f_yearcalToDate"]')
	end_year.send_keys(two_fridays_year)

	# Getting Next Page
	find_calendar = driver.find_element_by_xpath('//*[@id="showForm"]/tbody/tr[3]/td[2]/table/tbody/tr[2]/td[2]/input')
	find_calendar.click()

	# Getting around the Queens and Manhattan Screens...
	if court == 'Queens County Civil' or court == 'New York County Civil Court':
	    try:
	        select_all = driver.find_element_by_xpath("//tbody/tr[6]/td/input[@class='normal'][1]")
	        select_all.click()
	        submit_button = driver.find_element_by_xpath("//tbody/tr[6]/td/input[@class='normal'][3]")
	        submit_button.click()
	    except:
	        pass


def scrape_page_data(table_XPATH = "/html/body/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table"):
    '''Pulls dates, CV numbers, plaintiff names, defendant names and counties from from the result
    set of the populate_page_for_a_court() function. Returns a dataframe with all results for a given
    court.'''
    dates = []
    CVs = []
    plaintiff_names = []
    defendant_names = []
    counties = []
    
    for case in tqdm(driver.find_elements(By.XPATH, table_XPATH)):
        # Two separate types of table, those with two tr elements, and those with just one...

        # If condition will handle elements with two tr's
        if len(case.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')) == 2:

            # Set date
            try:
                date = case.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[0].text
            except:
                date = "Error. Check Date."

            # Set CV

            try:
                cv = case.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('dl').find_element_by_tag_name('dt').text.split()[0]    
            except:
                cv = "Error. Check CV."

            # Set plaintiff_name

            try:
                plaintiff_name = case.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('dl').find_element_by_tag_name('dt').text.split('-')[3].split('vs.')[0].strip() 
            except:
                plaintiff_name = "Error. Check plaintiff name."

            # Set defendant_name

            try:
                defendant_name = case.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('dl').find_element_by_tag_name('dt').text.split('-')[3].split('vs.')[1].strip() 
            except:
                defendant_name = "Error. Check defendant name."

            # Set county

            try:
                county = case.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('dl').find_element_by_tag_name('dt').text.split('-')[2].split('/')[1].strip() 
                county = courts_mapping[county]
            except:
                county = "Error. Check plaintiff name."


        # Else condition handles elements with just one tr.
        else:

            # We only set the date when there are 2 tr elements. Just writing this out to be explicit.
            try:
                date = date
            except:
                date = "Error. Check Date"

            # Set CV

            try:
                cv = case.find_element_by_tag_name('tbody').find_element_by_tag_name('tr').find_elements_by_tag_name('td')[1].find_element_by_tag_name('dl').find_element_by_tag_name('dt').text.split()[0]    
            except:
                cv = "Error. Check CV."

            # Set plaintiff_name

            try:
                plaintiff_name = case.find_element_by_tag_name('tbody').find_element_by_tag_name('tr').find_elements_by_tag_name('td')[1].find_element_by_tag_name('dl').find_element_by_tag_name('dt').text.split('-')[3].split('vs.')[0].strip()  
            except:
                plaintiff_name = "Error. Check plaintiff name."

            # Set defendant_name

            try:
                defendant_name = case.find_element_by_tag_name('tbody').find_element_by_tag_name('tr').find_elements_by_tag_name('td')[1].find_element_by_tag_name('dl').find_element_by_tag_name('dt').text.split('-')[3].split('vs.')[1].strip()  
            except:
                defendant_name = "Error. Check plaintiff name."

            # Set county

            try:
                county = case.find_element_by_tag_name('tbody').find_element_by_tag_name('tr').find_elements_by_tag_name('td')[1].find_element_by_tag_name('dl').find_element_by_tag_name('dt').text.split('-')[2].split('/')[1].strip()
                county = courts_mapping[county]
            except:
                county = "Error. Check plaintiff name."

        dates.append(date)
        CVs.append(cv)
        plaintiff_names.append(plaintiff_name)
        defendant_names.append(defendant_name)
        counties.append(county)
        
    df = pd.DataFrame({"County":counties, "Date":dates, "CV":CVs, "Plaintiff Name":plaintiff_names, "Defendant Name":defendant_names})
    df = df[['Date', 'CV', 'Defendant Name', 'Plaintiff Name', 'County']]

    return df


# Creating date logic. 
# We want to pull court schedules from Monday two weeks from now until Friday two weeks from now.
def next_weekday_two_weeks(d, weekday):
    '''# 0 = Monday, 1=Tuesday, 2=Wednesday...'''
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 14
    return d + datetime.timedelta(days_ahead)

# Specifying Courts and Mapping
relevant_courts = ['Bronx County Civil Court', 'New York County Civil Court', 'Queens County Civil']
courts_mapping = {"BX":'Bronx County Civil Court', "NY":'New York County Civil Court', "QU":'Queens County Civil'}

# Spoofing user-agent params.
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")


if __name__ == "__main__":
	# Creating date information to populate fields.
	today = datetime.date.today()
	two_mondays_from_today = next_weekday_two_weeks(today, 0)
	two_mondays_year, two_mondays_month, two_mondays_day = two_mondays_from_today.year, two_mondays_from_today.month, two_mondays_from_today.day
	two_fridays_from_today = next_weekday_two_weeks(two_mondays_from_today, 4)
	two_fridays_year, two_fridays_month, two_fridays_day = two_fridays_from_today.year, two_fridays_from_today.month, two_fridays_from_today.day


	# Grabbing page, entering Captcha
	url = 'https://iapps.courts.state.ny.us/webcivilLocal/LCMain'
	driver = webdriver.Chrome(executable_path='./chromedriver/chromedriver', chrome_options=opts)
	driver.get(url)
	raw_input("Enter the Captcha. Once done return here and press any key.")


	# This selects the court calendars link
	court_calendars = driver.find_element_by_xpath("//tr[9]/td[1]/a")
	court_calendars.click()
	df = pd.DataFrame()
	# Grabbing data for all three courts.
	for court in relevant_courts:
	    print("%s - Scrape Progress:" % court)
	    populate_page_for_a_court(court)
	    # Implicitly waiting for page to populate with data
	    try:
	        date_headings = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr[1]/th')))
	        court_data = scrape_page_data()
	        df = df.append(court_data)
	        # Get back to the calendars page to restart the loop
	        court_calendars = driver.find_element_by_xpath("//tbody/tr[15]/td[@class='center']")
	        court_calendars.click()
	    except:
	        print ("There were no future appearances for this date range for %s" % court)
	        court_calendars = driver.find_element_by_xpath("//tbody/tr[15]/td[@class='center']")
	        court_calendars.click()
	driver.close()

	# Reordering the columns in the df, dropping duplicates and saving.
	df = df[['Date', 'CV', 'Defendant Name', 'Plaintiff Name', 'County']]
	df.drop_duplicates(inplace=True)
	df.reset_index(inplace=True, drop =True)
	print("Results: %s unique records scraped." % str(df.shape[0]))
	df.to_csv('Upcoming_Cases_from_'+str(two_mondays_from_today)+'_to_'+str(two_fridays_from_today)+'.csv')
