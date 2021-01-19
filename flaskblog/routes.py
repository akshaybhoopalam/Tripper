from flask import render_template, url_for, flash, redirect, request,session
from flaskblog import app,mongo,bcrypt,mail
from flaskblog.forms import RegistrationForm, Login, forgotPassword, addCity, updateCity, addPlace, updatePlace
from flask_login import LoginManager
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
import numpy as np
import requests
from flask_table import Table, Col
from apyori import apriori
from flask_mail import Mail,Message


class Results(Table):
    id = Col('Id', show=False)
    title = Col('Filtered List')


login = LoginManager(app)
login.login_view = 'login'

@app.route("/")
@app.route("/tripper")
def tripper():
    return render_template('splashScreen.html')

@app.route("/home")
def home():
    
    cities=mongo.db.city.find({},{'_id':0,"city_name":1,"category":1,"ratings":1,"imgUrl":1, "description":1})
    #cities=mongo.db.city.find().sort("ratings")
    return render_template('home.html',city=cities)


@app.route("/addCities",methods=['GET', 'POST'])
def addCities():
    form=addCity()
    if request.method=='POST':
        category=request.form.getlist("category")
    if form.validate_on_submit():
        mongo.db.city.insert({'city_name':form.cityName.data, 'category':category, 'imgUrl':form.imageUrl.data,'ratings':form.ratings.data,'description':form.descript.data})
        msg = Message('New places added checkout', sender='tripper@gmail.com', recipients=["lohith6859@gmail.com","akshayba18@gmail.com"])
        msg.body = 'Hey user checkout new place added'
        mail.send(msg)
        flash('City added succesfully!', 'success')
        return redirect(url_for('viewCities'))
    return render_template('addCities.html', title='Add', form=form)


@app.route("/addPlaces",methods=['GET', 'POST'])
def addPlaces():
    form=addPlace()
    cities=mongo.db.city.find({},{'_id':0,"city_name":1,"category":1,"ratings":1,"imgUrl":1, "description":1})
    if request.method=='POST':
        category=request.form.getlist("category")
        city_name = request.form.getlist("subplaces_city")
       
        print(category)
       
    if form.validate_on_submit():
        mongo.db.places.insert({'place_name':form.placeName.data, 'category':category, 'imgUrl':form.imageUrl.data,'ratings':form.ratings.data,'description':form.descript.data,'city_name':city_name})
        flash('Place added succesfully!', 'success')
        return redirect(url_for('viewPlaces'))
    return render_template('addPlaces.html', title='Add', form=form,city=cities) 


@app.route("/viewCities",methods=['GET', 'POST'])
def viewCities():
    if 'username' not in session:
        return redirect(url_for('login'))
    cities=mongo.db.city.find({},{'_id':0,"city_name":1,"category":1,"ratings":1,"imgUrl":1, "description":1})
    return render_template('viewCities.html', title='View',city=cities)

@app.route("/viewPlaces",methods=['GET', 'POST'])
def viewPlaces():
    if 'username' not in session:
        return redirect(url_for('login'))
    places=mongo.db.places.find({},{'_id':0,"place_name":1,"category":1,"ratings":1,"imgUrl":1, "description":1})
    return render_template('viewPlaces.html', title='View',place=places)


@app.route("/deleteCities",methods=['GET', 'POST'])
def deleteCities():
    if request.method == 'POST':
        if 'username' not in session:
            return redirect(url_for('login'))
           
    cities=mongo.db.city.find({},{'_id':0,"city_name":1,"category":1,"ratings":1,"imgUrl":1, "description":1})
    return render_template('deleteCities.html', title='Delete',city=cities) 

@app.route("/deletePlaces",methods=['GET', 'POST'])
def deletePlaces():
    if request.method == 'POST':
        if 'username' not in session:
            return redirect(url_for('login'))
           
    places=mongo.db.places.find({},{'_id':0,"place_name":1,"category":1,"ratings":1,"imgUrl":1, "description":1})
    return render_template('deletePlaces.html', title='Delete',place=places) 


@app.route("/updateCities",methods=['GET', 'POST'])
def updateCities():
    form=updateCity()

    if 'username' not in session:
        return redirect(url_for('login'))
    cities=mongo.db.city.find({},{'_id':0,"city_name":1,"category":1,"ratings":1,"imgUrl":1, "description":1})
    
    # if request.method=='POST':
    #     category=request.form.get("category")
    # if form.validate_on_submit():
    #     mongo.db.city.insert({'city_name':form.cityName.data, 'category':category, 'imgUrl':form.imageUrl.data,'ratings':form.ratings.data,'description':form.descript.data})
    #     flash('City updated succesfully!', 'success')
    #     return redirect(url_for('viewCities'))
    return render_template('updateCities.html', title='Update', form=form, city=cities)

# @app.route("/updatePlaces",methods=['GET', 'POST'])
# def updatePlaces():
#     form=updatePlace()

#     if 'username' not in session:
#         return redirect(url_for('login'))
#     places=mongo.db.places.find({},{'_id':0,"place_name":1,"category":1,"ratings":1,"imgUrl":1, "description":1})
    
    # if request.method=='POST':
    #     category=request.form.get("category")
    # if form.validate_on_submit():
    #     mongo.db.places.insert({'place_name':form.placeName.data, 'category':category, 'imgUrl':form.imageUrl.data,'ratings':form.ratings.data,'description':form.descript.data})
    #     flash('Place updated succesfully!', 'success')
    #     return redirect(url_for('viewPlaces'))
    # return render_template('updatePlaces.html', title='Update', form=form, places=places)

@app.route("/updatePlaces")
def updatePlaces():
    form=updatePlace()

    if 'username' not in session:
        return redirect(url_for('login'))
    places=mongo.db.places.find({},{'_id':0,"place_name":1,"category":1,"ratings":1,"imgUrl":1, "description":1})
    return render_template('updatePlaces.html', title='Update', form=form, places=places)

@app.route("/admin")
def admin():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('admin.html', title='Admin')

@app.route("/forgot_password",methods=['GET', 'POST'])
def forgot_password():
    form = forgotPassword()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        
        users = mongo.db.users
        newpassword = hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = users.update_one({'email' : form.email.data},{"$set":{'password':newpassword}})
        print(user)
        flash('Your account password has been changed You are now able to log in with new password', 'success')
        return redirect(url_for('login'))
    return render_template('forgetPassword.html', title='Forgot Password', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        mongo.db.users.insert({'name':form.username.data, 'password': hashed_password,'email':form.email.data})
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    users = mongo.db.users
    form = Login()
    login_user = users.find_one({'name' : form.email.data})
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        users = mongo.db.users
        user = users.find_one({'email' : form.email.data})
        loggeduser = (user['name'])
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
            flash('log in succesfull','success')
            session['username'] = form.email.data
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    if 'username' in session:  
        session.pop('username',None)  
    return redirect(url_for('home'))


@app.route("/account")
def account(): 
    if 'username' not in session:
        flash('Login required to acccess account page', 'danger')
        return redirect(url_for('login'))
    return render_template('account.html', title='Account')    


@app.route("/places/<id>")
def places(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    place = id
    cities=mongo.db.city.find({'city_name':place},{'_id':0,"city_name":1,"category":1,"ratings":1,"imgUrl":1, "description":1})
    places=mongo.db.places.find({'city_name':place},{'_id':0,"place_name":1,"category":1,"ratings":1,"imgUrl":1, "description":1})
    return render_template('places.html', title='Places',placedetails=cities,place=places)

@app.route("/cities", methods=['GET', 'POST'])
def cities():
    dele = request.form.get('visit')
    print(dele)
    if 'username' not in session:
        return redirect(url_for('login'))
    cities=mongo.db.city.find({},{'_id':0,"city_name":1,"category":1,"ratings":1,"imgUrl":1})
    return render_template('cities.html', title='View',city=cities)

@app.route("/destination")
def destination():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('destination.html', title='Destination')

@app.route("/getInput", methods=["GET", "POST"])
def getInput():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif request.method=="POST":
        return render_template('showOutput.html')
    return render_template('getInput.html', title='UserInput')

@app.route("/showOutput", methods=["GET", "POST"])
def showOutput():
    if request.method == 'POST':
        #reading the original dataset
        df = pd.read_csv('cities.csv')

        #separating categories for each cities
        df = pd.concat([df, df.category.str.get_dummies(sep='|')], axis=1)


        Nature = int(request.form.get('Nature'))
        HillStation = int(request.form.get('HillStation'))
        Amusement = int(request.form.get('Amusement'))
        Temple = int(request.form.get('Temple'))
        Beach = int(request.form.get('Beach'))
        Historic = int(request.form.get('Historic'))
       

        
        resbl=[]
        if Beach==1:
            resb=df[(df["Beach"]==Beach ) ].head(5)
            resbl=resb["cities"].tolist()

        resal=[]
        if Amusement==1:
            resa=df[(df["Amusement"]==1 ) ].head(5)
            resal=resa["cities"].tolist()

        reshl=[]
        if Historic==1:
            resh=df[(df["Historic"]==1 ) ].head(5)
            reshl=resh["cities"].tolist()


        reshsl=[]
        if HillStation==1:
            reshs=df[(df["HillStation"]==1 ) ].head(5)
            reshsl=reshs["cities"].tolist()

        restl=[]
        if Temple==1:
            rest=df[(df["Temple"]==1 ) ].head(5)
            restl=rest["cities"].tolist()

        resnl=[]
        if Nature==1:
            resn=df[(df["Nature"]==1 ) ].head(5)
            resnl=resn["cities"].tolist()                
        

        output=[]
        resfinal=resbl+resal+reshl+reshsl+resnl+restl
        resfinal
        for x in resfinal: 
        # check if exists in unique_list or not 
            if x not in output: 
                output.append(x)    

        
        output=pd.Series(output)
        outputlist=output.tolist()
        table = Results(output)
        table.border = True
        return render_template('showOutput.html', table=table,out=outputlist)

@app.route("/test" , methods=['GET', 'POST'])
def test():
    select = request.form.get('comp_select')
    Responses=pd.read_excel('Tripper (Responses).xlsx')
    Responses=Responses.drop(['Timestamp', 'Enter your Name'], axis=1)
    records=[]
    for i in range(0,54):
        for j in range(0,5):
            records.append([  str(Responses.values[i,j])  for j in range(0,5)]) 

    association_rules=apriori(records,min_support=0.01,min_confidence=0.05,min_lift=0.05,max_length=3)
    rules=list(association_rules)  

    Rules = [list(rules[i][0]) for i in range(0,len(rules))]
    Clean_Rules = [x for x in Rules if str(x) != 'nan']

    Antecedent=[list(rules[i][2][0][0]) for i in range(0,len(rules))]
    Consequent=[list(rules[i][2][0][1]) for i in range(0,len(rules))]
    Support=[rules[i][1] for i in range(0,len(rules))]
    Confidence=[rules[i][2][0][2] for i in range(0,len(rules))]
    Lift=[rules[i][2][0][3] for i in range(0,len(rules))]      


    all1=pd.DataFrame({'Rules':Clean_Rules,'Antecedent':Antecedent,'Consequent':Consequent,'Support':Support,'Confidence':Confidence,'Lift':Lift})

    all1['Consequent']=all1['Consequent'].apply(lambda x: ', '.join(map(str, x)))    
    all1['Antecedent'] = all1['Antecedent'].dropna().apply(lambda x: ', '.join(map(str, x)))
    recommend = all1[all1['Antecedent'].notnull() & (all1['Antecedent'] == select)]
    finrec=recommend["Consequent"].head()
    print(type(finrec))
    finreclist =finrec.tolist()
    finreclist = [subl.split(',') for subl in finreclist]
    flatList = [ item for elem in finreclist for item in elem]
    def unique_list(l):
        x = []
        print("hi")
        for a in l:
            if a not in x:
                x.append(a)
        return x
    recommendation = unique_list(flatList)

    # originLat='51.4822656'
    # originLong='-0.1933769'

    # destLat ='51.4994794'
    # destLong ='-0.1269979'
    # url = "https://api.distancematrix.ai/maps/api/distancematrix/json?origins="+originLat+','+originLong+"&destinations="+destLat+','+destLong+"&key=cGRVeTF5nQj5pV3m2Ha996n2aU3dN"

    # r = requests.get(url)

    # data = r.json()

    # for d in data['rows']:
    #     for e in d['elements']:
    #         dist=e['distance']['text'];
    #         print(dist)

    return render_template('finrec.html', fin=recommendation, )        


@app.route("/test1" , methods=['GET', 'POST'])
def test1():
    dele = request.form.get('delcity_select')
    mongo.db.city.delete_one({"city_name":dele}) 
    print(dele)
    return str(dele)

@app.route("/test11" , methods=['GET', 'POST'])
def test11():
    dele = request.form.get('delplace_select')
    mongo.db.places.delete_one({"place_name":dele}) 
    print(dele)
    return str(dele)

@app.route("/updatecityname" , methods=['GET', 'POST'])
def updatecityname():
    form=updateCity()
    updatecity = request.form.get('updatecity')
    newratings=form.ratings.data
    cities = mongo.db.city
    cities = cities.update_one({'city_name' : updatecity},{"$set":{'ratings':newratings}})
    return str(updatecity)   

@app.route("/updateplacename" , methods=['GET', 'POST'])
def updateplacename():
    form=updatePlace()
    updateplace = request.form.get('updateplace')
    newratings=form.ratings.data
    print(updateplace)
    print(newratings)
    places = mongo.db.places
    places = places.update_one({'place_name' : updateplace},{"$set":{'ratings':newratings}})
    return str(updateplace)   