import re
from flask import Flask, request, render_template

from requests import get
from requests.models import Response
import series_database as db

var_list=[] #global list declartion for storing the URL from user input
total_sns_no=[] 
app = Flask(__name__) 

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       imdb_main_url = request.form.get("link") 
       var_list.append(imdb_main_url)
    
    def total_sns():
        url=var_list[0]
        from bs4 import BeautifulSoup
        try:
            response=get(url)
            soup=BeautifulSoup(response.text,'html.parser')
            seasons=soup.find("select",{"id":"bySeason"}).findAll("option")
            for sns in seasons:
                sns_no=sns.text
                total_sns_no.append(sns_no)
        except:
            a="bad"
            return render_template('form.html',err=a)

    total_sns() 
    return render_template("form.html")


@app.route('/results')

def results():
    total_episodes=[] #global list declaration to store the episode details
      #global list to store the season numbers

    #function to find the total number of seasons of the given series

    #finding the length of the list to find the total season count and adding one to it for iterating over the seasons
    total_seasons=len(total_sns_no)+1 

    #editing the url to add te season number to the url
    url=var_list[0]
    b="".join(url)
    split_url = b.split('?',1)
    edit=split_url[0]
    edit_string=edit+"?season="

    #finding the all the episodes and corresopnding deatails through nested for loop
    for sn in range(1,total_seasons):
        edit2=edit_string+str(sn)
        from bs4 import BeautifulSoup
        response=get(edit2)
        html_soup=BeautifulSoup(response.text, 'html.parser')
        episode_containers = html_soup.find_all('div', class_='info')

        for episodes in episode_containers:
            season = int(sn)
            episode_number = int(episodes.meta['content'])
            title = episodes.a['title']
            rating = episodes.find('span', class_='ipl-rating-star__rating').text
            episode_data = (season, episode_number, title, rating)
            total_episodes.append(episode_data)
            #db.imdb_insert(season,episode_number,title,rating)
    return render_template('results.html',total=total_episodes)


if __name__=='__main__':
   app.run(debug=True)