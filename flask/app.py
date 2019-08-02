from flask import Flask, escape, request, render_template
import random
import requests
from bs4 import BeautifulSoup
import csv

app = Flask(__name__)

@app.route('/')
def hello():
    # name = request.args.get("name", "World")
    # .get은 값이 없으면 None 반환, 혹은 default적으면 default 반환
    return render_template('index.html')


@app.route('/lotto')
def lotto():
    numbers = random.sample(range(1, 46), 6)
    print(numbers)
    return render_template('lotto.html', numbers=numbers)

@app.route('/lunch')
def lunch():
    lunch_dict = {
        '오징어주꾸미볶음': 'https://t1.daumcdn.net/cfile/tistory/14336F504F71582809', 
        '나주곰탕': 'http://www.djf.kr/images/contents/menu_02.jpg',
        '버섯닭개장': 'http://recipe.ezmember.co.kr/cache/recipe/2015/08/13/7a8004e7d470940973fa696e4d4d79461.jpg', 
        '소시지투움바파스타': 'https://t1.daumcdn.net/cfile/tistory/9981793C5B67B0BA08'
    }

    lunch_list = list(lunch_dict.keys())
    pick = random.choice(lunch_list)
    img = lunch_dict[pick]

    return render_template('lunch.html', pick=pick, img=img)

@app.route('/opgg')
def opgg():
    return render_template('opgg.html')

@app.route('/search')
def search():
    opgg_url = "https://www.op.gg/summoner/userName="
    summoner = request.args.get('summoner')
    url = opgg_url + summoner

    res = requests.get(url).text
    
    soup = BeautifulSoup(res, 'html.parser')
    tier = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo > div.TierRank')
    user_tier = tier.text.strip()
# opgg는 혼자서 결과가 나올 수 없다. 두개의 html 문서가 필요하다. 왜? 왜인지 아는게 중요!
    
    print(summoner)
    return render_template('search.html', user_tier=user_tier, summoner=summoner)

@app.route('/nono')
def nono():
    with open('data.csv', 'r', encoding='utf-8') as f:
        reader =csv.reader(f)
        products = list(reader)

    return render_template('nono.html', products=products)
    # render_template은 파이썬 문법을 읽어서 완전한 html 문서 형태로 만들어준다
    # render_template가 없으면 html 화면이 우리가 원하는 형태로 나타나지 않는다(render가 없으면파이썬 문법을 못읽기 때문에)
    # 단, render_template에서 주석을 사용하면, 주석을 건너지 않고 그냥 코드처럼 다 읽어버리기 때문에 주의해야한다.
    # html의 주석과 진자의 주석을 동시에 달아주면 읽지 않고 넘어간다.<--{# 주석주석 #}-->이렇게!
@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/create')
def create():
    product = request.args.get('product')
    category = request.args.get('category')
    replace = request.args.get('replace')

    with open('data.csv', 'a+', encoding = 'utf-8', newline = '') as f:
        writer = csv.writer(f)
        # csv 파일을 읽어준다.
        # ['해피해킹', '키보드', '한성']
        product_info = [product, category, replace]
        writer.writerow(product_info)
    return render_template('create.html')

@app.route('/card')
def card():
    with open('data.csv', 'r', encoding='utf-8') as f:
        reader =csv.reader(f)
        products = list(reader)
    
    return render_template('card.html', products=products)



if __name__ == "__main__":
    app.run(debug=True)