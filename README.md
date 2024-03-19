<H1>Web Crawler</H1>
This Python script, web_crawler.py, implements a simple web crawler that crawls a website starting from a given root URL. It extracts all internal links from the website and builds an interconnection matrix based on the links between web pages.

<H2>Usage</H2>
To use the web crawler:

1. Clone this repository to your local machine.
2. Navigate to the directory containing web_crawler.py.
3. Open the script in a text editor or an integrated development environment (IDE) of your choice.
4. Modify the root_url variable in the __main__ block to specify the URL of the website you want to crawl.
5. Optionally, adjust the max_iterations parameter in the crawl method to set the maximum number of iterations for crawling.
6. Run the script using Python: <B>python web_crawler.py</B>
7. The script will crawl the specified website, extract internal links, and build an interconnection matrix.
8. The interconnection matrix will be saved to an Excel file named Interconnection_Matrix.xlsx in the repository directory.

<H2>Customization</H2>
You can customize the behaviour of the web crawler by adjusting the following parameters:

<B>root_url</B>: The root URL of the website to crawl. You can change this URL to crawl a different website.<BR>
<B>max_iterations</B>: The maximum number of iterations for crawling. This parameter controls the depth of the crawl. Increase it for more comprehensive crawling.<BR>
<B>excel_filename</B>: The filename for saving the interconnection matrix Excel file. You can change this filename if needed.<BR>

<H2>Requirements</H2>
The following Python packages are required to run the web crawler:

<B>pandas</B>: For data manipulation and Excel file handling.<BR>
<B>requests</B>: For making HTTP requests.<BR>
<B>beautifulsoup4</B>: For HTML parsing.<BR>
<B>selenium</B>: For headless browsing with WebDriver.<BR>

<H2>Note</H2>
<UL>
<LI> This web crawler uses Selenium WebDriver for headless browsing. Ensure that you have a compatible WebDriver installed and its path configured appropriately.</LI>
<LI> The script may take some time to crawl larger websites depending on the number of pages and the server response time.</LI>
</UL>
