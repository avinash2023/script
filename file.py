import requests
from bs4 import BeautifulSoup
import json

# Send a GET request to the website with headers to mimic a real browser
url = "https://www.investorgain.com/report/live-ipo-gmp/331/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers)

# Check if the response is successful
if response.status_code == 200:
    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <tr> elements which represent rows in the table
    ipo_data = soup.find_all('tr')

    # List to store the IPO data as dictionaries
    ipo_list = []

    # Loop through each row in the table
    for row in ipo_data:
        # Find all <td> elements (columns) in the row
        columns = row.find_all('td')

        # Ensure that the row has enough columns to extract IPO name, GMP, and Est Listing
        if len(columns) > 2:
            # Extract IPO name (first <td> contains the <a> tag for IPO name)
            ipo_name = columns[0].find('a').text.strip() if columns[0].find('a') else None

            # Extract GMP value (4th <td>, containing GMP value)
            gmp = columns[3].text.strip()

            # Extract Est Listing (5th <td>, containing the estimated listing value in parentheses)
            est_listing_td = columns[4].find('b')  # Find the <b> tag inside the Est Listing column
            if est_listing_td:
                # Get the text and split it into numeric value and percentage
                est_listing_text = est_listing_td.text.strip()  # "426 (50.53%)"
                if '(' in est_listing_text and ')' in est_listing_text:
                    # Split into numeric value and percentage
                    numeric_value = est_listing_text.split(' ')[0]  # "426"
                    percentage = est_listing_text.split('(')[1].split(')')[0]  # "50.53%"
                    est_listing = f"{numeric_value} ({percentage})"
                else:
                    est_listing = est_listing_text
            else:
                est_listing = None

            # Only add to the list if all three values are available
            if ipo_name and gmp and est_listing:
                ipo_list.append({
                    "IPO": ipo_name,
                    "GMP": gmp,
                    "Est Listing": est_listing
                })

    # Convert the list to JSON and print it
    print(json.dumps(ipo_list, indent=4))
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")
