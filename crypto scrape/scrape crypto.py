from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import bs4
import pandas as pd
import time

def getCryptoData():
    # Through the Chrome browser enter the website
    driver = webdriver.Chrome() 
    driver.get("https://coinmarketcap.com/")

    # Create the array to store the data from the website
    cryptoData = []

    time.sleep(10)

    body = driver.find_element(By.CSS_SELECTOR, 'body')

    # Scroll down through the page to find all the 'tr' tags in the body in the html
    while True:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
        rows = soup.find_all('tr')

        # break if the rows go over 21 rows
        if len(rows)>21:
            break
    
    # Only get the first 20 rows exlcuding the header row which is the first row
    for rows in rows[1:22]:
        cols = rows.find_all("td")

        # Gather all the information in the cols which contain all the data in the 'td' tags from each 'tr' tags
        if len(cols) > 1:
            try:
                rank = cols[1].text.strip()
                name = cols[2].find("p", class_ = "sc-71024e3e-0 ehyBa-d").text.strip()
                symbol = cols[2].find("p", class_ = "coin-item-symbol").text.strip()
                price = cols[3].text.strip()
                hour = cols[4].text.strip()
                hour24 = cols[5].text.strip()
                days7 = cols[6].text.strip()
                market_cap = cols[7].text.strip()
                volume24 = cols[8].find("p", class_ = "sc-71024e3e-0 bbHOdE font_weight_500").text.strip()
                volume24Coin = cols[8].find("p", class_ = "sc-71024e3e-0 hbcVUE").text.strip()
                circulating_supply = cols[9].find("p", class_ = "sc-71024e3e-0 hhmVNu").text.strip()

                # Add the data to the array as a dictionary
                cryptoData.append({
                    "Rank": rank,
                    "Name": name,
                    "Symbol": symbol,
                    "Price": price,
                    "1h % Change": hour,
                    "24h % Change": hour24,
                    "7d % Change": days7,
                    "Market Cap": market_cap,
                    "Volume (24h)": volume24,
                    "Volume (24h) (Coins)": volume24Coin,
                    "Circulating Supply": circulating_supply
                })

            except AttributeError as e:
                print(f"Error Processing row: {e}")
                continue

    return cryptoData

def printCryptoData(data):
    print("\n\n" + "-" * 80)
    for crypto in data:
        print(f"Rank: {crypto['Rank']}")
        print(f"Name: {crypto['Name']}")
        print(f"Symbol: {crypto['Symbol']}")
        print(f"Price: {crypto['Price']}")
        print(f"1h % Change: {crypto['1h % Change']}")
        print(f"24h % Change: {crypto['24h % Change']}")
        print(f"7d % Change: {crypto['7d % Change']}")
        print(f"Market Cap: {crypto['Market Cap']}")
        print(f"Volume (24h): {crypto['Volume (24h)']}")
        print(f"Volume (24h) (Coins): {crypto['Volume (24h) (Coins)']}")
        print(f"Circulating Supply: {crypto['Circulating Supply']}")
        print("-" * 60)

columns = ["Rank", "Name", "Symbol", "Price", "1h % Change", "24h % Change", "7d % Change", "Market Cap", "Volume (24h)", "Volume (24h) (Coins)", "Circulating Supply"]

def main():
    while True:
        # Get the results and print it out as well
        results = getCryptoData()
        printCryptoData(results)

        # Create and add the results to the files
        df = pd.DataFrame(results, columns=columns)

        # Write the DataFrame to a CSV file
        df.to_csv('cryptoData.csv', index=False, encoding='utf-8')

        # Save the DataFrame to a JSON file
        df.to_json('cryptoData.json', orient='records', lines=True, force_ascii=False, indent=4)

        print("Data data saved to cryptoData.json")

        print("Data has been written to cryptoData.csv")
        
        time.sleep(60) # Will update the printCryptoData every minute

if __name__ == "__main__":
    main()