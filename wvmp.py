#!/usr/bin/python
 
#############
# LIBRARIES #
#############

import mechanize
import time
from lxml import html
import json

import demjson


#############
# FUNCTIONS #
#############

def setupBrowser():
    br = mechanize.Browser()
    cj = mechanize.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30')]
    return br

def login(username,password):
    print("[-] LOGIN")
    print("[+] username : " + username)
    print("[+] password : " + password)
    
    br = setupBrowser()

    br.open('https://facebook.com/')
    br.select_form(nr=0)
    br.form['email'] = username
    br.form['pass'] = password
    br.submit()

    # TODO: Catch and try

    print("[-] SUCCESS LOGIN")
    return br

def logout(br):
    print("[-] LOGOUT")
    br.open('https://m.facebook.com/')

    for link in br.links(url_regex="logout.php"):
        br.open('https://m.facebook.com' + link.url)

def getUserID(scrapedCode):
    print("Getting the user ID")
    tree = html.fromstring(scrapedCode)

    idValue = tree.xpath('//img[1]/@id')[1] #Weirdly it returns a list with two elements, the second one is the right ID value

    userID = idValue[19:] # Strip the beginning and get the id
    return userID

def getVisiterID(scrapedCode):
    print("Getting the visiters ID")
    # print(scrapedCode)
    tree = html.fromstring(scrapedCode)

    scriptTags = tree.xpath('//script')
    scriptTag = ""

    for s in scriptTags:
        if "InitialChatFriendsList" in html.tostring(s):
            print("Found")
            scriptTag = html.tostring(s)
            break

    visitersObject = scriptTag.split('shortProfiles:', 1)[-1].rsplit('nearby:', 1)[0][19:-1]

    # Because it is a JS object, the quotes arround the keys are missing. So we gotta add them
    

    with open('visiters.json', 'w') as visiters:
        visiters.write(demjson.decode(visitersObject))


def writeToTestfile(textToSave):
    print("[-] WRITE TO FILE")
    with open('test.html', 'w') as file:
        file.write(textToSave)


#################
# MAIN FUNCTION #
#################

if __name__ == '__main__':

    br = login("jeanggi90@gmail.com", "Dijcfa90")

    response = br.open('https://facebook.com/')
    userID = getUserID(str(response.read()))

    response = br.open('https://facebook.com/' + userID)
    # writeToTestfile(response.read())
    visiterID = getVisiterID(str(response.read()))
    

    logout(br)

