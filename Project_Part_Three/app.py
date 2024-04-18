from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Post, Tag
from users_routes import users_bp
from posts_routes import posts_bp
from tags_routes import tags_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'

db.init_app(app)

# Register blueprints
app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(tags_bp)

@app.route('/')
def index():
    """Homepage showing recent posts."""
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('index.html', recent_posts=recent_posts)

if __name__ == '__main__':
    app.run(debug=True)
