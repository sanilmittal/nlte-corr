import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv

"""
The code takes in values for the field parameters one star at a time from a file and then uses these fields to post an html request to the NLTE website and get the values
by parsing the result for the delta value. If there are changes made to the limits, wavelengths we can run for, or the format of output 
on the website, the code will have to be updated.

The elements done: Mg (12), Si (14), Fe II (26.1)

Make sure the required libraries [re, selenium, csv] are installed, otherwise first use pip on command line to install them 

Website value range: if correction: -1,..,1 OK; 0.000 no NLTE departures for this line; 
30 line too weak (EW < 1mA) or line is not in linelist;
20 NLTE not converged; 
10 error in lineformation

Will need to manually check for 10, 20 , 30-- 30 most common, just delete those Corr values

website: https://nlte.mpia.de/gui-siuAC_secE.php

Last updated: July 21, 2023 (sanilm@umich.edu)
"""

output_file = "nlte_fe1onaksimgfe2.csv"  # file headers: ["Name", "ID", "Wav", "EqW", "Abundance", "Corr", "Corrected"]  # ID must be in numbers, e.g. 26 for Fe I, 26.1 for Fe II

file1 = "nlte_fe1onak.csv"   # file headers in this order: ["Name", "ID", "Wav", "EqW", "Abundance", "Corr", "Corrected"]

file2 = "result_round5.csv"  # File headers in this order: "Name","Teff","Logg","FeH","Vt"

model_input = "mafags-os"  # mafags-os (plane-parallel 1D MAFAGS-OS), marcs (Spherical 1D MARCS), rsg (Spherical 1D RSG-MARCS)

# Not need to change the code below this line unless need to update the code
########################################################################################
########################################################################################
########################################################################################

def process_input(name, temperature, logg, feh, vt, lines):
    output = []
    url = 'https://nlte.mpia.de/gui-siuAC_secE.php'

    # Configure Chrome WebDriver options
    options = webdriver.ChromeOptions() # Options()
    # options.add_argument(
    options.add_argument('--headless')  # Run in headless mode (without a visible browser)
    options.add_argument('--no-sandbox')  # Bypass OS security model

    # Set path to the Chrome WebDriver executable
    # webdriver_path = "C:\\Users\\Sanil\\Downloads\\chromedriver_win32\\chromedriver.exe"

    # Create a new Chrome WebDriver

    # options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(), options=options)


    # Navigate to the URL
    driver.get(url)

    # Find model atmosphere
    model = driver.find_element(By.NAME, 'model')
    model.send_keys(model_input)

    # Find and clear the user input field
    user_input = driver.find_element(By.NAME, 'user_input')
    user_input.clear()
    user_input.send_keys(f'CS {temperature} {logg} {feh} {vt}')

    # Find and clear the lines input field
    lines_input = driver.find_element(By.NAME, 'lines_input')
    lines_input.clear()
    lines_input.send_keys(lines)

    # Find the submit buttons
    submit_buttons = driver.find_elements(By.TAG_NAME, 'input')
    for button in submit_buttons:
        if button.get_attribute('type') == 'submit':
            button.click()
            break

    # Get the page source
    page_source = driver.page_source
    # print(page_source)
    # Extract the desired values using regular expressions
    lines_values = re.findall(r'lines\(A\)\s+(.*?)</b>', page_source)[0].split()
    cs_values = re.findall(r'CS\s+(.*?)</b>', page_source)[0].split()

    # Print the extracted values in pairs
    for line_value, cs_value in zip(lines_values, cs_values):
        output.append([name, line_value.strip(), cs_value.strip()])

    # Quit the WebDriver
    driver.quit()
    return output

def get_lines(filename):
    lines_data = {}
    output_numbers = {}

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            name = row[0]
            wavelength = row[2]
            ID = row[1]
            if ID not in ["26.1", "12", "14"]:
                continue  # Skip lines with unsupported IDs

            if ID == '12':
                ID = '12.01'
            elif ID == '14':
                ID = '14.01'
            else:
                ID = '26.02'

            if name not in lines_data:
                lines_data[name] = []  # Create a new entry for the name
            lines_data[name].append(f"{wavelength} {ID}")  # Append the wavelength and ID pair to the respective name entry

    # Append output numbers to the respective lines_data
    for key, value in output_numbers.items():
        name, wavelength, ID = key
        lines_data[name].append(f"{wavelength} {ID} {value}")

    return lines_data


lines_data = get_lines(file1)
main_out = []


with open(file2, "r") as f:
            next(f)
            read = csv.reader(f, delimiter=",")
            num_rows = 0
            for row in read:
                num_rows += 1
                # Define the field values
                name = row[0]
                temperature = float(row[1])
                logg = float(row[2])
                feh = float(row[3])
                vt = float(row[4])
                # abun = float(row[-1])
                if name in lines_data:
                    data = lines_data[name]
                    # print(name)
                    lines = '\n'.join(data)
                    # print(lines)
                    output = process_input(name, temperature, logg, feh, vt, lines)
                    for i in output:
                        main_out.append(i)
                        # print(i)

with open(output_file, "w", newline="") as newfile:
    writer = csv.writer(newfile)
    writer.writerow(["Name", "ID", "Wav", "EqW", "Abundance", "Corr", "Corrected"])
    with open(file1, "r") as file:
        next(file)
        read2 = csv.reader(file, delimiter=",")
        for row in read2:
            if row[1] not in ["26.1", "12", "14"]:
                writer.writerow(row)
            else:
                # find row[0] and row[2] combination in main_out and write the 3rd element of the list the row[0] row[2] pair is in and write that at index 5, keeping earlier 4 entries in row same
                for entry in main_out:
                    if entry[0] == row[0] and entry[1] == row[2]:
                        new_row = row[0:5] + [entry[2]]  # Replace with the desired values
                        writer.writerow(new_row)
                        print(new_row)
                        break