from flask import Flask, render_template, request, jsonify, redirect, url_for
import database
from post import Post
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
db = database.dbConnection()


@app.route("/")
def home():
    posts = db["posts"]
    postsReceived = list(posts.find())
    return render_template("index.html", posts=postsReceived)


@app.route("/posts", methods=["POST"])
def add_post():
    posts = db["posts"]
    title = request.form.get("title")
    content = request.form.get("content")
    username = request.form.get("username")

    if not title or not content or not username:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        post = Post(title, content, username)
        result = posts.insert_one(post.to_collection())

        if result.inserted_id:
            return redirect(url_for("home"))
        else:
            return jsonify({"error": "No se pudo insertar el post"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/edit/<string:post_id>", methods=["POST"])
def edit_post(post_id):
    posts = db["posts"]

    title = request.form.get("title")
    content = request.form.get("content")
    # username = request.form.get("username")

    # if not title or not content or not username:
    if not title or not content:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        result = posts.update_one(
            {"_id": ObjectId(post_id)},
            {
                "$set": {
                    "title": title,
                    "content": content,
                    # "username": username,
                    "updatedAt": datetime.now(),
                }
            },
        )

        if result.matched_count > 0:
            return redirect(url_for("home"))
        else:
            return jsonify({"error": "No se encontró el post"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/delete/<string:post_id>")
def delete_post(post_id):
    posts = db["posts"]

    try:
        result = posts.delete_one({"_id": ObjectId(post_id)})
        if result.deleted_count > 0:
            return redirect(url_for("home"))
        else:
            return not_found()
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/posts/comment", methods=["POST"])
def add_comment():
    posts = db["posts"]

    post_id = request.form.get("post_id")
    username = request.form.get("username")
    comment_text = request.form.get("text")

    if not post_id or not username or not comment_text:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    comment = {
        "_id": ObjectId(),
        "username": username,
        "text": comment_text,
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
    }

    result = posts.update_one(
        {"_id": ObjectId(post_id)},
        {"$push": {"comments": comment}, "$set": {"updatedAt": datetime.now()}},
    )

    if result.modified_count > 0:
        return redirect(request.referrer or "/")
    else:
        return jsonify({"error": "No se encontró el post"}), 404


@app.route("/posts/comment/edit", methods=["POST"])
def edit_comment():
    posts = db["posts"]

    post_id = request.form.get("post_id")
    comment_id = request.form.get("comment_id")
    new_text = request.form.get("text")

    if not post_id or not comment_id or not new_text:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    result = posts.update_one(
        {"_id": ObjectId(post_id), "comments._id": ObjectId(comment_id)},
        {
            "$set": {
                "comments.$.text": new_text,
                "comments.$.updatedAt": datetime.now(),
            }
        },
    )

    if result.modified_count > 0:
        return redirect(request.referrer or "/")
    else:
        return jsonify({"error": "Comentario no encontrado"}), 404


@app.route("/posts/<string:post_id>/comments/<string:comment_id>")
def delete_comment(post_id, comment_id):
    posts = db["posts"]

    try:
        result = posts.update_one(
            {"_id": ObjectId(post_id)},
            {
                "$pull": {"comments": {"_id": ObjectId(comment_id)}},
                "$set": {"updatedAt": datetime.now()},
            },
        )

        if result.modified_count > 0:
            return redirect(url_for("home"))
        else:
            return not_found()

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error=None):
    return (
        jsonify({"error": "Recurso no encontrado", "url": request.url, "status": 404}),
        404,
    )


if __name__ == "__main__":
    app.run(debug=True)
