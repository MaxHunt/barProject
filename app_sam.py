from flask import Flask, render_template

from presets import PresetsAPI

app = Flask(__name__)
presets_view = PresetsAPI.as_view('presets')
app.add_url_rule('/presets/', view_func= presets_view, methods = ['GET', 'POST'])
app.add_url_rule('/presets/<string:preset_id>', view_func = presets_view, methods=['PUT', 'DELETE'])

#Flask and Ajax returns
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
