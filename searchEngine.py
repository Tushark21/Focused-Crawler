import requests
import re
import mysql.connector
import webbrowser
from bs4 import BeautifulSoup
from tkinter import *
from tkinter.ttk import *
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
urlSearched=['','','','','','','','','','']


def openLink(link):
    webbrowser.open(link)

window=Tk()

linkButton=[]
linkButton.append(Button(window,command=lambda:openLink(urlSearched[0])))
linkButton.append(Button(window,command=lambda:openLink(urlSearched[1])))
linkButton.append(Button(window,command=lambda:openLink(urlSearched[2])))
linkButton.append(Button(window,command=lambda:openLink(urlSearched[3])))
linkButton.append(Button(window,command=lambda:openLink(urlSearched[4])))
linkButton.append(Button(window,command=lambda:openLink(urlSearched[5])))
linkButton.append(Button(window,command=lambda:openLink(urlSearched[6])))
linkButton.append(Button(window,command=lambda:openLink(urlSearched[7])))
linkButton.append(Button(window,command=lambda:openLink(urlSearched[8])))
linkButton.append(Button(window,command=lambda:openLink(urlSearched[9])))

pagesReq=6

def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2)) 

#search query words in keywords
def findText(word,text):
    
    #print(word,":",text)
    #print(word,re.search(word,text),(re.search(word,text) is not re.search('3','dummy')));
    if (re.search(word+' ',text) is not re.search('3','dummy')) :
        #print(word,":",text)
        return True
        
    return False

#Searching Query
def searchQuery(queryField,resultLabel):

    for btn in linkButton:
        btn.place(x=1000,y=1000)
    
    query=queryField.get()
    query=query.upper()
    inputQuery=re.split('\s',query)


    print("query:",query)
    if len(query)==0:
        resultLabel.set("Query Field is Empty")
        return

    mycursor.execute("SELECT * FROM links")
    myResult = mycursor.fetchall()

    reqLinks="Links:\n"

    #2d List
    linkSet=[[] for i in range(len(inputQuery))]

    print(linkSet)
    print("Number of Words in Query:",len(inputQuery))

    for row in myResult:
        counter=0;
        #print(row)
        for word in inputQuery:
            if findText(word,row[0]):
                #linkSet[counter].add(row[1])
                tempList=row[1].split('^^^')
                for lnk in tempList:
                    linkSet[counter].append(lnk)
                    print(lnk)
            counter+=1


    #intersection
    inList=linkSet[0]
    #print("inList:",inList)
    #print("linkSet:",linkSet)
    #print("linkSet[0]:",linkSet[0])

    for lst in linkSet:
        inList=intersection(inList, lst)

    #print("inList:",inList)

    pos=0
    for lnk in inList:
        #openLink=partial(openLink,lnk)
        linkButton[pos]['text']=lnk;#=Button(window,text=lnk,command=lambda:openLink).place(x=20,y=240+pos*24)
        linkButton[pos].place(x=20,y=240+pos*24)
        urlSearched[pos]=lnk
        #linkButton[pos]['command']=lambda:openLink(lnk)
        reqLinks+="\n"+lnk
        pos+=1
        if pos==10:
            break

    resultLabel.set("Search Complete")


#Scrapping
def scrape(inputUrl,inputSearchText,resultLabel):
    initialUrl=inputUrl.get()
    inputText=inputSearchText.get()
    print("Seed Url:",initialUrl)
    print("Keyword:",inputText)

    if len(initialUrl)==0 or len(inputText)==0:
        resultLabel.set("URL or Keyword Field is Empty")
        return

    allLinks="Links:\n"
    count=1;
    #initialUrl=input("Enter Initial URL")

    linkList={initialUrl}
    linkPercent=[0]
    for i in linkList:
        soup=""
        try:
            page=requests.get(i)
            soup = BeautifulSoup(page.content, 'html.parser')
        except:
            pass
        
        ###
        inputText=inputText.upper()
        #List of input words
        inputList=re.split('\s',inputText)
        for word in removeWords:
            if word in inputList:
                inputList.remove(word)

        for a in soup.find_all(href=True,text=True):
            if re.match("\Ahttps",a['href']) or re.match("\Ahttp",a['href']) :
                
                try:
                    #print("Link:",a['href'])
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
                        print("Count:",count)
                        for txt in inputList:
                            #print(txt,re.search(txt,text),(re.search(txt,text) is not re.search('3','dummy')),a['href']);
                            if (re.search(txt+' ',text) is not re.search('3','dummy')) :
                                print(txt,re.search(txt,text),(re.search(txt,text) is not re.search('3','dummy')),a['href']);
                                cnt+=1;
                            if cnt>=len(inputList):
                                linkList.add(a['href'])
                                print("Relevant Links:",a['href'])
                                allLinks+='\n'+a['href']
                                count+=1
                                break;
                    
                        mycursor.execute("SELECT * FROM links where keyword='"+text+"'")
                        myResult = mycursor.fetchall()
                        #print("res:",myResult)

                        if myResult:
                            #print("res:",myResult[0][1])
                            sql = "update links set link='"+myResult[0][1]+"^^^"+a['href']+"' where keyword='"+myResult[0][0]+"'"
                            mycursor.execute(sql)
                        else:
                            sql = "INSERT INTO links VALUES (%s,%s)"
                            val = (text,a['href'])
                            mycursor.execute(sql, val)
                        
                        mydb.commit()
                    
                except:
                    #break
                    pass

            if count==pagesReq:
                break
        if count==pagesReq:
            break


    pos=0
    for lnk in linkList:
        #openLink=partial(openLink,lnk)
        linkButton[pos]['text']=lnk;#=Button(window,text=lnk,command=lambda:openLink).place(x=20,y=240+pos*24)
        linkButton[pos].place(x=20,y=240+pos*24)
        urlSearched[pos]=lnk
        #linkButton[pos]['command']=lambda:openLink(lnk)
        pos+=1
        if pos==10:
            break

    print("Training Complete")
    resultLabel.set("Training Succesful...")

#GUI
#window=Tk()
window.geometry("500x500")
window.resizable(0,0)
window.title("Web Scrapper")
url=StringVar()
keywordText=StringVar()
queryText=StringVar()
resultText=StringVar()

#Training Components
urlInputLabel=Label(window,text="Initial URL:").place(x=20,y=20)
keywordInputLabel=Label(window,text="Keyword:").place(x=20,y=60)

urlInputField=Entry(window,textvariable=url).place(x=120,y=20)
textInputField=Entry(window,textvariable=keywordText).place(x=120,y=60)

scrape=partial(scrape,url,keywordText,resultText)
Train=Button(window,text="Train",command=scrape).place(x=120,y=100)

#Searching Components
queryInputLabel=Label(window,text="Enter Query:").place(x=20,y=160)

queryInputField=Entry(window,textvariable=queryText).place(x=120,y=160)
resultLabel=Label(window,textvariable=resultText,anchor=CENTER).place(x=180,y=480)

searchQuery=partial(searchQuery,queryText,resultText)
submit=Button(window,text="Search",command=searchQuery).place(x=120,y=200)

window.mainloop()