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
browser.get("http://www.steamgifts.com/trades")
try:
    input("Please login through Steam and press Enter to continue...")
except SyntaxError:
    pass
browser.get("http://www.steamgifts.com/trades")
results = "No results were found."

# sort by games you have [hsort] or sort by the games you want [wsort]
sort = "wsort"

if sort is "hsort":
    for j in range(0,len(hlines)):
        for i in range(0, len(wlines)):
            browser.find_element_by_class_name("trade__search-have").clear()
            browser.find_element_by_class_name("trade__search-have").send_keys(hlines[j])
            browser.find_element_by_class_name("trade__search-want").clear()
            browser.find_element_by_class_name("trade__search-want").send_keys(wlines[i])
            browser.find_element_by_class_name("trade__search-submit").click()
            results = browser.find_element_by_class_name("pagination__results").text
            if results not in "No results were found.":
                print "Found results for [H]", hlines[j],"[W]",wlines[i],":",results
        print ""

if sort is "wsort":
    for i in range(0, len(wlines)):
        for j in range(0,len(hlines)):
            browser.find_element_by_class_name("trade__search-have").clear()
            browser.find_element_by_class_name("trade__search-have").send_keys(hlines[j])
            browser.find_element_by_class_name("trade__search-want").clear()
            browser.find_element_by_class_name("trade__search-want").send_keys(wlines[i])
            browser.find_element_by_class_name("trade__search-submit").click()
            results = browser.find_element_by_class_name("pagination__results").text
            if results not in "No results were found.":
                print "Found results for [H]", hlines[j],"[W]",wlines[i],":",results
        print ""