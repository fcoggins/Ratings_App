from flask import Flask, render_template, redirect, request, flash, session
import model, json
app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/userlist")
def userlist():
    user_list = model.session.query(model.User).limit(5).all()
    return render_template("user_list.html", user_list=user_list)

@app.route("/createuser", methods=["GET"])
def show_createuser():
    return render_template("create_user.html")

@app.route("/createuser", methods=["POST"])
def createuser():
    user = model.User(email=request.form['email'], 
        password=request.form['password'], age=request.form['age'], 
        zipcode=request.form['zipcode'])
    print request.form['email']
    r = model.session.query(model.User).filter_by(email = request.form['email']).all()
    print type(r)
    print r[0].email
    if len(r) > 0:
        print "Hello"
        return redirect("/login")
    model.session.add(user)
    model.session.commit()
    print "User has been added"
    return "User has been added"


@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    #user = model.User()
    email = request.form['email']
    r = model.session.query(model.User).filter_by(email = email).all()
    
    if len(r)==0:
        #user does not exist in database
        return redirect("/createuser")
    else:
        user = r[0]
        if user.password != request.form['password']:
            #passwords do not match/ Want to Flash method.
            print("Your password does not match")
            #message = 'Passwords do not match, please try again'
            #flash(message)
            return redirect("/login")        
        else:
            #passwords match store in session
            session['userid'] = user.id
            print session['userid']
            return redirect("userreviews/"+str(user.id))

@app.route("/viewusers")
def viewusers():

    v = model.session.query(model.User).limit(200).all()
    return render_template("user_list.html", user_list=v)

@app.route("/movielist")
def viewmovies():

    v = model.session.query(model.Movie).limit(200).all()
    return render_template("movielist.html", movie_list=v)

@app.route("/addrating")
def rate():

    return "This is the ratings page"



@app.route("/userreviews/<id>")
def viewreviews(id):
    userid = id 
    user = model.session.query(model.User).filter_by(id=userid).one()
    ratings = user.ratings
    return render_template("userreviews.html", user=user)

@app.route("/sessionclear")
def clear_session():
    session.clear()
    return "Clearing"
            

    


    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""


if __name__ == "__main__":
    app.run(debug = True)