import feedparser
from flask import*
import json
import urllib.request

app=Flask(__name__)

#rss feed
RSS_FEED={'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
          'cnn':'http://rss.cnn.com/rss/edition.rss',
          'fox':'http://www.iol.co.za/cmlink/1.640',
          'bdnews':'https://www.thedailystar.net/rss'}



#weather
source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=Jhenaidah&appid=d1b77c3eaa968bfb1f661059397c14d3').read()


list_of_data = json.loads(source)
weather = {"description":list_of_data["weather"][0]["description"],
    "temperature":list_of_data["main"]["temp"]-273.15,
        "city":list_of_data["name"],
           'country':list_of_data['sys']['country']
}





#currency
CURRENCY_URL =urllib.request.urlopen("https://openexchangerates.org//api/latest.json?app_id=c6b28118c4a54916a231727965cb4382").read()

list_of_data2=json.loads(CURRENCY_URL).get('rates')
datac=list_of_data2['BDT']




#the main app
@app.route('/')
def get_news():
    query=request.args.get('publication')
    if not query or query.lower() not in RSS_FEED:
        publication='bbc'
    else:
        publication=query.lower()
    feed=feedparser.parse(RSS_FEED[publication])
    return render_template('rss.html',
                           articles=feed['entries'],
                           weather=weather,
                           currenry=datac)




if __name__=='__main__':
    app.run(debug=True)