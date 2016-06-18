from concurrent.futures import ThreadPoolExecutor, wait, as_completed
import inspect
from urllib.parse import urljoin, urlsplit, urlparse
from collections import deque
import logging
import sys
import time
import traceback

from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

from .models import Page, Job
from .utils import get_logger



class BaseScraper:
    """
    A base class that all scrapers can inherit from.
    """
    initial_urls = []
    def __init__(self, max_threads=10):
        self.futures = []
        self.pool = ThreadPoolExecutor(max_workers=max_threads)
        self.logger = get_logger(__name__, 'scraper.log') 
        self.shutdown = False
    
    def do_initial(self, job, page):
        """
        Handle a page in the `initial_urls` list. Override to provide
        more functionality.
        """
        raise NotImplemented
            
    def start(self):
        """
        Start the scraper.
        """
        self.logger.info('Starting Scraper')
        for link in self.initial_urls:
            new_job = Job('initial', link)
            self._queue(new_job)
            
    def stop(self):
        """
        Cancel all scheduled jobs, and shutdown the thread pool.
        Blocking until all currently executing jobs are complete.
        """
        self.logger.info('Stopping Scraper')
        self.shutdown = True
        for fut in self.futures:
            fut.cancel()
        self.pool.shutdown()
        
    def status(self):
        """
        Print the number of completed, cancelled, currently running and
        total number of jobs.
        """
        futures = self.futures
        print('Total jobs: {}'.format(len(futures)))
        print('Currently Running: {}'.format(len([fut for fut in futures if fut.running()])))
        print('Completed: {}'.format(len([fut for fut in futures if fut.done() and not fut.cancelled()])))
        print('Cancelled: {}'.format(len([fut for fut in futures if fut.cancelled()])))
        
    def wait(self):
        """
        Block until all jobs are completed, printing a simple progress bar.
        """
        t = tqdm(leave=True)
        while any(not f.done() for f in self.futures):
            time.sleep(0.25)
            t.n = self.number_done()
            t.refresh()
            
    def number_done(self):
        """
        Get the number of completed futures.
        """
        return sum(map(lambda x: 1 if x.done() and not x.cancelled() else 0, self.futures))
            
    def _process_job(self, job):
        """
        Take a job and run it's associated handler, scheduling any
        yielded results to be executed soon.
        """
        self.logger.info('processing job: {}'.format(job))
        
        handler = getattr(self, 'do_'+job.name)
        if handler is None:
            raise ValueError('No method for processing job: {}'.format(job.name))
            
        r = requests.request(job.method, job.url, *job.args, **job.kwargs)
        page = Page(r)
        
        result = handler(job, page)
        
        if inspect.isgenerator(result):
            for job in result:
                self._queue(job)
        else:
            if result:
                self._queue(result)
                
    def _queue(self, job):
        """Queue a job to be executed."""
        if not self.shutdown:
            self.logger.debug('Queueing Job: {}'.format(job))
            fut = self.pool.submit(self._process_job, job)
            fut.add_done_callback(self._callback)
            self.futures.append(fut)
        
    def _callback(self, future):
        """
        A callback called when every future is completed checking
        if there were any errors and passing control to the
        error handler if necessary.
        """
        if future.exception():
            self.error_handler(future, future.exception())
        
    def error_handler(self, future, e):
        """
        A default error handler that will simply log the traceback
        and stop.
        """
        tb = ''.join(traceback.format_tb(e.__traceback__))
        self.logger.error('An error occurred...\n\n'
                          '{tb}\n'
                          '{e.__class__.__name__}: "{e}"\n'.format(tb=tb, e=e))
        self.stop()
