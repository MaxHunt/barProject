$(document).ready(function () {
  buildPresetDropdown();
});

//Shelves
var colorPicker1 = new iro.ColorPicker('#picker1');
var colorPicker2 = new iro.ColorPicker('#picker2');
var colorPicker3 = new iro.ColorPicker('#picker3');
var colorPicker4 = new iro.ColorPicker('#picker4');
var colorPicker5 = new iro.ColorPicker('#picker5');
var colorPicker6 = new iro.ColorPicker('#picker6');
var colorPicker7 = new iro.ColorPicker('#picker7');
var colorPicker8 = new iro.ColorPicker('#picker8');

// //Floor
var colorPicker10 = new iro.ColorPicker('#picker10');
var colorPicker11 = new iro.ColorPicker('#picker11');
var colorPicker12 = new iro.ColorPicker('#picker12');

//Blackboard
var colorPicker13 = new iro.ColorPicker('#picker13');

let presets = [];

function buildPresetDropdown() {
  $.ajax({
    type: 'GET',
    url: '/presets/',
    success: function (data) {
      presets = data;
      presets.forEach((preset) => {
        $('#preset-dropdown').append(`<option value="${preset.name.toLowerCase()}">${preset.name}</option>`);
      });
    },
    error: function () {
      console.error('Failed to retrieve presets');
    }
  });
}

$('#preset-dropdown').on('change', function () {
  for (let i = 0; i < presets.length; i++) {
    if (presets[i].name.toLowerCase() === this.value) {
      setPreset(presets[i]);
    }
  }
});

$('#add-preset-button').on('click', function () {
  const name = $('#add-preset-name').val();
  if (name === '') {
    console.error('Please provide a name for the new preset');
  } else {
    const id = name.toLowerCase().replace(' ', '_');
    const data = {
      id,
      name,
      shelf1: hexToRgb(colorPicker1.color),
      shelf2: hexToRgb(colorPicker2.color),
      shelf3: hexToRgb(colorPicker3.color),
      shelf4: hexToRgb(colorPicker4.color),
      shelf5: hexToRgb(colorPicker5.color),
      shelf6: hexToRgb(colorPicker6.color),
      shelf7: hexToRgb(colorPicker7.color),
      shelf8: hexToRgb(colorPicker8.color),
      floorLeft: hexToRgb(colorPicker10.color),
      floorMiddle: hexToRgb(colorPicker11.color),
      floorRight: hexToRgb(colorPicker12.color),
      blackboard: hexToRgb(colorPicker13.color),
    };
    $.ajax({
      type: 'POST',
      url: '/presets/',
      headers: {
        'Content-Type': 'application/json'
      },
      data,
      success: function (data) {
        console.log('Success');
      },
      error: function () {
        console.error('Failed to save preset \'', data.name, '\'');
      }
    });
  }
});

function setStripColor(shelf, hexColor) {
  $('.shelf[number=' + shelf + '] .strip').css('background', hexColor);
}

function setPreset(preset) {
  // Set strips
  setStripColor(1, `rgb(${preset.shelf1.r}, ${preset.shelf1.g}, ${preset.shelf1.b}`);
  setStripColor(2, `rgb(${preset.shelf2.r}, ${preset.shelf2.g}, ${preset.shelf2.b}`);
  setStripColor(3, `rgb(${preset.shelf3.r}, ${preset.shelf3.g}, ${preset.shelf3.b}`);
  setStripColor(4, `rgb(${preset.shelf4.r}, ${preset.shelf4.g}, ${preset.shelf4.b}`);
  setStripColor(5, `rgb(${preset.shelf5.r}, ${preset.shelf5.g}, ${preset.shelf5.b}`);
  setStripColor(6, `rgb(${preset.shelf6.r}, ${preset.shelf6.g}, ${preset.shelf6.b}`);
  setStripColor(7, `rgb(${preset.shelf7.r}, ${preset.shelf7.g}, ${preset.shelf7.b}`);
  setStripColor(8, `rgb(${preset.shelf8.r}, ${preset.shelf8.g}, ${preset.shelf8.b}`);

  setStripColor(10, `rgb(${preset.floorLeft.r}, ${preset.floorLeft.g}, ${preset.floorLeft.b}`);
  setStripColor(11, `rgb(${preset.floorMiddle.r}, ${preset.floorMiddle.g}, ${preset.floorMiddle.b}`);
  setStripColor(12, `rgb(${preset.floorRight.r}, ${preset.floorRight.g}, ${preset.floorRight.b}`);

  setStripColor(13, `rgb(${preset.blackboard.r}, ${preset.blackboard.g}, ${preset.blackboard.b}`);

  // Set lights
  setShelfLights(1, preset.shelf1.r, preset.shelf1.g, preset.shelf1.b);
  setShelfLights(2, preset.shelf2.r, preset.shelf2.g, preset.shelf2.b);
  setShelfLights(3, preset.shelf3.r, preset.shelf3.g, preset.shelf3.b);
  setShelfLights(4, preset.shelf4.r, preset.shelf4.g, preset.shelf4.b);
  setShelfLights(5, preset.shelf5.r, preset.shelf5.g, preset.shelf5.b);
  setShelfLights(6, preset.shelf6.r, preset.shelf6.g, preset.shelf6.b);
  setShelfLights(7, preset.shelf7.r, preset.shelf7.g, preset.shelf7.b);
  setShelfLights(8, preset.shelf8.r, preset.shelf8.g, preset.shelf8.b);

  setShelfLights(10, preset.floorLeft.r, preset.floorLeft.g, preset.floorLeft.b);
  setShelfLights(11, preset.floorMiddle.r, preset.floorMiddle.g, preset.floorMiddle.b);
  setShelfLights(12, preset.floorRight.r, preset.floorRight.g, preset.floorRight.b);

  setShelfLights(13, preset.blackboard.r, preset.blackboard.g, preset.blackboard.b);
  // Set Color Pickers: TODO
}

function setShelfLights(shelf, r, g, b) {
  const data = {
    colour: { r, g, b },
    shelf: shelf.toString()
  };
  $.ajax({
    type: 'POST',
    url: '/api/shelfLights',
    dataType: 'String',
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(data),
    success: function (callback) {
      console.log(callback);
      // Watch out for Cross Site Scripting security issues when setting dynamic content!
      $(this).html("They are on");
    },
    error: function () {
      $(this).html("error!");
    }
  });
}

let selectedColor = '#000000';

colorPicker1.on('color:change', function (color) {
  selectedColor = color.hexString;
});
colorPicker2.on('color:change', function (color) {
  selectedColor = color.hexString;
});
colorPicker3.on('color:change', function (color) {
  selectedColor = color.hexString;
});
colorPicker4.on('color:change', function (color) {
  selectedColor = color.hexString;
});
colorPicker5.on('color:change', function (color) {
  selectedColor = color.hexString;
});
colorPicker6.on('color:change', function (color) {
  selectedColor = color.hexString;
});
colorPicker7.on('color:change', function (color) {
  selectedColor = color.hexString;
});
colorPicker8.on('color:change', function (color) {
  selectedColor = color.hexString;
});
colorPicker10.on('color:change', function (color) {
  selectedColor = color.hexString;
});
colorPicker11.on('color:change', function (color) {
  selectedColor = color.hexString;
});
colorPicker12.on('color:change', function (color) {
  selectedColor = color.hexString;
});
colorPicker13.on('color:change', function (color) {
  selectedColor = color.hexString;
});

$('.picker').on('pointerup', function (e) {
  const shelf = e.currentTarget.attributes.getNamedItem('name').value;

  const data = {
    colour: hexToRgb(selectedColor),
    shelf: shelf
  };

  setStripColor(shelf, selectedColor);

  $.ajax({
    type: 'POST',
    url: '/api/shelfLights',
    dataType: 'text',
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(data),
    success: function (response) {
      console.log(`${response} - Shelf ${shelf} set to a colour`);
    },
    error: function () {
      console.log($`Couldn't set Shelf ${shelf} colour`);
    }
  });
});

function hexToRgb(hex) {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
}

$("#raise").click(function (e) {
  e.preventDefault();

  $('#raise-button').prop('disabled', true);

  $.ajax({
    type: 'POST',
    url: '/api/raise',
    dataType: 'text',
    contentType: 'application/json; charset=utf-8',
    success: function (response) {
      console.log(`${response} - Secret Revealed!`);
      $('#lower-button').prop('disabled', false);
    },
    error: function () {
      console.log('Error revealing secret!');
    }
  });
});

$("#lower").click(function (e) {
  e.preventDefault();

  $('#lower-button').prop('disabled', true);

  $.ajax({
    type: 'POST',
    url: '/api/lower',
    dataType: 'text',
    contentType: 'application/json; charset=utf-8',
    success: function (response) {
      console.log(`${response} - Secret Put Away!`);
      $('#raise-button').prop('disabled', false);
    },
    error: function () {
      console.log('Error putting away the secret!');
    }
  });
});

$("#decanter").click(function (e) {
  e.preventDefault();
  const starWars = document.getElementById('starwars');
  starWars.paused ? starWars.play() : starWars.pause();
});

$("#fab").click(function (e) {
  e.preventDefault();
  const fab = document.getElementById('thunderbirds');
  console.log(fab)
  fab.play()
  $.ajax({
    type: 'POST',
    url: '/api/raisefab',
    dataType: 'text',
    contentType: 'application/json; charset=utf-8',
    //data: JSON.stringify(data),
    success: function (response) {
      console.log(`${response} - Secrect Revealed!`);
      //fab.pause()
    },
    error: function () {
      console.log($`Error upon revealing secrect`);
    }
  });
});

$(".shelf").click(function (event) {
  const shelf = event.currentTarget;
  const picker = $(shelf).find('.picker')[0];
  const iroColorPicker = $(picker).find('.IroColorPicker')[0];

  if (!iroColorPicker) {
    return;
  }

  const iroPickerBounds = iroColorPicker.getBoundingClientRect();

  if (
    event.pageX >= iroPickerBounds.x &&
    event.pageY >= iroPickerBounds.y &&
    event.pageX <= iroPickerBounds.x + iroPickerBounds.width &&
    event.pageY <= iroPickerBounds.y + iroPickerBounds.height
  ) {
    console.log('Nah mate');
  } else {
    $(picker).toggleClass('picker-hidden');
  }
});

$('#allLightsOn').submit(function (e) {
  e.preventDefault();

  var data = {};

  $.ajax({
    type: 'POST',
    url: '/api/allLightsOn',
    dataType: 'String',
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(data),
    success: function (callback) {
      console.log(callback);
      // Watch out for Cross Site Scripting security issues when setting dynamic content!
      $(this).html("They are on");
    },
    error: function () {
      $(this).html("error!");
    }
  });
});

$('#allLightsOff').submit(function (e) {
  e.preventDefault();

  var data = {};

  $.ajax({
    type: 'POST',
    url: '/api/allLightsOff',
    dataType: 'String',
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(data),
    success: function (callback) {
      console.log(callback);
      // Watch out for Cross Site Scripting security issues when setting dynamic content!
      $(this).html("They are off");
    },
    error: function () {
      $(this).html("error!");
    }
  });
});

$('#movingLEDrun').submit(function (e) {
  e.preventDefault();

  var data = {};

  $.ajax({
    type: 'POST',
    url: '/api/movingLEDrun',
    dataType: 'String',
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(data),
    success: function (callback) {
      console.log(callback);
      // Watch out for Cross Site Scripting security issues when setting dynamic content!
      $(this).html("They are off");
    },
    error: function () {
      $(this).html("error!");
    }
  });
});

$('#shelfRandomColours').submit(function (e) {
  e.preventDefault();

  var data = {};

  $.ajax({
    type: 'POST',
    url: '/api/shelfRandomColours',
    dataType: 'String',
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(data),
    success: function (callback) {
      console.log(callback);
      // Watch out for Cross Site Scripting security issues when setting dynamic content!
      $(this).html("They are off");
    },
    error: function () {
      $(this).html("error!");
    }
  });
});

$('#rainbow').submit(function (e) {
  e.preventDefault();

  var data = {};

  $.ajax({
    type: 'POST',
    url: '/api/rainbow',
    dataType: 'String',
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify(data),
    success: function (callback) {
      console.log(callback);
      // Watch out for Cross Site Scripting security issues when setting dynamic content!
      $(this).html("They are off");
    },
    error: function () {
      $(this).html("error!");
    }
  });
});
