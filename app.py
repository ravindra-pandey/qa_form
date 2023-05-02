from flask import Flask, render_template, url_for, redirect, request,session
import db_connection

app = Flask(__name__)
app.secret_key = "a2bv34dssd5tggg"

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
    error=""
    if request.method == "POST":
        email=request.form["email"]
        password=request.form["psswd"]
        connection,error=db_operations.validate_login_credentials(email,password)
        session["user_name"]=error
        if connection:
            return redirect(url_for("user"))
    if "user_name" in session:
        user=session["user_name"]
        return redirect(url_for("user"))
    return render_template("login.html",error=error)
@app.route('/signup',methods=["POST","GET"])
def signup() :
    """
    This method is called when the user is going to login page.
    """
    error=""
    if request.method == "POST":
        user=request.form["name"]
        email=request.form["email"]
        psswd=request.form["psswd"]
        cnf_psswd=request.form["cnf_psswd"]
        error=db_operations.create_user(user,email,psswd,cnf_psswd)
        if error is None:
            return redirect(url_for("login",error=""))
        else:
            return render_template("signup.html",error=error)
            
    return render_template("signup.html",error=error)

@app.route("/user")
def user():
    if "user_name" in session:
        user=session["user_name"]
        return render_template("home.html",usr=user,show=True)
    else:
        return redirect(url_for("login"))

@app.route('/ask_me',methods=["POST","GET"])
def ask_me():
    """
    This method is called when the user is going to ask any question.
    """
    if request.method == "POST":
        question=request.form["ask"]
        user_id="user"
        db_operations.feed_question(question,user_id)
    return render_template("ask_me.html")

@app.route("/answers")
def temp_answers():
    """
    this method is called when the user is going to see all the answers of any question.
    """
    q_id=int(list(request.args)[0])
    ques,ans=db_operations.get_qa_by_id(q_id)
    if len(ques)==0:
        ques=""
    return render_template("temp.html",ques=ques,ans=ans)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
