from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from app_config import APP_HOST, APP_PORT

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    'user_1': generate_password_hash('password_1'),
    'user_2': generate_password_hash('password_2')
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@app.route('/')
def index():
    return 'This is the main page of an app'


@app.route('/profile')
@auth.login_required
def profile():
    return f'{auth.current_user()}, this is your profile!'


@app.route('/posts')
def posts():
    return 'List of user posts'


@app.route('/posts/<post_id>')
def post(post_id: int):
    return f'This is the post with id {post_id}'


@app.route('/posts/new')
@auth.login_required
def new_post():
    return f'{auth.current_user()}, your post has been created'


@app.route('/logout')
@auth.login_required
def logout():
    return f'You have successfully logged out', 401


if __name__ == '__main__':
    app.run(debug=False, host=APP_HOST, port=APP_PORT)
