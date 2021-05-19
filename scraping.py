# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "mars_hemispheres": mars_hemispheres()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url


def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


# 3. Create a function that will scrape the hemisphere data by using your code from the Mission_to_Mars_Challenge.py file
def mars_hemispheres():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Convert the browser html to a soup object
    html = browser.html
    mars_soup = soup(html, 'html.parser')

    # Find the HTML tag that holds all the links to the full-resolution images
    hemispheres_box = mars_soup.find_all('div',class_='item')
    print(hemispheres_box)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # Go through the links and get the url and title
    for index in range(len(hemispheres_box)):
        # create dictionary to store the hemispheres
        #hemispheres = {}

        # Find the hemisphere link and click on it
        image = browser.find_by_css("a.product-item img")[index]
        image.click()

        # Parse the current hermisphere page
        html = browser.html
        mars_soup = soup(html, 'html.parser')

        # Parse the hemisphere title from the page
        image_title = mars_soup.find('h2',class_='title').get_text()
        
        # TEST 1 - use 'sample' as the parent
        parent_class = mars_soup.find('li')
        url_link = parent_class.find('a', target='_blank')['href']
        image_url = (url+url_link)

        # Add image_title and image_url to the dictionary
        entries = {'img_url':image_url,'img_title':image_title}
        hemisphere_image_urls.append(entries)
        
        # Add the current dictionary to the hemisohere_image_urls list
        #hemisphere_image_urls.append(hemispheres)

        # Print(image_title and image_url)
        # print(image_title)
        # print(image_url)
        # print(f'--------------')
        
        # Return to the homepage
        browser.back()
    
    print(hemisphere_image_urls)    
    # return the dictionary with each image url and title. 
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())