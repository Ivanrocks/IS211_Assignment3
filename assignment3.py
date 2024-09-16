import argparse
import urllib.request
import csv
import re
import datetime
import logging

logging.basicConfig(
    filename="error.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
logger = logging.getLogger("assignment2")

class DownloadDataException(Exception):
    """
    Exception raised when there is an error downloading data from URL
    """
    pass

class CountImagesException(Exception):
    """
    Exception raised when there is an error counting images in file
    """
    pass

class CountBrowsersException(Exception):
    """
    Exception raised when there is an error counting browsers in file
    """
    pass

class ExtractHoursException(Exception):
    """
    Exception raised when there is an error counting browsers in file
    """
    pass


def main(url):
    print(f"Running main with URL = {url}...")
    try:
        #downloading csv file
        content = download_data(url)
    except:
        logger.error("Error downloading the file")
        raise DownloadDataException

    try:
        #counting images and printing results
        count_images(csv.reader(content.splitlines()))
    except:
        logger.error("Error counting the images")
        raise CountImagesException

    try:
        #Counting hits by browser and printing results
        count_browsers(csv.reader(content.splitlines()))
    except:
        logger.error("Error counting the browsers")
        raise CountBrowsersException

    try:
        #Extracting the hours and printing results
        extract_hours(csv.reader(content.splitlines()))
    except:
        logger.error("Error extracting the hours from file")
        raise ExtractHoursException

def extract_hours(csvContent):
    """
    Extracts number of hits per hour and prints a sorted list by total number of hits
    :param csvContent: the content of the csv file
    :return:
    """
    datePattern = '%Y-%m-%d %H:%M:%S'
    hoursDict = {}

    hour = 0
    print("Extracting hours...")
    for line in csvContent:
        hour = datetime.datetime.strptime(line[1],datePattern).strftime("%H")
        if hour in hoursDict:
            hoursDict[hour] +=1
        else:
            hoursDict[hour] = 1

    #Print sorted hours by number of hits
    """    while hoursDict.items():
        
    """
    highest = "00"
    sortedHours = sorted(hoursDict.items(), key=lambda kv: (kv[1],kv[0]) ,reverse=True)

    for item in sortedHours:
        print("Hour {} has {} hits".format(item[0],item[1]))




def count_images(csvContent):
    pattern = "[^\\s]+(.*?)\\.(jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF)$"
    totalRows = 0
    imagesCounter = 0
    print("Counting Images....")
    for line in csvContent:
        #counting images. index 0 has the name of the files
        if re.search(pattern,line[0]):
            imagesCounter +=1
        totalRows += 1
    imgPercentage = (imagesCounter / totalRows) * 100

    print("Images requests accounted for:", imgPercentage, "% of all requests")

def count_browsers(csvContent):
    """
    Counts the browsers used to visit the site.
    Prints the most popular browser
    :param csvContent: the content of the csv file
    :return:
    """
    browsers = {
        "Firefox":0,
        "Chrome": 0,
        "Internet Explorer": 0,
        "Safari": 0
    }

    popular = "Firefox"
    firefoxPattern = "Firefox"
    chromePattern = "Chrome"
    safariPattern = "Safari"
    IEPattern = "MSIE"
    # counting browsers. index 2 has the name of the browsers
    print("Counting Browsers....")

    for line in csvContent:
        if re.search(firefoxPattern,line[2]):
            browsers["Firefox"] +=1
        elif re.search(chromePattern,line[2]):
            browsers["Chrome"] +=1
        elif re.search(safariPattern, line[2]):
            browsers["Safari"] += 1
        elif re.search(IEPattern, line[2]):
            browsers["Internet Explorer"] += 1
    #Finding the most popular browser
    for browser in browsers:
        if browsers[browser] > browsers[popular]:
            popular = browser
        print(browser+":",browsers[browser])

    print("The most popular browser is",popular)


def download_data(url):
    """
    Reads the data from a URL
    :param URL: the URL to download the file from
    :return: The content of the downloaded file csv
    """

    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')

if __name__ == "__main__":
    """Main entry point"""

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
    

    #main("http://s3.amazonaws.com/cuny-is211-spring2015/weblog.cs")
    
