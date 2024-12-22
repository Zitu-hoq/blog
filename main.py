import os
from flask import Flask, flash, redirect, render_template, request,url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


db= SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(user_id):
    return Profiles.query.get(int(user_id))



class Blogs(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    subtitle=db.Column(db.String(400), nullable=False)
    description=db.Column(db.Text, nullable=False)
    thumbnail=db.Column(db.String(100), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)

class Profiles(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    fullName=db.Column(db.String(200), nullable=False)
    email=db.Column(db.String(400), nullable=False)
    password=db.Column(db.String(100), nullable=False)
    blogs=db.relationship('Blogs', backref='author', lazy=True)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    blogs=Blogs.query.paginate(max_per_page=6)
    return render_template('index.html', blogs=blogs)



@app.route('/blog/<int:id>')
def blog(id):
    blog = Blogs.query.filter_by(id=id).first()
    if not blog:
        flash("Blog Not Found!", "error")
        return redirect(url_for('home'))
    return render_template('blog.html', blog=blog)



@app.route('/blog/create', methods=['GET', 'POST'])
@login_required
def create_blog():
    if request.method == "POST":
        blog=Blogs(title=request.form.get("title"), subtitle=request.form.get("subtitle"), description=request.form.get("description"), thumbnail=request.form.get("thumbnail"), user_id=current_user.id)
        db.session.add(blog)
        db.session.commit()
        flash("Blog Created", "success")
        return redirect(url_for('home'))
    return render_template('create_blog.html')


@app.route('/blog/edit/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def edit_blog(blog_id):
    blog = Blogs.query.filter_by(id=blog_id).first()
    if current_user.id != blog.author.id:
        flash("Unauthorized Action!", "info")
        return redirect(url_for('home'))
    if not blog:
        flash("Blog Not Found!", "error")
        return redirect(url_for('home'))
    if request.method == "POST":
        blog.title=request.form.get("title") 
        blog.subtitle=request.form.get("subtitle")
        blog.description=request.form.get("description") 
        blog.thumbnail='1.png'
        
        db.session.commit()
        flash("Blog Updated.","success")
        return redirect(url_for('home'))
    return render_template('edit_blog.html', blog=blog)



@app.route('/blog/delete/<int:blog_id>')
@login_required
def delete_blog(blog_id):
    blog = Blogs.query.filter_by(id=blog_id).first()
    if current_user.id != blog.author.id:
        flash("Unauthorized Action!", "warning")
        return redirect(url_for('home'))
    if blog:
        db.session.delete(blog)
        db.session.commit()
        flash("Blog Deleted!", "success")
        return redirect(url_for('home'))
    flash("Uh OH!Somthing is not right!", "error")
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html")


@app.route('/blogs')
def blogs():
    page_no= int(request.args.get('page')) if request.args.get('page') else 1
    blogs=Blogs.query.paginate(page=page_no,  max_per_page=15)
    return render_template('blogs.html', blogs=blogs)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        user=Profiles(fullName=request.form.get("full_name"), email=request.form.get("email"), password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Account Created Successfully!", "success")
        return redirect(url_for('home'))
    return render_template('sign_up.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password= request.form.get("password")
        user = Profiles.query.filter_by(email=email).first()
        if not user:
            flash("User Not Found!", "warning")
            return redirect(url_for('login'))
        if(user.password == password):
            login_user(user)
            flash("Login Successful!", "success")
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home'))
        else:
            flash("Incorrect Password!", "warning")
            return redirect(url_for('login'))
        
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Log Out Successful", "success")
    return redirect(url_for('home'))


DEBUG_MODE = os.getenv('DEBUG_MODE') == 'True'
if __name__ == '__main__':
    app.run(debug=True)