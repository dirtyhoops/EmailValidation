from flask import Flask, redirect, render_template, request, flash
# import the function connectToMySQL from the file mysqlconnection.pycopy
from mysqlconnection import connectToMySQL
import re

app = Flask(__name__)
app.secret_key = 'denvernuggets'

# invoke the connectToMySQL function and pass it the name of the database we're using
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
mysql = connectToMySQL('emaildb')
# now, we may invoke the query_db method

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/add', methods=['POST'])
def addFriend():
    query = "INSERT INTO emailaddress (email) VALUES (%(email)s);"
    data = {
             'email': request.form['email']
           }

    if len(request.form['email']) < 1:
        flash(f"Email can't be empty")
        return redirect('/')

    if not EMAIL_REGEX.match(request.form['email']):
        flash(f"Invalid Email Address!")
        return redirect('/')

    query_select = "SELECT email FROM emailaddress WHERE email = %(email)s;"
    data = {
             'email': request.form['email']
           }
    email_dup = mysql.query_db(query_select, data)

    if email_dup:
        flash(f"Email is Already Taken!")
        return redirect('/')
    
    
    mysql.query_db(query, data)
    flash(f"Added Email Successfully")
    return redirect('/success')


@app.route('/delete', methods=['POST'])
def deleteEmail():
    id = int(request.form['deleteId'])
    query1 = "DELETE FROM emailaddress WHERE id = '{}'".format(id)
    mysql.query_db(query1)
    return redirect('/success')


@app.route('/success')
def success():
    all_emails = mysql.query_db("SELECT * FROM emailaddress")
    print("Fetched all email", all_emails)

    return render_template("success.html", all_emails = all_emails)


if __name__ == "__main__":
    app.run(debug=True)