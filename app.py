import urllib2, google, bs4, re
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
@app.route("/home",methods=["GET","POST"])
@app.route("/home/",methods=["GET","POST"])
def home():
    query = "Who is the lead singer of radiohead?"
    if request.method == "POST":
        query = request.form["query"]
    for space in [' ']:
        query = query.replace(space, "%20")
    
    N = 10
    results = google.search(query,num=N,start=0,stop=N)
    rlist = []
    for r in results:
        rlist.append(r)
    rawlist = []
    rawString = ""
    for x in rlist:
        url = urllib2.urlopen(rlist[0])
        page = url.read()
        soup = bs4.BeautifulSoup(page,'lxml')
        raw = soup.get_text()
        text = re.sub("[ \t\n]+"," ",raw)
        rawlist.appned(text)
        rawString = rawString + text + " "
    
    whoPattern = "([A-Z]+[a-z]+[\.]?) ([A-Z]+[a-z]+[ ]?)([A-Z]+[a-z]+[ ]?)?"
    result = findall(pattern,rawString)
    particles = []
    subPattern = "([A-Z]+[a-z]+[\.]?)"
    for sub in result:
        subParts = findall(subPattern,sub)
        particles = particles + subParts
    partSet = set(particles)
    partDict = {}
    for part in partSet:
        partDict[part] = 0
    for part in particles:
        partDict[part] = partDict[part] + 1
    possibleNames = sorted(result, key=len)
    mainPart = partDict.keys()[partDict.values().sort()[-1]]
    found = False
    Result = ""
    for name in possibleNames:
        if not found and mainPart in name:
            found = True
            Result = name
    

    return render_template("home.html")

if __name__ == "__main__":
   app.debug = True
   app.secret_key = "Secret secrets"
   app.run(host="0.0.0.0", port=8000)
