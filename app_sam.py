from flask import Flask, render_template

from presets import PresetsAPI

app = Flask(__name__)
app.add_url_rule('/presets/', view_func=PresetsAPI.as_view('presets'))

#Flask and Ajax returns
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
