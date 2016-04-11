const N = 1;
const TIME_STIM = 3000;
const TIME_RESP = 10000;
const PHASE_1_NUM = 30;
const PHASE_2_NUM = 20;
const STIMULI = ['bardzomalo', 'malo', 'srednio', 'duzo', 'bardzoduzo','mnostwo'];
const entry_questions = ['Podaj adres e-mail', 'Podaj wiek'];


const GROUP_ID = 'G1';//G1-grupa kontrolna  lub G2-grupa eksperymentalna

jsPsych.data.addProperties({
	subject: GROUP_ID
});

function saveData_csv(filename, filedata){
	$.ajax({
		type:'post',
		cache: false,
		url: 'save_data_csv.php',
		data: {filename: filename, filedata: filedata}
	});
};

// data parameter should be either the value of jsPsych.data()
// or the parameter that is passed to the on_data_update callback function for the core library
// jsPsych.data() contains ALL data
// the callback function will contain only the most recently written data.
function save_Data_mysql(data){
   var data_table = "my_experiment_table"; // change this for different experiments
   $.ajax({
      type:'post',
      cache: false,
      url: 'save_data_mysql.php', // change this to point to your php file.
      // opt_data is to add additional values to every row, like a subject ID
      // replace 'key' with the column name, and 'value' with the value.
      data: {
          table: data_table,
          json: JSON.stringify(data),
          opt_data: {key: value}
      },
      success: function(output) { console.log(output); } // write the result to javascript console
   });
}

var trial = {
	type: 'text',
	text: 'czesc lic. nacisnij przycisk'
};

var instruction = {
	type: 'instructions',
	pages: ['Witaj w eksperymencie. Nacisnij dalej',
	'Udział w eksperymencie jest dowolny, a wyniki będą analizowane anonimowo.'],
	show_clickable_nav: true
};


// ################
// TEST
var scale = [];
for (var i=0; i<101; i++) scale.push(i);


var slider = {
	type: 'survey-likert',
	questions: ['odp1', 'odp2'],
	labels: [scale,[]],

};
var text_response = {
	type: 'survey-text',
	questions: entry_questions
};

// #############

var similarity_block = {
	type: 'similarity',
	stimuli: ['img/'+STIMULI[0]+'.png', 'img/'+STIMULI[3]+'.png'],
	prompt: "Suwak:",
	show_response: "POST_STIMULUS",
};

// #############
var presentation_block2 = {
	type: 'single-stim',
	timing_response: TIME_RESP,
	stimulus: 'img/'+STIMULI[Math.floor(Math.random()*STIMULI.length)]+'.png'
};
var i = 29;
var presentation_block = {
	type: 'single-stim',
	timing_stim: TIME_STIM,
	timing_response: TIME_RESP,
	timeline: [
		{stimulus: 'img/'+STIMULI[0]+'.png'},
		{stimulus: 'img/'+STIMULI[1]+'.png'},
		{stimulus: 'img/'+STIMULI[2]+'.png'},
		{stimulus: 'img/'+STIMULI[3]+'.png'},
		{stimulus: 'img/'+STIMULI[4]+'.png'},
		{stimulus: 'img/'+STIMULI[5]+'.png'}
	],
	randomize_order: true //powinno byc losowanie ze zwracaniem a jest bez
};

var learning_loop = {
	type: 'single-stim',
	prompt: 'Oceń ilość kropek na rysunku:</p>1 - bardzo mało, 2 - mało, 3 - średnio, 4 - dużo, 5 - bardzo dużo, 6 - mnóstwo',
	choices: ['1', '2', '3', '4', '5','6'],
	timeline: [presentation_block],
	loop_function: function(){
		i++;
		if (i>=PHASE_1_NUM) return false;
		//if (learning == true): return false

		return true; 
	}
};

var interaction_loop = {
	type: 'single-stim',
	prompt: 'Oszacuj ilość kropek na obrazku'
};

var timeline = [trial];
timeline.push(similarity_block);
timeline.push(instruction);
timeline.push(text_response);
timeline.push(slider);
timeline.push(learning_loop);
//timeline.push(interaction_loop);

jsPsych.init({
	timeline: timeline,
	on_finish: function(data) { saveData_csv("filename.csv", jsPsych.data.dataAsCSV()) }
});