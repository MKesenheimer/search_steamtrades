#!/usr/bin/python

# selenium and the latest gecko driver are necessary
# Download the geckodriver from https://github.com/mozilla/geckodriver/releases
# and copy it to ~/local/bin
# use sudo pip install -U selenium to update selenium

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint

import selenium, time
import sys

# read the games you want
wlines = [line.rstrip('\n') for line in open("wgames.list")]
# read the games you have
hlines = [line.rstrip('\n') for line in open("hgames.list")]

browser = webdriver.Firefox()
browser.get("https://www.steamtrades.com/trades")
#try:
#    input("Please login through Steam and press Enter to continue...")
#except SyntaxError:
#    pass
#browser.get("https://www.steamtrades.com/trades")
results = "No results were found."

# don't show or show the locked links
#showbad = "yes"
showbad = "no"

# colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

for i in range(0, len(wlines)):
    
    # first check if the game exists:
    url = "https://www.steamtrades.com/trades/search?"
    #link = url+"have="+hlines[0]+"&want="+wlines[i]
    link = url+"want="+wlines[i]
    #print link
    browser.get(link)
    results = browser.find_element_by_class_name("pagination_results").text
    # reset the browser (sometimes an error occured when the page is still filled)
    browser.get("https://www.steamtrades.com/trades")
    
    # if the search was succesful, continue
    if results not in "No results were found.":
        for j in range(0,len(hlines)):
            
            # reset
            results = "No results were found."
            
            # then check every combination
            url = "https://www.steamtrades.com/trades/search?"
            link = url+"have="+hlines[j]+"&want="+wlines[i]
            browser.get(link)
            results = browser.find_element_by_class_name("pagination_results").text
            #print results
            # if a combination gives results, print informations
            if results not in "No results were found.":
                
                # reset the counters and the flags
                resultsfound = "no"
                ngood = 0
                nbad  = 0
                glinks = []
                blinks = []
                
                # go through all entries
                for entries in browser.find_elements_by_xpath("//*[@class='row_outer_wrap']"):
                    
                    # look if the entry is faded (locked), if yes don't print it's informations
                    if not entries.find_elements_by_xpath("//*[@class='row_inner_wrap is_faded']"):
                        resultsfound = "yes"
                        
                        # save the links
                        for info in entries.find_elements_by_xpath("//*[@class='row_inner_wrap']//*[@class='column_flex']/h3/a"):
                            #print info.text
                            #print info.get_attribute("href")
                            glinks.append(info.get_attribute("href"))
                            ngood += 1
                            
                    else:
                        if showbad is "yes":
                            resultsfound = "yes"
                        
                        for info in entries.find_elements_by_xpath("//*[@class='row_inner_wrap']//*[@class='column_flex']/h3/a"):
                            blinks.append(info.get_attribute("href"))
                            nbad += 1
                
                # now print the links if results found
                if resultsfound is "yes":
                    print bcolors.OKBLUE+"Found results for [H]",bcolors.HEADER+hlines[j],bcolors.OKBLUE+"[W]",bcolors.HEADER+wlines[i],bcolors.OKBLUE+":",results,bcolors.ENDC
                    if showbad is "yes":
                        print "-> Good entries:"
                    for k in range(0,ngood):
                        print "  ",glinks[k]
                
                    if showbad is "yes":
                        print "-> Bad entries:"
                        for k in range(0,nbad):
                            print "  ",blinks[k]

                # stop for debugging
                #sys.exit(1)
    print ""
