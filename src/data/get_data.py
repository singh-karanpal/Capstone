# author: Carlina Kim, Karanpal Singh, Sukriti Trehan, Victor Cuspinera
# date: 2020-06-05

'''This script will download data from any URL and saves it in directory
specified. There are 2 parameters URL and Output Path where you want to
write this data.
Usage: get_data.py --url=<url> --file_location=<file_location>
'''

import requests
from docopt import docopt
import pandas as pd

opt = docopt(__doc__)

def main(url, file_location):
    """
    This method will download data from URL and save it to a project directory
    
    Arguments:
    ----------
    url: String
    url as a string
    
    file_location: String
    output file path as a string
    
    Return:
    ----------
    f.write(r.content): file
    data file saved to specified project directory
    """
    
    # download and save data
    r = requests.get(url)
    with open(file_location, "wb") as f:
        f.write(r.content)

    test(file_location)

def test(file_location):
    df = pd.read_csv(file_location)
    assert df.shape[0] != 0
    print(f"file successfully saved to {file_location}")


if __name__ == "__main__":
    main(opt["--url"], opt["--file_location"])
