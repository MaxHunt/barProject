import os

from flask.json import jsonify
from flask.views import MethodView

class PresetsAPI(MethodView):
  def get(self):
    directory = os.path.dirname(os.path.abspath(__file__))
    presets_path = os.path.join(directory, 'data', 'presets.json')
    with open(presets_path) as f:
      presets_data = f.read()
    return presets_data, 200

  def post(self):
    return ('Post Preset'), 200
