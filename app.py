import urllib2, google, bs4, re
from flask import Flask, render_template, request
from itertools import chain
from nltk.corpus import stopwords
from operator import itemgetter
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
@app.route("/home",methods=["GET","POST"])
@app.route("/home/",methods=["GET","POST"])
def home():
    query = "Who is the lead singer of radiohead?"
    if request.method == "POST":
        query = request.form["query"]
    if re.findall("(who)",query.lower()):
        WhoFinal = whoSearch(query)
        return render_template("home.html", result = WhoFinal)
        
    return render_template("home.html")

def whoSearch(query):
    N = 10
    stopList =  stopwords.words('english')
    x = 0
    
    while x < len(stopList):
        try:
            stopList[x] = stopList[x].encode("ascii","ignore")
        except Exception:
            stopList[x] = stopList[x]
        x = x+1
    stopList = stopwords.words("english")
    print stopList
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
    rawString = ' '.join([word for word in rawString.split() if word not in stopList])
    
    whoPattern = "([A-Z]+[a-z]+[\.][ ])?([A-Z]+[a-z]+[ ])([A-Z]+[a-z]+[ ])"
    result = re.findall(whoPattern,rawString)
    print result
    #result = list(chain.from_iterable(result))
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
    partSet = set(particles)
    partDict = {}
    for part in partSet:
        partDict[part] = 0
    for part in particles:
        partDict[part] = partDict[part] + 1
    print partDict
    
    #possibleNames = sorted(list(set(result)), key=len)[::-1]
    nameSet = set(result)
    nameDict = {}
    for name in nameSet:
        nameDict[name] = 0
    for name in result:
        nameDict[name] = nameDict[name] + 1
    
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
    print possibleNames
    for name in possibleNames:
        if not found and mainPart in name[0]:
            found = True
            Result = name[0]
    return Result

if __name__ == "__main__":
   app.debug = True
   app.secret_key = "Secret secrets"
   app.run(host="0.0.0.0", port=8000)
