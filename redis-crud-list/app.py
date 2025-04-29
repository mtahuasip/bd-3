from flask import Flask, render_template, request, redirect, url_for
import redis

app = Flask(__name__)
r = redis.Redis(host="localhost", port=6379, decode_responses=True)


@app.route("/", methods=["GET"])
def index():
    subjects = r.lrange("subjects", 0, -1)
    return render_template("index.html", subjects=enumerate(subjects))


@app.route("/add-subject", methods=["GET", "POST"])
def add_subject():
    if request.method == "POST":
        subject = request.form.get("subject")
        if subject:
            r.rpush("subjects", subject)
            r.expire("subjects", 3600)
        return redirect(url_for("index"))
    return render_template("add_subject.html")


@app.route("/update-subject/<int:index>", methods=["GET", "POST"])
def update_subject(index):
    subjects = r.lrange("subjects", 0, -1)
    if request.method == "POST":
        new_subject = request.form.get("subject")
        if new_subject:
            r.lset("subjects", index, new_subject)
        return redirect(url_for("index"))
    if 0 <= index < len(subjects):
        current_subject = subjects[index]
        return render_template(
            "update_subject.html", index=index, subject=current_subject
        )
    return redirect(url_for("index"))


@app.route("/delete-subject/<int:index>", methods=["POST"])
def delete_subject(index):
    subjects = r.lrange("subjects", 0, -1)
    if 0 <= index < len(subjects):
        r.lset("subjects", index, "__TO_DELETE__")
        r.lrem("subjects", 1, "__TO_DELETE__")
    return redirect(url_for("index"))
