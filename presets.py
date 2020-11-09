import json
import os

from flask import Response, request
from flask.json import jsonify
from flask.views import MethodView

class PresetsAPI(MethodView):
  def get(self):
    return json.dumps(self.load_presets()), 200, { 'Content-Type': 'application/json' }

  def post(self):
    preset = request.get_json()
    presets = self.load_presets()

    if self.is_valid_preset(preset):
      existing = self.get_preset(presets, preset["id"])
      if existing is None:
        presets.append(preset)

        with open(self.get_presets_path(), 'w') as f:
          f.write(json.dumps(presets, indent = 2))

        return ('Preset with ID \'%s\' added' % preset["id"]), 200
      else: 
        return ('Preset already exists with ID \'%s\'' % preset["id"]), 403
    else:
      return ('Invalid Preset Provided'), 400

  def delete(self, preset_id):
    return ('Delete Preset'), 200

  def put(self, preset_id):
    return ('Update Preset'), 200

  def get_presets_path(self):
    directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directory, 'data', 'presets.json')

  def load_presets(self):
    with open(self.get_presets_path()) as f:
      presets_data = f.read()

    return json.loads(presets_data)

  def get_preset(self, presets, preset_id):
    for preset in presets:
      if preset["id"] == preset_id:
        return preset
    return None

  def is_valid_preset(self, preset):
    if "id" not in preset:
      return False
    if "name" not in preset:
      return False
    if not self.is_valid_shelf(preset["shelf1"]):
      return False
    if not self.is_valid_shelf(preset["shelf2"]):
      return False
    if not self.is_valid_shelf(preset["shelf3"]):
      return False
    if not self.is_valid_shelf(preset["shelf4"]):
      return False
    if not self.is_valid_shelf(preset["shelf5"]):
      return False
    if not self.is_valid_shelf(preset["shelf6"]):
      return False
    if not self.is_valid_shelf(preset["shelf7"]):
      return False
    if not self.is_valid_shelf(preset["shelf8"]):
      return False
    if not self.is_valid_shelf(preset["floorLeft"]):
      return False
    if not self.is_valid_shelf(preset["floorMiddle"]):
      return False
    if not self.is_valid_shelf(preset["floorRight"]):
      return False
    if not self.is_valid_shelf(preset["blackboard"]):
      return False
    return True

  def is_valid_shelf(self, shelf):
    return "r" in shelf and type(shelf["r"]) == int and "g" in shelf and type(shelf["g"]) == int and "b" in shelf and type(shelf["b"]) == int
