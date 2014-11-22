__author__ = 'Jake'


from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yx R~XHH!jmh]LWX/,?RT'


session_store = dict() #TODO: Thread-safe

@app.route('/')
def main():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
