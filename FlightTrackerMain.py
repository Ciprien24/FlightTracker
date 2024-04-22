from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
import time

import pandas as pd

import smtplib
from email.message import EmailMessage

import schedule

departure_flight_inputs = {'Departure ' : " CLJ",
                           'Arrival': " EIN", 'Date': "Jun 20, 2024"}
return_flight_inputs = {'Departure': " EIN", 'Arrival': " CJ", 'Date': "Aug 28, 2024"}
def find_cheapest_flight(flight_info):
    PATH = '/Users/test1/Desktop/chromedriver'
    driver = webdriver.Chrome(PATH)
    leaving_from = flight_info['Departure']
    going_to = flight_info['Arrival']
    trip_date = flight_info['Date']

    driver.get('https://www.kiwi.com/')

    #Click on the DropDown Menu to select type of flight
    oneway_xpath = '//div[@class="orbit-button-primitive-content" and contains(text(), "Dus-întors")]'
    one_way_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located(ByXpath(oneway_xpath)))
    one_way_element.click()
    time.sleep(0.2)

    #Click on OneWay
    oneway_xpath = '//span[contains(text(), "Dus")]'
    one_way_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located(ByXpath(oneway_xpath)))
    one_way_element.click()
    time.sleep(0.2)

    #Flying From, Flying to, Departure Date, Return Date

    #Leaving From
    leaving_from_xpath = '//*[@id="react-view"]/div[2]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/div/div/div[1]/div/div[2]/div/input'
    leaving_from_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(ByXpath(leaving_from_xpath)))
    leaving_from_element.click.clear()
    leaving_from_element.click()
    time.sleep(1)
    leaving_from_element.send_keys(leaving_from)
    time.sleep(1) #Without this it would be too fast for the browser
    leaving_from_element.send_keys(Keys.DOWN,Keys.RETURN)

    #Going To
    going_to_xpath = '//*[@id="react-view"]/div[2]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/div/input'
    going_to_element = WebDriverWait(driver,10).until(EC.presence_of_element_located(ByXpath(going_to_xpath)))
    going_to_element.click.clear()
    going_to_element.send_keys()
    time.sleep(1)
    going_to_element.send_keys(going_to)
    time.sleep(1)
    going_to_element.send_keys(Keys.DOWN,Keys.RETURN)

    #Date selection
    trip_date_xpath = '//*[@id="react-view"]/div[2]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div".format(trip_date)'
    departing_date_element = ""
    while departing_date_element == "":
        try:
            departing_date_element =WebDriverWait(driver,10).until(EC.presence_of_element_located(By.XPATH,trip_date_xpath))
            departing_date_element.click()
        except TimeoutException:
            departing_date_element = ""
            next_month_xpath = '//*[@id="react-view"]/div[2]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/div[2]/div/div/div[3]/div[3]/button/div/svg'
            driver.find_element_by_xpath(next_month_xpath).click()
            time.sleep(1)

            depart_date_done_xpath = '//*[@id="react-view"]/div[2]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/div[2]/div/div/div[4]/div/div/button[2]/div'
            driver.find_element_by_xpath(depart_date_done_xpath)

            #Click Search
            search_button_xpath = '//*[@id="react-view"]/div[2]/div[3]/div[2]/div[2]/div[2]/div/div[2]/a'
            driver.find_element_by_xpath(search_button_xpath).click()
            time.sleep(15) #Time for the page to load





#Check for non-stop flights sorted by Lowest price

            Direct_flight_xpath = '//*[@id=":r16r:-slideID"]/div/div[1]/div/div/label[2]/div[2]/span'
            any_flight_xpath = '//*[@id=":rkn:-slideID"]/div/div[1]/div/div/label[1]/div[2]/span'

            if len(driver.find_elements_by_xpath(Direct_flight_xpath)) > 0:

                driver.find_element_by_xpath(Direct_flight_xpath).click()
                time.sleep(5)

                # Check if there are available flights
                available_flights = driver.find_elements_by_xpath(
                    "//*[@id='react-view']/div[2]/div[4]/div/div/div/div/div/div[3]/div/div/div[5]/div/div/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div[2]")
                if len(available_flights) > 0:
                    if len(available_flights) == 1:  # Don't have to sort by prices here
                        flights = [(item.text.split(",")[0].split('for')[-1].title(),
                                    item.text.split(",")[1].title().replace("At", ":"),
                                    item.text.split(",")[2].title().replace("At", ":"),
                                    item.text.split(",")[3].title().replace("At", ":")) for item in
                                   available_flights[0:5]]

                    else:
                        # Sort by lowest prices
                        driver.find_element_by_xpath('//*[@id="react-view"]/div[2]/div[4]/div/div/div/div/div/div[3]/div/div/div[2]/div/button[2]/div[1]/span').click()
                        time.sleep(5)
                        flights = [(item.text.split(",")[0].split('for')[-1].title(),
                                    item.text.split(",")[1].title().replace("At", ":"),
                                    item.text.split(",")[2].title().replace("At", ":"),
                                    item.text.split(",")[3].title().replace("At", ":")) for item in
                                   available_flights[0:5]]

                    print("Conditions satisfied for: {}:{}, {}:{}, {}:{}".format("Departure", leaving_from,
                                                                                 "Arrival", going_to,
                                                                                 "Date", trip_date))
                    driver.quit()
                    return flights
            else:
                print('Not all conditions could be met for the following: "{}:{}, {}:{}, {}:{}'.format("Departure",
                                                                                                       leaving_from,
                                                                                                       "Arrival",
                                                                                                       going_to,
                                                                                                       "Date",
                                                                                                       trip_date))
                driver.quit()
                return []







            #Function to send email
            def send_email():
                # Get return values
                departing_flights = find_cheapest_flights(departure_flight_inputs)
                return_flights = find_cheapest_flights(return_flight_inputs)

                # Put it into a dataframe to visualize this more easily
                df = pd.DataFrame(departing_flights + return_flights)

                if not df.empty:  # Only send an email if we have actual flight info
                    email = open('ciprianbalan244@gmail.com').read()
                    password = open('***********').read()

                    msg = EmailMessage()

                    msg['Subject'] = "Python Flight Info! {} --> {}, Departing: {}, Returning: {}".format(
                        departure_flight_inputs['Departure'], departure_flight_inputs['Arrival'],
                        departure_flight_inputs['Date'], return_flight_inputs['Date'])

                    msg['From'] = email
                    msg['To'] = email

                    msg.add_alternative('''\
                        <!DOCTYPE html>
                        <html>
                            <body>
                                {}
                            </body>
                        </html>'''.format(df.to_html()), subtype="html")

                    with smtplib.SMTP_SSL('Email server name here', 465) as smtp:
                        smtp.login(email, password)
                        smtp.send_message(msg)

            schedule.clear()
            schedule.every(30).minutes.do(send_email)

            while True:
                schedule.run_pending()
                time.sleep(1)
