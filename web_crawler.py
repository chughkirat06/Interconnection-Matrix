from urllib.parse import urlparse, urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class WebCrawler:
    def __init__(self, root_url):
        """ root_url: Initialize the WebCrawler with the root URL 
        internal_urls: List to store internal URLs to be crawled 
        scanned_urls: Set to store URLs that have been crawled
        link_dict: Dictionary to store links
        driver: Selenium WebDriver for headless browsing
        interconnection_matrix: DataFrame to store the interconnection matrix """
        self.root_url = root_url
        self.domain = urlparse(root_url).netloc
        self.internal_urls = [root_url]
        self.scanned_urls = set()
        self.link_dict = {}
        self.driver = None
        self.interconnection_matrix = None

    def is_valid_url(self, url):
        """ Checks if a given URL is valid """
        parsed_url = urlparse(url)
        return bool(parsed_url.netloc) and bool(parsed_url.scheme)

    def is_same_domain(self, url):
        """ Checks if a given URL belongs to the same domain as the root URL """
        return urlparse(url).netloc == self.domain

    def scrape_links(self, url):
        """ Extracts all links from the given URL.
        Iterates through 'a' tags, extracts href attribute, and processes the URL.
        Checks if the URL is valid, not already visited, and belongs to the same domain.
        Returns a set of links. """
        try:
            # Downloads HTML content in an object for HTML parsing
            html_soup = BeautifulSoup(requests.get(url).content, "html.parser")

            # Find all 'a' tags in the object
            links = set()
            for a_tag in html_soup.find_all("a"):
                href = a_tag.attrs.get("href")

                if not href or href.startswith("#"):
                    continue

                # Join relative URLs
                full_url = urljoin(url, href)

                # Normalize the URL
                parsed_href = urlparse(full_url)
                full_url = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path.rstrip('/')

                # Check if the URL is valid and belongs to the same domain
                if not self.is_valid_url(full_url) or full_url in self.scanned_urls or not self.is_same_domain(
                    full_url
                ):
                    continue

                links.add(full_url)

            return links

        except requests.exceptions.RequestException as e:
            print(f"Error while scraping links from {url}: {e}")
            return set()

    def build_interconnection_matrix(self, excel_filename='Interconnection_Matrix.xlsx'):
        """ Builds the interconnection matrix DataFrame and saves it to an Excel file. """
        websites = list(self.link_dict.keys())
        matrix_data = []

        # Build matrix data
        for row_website in websites:
            row_data = [row_website]
            for col_website in websites:
                if row_website == col_website:
                    row_data.append('NA')
                elif col_website in self.link_dict[row_website]:
                    row_data.append('Y')
                else:
                    row_data.append('N')
            matrix_data.append(row_data)

        columns = [''] + websites
        self.interconnection_matrix = pd.DataFrame(matrix_data, columns=columns)

        # Save the interconnection matrix to an Excel file
        self.interconnection_matrix.to_excel(excel_filename, index=False)
        print(f"Interconnection Matrix saved to {excel_filename}")

    def crawl(self, max_iterations=100):
        """ Initiates the crawling process. """
        try:
            self.driver = webdriver.Chrome(options=webdriver.ChromeOptions().add_argument("--headless"))
            i = 0

            while self.internal_urls and i < max_iterations:
                url = self.internal_urls.pop(0)

                if url in self.scanned_urls:
                    continue

                i += 1
                self.scanned_urls.add(url)
                self.link_dict[url] = set()

                # Perform scraping on the URL
                links = self.scrape_links(url)
                print(f"{i}. Scanned: {url}")

                # Update link dictionary
                self.link_dict[url] = links

                # Add new links to internal_urls
                self.internal_urls.extend(links)

            # Build the interconnection matrix
            self.build_interconnection_matrix()

            print("Crawling completed successfully.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        finally:
            if self.driver:
                self.driver.quit()

        return self.interconnection_matrix

if __name__ == "__main__":
    try:
        root_url = "https://www.webtoolkit.eu/wt"
        web_crawler = WebCrawler(root_url)
        interconnection_matrix = web_crawler.crawl(max_iterations=1000)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
