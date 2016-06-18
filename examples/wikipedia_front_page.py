from urllib.parse import urljoin
from scraper.spider import BaseScraper
from scraper.models import Job

class Scraper(BaseScraper):
    initial_urls = ['https://en.wikipedia.org/']

    def do_initial(self, job, page):
        """
        Process all the pages in our `Spidey.initial_urls` list.
        """
        # Get the "On This Day" list
        on_this_day = page.find(id='mp-otd')

        print('On this day...')

        # Print each list item
        for line in on_this_day.find_all('li'):
            print(line.text.strip())

        # Now get a random wikipedia page
        random_url = 'https://en.wikipedia.org/wiki/Special:Random'
        yield Job('random', random_url)

    def do_random(self, job, page):
        """
        Process all "link" jobs.
        """
        print('Scraping page: {}'.format(page.url))

        # How many images are on this page?
        images = page.find_all('img')

        print('There are {} images on this page.'.format(len(images)))

def main():
    bob = Scraper()
    bob.start()

    try:
        bob.wait()
    except KeyboardInterrupt:
        bob.stop()
        
    bob.status()

if __name__ == "__main__":
    main()
