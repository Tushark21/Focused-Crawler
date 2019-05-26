import requests
import re
import mysql.connector
from bs4 import BeautifulSoup
from tkinter import *
from functools import partial

#database setup
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="tushar@123",
  database="searchengine"
)

mycursor = mydb.cursor()

#initialUrl="https://www.javatpoint.com/python-tkinter"
removeWords=['THE','IS','AM','ARE','GO','THIS','WE','A','AN','THAT']

pagesReq=6

def findText(word,text):
    
    print(word,":",text)
    print(word,re.search(word,text),(re.search(word,text) is not re.search('3','dummy')));
    if (re.search(word+' ',text) is not re.search('3','dummy')) :
        return True
        
    return False

#Searching Query
def searchQuery(queryField,linksLabel):
    linksLabel.set(" ")

    query=queryField.get()
    query=query.upper()
    mycursor.execute("SELECT * FROM links")
    myResult = mycursor.fetchall()

    reqLinks="Links:\n"
    inputQuery=re.split('\s',query)

    for row in myResult:
        cnt=0
        print(row)
        for word in inputQuery:
            if findText(word,row[0]):
                cnt+=1

        print(len(inputQuery),":",cnt)
        if cnt==len(inputQuery):
            #reqLinks+="\n"+row[1]
            tempList=row[1].split('^^^')
            for lnk in tempList:
                reqLinks+="\n"+lnk

    linksLabel.set(reqLinks)

#Scrapping
def scrape(inputUrl,inputSearchText):
    initialUrl=inputUrl.get()
    inputText=inputSearchText.get()
    print(initialUrl)
    allLinks="Links:\n"
    count=1;
    #initialUrl=input("Enter Initial URL")

    linkList={initialUrl}
    linkPercent=[0]
    for i in linkList:
        page=requests.get(i)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        ###
        inputText=inputText.upper()
        #List of input words
        inputList=re.split('\s',inputText)
        for word in removeWords:
            if word in inputList:
                inputList.remove(word)

        for a in soup.find_all(href=True,text=True):
            if re.match("\Ahttps",a['href']) or re.match("\Ahttp",a['href']) :
                tempPage=requests.get(a['href'])
                tempSoup=BeautifulSoup(tempPage.content,'html.parser')
                #print(tempSoup)
                tag=tempSoup.find('title')
                #print(tag)

                if tag:
                    text=tag.get_text()
                    #print(text)
                    text=text.upper()
                    text.strip()
                    cnt=0
                    for txt in inputList:
                        print(txt,re.search(txt,text),(re.search(txt,text) is not re.search('3','dummy')),a['href']);
                        if (re.search(txt+' ',text) is not re.search('3','dummy')) :
                            cnt+=1;
                        if cnt==len(inputList):
                            linkList.add(a['href'])
                            allLinks+='\n'+a['href']
                            count+=1
                            break;
                    
                    mycursor.execute("SELECT * FROM links where keyword='"+text+"'")
                    myResult = mycursor.fetchall()
                    #print("res:",myResult)

                    if myResult:
                        print("res:",myResult[0][1])
                        sql = "update links set link='"+myResult[0][1]+"^^^"+a['href']+"' where keyword='"+myResult[0][0]+"'"
                        mycursor.execute(sql)
                    else:
                        sql = "INSERT INTO links VALUES (%s,%s)"
                        val = (text,a['href'])
                        mycursor.execute(sql, val)
                        
                    mydb.commit()


            if count==pagesReq:
                break
        if count==pagesReq:
            break

#GUI
window=Tk()
window.geometry("500x500")
window.title("Web Scrapper")
url=StringVar()
keywordText=StringVar()
queryText=StringVar()
links=StringVar()

#Training Components
urlInputLabel=Label(window,text="Initial URL:").place(x=20,y=20)
keywordInputLabel=Label(window,text="Keyword:").place(x=20,y=60)

urlInputField=Entry(window,textvariable=url).place(x=120,y=20)
textInputField=Entry(window,textvariable=keywordText).place(x=120,y=60)

scrape=partial(scrape,url,keywordText)

Train=Button(window,text="Train",command=scrape).place(x=120,y=100)

#Searching Components
queryInputLabel=Label(window,text="Enter Query:").place(x=20,y=160)

queryInputField=Entry(window,textvariable=queryText).place(x=120,y=160)
linksLabel=Label(window,textvariable=links).place(x=20,y=250)

searchQuery=partial(searchQuery,queryText,links)
submit=Button(window,text="Search",command=searchQuery).place(x=120,y=200)

window.mainloop()