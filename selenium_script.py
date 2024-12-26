from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from googletrans import Translator
from collections import Counter


def count_repeatition(translated_headers):
    words = translated_headers.lower().split()
    word_counts = Counter(words)
    repeated_words = {word: count for word, count in word_counts.items() if count > 2}

    for word, count in repeated_words.items():
        print(f"{word}: {count}")


def translate_to_english(message):
    """Translates text to English."""
    try:
        translator = Translator()
        detect_lang = translator.detect(message)
        translation = translator.translate(message,src='es',dest='en').text
        return translation
    except Exception as e:
        print(f"Error translating message: {e}")
        return message


# Configure the Selenium WebDriver
chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)  # Ensure ChromeDriver is installed and in your PATH



# URL of the website
base_url = "https://elpais.com/opinion"

try:
    # Step 1: Open the main webpage
    driver.get(base_url)
    time.sleep(3)  # Allow the page to load

    # Step 2: Handle User Agreement or Cookie Popup
    try:
        # Locate the "Accept" button (adjust selector based on the website)
        accept_button = driver.find_element(By.ID, "didomi-notice-agree-button")  # Example XPath
        accept_button.click()
        print("User agreement popup accepted.")
        time.sleep(2)  # Allow time for the popup to close
    except Exception as e:
        print("No user agreement popup detected or unable to close it.")

    # Step 3: Navigate to the "Opinion" section
    opinion_link = driver.find_element(By.LINK_TEXT, "Opinión")  # 'Opinión' is Spanish for 'Opinion'
    opinion_link.click()
    time.sleep(3)


    # Step 4: Scrape articles from the "Opinion" section
    max_articles = 5  # Limit to the first 5 articles
    scraped_articles = 0

    while scraped_articles < max_articles:
        # Fetch all available articles after returning to the "Opinion" section
        articles = driver.find_elements(By.CSS_SELECTOR, "h2.c_t")  # Adjust the selector based on the website structure

        # Check if there are enough articles to scrape
        if len(articles) == 0:
            print("No articles found on the page.")
            break

        if scraped_articles >= len(articles):
            print(f"Only {len(articles)} articles available. Stopping the scrape.")
            break

        try:
            # Select the current article
            article = articles[scraped_articles]

            # Get the title and link
            title = article.text
            article_link = article.find_element(By.TAG_NAME, "a").get_attribute("href")

            # Navigate to the article page
            driver.get(article_link)
            time.sleep(3)

            # Scrape the content
            paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")  # Adjust selector based on content structure
            content = "\n".join([p.text for p in paragraphs])

            # Print the article details
            print(f"Article {scraped_articles + 1}:")
            print(f"Title: {title}\n")
            print(f"Title(English): {translate_to_english(title)}\n")
            print(f"Content:\n{content}\n")
            print(f"Content(English):\n{translate_to_english(content)}\n")
            print("-" * 80)

            scraped_articles += 1  # Increment the counter for scraped articles

            # Go back to the Opinion page
            driver.back()
            time.sleep(3)

        except Exception as e:
            print(f"Error fetching article {scraped_articles + 1}: {e}")

    print('Analyze Translated Headers')
    headers_list = []
    combine_headers = articles = driver.find_elements(By.CSS_SELECTOR, "h2.c_t")[:5]
    for i in combine_headers:
        headers_list.append(i.text)
    print(headers_list)
    translated_headers = translate_to_english(' '.join(headers_list))
    print(translated_headers)
    print('Repeated words across headers - ',count_repeatition(translated_headers))
finally:
    # Close the browser
    driver.quit()
