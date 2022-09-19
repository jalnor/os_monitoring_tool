import socket

import requests
from _socket import gaierror
from bs4 import BeautifulSoup
from urllib3.exceptions import NewConnectionError, MaxRetryError


class WebData:

    def __init__(self, process_name):
        self.get_web_data(process_name)

    def get_web_data(self, process_name):
        space_filler = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor " \
                   "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud " \
                   "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure " \
                   "dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. " \
                   "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit " \
                   "anim id est laborum."
        scrape_url = f'https://www.file.net/process/{process_name.lower()}.html'
        try:
            page = requests.get(scrape_url)
        except (Exception, gaierror, OSError, NewConnectionError, MaxRetryError, ConnectionError):
            return "Please check your internet connection!\n\n", space_filler
        if not page:
            return "No Data Available!\n\n", space_filler

        soup = BeautifulSoup(page.content, 'html.parser')

        print(type(soup.find(id='GreyBox').get_text()))
        return soup.find(id='GreyBox').get_text()
