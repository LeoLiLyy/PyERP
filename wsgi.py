from app import create_app
from flask import redirect

app = create_app()

@app.route("/")
def homepage_redirect():
    return redirect("/core/welcome")

if __name__ == '__main__':
    app.run(debug=True)
