from flask import Flask, render_template, redirect, request, url_for #importing Flask, render_template, redirect, request, url_for
import sqlite3 #importing sqlite3 module
import web_functions #importing web_functions module
import os #importing os module
from werkzeug.utils import secure_filename #importing secure_filename from werkzeug.utils
app = Flask(__name__) #creating an instance of the Flask class

@app.route('/', methods=["GET", "POST"]) #decorator that creates a route for the home page
def home():
        if request.method == "POST": #if the request method is POST
            recipename = request.form["recipeName"] #get the recipeName from the form
            if web_functions.check_recipe(recipename) == True: #if the recipeName is in the database
                db = sqlite3.connect("database/recipe.db") #connecting to the database
                db.row_factory = sqlite3.Row #setting the row factory to sqlite3.Row
                data = db.execute("SELECT * FROM Recipe WHERE recipeName LIKE ?", (recipename,)).fetchall() #fetching all the data from the Recipe table where the recipeName is like the recipename
                return render_template('home.html', recipe=data, search=recipename) #rendering the home.html template with the data and the recipename
            else: #if the recipeName is not in the database
                return render_template('home.html',message="Recipe not found") #rendering the home.html template with a message
        return render_template("home.html") #rendering the home.html template


app.config["UPLOAD_FOLDER"] = "static/images/" #setting the upload folder to static/images

@app.route('/addRecipe', methods=['GET', 'POST']) #decorator that creates a route for the addRecipe page
def add_recipe():
    if request.method == "POST":   #if the request method is POST
        recipename = request.form['recipeName']    #get the recipeName from the form
        date = request.form['date'] 
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        notes = request.form['notes']
        recipeID = request.form['recipeID']
        image_file = request.files["image"]
        if image_file and image_file.filename != "": #if the image file exists and the filename is not empty
            filename = secure_filename(image_file.filename) #secure the filename
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename) #join the upload folder and the filename
            image_file.save(image_path) #save the image file
        else: #if the image file does not exist or the filename is empty
            image_path = "static/images/default.jpg" #set the image path to static/images/default.jpg

        if web_functions.check_recipe_ID(recipeID) == False: #if the recipeID is not in the database
            db = sqlite3.connect("database/recipe.db") #connecting to the database
            db.execute("INSERT INTO Recipe(recipeName, date, ingredients, instructions, notes, recipeID, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)", (recipename, date, ingredients, instructions, notes, recipeID, image_path)) #inserting the recipeName, date, ingredients, instructions, notes, recipeID, and image_path into the Recipe table
            db.commit() #commit the changes

            message = "Your recipe is added!" #gives the message in the website that the recipe is added
            return render_template('addRecipe.html', confirm=message) #render the addRecipe.html template with the message
        else:
            return render_template('addRecipe.html', error="Recipe ID is already taken, Choose another one") #render the addRecipe.html template with an error message

    return render_template('addRecipe.html')

app.config["UPLOAD_FOLDER"] = "static/images/" #setting the upload folder to static/images

@app.route('/update', methods=['GET', 'POST']) #decorator that creates a route for the update page
def update(): 
    if request.method == "POST":
        recipename = request.form['recipeName']
        date = request.form['date']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        notes = request.form['notes']
        recipeID = request.form['recipeID']
        image_file = request.files["image"]
        if image_file and image_file.filename != "": #if the image file exists and the filename is not empty
            filename = secure_filename(image_file.filename) #secure the filename
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename) #join the upload folder and the filename
            image_file.save(image_path) #save the image file
            image_url=image_path #set the image_url to the image_path
        else: #if the image file does not exist or the filename is empty
            image_url = "static/images/default.jpg" #set the image_url to static/images/default.jpg

        if web_functions.check_recipe_ID(recipeID) == True: #if the recipeID is in the database
            db = sqlite3.connect("database/recipe.db") #connecting to the database
            db.execute("UPDATE Recipe SET recipeName=?, date=?, ingredients=?, instructions=?, notes=?, image_url=? WHERE recipeID=?", (recipename, date, ingredients, instructions, notes, image_url, recipeID)) #updating the Recipe table with the recipeName, date, ingredients, instructions, notes, image_url where the recipeID is equal to the recipeID
            db.commit()

            message = "Your recipe is Updated!" #gives the message in the website that the recipe is updated
            return render_template('update.html', confirm=message) #render the update.html template with the message
        else: #if the recipeID is not in the database
            return render_template('update.html', error="Couldn't update the Recipe") #render the update.html template with an error message which says that the recipe couldn't be updated

    return render_template('update.html') #render the update.html template


@app.route('/catalogue')
def catalogue():
    db = sqlite3.connect("database/recipe.db")
    db.row_factory = sqlite3.Row
    RecipeData = db.execute("SELECT * FROM Recipe").fetchall() #fetching all the data from the Recipe table
    return render_template('catalogue.html', recipe=RecipeData) 

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == "POST":
        recipeID = request.form['recipeID']

        if web_functions.check_recipe_ID(recipeID) == True: #if the recipeID is in the database
            db = sqlite3.connect("database/recipe.db")
            db.row_factory = sqlite3.Row
            db.execute("DELETE FROM Recipe WHERE RecipeID=?", (recipeID,)) #deleting the data from the Recipe table where the recipeID is equal to the recipeID
            db.commit()
            return render_template('delete.html', message="Your Recipe is deleted") #render the delete.html template and give a message in the website that the recipe is deleted
        else:
            return render_template('delete.html',message="Recipe ID not found") #render the delete.html template and give a message in the website that the recipe ID is not found
    return render_template("delete.html")

if __name__ == "__main__": #if the name is equal to main
    app.run(debug=True) #run the app on port 5000

