from flask import Flask, render_template, request, jsonify, redirect, url_for
import database
from library import Library
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
db = database.dbConnection()


@app.route("/")
def home():
    libs = db["bibliotecas"]
    libsReceived = list(libs.find())
    return render_template("index.html", libsList=libsReceived)


@app.route("/libs", methods=["POST"])
def add_lib():
    libs = db["bibliotecas"]
    carrera = request.form.get("carrera")
    facultad = request.form.get("facultad")

    if not carrera or not facultad:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        lib = Library(carrera, facultad)
        result = libs.insert_one(lib.to_collection())

        if result.inserted_id:
            return redirect(url_for("home"))
        else:
            return jsonify({"error": "No se pudo insertar"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/edit/<string:lib_id>", methods=["POST"])
def edit_lib(lib_id):
    libs = db["bibliotecas"]

    carrera = request.form.get("carrera")
    facultad = request.form.get("facultad")

    if not carrera or not facultad:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        result = libs.update_one(
            {"_id": ObjectId(lib_id)},
            {
                "$set": {
                    "carrera": carrera,
                    "facultad": facultad,
                    "updatedAt": datetime.now(),
                }
            },
        )

        if result.matched_count > 0:
            return redirect(url_for("home"))
        else:
            return jsonify({"error": "No se encontró"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/delete/<string:lib_id>")
def delete_lib(lib_id):
    libs = db["bibliotecas"]

    try:
        result = libs.delete_one({"_id": ObjectId(lib_id)})
        if result.deleted_count > 0:
            return redirect(url_for("home"))
        else:
            return not_found()
    except Exception as e:
        return jsonify({"error": str(e)})


@app.errorhandler(404)
def not_found(error=None):
    return (
        jsonify({"error": "Recurso no encontrado", "url": request.url, "status": 404}),
        404,
    )


if __name__ == "__main__":
    app.run(debug=True)
