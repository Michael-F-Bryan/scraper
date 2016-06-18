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

    class Spidey(BaseScraper):
        initial_urls = ['http://wikipedia.com/']
            
        def do_initial(self, job, page):
            """
            Process all the pages in our `Spidey.initial_urls` list.
            """
            for tag in page.find_all('a'):
                # Get the tag's href and turn it from a relative to
                # absolute url (urljoin will ignore page.url if the href
                # is already an absolute URL)
                href = tag['href']
                url = urljoin(page.url, href)

                if 'www.wikipedia.com' not in url:
                    continue
                    
                # Yield a "Job" to add it to the job queue
                yield Job('link', url)
                
        def do_link(self, job, page):
            """
            Process all "link" jobs.
            """
            print('Scraping page: {}'.format(page.url))

            # Get all the images on the page and print their alt text
            for img in page.find_all('img'):
                if 'alt' in img:
                    print(img['alt'])


.. _requests: http://docs.python-requests.org/en/master/
.. _BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
