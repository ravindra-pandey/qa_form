from flask import Flask, render_template, url_for, redirect, request
import db_connection

app = Flask(__name__)

URL = "mongodb://localhost:27017"

db_operations=db_connection.DatabaseOperations(URL)



@app.route('/')
def hello():
    """
    This is main function which will be called when the user will 
    to the home page.
    """
    qa_set=db_operations.get_question_answer_set()
    return render_template("home.html",qa_set=qa_set)


@app.route('/login',methods=["POST","GET"])
def login() :
    """
    This method is called when the user is going to login page.
    """
    return render_template("login.html")


@app.route('/ask_me',methods=["POST","GET"])
def ask_me():
    """
    This method is called when the user is going to ask any question.
    """
    if request.method == "POST":
        question=request.form["ask"]
        user_id="user4"
        db_operations.feed_question(question,user_id)
    return render_template("ask_me.html")


if __name__ == "__main__":
    app.run(debug=True)
