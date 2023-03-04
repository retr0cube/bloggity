from flask import Flask, url_for, render_template, request, redirect, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from wtforms import TextAreaField
from sqlalchemy import func
import mistune
import requests
import os

app = Flask(__name__)

app.config['FLASK_ADMIN_SWATCH'] = "cerulean"
app.config['SECRET_KEY'] = "retr0cube"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://bloggitydb_user:ilYZa40ILv1FP4IvzGYhZjer9CHCVwF1@dpg-cfb88i1gp3jsh69mvau0-a.frankfurt-postgres.render.com/bloggitydb"

db = SQLAlchemy()
migrate = Migrate(app, db)

@app.context_processor
def add_imports():
    return dict(os=os,mistune=mistune)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    special_code = db.Column(db.String(255), unique=True)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    genre = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, nullable=False)
    user_email = db.Column(db.String, nullable=False, unique=True)
    post_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime)


class Edito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)


class Multimedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)


class BloggityAV(AdminIndexView):
    def is_visible(self):
        return False

    @expose('/')
    def index(self):
        return self.render(
            'admin/dashboard.html',
        )


class BloggityMV(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)

    form_overrides = {'content': TextAreaField, }
    form_choices = {
        'genre': [
            ("SPORT", "Sport"),
            ("PERSPECTIVES", "Perspectives"),
            ("TECH", "Technologie"),
            ("ES", "Expériences Sociales"),
            ("AS", "Activités Scolaires")
        ]
    }


class UserView(ModelView):
    can_delete = False
    can_edit = False
    can_create = False

administrator = Admin(app, name="Bloggity", template_mode='bootstrap3')
administrator.add_view(UserView(User, db.session))
administrator.add_view(BloggityMV(Posts, db.session))
administrator.add_view(BloggityMV(Edito, db.session))
administrator.add_view(BloggityMV(Multimedia, db.session))
administrator.add_view(BloggityMV(Comments, db.session))

db.init_app(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def locked_page(e):
    return render_template('403.html'), 403

genre_list = {
    "sport":"SPORT",
    "perspectives":"PERSPECTIVES",
    "techno":"TECH",
    "ex_sociale":"ES",
    "activite_ecole":"AS"
}

genre_name = {
    "⚽ sport":"SPORT",
    "✨ perspectives":"PERSPECTIVES",
    "💾 technologie":"TECH",
    "👨‍👧‍👧 Actu/Société":"ES",
    "🏫 activités scolaires":"AS"
}
inv_dict = {value:key for key, value in genre_name.items()}
inv_dict_2 = {value:key for key, value in genre_list.items()}


@app.route("/")
def base():
    projets = Multimedia.query.filter(Multimedia.type == "projets").all()
    return render_template("index.html",projets=projets ,edito=db.get_or_404(Edito, 1).content, genre=[*set(db.session.query(Posts.genre).all())], name=inv_dict, route=inv_dict_2)


@app.route("/articles")
def articles():
    wposts = db.session.execute(
        db.select(Posts).order_by(Posts.title)).scalars()
    return render_template("articles.html", articles=wposts, genre=inv_dict)


@app.route("/articles/<int:id>", methods=["GET", "POST"])
def article(id):
    wpost = db.get_or_404(Posts, id)
    md_post = mistune.html(wpost.content)
    wposts = db.session.execute(
    db.select(Posts).order_by(Posts.title)).scalars()
    comments = Comments.query.filter(Comments.post_id == id).all()
    return render_template("post.html", article=wpost, articles=wposts, genre=inv_dict, md=md_post, comments=comments)

@app.post("/comments/<int:id>")
def comments(id):
    email_address = request.form["email"]
    cont = request.form["content"]
    name = request.form["name"]
    email_valid = requests.get(
    "https://isitarealemail.com/api/email/validate",
    params = {'email': email_address})
    status = email_valid.json()['status']
    if status == "valid":
        db.session.add(Comments(user=name, user_email=email_address, post_id=id, content=cont, date=func.now()))
        db.session.commit()
        return redirect(url_for("article", id=id))
    else:
        valid = False
        return redirect(url_for("article", id=id))    


@app.route("/articles/<p_genre>")
def article_by_genre(p_genre):
    if str(p_genre) in genre_list :
        genre_posts = Posts.query.filter(Posts.genre == genre_list[f"{p_genre}"]).all()
        return render_template("articles.html", articles=genre_posts, genre=inv_dict)
    else:
        abort(404)

@app.route("/contactez_nous")
def contact():
    return render_template("contact.html")


@app.route("/multimedia")
def multimedia():
    talents = Multimedia.query.filter(Multimedia.type == "Talents").all()
    schoolstuff = Multimedia.query.filter(Multimedia.type == "schoolstuff").all()
    discover = Multimedia.query.filter(Multimedia.type == "discover").all()
    bloopers = Multimedia.query.filter(Multimedia.type == "bloopers").all()
    return render_template("multimedia.html", talents=talents, schoolstuff=schoolstuff, discover=discover, bloopers=bloopers)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def check_code():
    try:
        code = db.session.query(User.name).filter(
            User.special_code == request.form["pass"]).first()
        session['username'] = code[0]
        session["logged_in"] = True
        return redirect(url_for("admin.index"))
    except:
        return render_template("login.html", failed=True)


@app.route("/comment_manage", methods=["GET","POST"])
def manage_comment():
    return render_template("comment.html")


@app.route('/logout')
def logout():
    session["logged_out"] = True
    session.pop('username', None)
    return redirect(url_for("base"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8080")
