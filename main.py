import sys
import csv

import datetime
from selenium import webdriver

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def main(argv):
    f = raw_input('file with sites: ')
    filename = webanalysis(f)

    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    gfile = drive.CreateFile({'title': filename,
                              "parents": [{"kind": "drive#fileLink", "id": '0BzAvb4VffxhvQ1NZY2JrbW9sOFE'}]})
    gfile.SetContentFile(filename)
    gfile.Upload({'convert': True})


def webanalysis(file):
    filename =str(datetime.datetime.now()) + '.csv'
    myfile = open(filename, 'wb')

    try:
        writer = csv.writer(myfile)
        writer.writerow(('url', 'webcomponents'))

        # driver = webdriver.PhantomJS(
        #        executable_path='/Users/nickbortolotti/CodeDevelopers/Python/scraping/node_modules/phantomjs/bin/phantomjs')
        driver = webdriver.Firefox()
        driver.implicitly_wait(10)

        with open(file) as f:
            for url in f:
                driver.implicitly_wait(10)
                driver.get(url)
                scripts = driver.find_elements_by_tag_name("script")
                wc = False
                for s in scripts:
                    if "webcomponents" in str(s.get_attribute("src")):
                        wc = True
                        break
                    else:
                        wc = False
                        continue
                writer.writerow((url, str(wc)))
        return filename

    finally:
        driver.quit()
        myfile.close()


if __name__ == '__main__':
    main(sys.argv)
