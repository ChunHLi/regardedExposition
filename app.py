import urllib2, google, bs4, re
from flask import Flask, render_template, request
from itertools import chain
from nltk.corpus import stopwords
from operator import itemgetter
from collections import OrderedDict
from dateutil.parser import parse
app = Flask(__name__)


#/***
#Home
#
#Takes a query given via the website's form field and uses it to generate a Who or When query. When there is no input
#a hardcoded query is used.
#
#Works as intended.
#
#***/
@app.route("/",methods=["GET","POST"])
@app.route("/home",methods=["GET","POST"])
@app.route("/home/",methods=["GET","POST"])
def home():
    query = ""
    if request.method == "POST":
        query = request.form["query"]
    if re.findall("(who)",query.lower()):
        WhoFinal = whoSearch(query)
        return render_template("home.html", Answer = WhoFinal[0], Question = query, RunnersUp = WhoFinal[1:6])
    if re.findall("(when)",query.lower()):
        WhenFinal = whenSearch(query)
        return render_template("home.html", Answer = WhenFinal[0], Question = query, RunnersUp = WhenFinal[1:6])
    return render_template("home.html", Answer = "Mike Zamansky", Question = "Who is the Best Stuy Teacher?", RunnersUp = [])

#/***
#whoSearch
#
#Params: Query: A string to be google'd and then analyzed to find a name as a response.
#
#This method uses the query to find 10 results and then uses a list of stopwords to remove invalid nouns. The text is then
#searched for names consisting of two or three parts. These names are then sorted based on how common they are, and their
#parts are indexed the same way. The most frequent name containing the most frequence part is considered the corrent name.
#The correct name is used to render the webpage.
#
#Works as intended in the sense that it finds names. Sadly, google cannot gaurentee the relevancy of names. Occastionally,
#a city or company name will also be returned which is an issue.
#
#***/
def whoSearch(query):
    stopList =  stopwords.words('english')
    x = 0
    while x < len(stopList):
        try:
            stopList[x] = stopList[x].encode("ascii","ignore")
        except Exception:
            stopList[x] = stopList[x]
        x = x+1
    results = google.search(query,num=10,start=0,stop=10)
    rlist = []
    for r in results:
        rlist.append(r)
    rawlist = []
    rawString = ""
    for x in rlist:
        url = urllib2.urlopen(rlist[0])
        raw = url.read()
        text = re.sub("[ \t\n]+"," ",raw)
        rawlist.append(text)
        rawString = rawString + text + " "
    for word in stopList:
        rawString = re.sub(word + " ","",rawString)
    
    whoPattern = "([A-Z]+[a-z]+[\.][ ])?([A-Z]+[a-z]+[ ])([A-Z]+[a-z]+[ ])"
    result = re.findall(whoPattern,rawString)
    x = 0
    while x < len(result):
        z = ""
        for y in result[x]:
            z = z + y
        result[x] = z
        x = x+1
    particles = []
    subPattern = "[A-Z]+[a-z]+[\.]?"
    for sub in result:
        subParts = re.findall(subPattern,sub)
        particles = particles + subParts
    partDict = count(particles)
    nameDict = count(result)
    possibleNames = sorted(nameDict.iteritems(), key=itemgetter(1), reverse=True)
    counter = 0
    current = ""
    for key in partDict.keys():
        if partDict[key] > counter:
            counter = partDict[key]
            current = key
    mainPart = current
    found = False
    Result = ""
    finals = []
    print possibleNames
    for name in possibleNames:
        if mainPart in name[0] and not found:
            finals.append(name[0])
            found = True
    for name in possibleNames:
        finals.append(name[0])
    return finals[0:6]

#/***
#whenSearch
#
#Params: Query: A string to be google'd and then analyzed to find a date as a response.
#
#This method uses the query to find 10 results from which it searches for dates. It then attempts to convert them to a
#consistent format and then sorts those dates based on frequency. The most common date is returned as the answer and is 
#used to render the webpage.
#
#Essentially broken. It'll find some dates but because not all dates are formatted the same way, the format conversion
#will often fail in weird ways. This makes the results rather odd and unpredictable. Making it work would probably 
#require a full, elaborate, rewrite. My bad.
#
#***/
def whenSearch(query):
    results = google.search(query,num=10,start=0,stop=10)
    rlist = []
    for r in results:
        rlist.append(r)
    print rlist
    rawlist = []
    rawString = ""
    for x in rlist:
        url = urllib2.urlopen(rlist[0])
        raw = url.read()
        text = re.sub("[ \t\n]+"," ",raw)
        rawlist.append(text)
        rawString = rawString + text + " "
    whenPattern = "((?:(?:\d){1,2} (?:oct|nov|dec|jan|feb|mar|apr|may|jun|jul|aug|sep)\w* (?:\d{4}))|(?:(?:oct|nov|dec|jan|feb|mar|apr|may|jun|jul|aug|sep)\w* (?:(?:\d{1,2}))(?:,? (?:\d{2,4}))?)|(?:(?:\d{1,4})[\/ \-](?:\d{1,2})[\/ \-](?:\d{4})))"
    result = re.findall(whenPattern,rawString)
    x = 0
    while x < len(result):
        result[x] = re.sub("(october|October)", "10", result[x])
        result[x] =re.sub("(november|November)", "11", result[x])
        result[x] =re.sub("(december|December)", "12", result[x])
        result[x] =re.sub("(january|January)", "1", result[x])
        result[x] =re.sub("(february|February)", "2", result[x])
        result[x] =re.sub("(march|March)", "3", result[x])
        result[x] =re.sub("(april|April)", "4", result[x])
        result[x] =re.sub("(may|May)", "5", result[x])
        result[x] =re.sub("([.]une)", "6", result[x])
        result[x] =re.sub("([.]uly)", "7", result[x])
        result[x] =re.sub("([.]ugust)", "8", result[x])
        result[x] =re.sub("([.]eptember)", "9", result[x])
        x = x + 1
    print result
    x = 0
    while x < len(result):
        result[x] = list(OrderedDict.fromkeys(result[x]))
        x = x + 1
    x = 0
    print result
    while x < len(result):
        z = ""
        print result[x]
        for y in result[x]:
            z = z + y
            z = re.sub("[ \-\/]"," ",z)
        try:
            result[x] = parse(z).strftime('%d/%m/%Y')
        except Exception:
            result[x] = z
        x = x+1
    partDict = count(result)
    possibleDates = sorted(partDict.iteritems(), key=itemgetter(1), reverse=True)
    finals = []
    for date in possibleDates:
        finals.append(date[0])
    if len(finals) < 6:
        return finals[0:len(finals)]
    return finals[0:6]
    
    
#/***
#count
#
#Params: Result: A list of items.
#
#Creates a dictionary containing the ammount of occurences of each item in result. 
#
#Works as intended.
#
#***/
def count(result):
    partSet = set(result)
    partDict = {}
    for part in partSet:
        partDict[part] = 0
    for part in result:
        partDict[part] = partDict[part] + 1
    return partDict

if __name__ == "__main__":
   app.debug = True
   app.secret_key = "Secret secrets"
   app.run(host="0.0.0.0", port=8000)
