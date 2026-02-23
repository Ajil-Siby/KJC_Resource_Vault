from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# 1. Connect to MongoDB Atlas (Cloud) instead of localhost
# Replace <db_password> with the password you copied from the Atlas screen
uri = "mongodb+srv://ajilsiby01_db_user:lcAseHOqFU2qjp2r@cluster0.ixxrisn.mongodb.net/?appName=Cluster0"

try:
    client = MongoClient(uri)
    db = client['KJC_Vault_DB']    
    collection = db['resources']
    # Trigger a quick check to ensure the cloud connection works
    client.admin.command('ping')
    print("Successfully connected to MongoDB Atlas Cloud!")
except Exception as e:
    print(f"Connection Error: {e}")

@app.route('/')
def index():
    # 2. Fetch all data from the Cloud Database
    items = list(collection.find().sort("_id", -1))
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_resource():
    # 3. Get data from the HTML form
    title = request.form.get('title')
    url = request.form.get('url')
    
    if title and url:
        # 4. Insert the data into the Cloud Database
        collection.insert_one({"title": title, "url": url})
    
    # 5. Redirect back to homepage
    return redirect('/')

if __name__ == '__main__':
    # Flask server starts here
    app.run(debug=True)