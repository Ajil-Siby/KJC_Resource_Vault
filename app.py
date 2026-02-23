from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId # Crucial for finding specific items by ID

app = Flask(__name__)

# Cloud Connection - Using your verified Atlas URI
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
    # Filter results by category if a filter button is clicked
    selected_category = request.args.get('category')
    
    if selected_category:
        items = list(collection.find({"category": selected_category}).sort("_id", -1))
    else:
        # Default view: show all entries
        items = list(collection.find().sort("_id", -1))
        
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_resource():
    title = request.form.get('title')
    url = request.form.get('url')
    category = request.form.get('category')
    
    if title and url:
        # Save to the cloud collection
        collection.insert_one({
            "title": title, 
            "url": url, 
            "category": category
        })
    return redirect('/')

# --- NEW: DELETE ROUTE ---
@app.route('/delete/<id>')
def delete_resource(id):
    # collection.delete_one removes the specific document from Atlas
    collection.delete_one({"_id": ObjectId(id)})
    return redirect('/')

# --- NEW: MODIFY (EDIT) ROUTE ---
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_resource(id):
    if request.method == 'POST':
        # Apply the updated values from the edit form
        collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "title": request.form.get('title'),
                "url": request.form.get('url'),
                "category": request.form.get('category')
            }}
        )
        return redirect('/')
    
    # For GET requests, find the existing data to pre-fill the form
    item = collection.find_one({"_id": ObjectId(id)})
    return render_template('edit.html', item=item)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)