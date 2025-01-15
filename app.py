
from flask import Flask, request,render_template, redirect,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker, scoped_session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.influencer'
app.config['SQLALCHEMY_BINDS']={'two':'sqlite:///database.brand'}
influencer = SQLAlchemy(app)

app.secret_key = 'secret_key'

class Brand(influencer.Model):
    __bind_key__='two'
    company = influencer.Column(influencer.String(100), nullable=False)
    email = influencer.Column(influencer.String(100), unique=True,primary_key=True)
    password = influencer.Column(influencer.String(100))
    budget = influencer.Column(influencer.String(100), nullable=False)
    followers_type = influencer.Column(influencer.String(100), nullable=False)
    genre = influencer.Column(influencer.String(100), nullable=False)
    gender = influencer.Column(influencer.String(100), nullable=False)
    country = influencer.Column(influencer.String(100), nullable=False)
    age_group = influencer.Column(influencer.String(100), nullable=False)
    
    def __init__(self,email,password,company,budget,followers_type,genre,gender,country,age_group):
        self.company = company
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.genre=genre
        self.gender=gender
        self.country=country
        self.age_group=age_group
        self.followers_type=followers_type
        self.budget=budget
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))
    

def get_secondary_session():
    # Create a session for the secondary database (bind='two')
    engine = influencer.get_engine(app, bind='two')
    Session = scoped_session(sessionmaker(bind=engine))  # Create a scoped session tied to 'two' database
    return Session()

class User(influencer.Model):
    fname = influencer.Column(influencer.String(100), nullable=False)
    email = influencer.Column(influencer.String(100), unique=True,primary_key=True)
    password = influencer.Column(influencer.String(100))
    lname = influencer.Column(influencer.String(100), nullable=False)
    followers = influencer.Column(influencer.String(100), nullable=False)
    followers_type = influencer.Column(influencer.String(100), nullable=False)
    genre = influencer.Column(influencer.String(100), nullable=False)
    gender = influencer.Column(influencer.String(100), nullable=False)
    insta_name = influencer.Column(influencer.String(100), nullable=False)
    yt_name = influencer.Column(influencer.String(100), nullable=False)
    country = influencer.Column(influencer.String(100), nullable=False)
    other_platform = influencer.Column(influencer.String(100), nullable=False)
    age_group = influencer.Column(influencer.String(100), nullable=False)
    def __init__(self,email,password,fname,lname,followers,followers_type,genre,gender,insta_name,yt_name,country,other_platform,age_group):
        self.fname = fname
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.lname=lname
        self.followers=followers
        self.genre=genre
        self.gender=gender
        self.insta_name=insta_name
        self.yt_name=yt_name
        self.country=country
        self.other_platform=other_platform
        self.age_group=age_group
        self.followers_type=followers_type
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))
    def to_dict(self):
        return {
            "followers_type": self.followers_type,
            "age_group": self.age_group,
            "country": self.country,
            "gender":self.gender,
            "genre":self.genre,
            "email":self.email,
            "fname":self.fname,
            "profile_url":self.lname
        }

with app.app_context():
    # Create tables for the primary (influencer) database
    influencer.create_all()

    # Create tables for the secondary (brand) database
    engine = influencer.get_engine(app, bind='two')
    influencer.metadata.create_all(bind=engine)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/brand-register', methods=['GET', 'POST'])
def brand_register():
    if request.method == 'POST':
        company = request.form['fname']
        email = request.form['email']
        password = request.form['pass']
        followers_type = request.form['typeinfluence']
        country = request.form['State']
        age_group = request.form['age']
        genre = request.form['genre']
        gender = request.form['gender']
        budget = request.form['follow']

        # Get a session for the secondary database (brand)
        session = get_secondary_session()

        # Check if the email already exists in the brand database
        brand = Brand.query.filter_by(email=email).first()
        if brand:
            return render_template('brand_signup.html', error=True)

        # Create and add a new brand record
        new_user = Brand(
            gender=gender,
            genre=genre,
            followers_type=followers_type,
            company=company,
            email=email,
            password=password,
            country=country,
            age_group=age_group,
            budget=budget
        )
        session.add(new_user)
        session.commit()

        # No need to call session.remove(), as Flask-SQLAlchemy handles cleanup
        session.close()  # You can call session.close() explicitly if needed

        return redirect('/brand-login')

    return render_template('brand_signup.html', error=False)





@app.route('/brand-login', methods=['GET', 'POST'])
def brand_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        
        # Query the Brand model (this will return an instance of the class, not the class itself)
        brand_user = Brand.query.filter_by(email=email).first()
        
        # Check if the user exists and the password is correct
        if brand_user and brand_user.check_password(password):  # Now calling on the instance (brand_user)
            session['email'] = brand_user.email  # Store email in Flask's session
            return redirect('/brand_dashboard')
        else:
            return render_template('brand-login.html', error=True)  # Pass 'error' to the template

    return render_template('brand-login.html', error=False)  # Pass 'error' to the template


@app.route('/brand_dashboard')
def brand_dashboard():
    if 'email' in session:  # Check if the user is logged in
        users = User.query.all()
        users_json = [user.to_dict() for user in users]
        return render_template('filter1.html') 


@app.route('/influencer-register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        fname = request.form['fname']
        email = request.form['email']
        password = request.form['pass']
        lname=request.form['lname']
        followers=request.form['follow']
        followers_type=request.form['typeinfluence']
        insta_name=request.form["instaname"]
        yt_name=request.form['ytname']
        country=request.form['state']
        other_platform=request.form['other']
        age_group=request.form['age']
        genre=request.form['genre'] 
        gender=request.form['gender'] 
        user = User.query.filter_by(email=email).first()
        if user:
           return render_template('signup.html',error=True)
        new_user = User(gender=gender,genre=genre,followers_type=followers_type,fname=fname,email=email,password=password,lname=lname,followers=followers,insta_name=insta_name,yt_name=yt_name,country=country,other_platform=other_platform,age_group=age_group)
        influencer.session.add(new_user)
        influencer.session.commit()


        return redirect('/influencer-login')
    


    return render_template('signup.html',error=False)

@app.route('/influencer-login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/dashboard')
        else:
            return render_template('login.html',error=True)

    return render_template('login.html',error=False)


@app.route('/dashboard')
def dashboard():
    if 'email' in session:  # Check if the user is logged in
        users = User.query.all()# Retrieve all users from the database
        users1=users[-1]
        
        return render_template('influencer_dashboard.html' ,user=users1)  # Pass all users to the template
    
    return redirect('/influencer-login')  # Redirect to login if not logged in


@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/influencer-login')

@app.errorhandler(404)
def error(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error(e):
    return render_template('500.html'), 500

@app.route('/redirect-to-django')
def redirect_to_django():
    return redirect("http://127.0.0.1:8000/login/", code=302)



if __name__ == '__main__':
    app.run(debug=True,port=9000)