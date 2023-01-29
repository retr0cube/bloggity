from flask import Flask, url_for, render_template, request, redirect, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from wtforms import TextAreaField
# from flask_markdown import Markdown

app = Flask(__name__)
# Markdown(app)

app.config['FLASK_ADMIN_SWATCH'] = "cerulean"
app.config['SECRET_KEY'] = "retr0cube"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://bloggitydb_user:ilYZa40ILv1FP4IvzGYhZjer9CHCVwF1@dpg-cfb88i1gp3jsh69mvau0-a.frankfurt-postgres.render.com/bloggitydb"

db = SQLAlchemy()

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

class Multimedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source= db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String, nullable= False)

class Edito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)

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

    form_overrides = {'content': TextAreaField,}
    form_choices = {
    'genre': [
        ("SPORT","Sport"),
        ("PERSPECTIVES","Perspectives"),
        ("TECH","Technologie"),
        ("ES","Expériences Sociales"),
        ("AS","Activités Scolaires")
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

db.init_app(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def locked_page(e):
    return render_template('403.html'), 403

@app.route("/")
def base():
    return render_template("index.html", edito=db.get_or_404(Edito, 1).content, genre=db.session.query(Posts.genre).all())

@app.route("/articles")
def articles():
    wposts = db.session.execute(db.select(Posts).order_by(Posts.title)).scalars()
    return render_template("articles.html", articles=wposts)

@app.route("/article/<int:id>")
def article(id):
    wpost = db.get_or_404(Posts, id)
    return render_template("post.html", article=wpost)
    
@app.route("/contactez_nous")
def contact():
    return render_template("contact.html")

@app.route("/multimedia")
def multimedia():
    return render_template("multimedia.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["GET","POST"])
def check_code():
    try:
        code = db.session.query(User.name).filter(User.special_code == request.form["pass"]).first()
        session['username'] = code[0]
        session["logged_in"] = True
        return redirect(url_for("admin.index"))
    except:
        return render_template("login.html", failed=True)

@app.route('/logout')
def logout():
    session["logged_out"] = True
    session.pop('username',None)
    return redirect(url_for("base"))

if __name__ == "__main__":
    app.run(debug=True)