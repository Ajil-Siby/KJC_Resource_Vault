from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# 1. Connect to your local MongoDB Compass
# This looks for the MongoDB server running on your laptop
client = MongoClient("mongodb://localhost:27017/")
db = client['KJC_Vault_DB']    # Your Database Name
collection = db['resources']   # Your Collection (like a Table)

@app.route('/')
def index():
    # 2. Fetch all data from MongoDB
    # .find() gets the data; .sort("_id", -1) shows newest first
    items = list(collection.find().sort("_id", -1))
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_resource():
    # 3. Get data from the HTML form
    title = request.form.get('title')
    url = request.form.get('url')
    
    if title and url:
        # 4. Insert the data into MongoDB
        collection.insert_one({"title": title, "url": url})
    
    # 5. Send the user back to the homepage to see the update
    return redirect('/')

if __name__ == '__main__':
    # Start the Flask server
    app.run(debug=True)