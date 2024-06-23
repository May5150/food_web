from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(100), nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Food('{self.food_name}', '{self.expiry_date}')"

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
    if existing_user:
        return jsonify({'message': 'ユーザー名またはメールアドレスが既に存在します。'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(email=email, username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'アカウントが正常に作成されました。'}), 200

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'メールアドレスまたはパスワードが正しくありません。'}), 401

    # ログイン成功時の処理（例：セッション管理、トークン発行など）
    return jsonify({'message': 'ログインに成功しました。'}), 200

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/add_food')
def add_food_page():
    return render_template('add_food.html')

@app.route('/api/add_food', methods=['POST'])
def add_food():
    data = request.get_json()
    food_name = data.get('foodName')
    expiry_date_str = data.get('expiryDate')

    # ユーザーを特定するためにセッションから取得（適宜実装を変更）
    user = User.query.filter_by(id=1).first()  # 例としてid=1のユーザーとして処理

    # 賞味期限を日付型に変換
    expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()

    # 食品をデータベースに追加
    new_food = Food(food_name=food_name, expiry_date=expiry_date, user_id=user.id)
    db.session.add(new_food)
    db.session.commit()

    return jsonify({'message': '食品が正常に登録されました。'}), 200

@app.route('/api/get_expiring_foods', methods=['GET'])
def get_expiring_foods():
    # ユーザーを特定するためにセッションから取得（適宜実装を変更）
    user = User.query.filter_by(id=1).first()  # 例としてid=1のユーザーとして処理

    # 今日の日付
    today = datetime.now().date()

    # 3日前の日付
    three_days_ago = today - timedelta(days=3)

    # 3日後の日付
    three_days_later = today + timedelta(days=3)

    # 賞味期限が3日前から3日後の食品を取得
    expiring_foods = Food.query.filter_by(user_id=user.id).filter(Food.expiry_date >= three_days_ago, Food.expiry_date <= three_days_later).all()

    # レスポンスの準備
    response = []
    for food in expiring_foods:
        days_until_expiry = (food.expiry_date - today).days
        response.append({
            'id': food.id,
            'foodName': food.food_name,
            'expiryDate': food.expiry_date.strftime('%Y-%m-%d'),
            'daysUntilExpiry': days_until_expiry
        })

    return jsonify(response), 200

@app.route('/api/delete_food/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
    food = Food.query.get(food_id)
    if not food:
        return jsonify({'message': '食品が見つかりません。'}), 404

    db.session.delete(food)
    db.session.commit()

    return jsonify({'message': '食品が正常に削除されました。'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
