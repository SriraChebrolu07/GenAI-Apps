from crewai_tools import ScrapeWebsiteTool
from bs4 import BeautifulSoup


class CustomScrapeWebsiteTool(ScrapeWebsiteTool):
    def get_links(self):
        """
        Extracts and returns all the links from the webpage.
        """
        soup = BeautifulSoup(self.content, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a', href=True)]
        return links


tool = CustomScrapeWebsiteTool(website_url="https://www.staidlogic.com/")
text = tool.run()


print("Text content of the webpage:")
print(text)

links = tool.get_links()
print("\nTotal links on the webpage:", len(links))
print("URLs of all links:")
for link in links:
    print(link)