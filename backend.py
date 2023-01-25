from flask import Flask, url_for, render_template

app = Flask(__name__)

edito = '''
Chers lecteurs, nous avons l'immense plaisir de vous présenter notre journal électronique "Bloggity". Notre journal présente tout ce qui concerne la vie scolaire comme : des activités sportives , ludiques et sociales. Dans cette édition nous souhaitons encourager les élèves à partager leurs opinions, loisirs et leurs talents.
En vous laissant le choix de les commenter, de vous exprimer car vos critiques et suggestions nous intéressent. 
Merci pour votre attention et, nous vous souhaitons une bonne lecture!
'''

@app.route("/")
def base():
    return render_template("index.html", edito=edito)

@app.route("/articles")
def articles():
    return render_template("articles.html")
    
@app.route("/contactez_nous")
def contact():
    return render_template("contact.html")

@app.route("/multimedia")
def multimedia():
    return render_template("multimedia.html")

@app.route("/admin")
def admin():
    return render_template("login.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)