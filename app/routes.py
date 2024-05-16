from app import app
from flask import render_template

@app.route("/")
@app.route("/index")
@app.route("/search")
def index():
    # display search page
    # get search request
    # return result
    return "<p>Search Page.</p>"

@app.route("/doc=<id>")
def document(id):
    # get document with specific id
    print("Requesting doc: ", id)
    title, head, content= "doc title", "doc header", "doc content......."
    return render_template("doc.html", id=id, title=title, head=head, content=content)

@app.route("/test")
def test():
    # to run flask: $flask --app app run
    global app
    return "<p>Server is on.</p>"
