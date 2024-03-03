from bs4 import BeautifulSoup
import requests
import csv
import sys

test_url = ["https://www.hotelassociationnepal.org.np/hotels/fivestar"]
URL = input("Enter the url of the hotel association:")

if URL not in test_url:
  print("only test_url is accepted")
  sys.exit()

page = requests.get(URL)

data = []
fields = ["phone_number","map_data","email_address","website"]
soup = BeautifulSoup(page.content, "html.parser")

all_block = soup.find_all(attrs={"class":"geodir-opt-list"})

def parse_html(html_strings):
  website = html_strings.find(attrs={"title": "Visit Site"})['href'] if html_strings.find(attrs={"title": "Visit Site"}) else "None"
  phone_number = html_strings.find(attrs={"title": "Make Call"})['href'] if html_strings.find(attrs={"title": "Make Call"}) else "None"
  email_address = html_strings.find(attrs={"title": "Send Mail"})['href'] if html_strings.find(attrs={"title": "Send Mail"}) else "None"
  map_data = soup.find(attrs={"title": "Visit Map"})['href'] if html_strings.find(attrs={"title": "Visit Map"}) else "None"
  return {
        "website": website,
        "phone_number": phone_number,
        "email_address": email_address,
        "map_data":map_data
    }

for i in range(len(all_block)):
  b =parse_html(all_block[i])
  data.append(b)

with open("combined_data.csv", 'w') as csvfile:
  writer = csv.DictWriter(csvfile, fieldnames=fields)
  writer.writeheader()
  writer.writerows(data)


with open('combined_data.txt', 'w') as file:
  for i in range(len(data)):
      phone_number = data[i]["phone_number"]
      map_data = data[i]["map_data"]
      email_address = data[i]["email_address"]
      website = data[i]["website"]
      
      combined_data = ', '.join(filter(None, [phone_number, map_data, email_address, website]))
      
      file.write(combined_data + '\n')

