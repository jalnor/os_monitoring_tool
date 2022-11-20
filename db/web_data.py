import os

import requests


def get_web_data(process_name, os_name):
    """Call external service for process information.

    Keyword arguments:
    process_name -- the name of the process to obtain information on
    os_name      -- the operating system used by caller
    """
    space_filler = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor " \
               "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud " \
               "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure " \
               "dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. " \
               "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit " \
               "anim id est laborum."

    url = f'{os.environ["web_lookup"]}{process_name}&{os_name}'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        return f'{str(error).split(":")[1:2]}\n\n{space_filler}'
    except requests.exceptions.ConnectionError as error:
        return f'{str(str(error).split(":")[1:2])[2:23] + ":"}\n\n{"Please check your internet connection."}'
    return response.text
