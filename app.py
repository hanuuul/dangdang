# 1. python app run 검색해서 가져옴, "/" 경로에 출력되는 문구로 연결됐나 확인
# 2. redner_template 추가해서 html 연결 (html은 templates 폴더 안에)
# 3. 컬렉션 만들기 - compass에서 local database에 market_product 만듦
# 4. flask와 mongoDB 연결을 위해 flask-pymongo 설치, import

from flask import Flask, render_template, request, redirect
# API 만들때 jsonify라는 함수 이용
from flask.json import jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
# 5. mongoDB와 연결 주소 끝에 local(이 database를 사용하겠다는 것)
#    연결하면 PyMongo(app) 사용가능, 이제 DB에 저장 가능
app.config["MONGO_URI"] = "mongodb://localhost:27017/local"
mongo = PyMongo(app)


# API 만들기
@app.route('/detail')
def detail():
    product = mongo.db['market_product'].find_one({"title": request.args.get('title')})

    # API에서 가격, 위치, 이미지도 반환하도록 변경
    return jsonify({
        'title': product.get('title'),
        'content': product.get('content')
    })

# write 화면 출력
@app.route('/writepage')
def writepage():
    return render_template('write.html')

# 6. 입력 받아오기, moethod=["POST"]로 데이터 전달받음
@app.route('/write', methods=['POST'])
def write():
    # 내용을 받아서 DB에 넣어야함, 상단에 request, redirect 추가
    # request : 요청, 사용자로부터 요청을 받을 때 그 정보를 가지고 있는 변수
    # redirect : 이동, redirect('/')쓰면 ('/write')에서 글을 쓴 후 ('/')로 가서 쓴 글을 보여줌
    title = request.form.get('title') # title 받아서 title 변수에
    location = request.form.get('location')
    price = request.form.get('price')
    content = request.form.get('content')

    # DB에 저장
    mongo.db['market_product'].insert_one({
        # JSON - 딕셔너리 형태로 넣음
        "title" : title,
        "location" : location,
        "price" : price,
        "content" : content
    })
    # main 화면으로
    return redirect('/')

# main 화면 출력
@app.route("/")
def main():
    # DB에서 데이터 가져오기 / find()는 모든걸 가져옴
    product_info = mongo.db['market_product'].find()

    # product_info를 product_info로 전달
    return render_template('list.html', product_info=product_info)


if __name__ == '__main__':
    app.run(debug=True)