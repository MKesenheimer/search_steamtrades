#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import selenium, time
import sys

# read the games you want
wlines = [line.rstrip('\n') for line in open("wgames.list")]
# read the games you have
hlines = [line.rstrip('\n') for line in open("hgames.list")]

browser = webdriver.Firefox()
#browser.get("http://www.steamgifts.com/trades")
#try:
#    input("Please login through Steam and press Enter to continue...")
#except SyntaxError:
#    pass
browser.get("http://www.steamgifts.com/trades")
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
    browser.find_element_by_class_name("trade__search-have").clear()
    browser.find_element_by_class_name("trade__search-want").clear()
    browser.find_element_by_class_name("trade__search-want").send_keys(wlines[i])
    browser.find_element_by_class_name("trade__search-submit").click()
    results = browser.find_element_by_class_name("pagination__results").text
    
    # if the search was succesful, continue
    if results not in "No results were found.":
        for j in range(0,len(hlines)):
            
            # then check every combination
            browser.find_element_by_class_name("trade__search-have").clear()
            browser.find_element_by_class_name("trade__search-have").send_keys(hlines[j])
            browser.find_element_by_class_name("trade__search-want").clear()
            browser.find_element_by_class_name("trade__search-want").send_keys(wlines[i])
            browser.find_element_by_class_name("trade__search-submit").click()
            results  = browser.find_element_by_class_name("pagination__results").text
            
            # if a combination gives results, print informations
            if results not in "No results were found.":
                
                # reset the counters and the flags
                resultsfound = "no"
                ngood = 0
                nbad  = 0
                glinks = []
                blinks = []
                
                # go through all entries
                for entries in browser.find_elements_by_xpath("//*[@class='table__row-outer-wrap']"):
                    
                    # look if the entry is faded (locked), if yes don't print it's informations
                    if not entries.find_elements_by_xpath(".//*[@class='table__row-inner-wrap is-faded']"):
                        resultsfound = "yes"
                        
                        # save the links
                        for info in entries.find_elements_by_xpath(".//*[@class='table__column__heading']"):
                            glinks.append(info.get_attribute("href"))
                            ngood += 1
                    else:
                        if showbad is "yes":
                            resultsfound = "yes"
                        
                        for info in entries.find_elements_by_xpath(".//*[@class='table__column__heading']"):
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






