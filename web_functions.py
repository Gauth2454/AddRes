import sqlite3 #importing sqlite3 module
def check_recipe(word): #defining a function called check_recipe
    db = sqlite3.connect("database/recipe.db") #connecting to the database
    db.row_factory = sqlite3.Row #setting the row factory to sqlite3.Row
    data = db.execute("SELECT recipeName FROM Recipe WHERE recipeName = ?", (word,)).fetchone() #fetching the recipeName from the Recipe table where the recipeName is equal to the word
    return data is not None #returns True if the word is in the data

def check_recipe_ID(word): #defining a function called check_recipe
    db = sqlite3.connect("database/recipe.db") #connecting to the database
    db.row_factory = sqlite3.Row #setting the row factory to sqlite3.Row
    data = db.execute("SELECT recipeID FROM Recipe WHERE recipeID = ?", (word,)).fetchone() #fetching the recipeID from the Recipe table where the recipeID is equal to the word
    return data is not None #returns True if the recipeID is in the data

