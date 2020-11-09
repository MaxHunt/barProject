import json
import os

from flask import Response, request
from flask.json import jsonify
from flask.views import MethodView

class PresetsAPI(MethodView):
  def get(self):
    return json.dumps(self.load_presets()), 200, { 'Content-Type': 'application/json' }

  def post(self):
    return ('Post Preset'), 200

  def delete(self, preset_id):
    return ('Delete Preset'), 200

  def put(self, preset_id):
    return ('Update Preset'), 200

  def load_presets(self):
    directory = os.path.dirname(os.path.abspath(__file__))
    presets_path = os.path.join(directory, 'data', 'presets.json')
    with open(presets_path) as f:
      presets_data = f.read()

    return json.loads(presets_data)
