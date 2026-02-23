from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Cloud Connection
uri = "mongodb+srv://ajilsiby01_db_user:lcAseHOqFU2qjp2r@cluster0.ixxrisn.mongodb.net/?appName=Cluster0"

try:
    client = MongoClient(uri)
    db = client['KJC_Vault_DB']    
    collection = db['resources']
    client.admin.command('ping')
    print("Successfully connected to MongoDB Atlas Cloud!")
except Exception as e:
    print(f"Connection Error: {e}")

@app.route('/')
def index():
    # 1. Look for a category filter in the URL (e.g., /?category=Data+Structures)
    selected_category = request.args.get('category')
    
    if selected_category:
        # Filter results based on the chosen course
        items = list(collection.find({"category": selected_category}).sort("_id", -1))
    else:
        # If no filter is active, show all resources
        items = list(collection.find().sort("_id", -1))
        
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_resource():
    # 2. Extract the title, url, AND the selected category from the form
    title = request.form.get('title')
    url = request.form.get('url')
    category = request.form.get('category')
    
    if title and url:
        # 3. Save the resource with its category to the cloud
        collection.insert_one({
            "title": title, 
            "url": url, 
            "category": category
        })
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)