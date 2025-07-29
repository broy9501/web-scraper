from bs4 import BeautifulSoup as bs4
import requests
import spacy
import pandas as pd

blogsUrls = [
    "https://www.bruisedpassports.com/wheres/guide-planning-itinerary-trip-bhutan",
    "https://www.bruisedpassports.com/wheres/planning-itinerary-four-days-doha-qatar",
    "https://www.bruisedpassports.com/central-asia/india-to-kyrgyzstan-an-unforgettable-5-day-trip-along-the-spice-route",
    "https://www.nomadicmatt.com/travel-blogs/61-travel-tips/",
    "https://www.nomadicmatt.com/travel-blogs/home-and-travel/"
]

locations, visited_cleaned, titles, links, content, first_paras = [], [], [], [], [], []
blog_data = []

nlp = spacy.load("en_core_web_lg")

def extractWithSpacyLoc(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent.text
    return None

def extractWithSpacyPlaces(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ in ["LOC", "FAC", "ORG"]]

def clean_text(text):
    return text.strip().replace('\n', ' ').replace('\r', '').replace('\xa0', ' ')

for url in blogsUrls:
    links.append(url)
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = bs4(response.text, "html.parser")

    if "bruisedpassports" in url:
        title = soup.find("h1", class_="title")
        if title:
            titles.append(clean_text(title.text))

        article = soup.find("article")
        if article:
            content_div = article.find("div", class_=lambda x: x and "single-content" in x)
            if content_div:
                paragraphs = content_div.find_all("p")
                if paragraphs:
                    first_paragraph = clean_text(paragraphs[0].text)
                    first_paras.append(first_paragraph)
                    locations.append(extractWithSpacyLoc(first_paragraph))

                    for para in paragraphs:
                        text = clean_text(para.text)
                        content.append(text)
                        visited_cleaned.extend(extractWithSpacyPlaces(text))

    elif "nomadicmatt" in url:
        title = soup.find("h1", class_="entry-title")
        if title:
            titles.append(clean_text(title.text))

        content_div = soup.select_one("div.entry-content.single-content")
        if content_div:
            paragraphs = content_div.find_all("p")
            if paragraphs:
                first_paragraph = clean_text(paragraphs[1].text)
                first_paras.append(first_paragraph)

                for para in paragraphs:
                    text = clean_text(para.text)
                    content.append(text)
                    visited_cleaned.extend(extractWithSpacyPlaces(text))
                    locations.append(extractWithSpacyLoc(text))

visited_cleaned = list({x for x in visited_cleaned if x and x.strip()})

blog_data.append({
        "Title": title or "N/A",
        "Link": url,
        "First Paragraph": first_paragraph or "N/A",
        "Location": locations or "N/A",
        "Visited Places": ', '.join(visited_cleaned) if visited_cleaned else "None",
        "Content": '\n\n'.join(content) if content else "No content available"
})

# Output
print("Content extracted successfully.\n")

for i in range(len(links)):
    print("Place:", i)
    print("Title:", titles[i] if i < len(titles) else "N/A")
    print("Link:", links[i])
    print("First Paragraph:", first_paras[i] if i < len(first_paras) else "N/A")
    print("Location:", locations[i] if i < len(locations) else "N/A")

    print("Visited Places:")
    for j, place in enumerate(visited_cleaned):
        print(f"  {j+1}. {place}")

    print("\n" + "*"*50 + "\n")


df = pd.DataFrame(blog_data)

# Write the DataFrame to a CSV file
df.to_csv('travel.csv', index=False, encoding='utf-8')

# Save the DataFrame to a JSON file
df.to_json('travel.json', orient='records', lines=True, force_ascii=False, indent=4)
