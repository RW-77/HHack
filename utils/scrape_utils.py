from PIL import Image

from datetime import datetime

import PyPDF2
import json

from operator import itemgetter

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

def extractor(pdf_file):
    pdfReader = PyPDF2.PdfReader(pdf_file)
    
    pageObj = pdfReader.pages[1]
    allText = pageObj.extract_text()
    print(allText)
    arrText = allText.split("\n")
    start=[0]*10
    j=0
    for i in range(len(arrText)):
        if "Date" in arrText[i] and len(arrText[i])>30:
            start[j]=i
            j+=1
    start[j]=(len(arrText))
    #start stores the lines in arrText where the student has the classes and also the final line in arrText.
    mon=[]
    tue=[]
    wed=[]
    thu=[]
    fri=[]
    for i in range(j):
        print("\n"+arrText[start[i]][0:8])
        for k in range(start[i],start[i+1]):
            if "Building" in arrText[k]:
                print(arrText[k-1])
                if('M ' in arrText[k-1]):
                    mon.append("Class~"+arrText[start[i]][0:8]+"|Building~"+arrText[k][9:13]+ "|Room~"+arrText[k][20:24].replace(" ", "")+"|Start~"+ arrText[k-1][arrText[k-1].index("Time")+6:arrText[k-1].index("Time")+11]+"|End~"+ arrText[k-1][arrText[k-1].index("Time")+14:len(arrText[k-1])])
                if('T ' in arrText[k-1]):
                    tue.append("Class~"+arrText[start[i]][0:8]+"|Building~"+arrText[k][9:13]+ "|Room~"+arrText[k][20:24].replace(" ", "")+"|Start~"+ arrText[k-1][arrText[k-1].index("Time")+6:arrText[k-1].index("Time")+11]+"|End~"+ arrText[k-1][arrText[k-1].index("Time")+14:len(arrText[k-1])])
                if('W ' in arrText[k-1]):
                    wed.append("Class~"+arrText[start[i]][0:8]+"|Building~"+arrText[k][9:13]+ "|Room~"+arrText[k][20:24].replace(" ", "")+"|Start~"+ arrText[k-1][arrText[k-1].index("Time")+6:arrText[k-1].index("Time")+11]+"|End~"+ arrText[k-1][arrText[k-1].index("Time")+14:len(arrText[k-1])])
                if('R ' in arrText[k-1]):
                    thu.append("Class~"+arrText[start[i]][0:8]+"|Building~"+arrText[k][9:13]+ "|Room~"+arrText[k][20:24].replace(" ", "")+"|Start~"+ arrText[k-1][arrText[k-1].index("Time")+6:arrText[k-1].index("Time")+11]+"|End~"+ arrText[k-1][arrText[k-1].index("Time")+14:len(arrText[k-1])])
                if('F ' in arrText[k-1]):
                    fri.append("Class~"+arrText[start[i]][0:8]+"|Building~"+arrText[k][9:13]+ "|Room~"+arrText[k][20:24].replace(" ", "")+"|Start~"+ arrText[k-1][arrText[k-1].index("Time")+6:arrText[k-1].index("Time")+11]+"|End~"+ arrText[k-1][arrText[k-1].index("Time")+14:len(arrText[k-1])])
                print(arrText[k])

    monDict=[]
    tueDict=[]
    wedDict=[]
    thuDict=[]
    friDict=[]

    #print("\nMONDAY:")
    for a in range(len(mon)):
        monDict.append(dict(item.split("~") for item in mon[a].split("|")))
    #print(monDict)
    #print("\nTUESDAY:")
    for a in range(len(tue)):
        tueDict.append(dict(item.split("~") for item in tue[a].split("|")))
    #print(tueDict)
    #print("\nWEDNESDAY:")
    for a in range(len(wed)):
        wedDict.append(dict(item.split("~") for item in wed[a].split("|")))
    #print(wedDict)
    #print("\nTHURSDAY:")
    for a in range(len(thu)):
        thuDict.append(dict(item.split("~") for item in thu[a].split("|")))
    #print(thuDict)
    #print("\nFRIDAY:")
    for a in range(len(fri)):
        friDict.append(dict(item.split("~") for item in fri[a].split("|")))
    #print(friDict)

    finalList=[monDict,tueDict,wedDict,thuDict,friDict]

    # with open('monday.json', 'w') as fp:
    #     json.dump(monDict, fp, indent=4)
    # with open('tuesday.json', 'w') as fp:
    #     json.dump(tueDict, fp, indent=4)
    # with open('wednesday.json', 'w') as fp:
    #     json.dump(wedDict, fp, indent=4)
    # with open('thursday.json', 'w') as fp:
    #     json.dump(thuDict, fp, indent=4)
    # with open('friday.json', 'w') as fp:
    #     json.dump(friDict, fp)
    # with open('final.json', 'w') as fp:
    #     json.dump(finalList, fp)

    pdf_file.close()

    for i in finalList:
        print(i)
    
    return finalList


def mapScreenshoter(origin,destination,image_file):
    
    global time
    global distance
    options = Options()
  
# this parameter tells Chrome that
# it should be run without UI (Headless)
    options.headless = True
  
# initializing webdriver for Chrome with our options
    driver = webdriver.Chrome(options=options)

    #driver.maximize_window() # For maximizing window
    driver.get('https://aggiemap.tamu.edu/map/d')

    driver.find_element(By.CSS_SELECTOR,'[alt="Toggle directions controls (routing and way-finding)"]').click()

    searchBubble = driver.find_elements(By.CSS_SELECTOR,'[placeholder="Choose point or click on the map"]')
    searchBubble[1].click()
    searchBubble[1].send_keys(destination)
    sleep(3)
    searchBubble[1].send_keys("\uE015\uE015\uE007")
    searchBubble[0].click()
    searchBubble[0].send_keys(origin)
    sleep(3)
    searchBubble[0].send_keys("\uE015\uE015\uE007")
    sleep(3)

    searchQuantity = driver.find_elements(By.CLASS_NAME,'quantity')
    sleep(2)
    #for a in searchQuantity:
    #    print(a)
    #    print("i tried to print searchQnty")
    time=(searchQuantity[0].text+" minutes")
    distance=(searchQuantity[1].text+" miles")
    print(time)
    print(distance)
    sleep(1)

    driver.find_element(By.CSS_SELECTOR,'[alt="Toggle directions controls (routing and way-finding)"]').click()

    sleep(5)
    driver.get_screenshot_as_file(image_file)

    im = Image.open(image_file)
    im = im.crop((126, 0, 675, 600))
    im.save(image_file)

    driver.quit()
    print("end...")

def generate(day_obj): # accepts 
    
    now = datetime.now()

    current_time = now.strftime("%H:%M")
    #below im using beginning as 00:00 for testing purposes
    beginning = now.replace(hour=0, minute=1)

    data = day_obj
    classes=[]
    buildings=[]
    rooms=[]
    startClassesTimes=[]
    endClassesTimes=[]

    numOfTravels=len(buildings)-1
    #will need to check if b2b classes are in the same building!
    starting_index=0
    data.sort(key = itemgetter('Start'), reverse=False)
    
    for i in data:
        classes.append(i['Class'])
        buildings.append(i['Building'])
        rooms.append(i['Room'])
        startClassesTimes.append(i['Start'])
        endClassesTimes.append(i['End'])

    #find earliest
    earliest=0
    for i in range(len(startClassesTimes)):
        if(beginning>datetime.strptime(startClassesTimes[i],"%H:%M")):
            earliest=i
            break
    print(earliest)
    print("You will need to go to",buildings[earliest],rooms[earliest],"for",classes[earliest],"at",startClassesTimes[earliest],"first.")
    for i in range(earliest,len(startClassesTimes)):
        if(i!=len(startClassesTimes)-1 and buildings[i]!=buildings[i+1]):
            mapScreenshoter(buildings[i],buildings[i+1],(f"map_{i+1}.png"))