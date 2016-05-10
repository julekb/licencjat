/**
 * modified jspsych-similarity.js
 * This plugin create a trial where one image id shown, and the subject rates it using a slider controlled with the mouse.
 *
 */

//globalne zmienne tutaj
jsPsych.plugins.similarity = (function() {

  var plugin = {};

  jsPsych.pluginAPI.registerPreload('similarity', 'stimuli', 'image');

  plugin.trial = function(display_element, trial) {

    // default parameters
    trial.labels = (typeof trial.labels === 'undefined') ? ["Not at all similar", "Identical"] : trial.labels;
    trial.img_labels = trial.img_labels || null; //urls to image labels for slider
    trial.intervals = trial.intervals || 100;
    trial.show_ticks = (typeof trial.show_ticks === 'undefined') ? false : trial.show_ticks;

    trial.show_response = trial.show_response || "FIRST_STIMULUS";

    trial.timing_first_stim = trial.timing_first_stim || 1000; // default 1000ms
    trial.timing_fixation = 500;
    trial.timing_mask = 100;

    trial.is_html = (typeof trial.is_html === 'undefined') ? false : trial.is_html;
    trial.prompt = (typeof trial.prompt === 'undefined') ? '' : trial.prompt;

    // if any trial variables are functions
    // this evaluates the function and replaces
    // it with the output of the function
    trial = jsPsych.pluginAPI.evaluateFunctionParameters(trial);

    // this array holds handlers from setTimeout calls
    // that need to be cleared if the trial ends early
    var setTimeoutHandlers = [];

    // show the images
    showFixationScreen();
   

    setTimeoutHandlers.push(setTimeout(function() {
      $('#jspsych-sim-stim').attr('src', trial.stimuli[0])
      setTimeoutHandlers.push(setTimeout(function() {
        showMaskScreen();
      }, trial.timing_first_stim));
    }, trial.timing_fixation));


    function showBlankScreen() {

      $('#jspsych-sim-stim').css('visibility', 'hidden');
      setTimeoutHandlers.push(setTimeout(function() {
      if (trial.show_response == "POST_STIMULUS") {
        show_response_slider(display_element, trial);
      }
    }, trial.timing_first_stim));
      
    }


    function showFixationScreen(){
      display_element.append($('<img>', {
        "src": 'img/cross.png',
        "id": 'jspsych-sim-stim'
      }));
    }


    function showMaskScreen(){
      $('#jspsych-sim-stim').attr('src', 'img/mask.png')
      setTimeoutHandlers.push(setTimeout(function() {
        showBlankScreen();
      }, trial.timing_mask));

    }

    function showCommunicationWithPeer(){

    }


    function show_response_slider(display_element, trial) {

      var startTime = (new Date()).getTime();

      // create slider
      display_element.append('<img src="img/dots/dots_007.png" style="float: left" width=25% border=1.5 style="PADDING-TOP: 10px;" /> ');
      // display_element.append($('<div>', {
      //   "id": 'slider',
      //   "class": 'sim'
      // }));
      display_element.append('<div id="slider" class="sim" style="float: middle"> </div> ');
      display_element.append('<img src="img/dots/dots_200.png" style="float: right;" width=25% border=1.5/>');

      $("#slider").slider({
        value: Math.ceil(trial.intervals / 2),
        min: 1,
        max: trial.intervals,
        step: 0.01,
      });

      // show tick marks
      if (trial.show_ticks) {
        for (var j = 1; j < trial.intervals - 1; j++) {
          $('#slider').append('<div class="slidertickmark"></div>');
        }

        $('#slider .slidertickmark').each(function(index) {
          var left = (index + 1) * (100 / (trial.intervals - 1));
          $(this).css({
            'position': 'absolute',
            'left': left + '%',
            'width': '1px',
            'height': '100%',
            'background-color': '#222222'
          });
        });
      }

      // create labels for slider
      
      // display_element.append($('<ul>', {
      //   "id": "sliderlabels",
      //   "class": 'sliderlabels',
      //   "css": {
      //     "width": "100%",
      //     "height": "3em",
      //     "margin": "10px 0px 0px 0px",
      //     "padding": "0px",
      //     "display": "block",
      //     "position": "relative"
      //   }
      // }));

      // display_element.append($('<img>', {
      //   "src": 'img/cross.png',
      //   "id": 'jspsych-sim-stim'
      // }));

      // <img src="img_label_0.jpg" style="float: left" />
      // <div id="slider" style="float: left"></div>
      // <img src="img_label_1.jpg" style="float: left" />



      // if (trial.img_labels == null) {
      //     display_element.append($('<ul>', {
      //       "id": "sliderlabels",
      //       "class": 'sliderlabels',
      //       "css": {
      //         "width": "100%",
      //         "height": "3em",
      //         "margin": "10px 0px 0px 0px",
      //         "padding": "0px",
      //         "display": "block",
      //         "position": "relative",
      //         //"border-style": "solid"
      //       }}));
      //   for (var j = 0; j < trial.labels.length; j++) {
      //     $("#sliderlabels").append('<li>' + trial.labels[j] + '</li>');
      //   }}
      // else {
      //   // display_element.append($('<img>', {
      //   //     "src": trial.img_labels[0],
      //   //     "id": 'jspsych-sim-stim',
      //   //     "css": {
      //   //       "width": "25%",
      //   //       " height": "25%",
      //   //       "float": "left",
      //   //       "margin": "10px -0px 0px 0px",
      //   //       "border-style": "groove"
      //   //     }}));
      //   display_element.append('<img src="img/dots/dots_007.png" style="float: left "width="25%"/> ')
      //   display_element.append($('<img>', {
      //       "src": trial.img_labels[1],
      //       "id": 'jspsych-sim-stim',
      //       "css": {
      //         "width": "25%",
      //         " height": "25%",
      //         "float": "right",
      //         "margin": "10px 0px 0px 0px",
      //         "border-style": "groove"
      //       }}));
      // }
      

      // position labels to match slider intervals
      var slider_width = $("#slider").width();
      var num_items = trial.labels.length;
      var item_width = slider_width / num_items;
      var spacing_interval = slider_width / (num_items - 1);

      $("#sliderlabels li").each(function(index) {
        $(this).css({
          'display': 'inline-block',
          'width': item_width + 'px',
          'margin': '0px',
          'padding': '0px',
          'text-align': 'center',
          'position': 'absolute',
          'left': (spacing_interval * index) - (item_width / 2)
        });
      });

      //  create button
      display_element.append($('<button>', {
        'id': 'next',
        'class': 'sim',
        'html': 'Dodaj odpowiedź',
        'css':{
          'float': 'middle',
          'margin': '10px'
        }
      }));

      // if prompt is set, show prompt
      if (trial.prompt !== "") {
        display_element.append(trial.prompt);
      }

      $("#next").click(function() {
        var endTime = (new Date()).getTime();
        var response_time = endTime - startTime;

        // kill any remaining setTimeout handlers
        for (var i = 0; i < setTimeoutHandlers.length; i++) {
          clearTimeout(setTimeoutHandlers[i]);
        }

        var score = $("#slider").slider("value");
        var trial_data = {
          "sim_score": score,
          "rt": response_time,
          "stimulus": trial.stimuli[0]
        };
        // goto next trial in block
        display_element.html('');

        // send message and read from and to peer, wyswietlanie 2 suwaków, zadaje pytanie, przyjęcie odpowiedzi
        jsPsych.finishTrial(trial_data);
      });
    }
  };
  return plugin;
})();