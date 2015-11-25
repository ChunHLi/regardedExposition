import urllib2, google, bs4, re
from flask import Flask, render_template, request
from itertools import chain
from nltk.corpus import stopwords
from operator import itemgetter
from collections import OrderedDict
from dateutil.parser import parse
app = Flask(__name__)

#For 1000$ I will stop writing such shitty code. Please make your checks billable to Albert Mokrejs.

@app.route("/",methods=["GET","POST"])
@app.route("/home",methods=["GET","POST"])
@app.route("/home/",methods=["GET","POST"])
def home():
    query = "Who is the lead singer of radiohead?"
    if request.method == "POST":
        query = request.form["query"]
    if re.findall("(who)",query.lower()):
        WhoFinal = whoSearch(query)
        return render_template("home.html", Answer = WhoFinal[0], Question = query, RunnersUp = WhoFinal[1:6])
    if re.findall("(when)",query.lower()):
        WhenFinal = whenSearch(query)
        return render_template("home.html", Answer = WhenFinal[0], Question = query, RunnersUp = WhenFinal[1:6])
        
    return render_template("home.html")

def whoSearch(query):
    N = 1
    stopList =  stopwords.words('english')
    x = 0
    while x < len(stopList):
        try:
            stopList[x] = stopList[x].encode("ascii","ignore")
        except Exception:
            stopList[x] = stopList[x]
        x = x+1
    results = google.search(query,num=N,start=0,stop=N)
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
    
def whenSearch(query):
    N = 1
    results = google.search(query,num=N,start=0,stop=N)
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
    whenPattern = "((?:(?:\d){1,2} (?:oct|nov|dec|jan|feb|mar|apr|may|jun|jul|aug|sep)\w* (?:\d{4}))|(?:(?:oct|nov|dec|jan|feb|mar|apr|may|jun|jul|aug|sep)\w* (?:(?:\d{1,2})\w{0,2})(?:,? (?:\d{2,4}))?)|(?:(?:\d{1,4})[\/ \-](?:\d{1,4})[\/ \-](?:\d{1,4})))"
    result = re.findall(whenPattern,rawString)
    print result
    x = 0
    while x < len(result):
        result[x] = list(OrderedDict.fromkeys(result[x]))
        x = x + 1
    x = 0
    print result
    while x < len(result):
        z = ""
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
