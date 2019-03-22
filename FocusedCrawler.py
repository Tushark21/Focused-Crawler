import requests
import re
from bs4 import BeautifulSoup
from tkinter import *
from functools import partial

#initialUrl="https://www.javatpoint.com/python-tkinter"

pagesReq=2

#Scrapping
def scrape(inputUrl,inputSearchText,linksLabel):
    initialUrl=inputUrl.get()
    inputText=inputSearchText.get()
    print(initialUrl)
    allLinks="Links:\n"
    count=1;
    #initialUrl=input("Enter Initial URL")

    linkList=[initialUrl]
    linkPercent=[0]
    for i in linkList:
        page=requests.get(i)
        soup = BeautifulSoup(page.content, 'html.parser')
        ###
        inputText=inputText.upper()
        inputList=re.split('\s',inputText)
        for a in soup.find_all(href=True,text=True):
            if re.match("\Ahttps",a['href']) or re.match("\Ahttp",a['href']) :
                tempPage=requests.get(a['href'])
                tempSoup=BeautifulSoup(tempPage.content,'html.parser')
                #print(tempSoup)
                tag=tempSoup.find('meta', attrs={'name':'description'})#find('meta',name='description')
                #print(tag)
                if tag:
                    text=tag['content']
                    #print(text)
                    text=text.upper()
                    text.strip()
                    cnt=0
                    for txt in inputList:
                        print(txt,re.search(txt,text),(re.search(txt,text) is not re.search('3','dummy')),a['href']);
                        if (re.search(txt,text) is not re.search('3','dummy')) :
                            cnt+=1;
                        if cnt==len(txt):
                            linkList.append(a['href'])
                            allLinks+='\n'+a['href']
                            count+=1
                            break;
            if count==pagesReq:
                break
        if count==pagesReq:
            break
	###
    linksLabel.set(allLinks)
"""
	for i in linkList:
		
		page=requests.get(i)
		
		soup = BeautifulSoup(page.content, 'html.parser')
		k=0
		score=0
		total=1

		allLinks=allLinks+"\n"+i+" : "
		for tag in soup.find_all('h1',text=True):
			#if re.match("\Ahttps",a['href']) or re.match("\Ahttp",a['href']):
			text=tag.get_text()
			text=text.upper()
			inputText=inputText.upper()
			text.strip()
			temp=""
			
			for ch in text:
				if ch==inputText[k]:
					temp=temp+ch
					k+=1

				else:
					k=0

				if temp==inputText:
					k=0
					temp=""
					score=score+1

				if ch==' ' or ch==':':
					total=total+1
			#print("Found the URL:", a['href'])
		linkPercent.append((score/total)*100)
		allLinks=allLinks+str(score)+"/"+str(total)+":"+str((score/total)*100)+"%"
		#allLinks=allLinks+str((score/total)*100)+"%"
		#print(i)
	linksLabel.set(allLinks)
"""

#https://www.javatpoint.com/python-tkinter

#GUI
window=Tk()
window.geometry("500x500")
window.title("Web Scrapper")
url=StringVar()
searchText=StringVar()
links=StringVar()

inputLabel=Label(window,text="Initial URL:").place(x=20,y=20)
textInputLabel=Label(window,text="Keyword:").place(x=20,y=60)
linksLabel=Label(window,textvariable=links).place(x=20,y=150)

urlInputField=Entry(window,textvariable=url).place(x=120,y=20)
textInputField=Entry(window,textvariable=searchText).place(x=120,y=60)

scrape=partial(scrape,url,searchText,links)
submit=Button(window,text="Submit",command=scrape).place(x=120,y=100)

window.mainloop()

"""page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")"""
#page=requests.get("https://www.good.is/");
"""print(page.content)"""

#soup = BeautifulSoup(page.content, 'html.parser')

""" or re.match("\Awww",a['href'])"""

