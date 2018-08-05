from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import os

def get_jobs(html):
    # url = "https://www.seek.com.au/Salesforce-jobs/in-All-Sydney-NSW"
    # response = simple_get(url)
    # response = open('example.html').read()

    # if response is not None:
        # html = BeautifulSoup(response, 'html.parser')
    jobs = set()
    for article in html.select('article'):
        # Save the job title
        title = article['aria-label']
        spans = article.select('span')

        # Save the wage, if possible
        money = ""
        for span in spans:
            if span.text.find("$") > -1:
                money = span.text

        if money:
            print(title + "," + money)


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def get_html_from_file(filename):
    return BeautifulSoup(open(filename).read(), 'html.parser')

def get_html_from_url(url):
    return ( BeautifulSoup(simple_get(url), 'html.parser') )

def read_files():
    directory = './pages/'
    for filename in os.listdir(directory):
        print(filename)
        get_jobs( get_html_from_file(directory + filename) )

read_files()