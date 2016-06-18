=======
Scraper
=======

Description
-----------

A simple web scraping framework for quickly and easily scraping websites.


Installation
------------

To install the framework, run the `setup.py` script::

    python3 setup.py install

Quickstart
----------

The spider works by processing "jobs", these jobs are handled by a method 
called `do_jobName()`. To schedule new jobs to be processed, you create a 
`Job` object and then yield it.

To start off the spider, you specify a list of initial urls, `initial_urls`, 
and then a handler to handle the initial jobs, `do_initial()`.

Each job handler is passed the job and it's corresponding page object. A `Page`
is simply a wrapper around a response from the powerful `requests`_ library.
It also has a couple helper methods, `find()` and `find_all()` which give
the user the ability to interact with a `BeautifulSoup`_ representation of
the response page.

A `Job` is pretty much a wrapper around a request for the `requests`_ library
with a name attached to it. Any extra parameters given to the job will be 
passed on to the request.

The following example will go to the front page of Wikipedia, grabbing all 
links which point to other Wikipedia pages. The scraper will then process these
links by first printing the url and then finding all the images on the page,
printing out their alt text.

::

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
        bob.wait()

    if __name__ == "__main__":
        main()
