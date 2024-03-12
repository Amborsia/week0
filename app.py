from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('template.html', title='Hello, Jinja2', header='Welcome!', body='This is a Jinja2 rendered page.')

if __name__ == '__main__':
    app.run(debug=True)
