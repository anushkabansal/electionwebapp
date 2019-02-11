from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
# from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, DateField ,DecimalField, IntegerField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rootroot'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

#
# Articles = Articles()

# Home
@app.route('/')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('entries'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))




# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT DISTINCT country, date FROM candidates")
    candidates = cur.fetchall()
    print (candidates)
    # Close connection
    cur.close()

    if result > 0:
        return render_template('dashboard.html', candidates=candidates)
    else:
        msg = 'No Articles Found'

        return render_template('dashboard.html', msg=msg)
    # return render_template('articles.html', articles=Articles)



@app.route('/query')
def query():

    return render_template('entries.html')
    # return render_template('articles.html', articles=Articles)




# Article Form Class
class ArticleForm(Form):
    polldate = DateField('Poll Date')
    fieldworkdate = DateField('Field Work Date')
    pollingfirm = StringField('Polling Firm')
    samplesize = IntegerField('Sample Size')
    moe = DecimalField('M O Error')
    calculate = DecimalField('Lead')
    candidatenames = StringField('Candidate Names')
    pollnumbers = DecimalField('Poll Numbers')

# Articles
@app.route('/entries')
@is_logged_in
def entries():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT DISTINCT country, date FROM candidates")
    candidates = cur.fetchall()
    print (candidates)
    # Close connection
    cur.close()

    if result > 0:
        return render_template('entries.html', candidates=candidates)
    else:
        msg = 'No Articles Found'

        return render_template('entries.html', msg=msg)
    # return render_template('articles.html', articles=Articles)

#Single election
@app.route('/entry/<string:country>/<string:date>')
def entry(country,date):
    # Create cursor
    cur = mysql.connection.cursor()

    # print(country)
    # print (date)
    #
    # # Get articles
    # result = cur.execute("SELECT * FROM articles WHERE country = %s", [country])
    # #result = cur.execute("SELECT DISTINCT country, date FROM candidates")
    #
    # articles = cur.fetchone()
    # candidates = cur.fetchall()
    # print(articles)
    # print (candidates)

    # Get articles
    result1 = cur.execute("SELECT * FROM articles WHERE country = %s", [country])

    candidates = cur.fetchall()
    print (candidates)

    result = cur.execute("SELECT * FROM candidates")
    #
    print (result)
    articles = cur.fetchone()

    if result > 0:
        return render_template('entry.html', candidates=candidates,articles= articles)
    else:
        msg = 'No Articles Found'
        return render_template('entry.html', msg=msg)
    return render_template('entry.html', country = country,date=date)

#Single election
@app.route('/edit/<string:country>/<string:date>')
def edit(country,date):

    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result1 = cur.execute("SELECT * FROM articles WHERE country = %s", [country])

    candidates = cur.fetchall()
    print (candidates)

    result = cur.execute("SELECT * FROM candidates")
    #
    print (result)
    articles = cur.fetchone()

    if result > 0:
        return render_template('edit.html', candidates=candidates, articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('edit.html', msg=msg)
    return render_template('edit.html', country = country,date=date)



# Add ENTRY
@app.route('/add_entry/<string:ifpid>/<string:eformat>/<string:country>/<string:date>', methods=['GET', 'POST'])
@is_logged_in
def add_entry(ifpid,eformat,country,date):

    form = ArticleForm(request.form)

    country = country
    date = date
    ifpid = ifpid
    eformat = eformat

    if request.method == 'POST' and form.validate():
        polldate = form.polldate.data
        fieldworkdate = form.fieldworkdate.data
        pollingfirm = form.pollingfirm.data
        samplesize= form.samplesize.data
        moe = form.moe.data
        calculate = form.calculate.data
        candidatenames = form.candidatenames.data
        pollnumbers = form.pollnumbers.data

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("INSERT INTO articles(ifpid,country,eformat,date,polldate,fieldworkdate,pollingfirm,samplesize,moe,calculate,candidatenames,pollnumbers) VALUES(%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s)",[ifpid,country,eformat,date,polldate,fieldworkdate,pollingfirm,samplesize,moe,calculate,candidatenames,pollnumbers])

        # cur.execute("INSERT INTO articles(ifpid,country,eformat,date,polldate,fieldworkdate,pollingfirm,samplesize,moe,calculate)VALUES(%s,%s,%s,%s,%s,%s,%s,%s, %s,%s)",[ifpid,country,eformat,date,polldate,fieldworkdate,pollingfirm,samplesize,moe,calculate])
        #
        # cur.execute("INSERT INTO articles(ifpid,country,eformat,date,polldate,fieldworkdate,pollingfirm,samplesize,moe,calculate)VALUES(%s,%s,%s,%s,%s,%s,%s,%s, %s,%s)",[ifpid,country,eformat,date,polldate,fieldworkdate,pollingfirm,samplesize,moe,calculate])

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Article Created', 'success')

        return redirect(url_for('edit',country = country,date =date))

    return render_template('add_entry.html', form=form)


# Edit Article
@app.route('/edit/<string:country>/edit_entry/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_entry(id,country):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    entry = cur.fetchone()
    # mysql.connection.commit()
    cur.close()
    # Get form
    form = ArticleForm(request.form)
    # ifpid=ifpid
    # eformat = eformat
    date = entry['date']

    # Populate article form fields
    form.polldate.data = entry['polldate']
    form.fieldworkdate.data = entry['fieldworkdate']
    form.pollingfirm.data = entry['pollingfirm']
    form.samplesize.data = entry['samplesize']
    form.moe.data = entry['moe']
    form.calculate.data = entry['calculate']
    form.candidatenames.data = entry['candidatenames']
    form.pollnumbers.data = entry['pollnumbers']



    if request.method == 'POST' and form.validate():
        polldate = request.form['polldate']
        fieldworkdate = request.form['fieldworkdate']
        pollingfirm = request.form['pollingfirm']
        samplesize = request.form['samplesize']
        moe = request.form['moe']
        calculate = request.form['calculate']
        candidatenames = request.form['candidatenames']
        pollnumbers = request.form['pollnumbers']


        # Create Cursor
        cur = mysql.connection.cursor()
        app.logger.info(polldate)
        # Execute
        cur.execute ("UPDATE articles SET polldate=%s, fieldworkdate=%s ,pollingfirm=%s,samplesize=%s,moe = %s,calculate = %s,candidatenames = %s,pollnumbers = %s WHERE id=%s",(polldate, fieldworkdate, pollingfirm,samplesize,moe,calculate,candidatenames,pollnumbers,id))
        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Article Updated', 'success')

        return redirect(url_for('edit',country = country,date =date))

    return render_template('edit_entry.html', form=form)

# Delete Article
@app.route('/delete_entry/<string:country>/<string:date>/<string:id>', methods=['POST'])
@is_logged_in
def delete_entry(country,date,id):
    # Create cursor

    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM articles WHERE id = %s", [id])
    entry = cur.fetchone()

    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Article Deleted', 'success')

    return redirect(url_for('edit',country=country,date=date))
if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
