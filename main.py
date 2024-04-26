import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime


# Function to scrape solar power data from NREL website
def scrape_solar_power_data(start_date, end_date):
    url = "https://www.nrel.gov/grid/solar-power-data.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing solar power data
    table = soup.find('table')

    # Initialize lists to store data
    date_data = []
    power_data = []

    # Possible date formats
    date_formats = ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S']

    # Check if the table is found
    if table:
        # Iterate over each row in the table
        for row in table.find_all('tr')[1:]:
            # Extract data from each column
            columns = row.find_all('td')
            date_str = columns[0].text.strip()
            power_str = columns[1].text.strip()

            # Try different date formats
            date = None
            for date_format in date_formats:
                try:
                    date = datetime.strptime(date_str, date_format)
                    break
                except ValueError:
                    pass

            # Check if both date and power data are valid
            if date and power_str.isdigit():
                # Convert power data to float
                power = float(power_str)

                # Check if the date is within the specified range
                if start_date <= date <= end_date:
                    # Append data to lists
                    date_data.append(date)
                    power_data.append(power)

    return date_data, power_data


# Function to save data to CSV file
def save_to_csv(date_data, power_data):
    with open('solar_power_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Power (MW)'])
        for i in range(len(date_data)):
            writer.writerow([date_data[i], power_data[i]])


# Main function
def main():
    # Interactive user input for start and end dates
    start_date_str = input("Enter start date (YYYY-MM-DD): ")
    end_date_str = input("Enter end date (YYYY-MM-DD): ")
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    date_data, power_data = scrape_solar_power_data(start_date, end_date)
    if date_data:  # Check if data was successfully scraped
        save_to_csv(date_data, power_data)
        print("Data scraped and saved to 'solar_power_data.csv'")
    else:
        print("Failed to scrape data. The table may not be available or the data format has changed.")


if __name__ == "__main__":
    main()
