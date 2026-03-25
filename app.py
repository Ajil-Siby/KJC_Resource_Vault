from flask import Flask, render_template, request, redirect, flash, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
# CRITICAL: Secret key is required for the 'flash' system to work
app.secret_key = "kjc_neural_vault_2026" 

# Cloud Connection
uri = "mongodb+srv://ajilsiby01_db_user:lcAseHOqFU2qjp2r@cluster0.ixxrisn.mongodb.net/?appName=Cluster0"

try:
    client = MongoClient(uri)
    db = client['KJC_Vault_DB']    
    collection = db['resources']
    print("Neural Link Established: MongoDB Atlas Connected.")
except Exception as e:
    print(f"Connection Error: {e}")

@app.route('/')
def index():
    search_query = request.args.get('search')
    query = {}
    if search_query:
        # Regex allows for partial, case-insensitive matching
        query["title"] = {"$regex": search_query, "$options": "i"}
    
    items = list(collection.find(query).sort("_id", -1))
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_resource():
    title = request.form.get('title')
    url = request.form.get('url')
    category = request.form.get('category')
    
    if title and url:
        collection.insert_one({"title": title, "url": url, "category": category})
        flash(f"Success: '{title}' has been synced to the cloud.", "success")
    else:
        flash("Error: Data packet incomplete.", "danger")
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete_resource(id):
    collection.delete_one({"_id": ObjectId(id)})
    flash("Resource purged from the vault.", "info")
    return redirect(url_for('index'))

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_resource(id):
    if request.method == 'POST':
        collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "title": request.form.get('title'),
                "url": request.form.get('url'),
                "category": request.form.get('category')
            }}
        )
        flash("System Update: Resource parameters modified.", "success")
        return redirect(url_for('index'))
    
    item = collection.find_one({"_id": ObjectId(id)})
    return render_template('edit.html', item=item)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)