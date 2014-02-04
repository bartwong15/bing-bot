#############
#   GLOBALS #
#############
   
#############
#   IMPORTS #
#############
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import random


def search(driver,searchTerms):
    numLists = len(searchTerms)    
    firstList = random.randint(0,numLists-1)
    firstLen = len(searchTerms[firstList][0])
    secondLen = len(searchTerms[firstList][1])
    print firstLen
    print secondLen
    if firstLen > 0:
        firstTerm = searchTerms[firstList][0][random.randint(0,firstLen-1)]
        print firstTerm
    if secondLen > 0 and random.random() < 0.8:
        secondTerm = searchTerms[firstList][1][random.randint(0,secondLen-1)]
        if random.random() < 0.8:
            secondTerm = secondTerm + ' ' + searchTerms[firstList][1][random.randint(0,secondLen-1)]
        print secondTerm
        fullTerm = firstTerm + ' ' + secondTerm
    else:
        fullTerm = firstTerm
        
    finalTerm = fullTerm
    #   Forget 1 letter
    if random.random() < 0.15:
        print 'Messing up 1 letter'
        breakPoint = random.randint(1,len(fullTerm)-2)
        finalTerm = fullTerm[0:breakPoint]+fullTerm[breakPoint+2:-1]
    print 'Searching for:\t', finalTerm

    #   Clear anything.
    searchbar = driver.find_element_by_id('sb_form_q')
    searchbar.send_keys(Keys.CONTROL,'a')
    searchbar.send_keys(Keys.DELETE)
    try:    
        searchbar.send_keys(finalTerm,Keys.ENTER)
        time.sleep(random.randint(25,45))            
        
        if random.random() < 0.5:
            try:
                linkElement = driver.find_element_by_partial_link_text(finalTerm[1:3])
                print linkElement.text
                linkElement.click()
                time.sleep(random.randint(15,25))
                driver.back()
            except:
                print "No Links found.  Searching again."
        
        if random.random() < 0.0:
            print "waiting for a time."
            time.sleep(60*random.randint(3,5))
    except:
        print 'Problem searching that term...'
    
def loadCredentials(credentialsFile='authenticate.txt'):
    ''' Loads CSV of site,user,passw format '''
    print 'Loading Credentials...'
    users = []
    if os.path.isfile(credentialsFile):
        creds = open(credentialsFile,'r')
        for line in creds:
            print line
            if line[0] != '#':
                tmp = line.strip().rstrip('\n').split(',')
                print tmp
                [site,username,password,numSearches] = line.strip().rstrip('\n').split(',')
                print tmp[0]
                print tmp[1]
                users.append((site,username,password,int(numSearches)))
        return users
    
    
def loadSearchTerms():
    print 'Loading Search Terms'
    fullList = []
    for i in range(1,10):
        filea = 'file'+str(i)+'a.txt'
        fileb = 'file'+str(i)+'b.txt'
        terms=[]
        mods=[]
        if os.path.isfile(filea):
            print 'Opening: ', filea
            termsFile = open(filea,'r')
            for line in termsFile:
                terms.append(line.strip())
        else:
            return fullList
        if os.path.isfile(fileb):
            print 'Opening: ', fileb
            modsFile = open(fileb,'r')
            for line in modsFile:
                mods.append(line.strip())       
        fullList.append((terms,mods))
    return fullList

def main():
    #   Set seed for decision making
    random.seed()
    
    print "Ola"
    
    users = loadCredentials()
    searchTerms = loadSearchTerms()

    for (site,user,password,numSearches) in users:
        
        try:
            driver = webdriver.Firefox()
            if site == 'facebook':
                driver.get('http://www.facebook.com')
                email = driver.find_element_by_id("email")
                email.send_keys(user)
                pwd = driver.find_element_by_id('pass')
                pwd.send_keys(password)
                pwd.send_keys(Keys.ENTER)
                time.sleep(5)
            if site == 'live':
                driver.get('http://www.live.com')
                email = driver.find_element_by_id("i0116")
                email.send_keys(user)
                pwd = driver.find_element_by_id('i0118')
                pwd.send_keys(password)
                pwd.send_keys(Keys.ENTER)
                time.sleep(5)                
                
            driver.get("http://www.bing.com")
            driver.set_window_size(500,500)
            driver.set_window_position(-1000,-1000)
            time.sleep(3)
            for i in range(0,numSearches):
                try:
                    search(driver,searchTerms)
                    assert 'Bing' in driver.title
                except AssertionError:
                    print "Stuck Elsewhere..."
                    driver.get("http://www.bing.com")
        finally:
            driver.quit()
   
    print "done"

    
        
    #time.sleep(1)
    #driver.quit()
if __name__ == '__main__':
    main()

