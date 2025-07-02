#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# app.py

from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

import os
import uuid
from matcher import match
from utils import get_embedding
import numpy as np
from converter import convert_ply_to_depth  # Ayush's function

app = Flask(__name__)

UPLOAD_FOLDER = "ply_uploads"
DEPTH_FOLDER = "depth_maps"
EMBED_FOLDER = "embeddings"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DEPTH_FOLDER, exist_ok=True)
os.makedirs(EMBED_FOLDER, exist_ok=True)

# --------------------------
# 1. Upload and Match (API 1)
# --------------------------
@app.route('/upload', methods=['POST'])
def upload_and_match():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    scan_id = str(uuid.uuid4())
    ply_path = os.path.join(UPLOAD_FOLDER, f"{scan_id}.ply")
    file.save(ply_path)

    # Convert to depth map
    depth_path = os.path.join(DEPTH_FOLDER, f"{scan_id}.png")
    convert_ply_to_depth(ply_path, depth_path)

    # Match
    results = match(depth_path, DEPTH_FOLDER, threshold=0.9)
    if results:
        top_match = results[0]
        return jsonify({
            "match": top_match[0],
            "similarity": round(top_match[1], 4)
        })
    else:
        return jsonify({"message": "No good matches found"}), 200

# --------------------------
# 2. Register User (API 2)
# --------------------------
@app.route('/register', methods=['POST'])
def register_user():
    file = request.files.get('file')
    user_id = request.form.get('user_id')

    if not file or not user_id:
        return jsonify({"error": "Missing user_id or file"}), 400

    depth_path = os.path.join(DEPTH_FOLDER, f"{user_id}.png")
    file.save(depth_path)

    emb = get_embedding(depth_path)
    np.save(os.path.join(EMBED_FOLDER, f"{user_id}.npy"), emb.numpy())

    return jsonify({"message": f"User {user_id} registered successfully"}), 200

# --------------------------
# 3. Authenticate User (API 3)
# --------------------------
@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    temp_path = os.path.join(DEPTH_FOLDER, "temp_auth.png")
    file.save(temp_path)

    query_emb = get_embedding(temp_path)

    best_match = None
    best_score = -1

    for fname in os.listdir(EMBED_FOLDER):
        if fname.endswith(".npy"):
            user_id = fname.replace(".npy", "")
            db_emb = np.load(os.path.join(EMBED_FOLDER, fname))
            db_emb = np.array(db_emb, dtype=np.float32)

            score = float(np.dot(query_emb, db_emb) / 
                          (np.linalg.norm(query_emb) * np.linalg.norm(db_emb)))

            if score > best_score:
                best_score = score
                best_match = user_id

    if best_score >= 0.9:
        return jsonify({"user": best_match, "similarity": round(best_score, 4)})
    else:
        return jsonify({"message": "Authentication failed"}), 401

# --------------------------
# Main entry
# --------------------------

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["file"]
        action = request.form.get("action")
        user_id = request.form.get("user_id", "")

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        file_ext = filename.split(".")[-1]
        temp_path = os.path.join(DEPTH_FOLDER if file_ext == "png" else UPLOAD_FOLDER, filename)
        file.save(temp_path)

        if action == "upload":  # .ply input
            if file_ext != "ply":
                return render_template("index.html", result="❌ Upload a .ply file for this action")
            depth_path = os.path.join(DEPTH_FOLDER, f"{uuid.uuid4()}.png")
            convert_ply_to_depth(temp_path, depth_path)
            results = match(depth_path, DEPTH_FOLDER, threshold=0.9)
            if results:
                top_match = results[0]
                result = f"✅ Match found: {top_match[0]} with similarity {round(top_match[1], 4)}"
            else:
                result = "❌ No good matches found"

        elif action == "register":  # .png input
            if not user_id:
                result = "❌ User ID required for registration"
            else:
                depth_path = os.path.join(DEPTH_FOLDER, f"{user_id}.png")
                os.rename(temp_path, depth_path)  # move uploaded .png to named path
                emb = get_embedding(depth_path)
                np.save(os.path.join(EMBED_FOLDER, f"{user_id}.npy"), emb.numpy())
                result = f"✅ Registered user: {user_id}"

        elif action == "authenticate":  # .png input
            query_emb = get_embedding(temp_path)
            best_match = None
            best_score = -1
            for fname in os.listdir(EMBED_FOLDER):
                if fname.endswith(".npy"):
                    uid = fname.replace(".npy", "")
                    db_emb = np.load(os.path.join(EMBED_FOLDER, fname))
                    score = float(np.dot(query_emb, db_emb) /
                                  (np.linalg.norm(query_emb) * np.linalg.norm(db_emb)))
                    if score > best_score:
                        best_score = score
                        best_match = uid
            if best_score >= 0.9:
                result = f"✅ Authenticated as {best_match} (similarity: {round(best_score, 4)})"
            else:
                result = "❌ Authentication failed"

        else:
            result = "❌ Invalid action selected"

        return render_template("index.html", result=result)

    return render_template("index.html", result=None)

if __name__ == '__main__':
    app.run(debug=True)







