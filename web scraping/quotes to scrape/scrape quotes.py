from bs4 import BeautifulSoup
import requests
import pandas as pd

# Request the webpage content
parseWeb = requests.get("http://quotes.toscrape.com")
parseWeb.encoding = 'utf-8'
soup = BeautifulSoup(parseWeb.text, "html.parser")

# Prepare lists to hold the data
quotes_list = []
authors_list = []
tags_list = []

# Find all quote containers
quote_blocks = soup.find_all("div", class_="quote")

# Iterate over each quote block and extract data
for block in quote_blocks:
    quote = block.find("span", class_="text").text.strip()
    author = block.find("small", class_="author").text.strip()
    tags = [tag.text for tag in block.find_all("a", class_="tag")]
    tags_str = ', '.join(tags)
    
    # Append data to lists
    quotes_list.append(quote)
    authors_list.append(author)
    tags_list.append(tags_str)

# Create a DataFrame
data = {
    "Quote": quotes_list,
    "Author": authors_list,
    "Tags": tags_list
}

df = pd.DataFrame(data)

# Write the DataFrame to a CSV file
df.to_csv('quotes.csv', index=False, encoding='utf-8')

# Save the DataFrame to a JSON file
df.to_json('quotes_data.json', orient='records', lines=True, force_ascii=False, indent=4)

print("Quotes data saved to quotes_data.json")

print("Data has been written to quotes.csv")
