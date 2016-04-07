const N = 1;
const TIME_RESP = 10000;
const STIMULI = ['bardzomalo', 'malo', 'srednio', 'duzo', 'bardzoduzo','mnostwo'];
const ID;
const entry_questions = ['Podaj adres e-mail', 'Podaj wiek'];

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

// #############
var presentation_block2 = {
	type: 'single-stim',
	timing_response: TIME_RESP,
	stimulus: 'img/'+STIMULI[Math.floor(Math.random()*STIMULI.length)]+'.png'
};
var presentation_block = {
	type: 'single-stim',
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
		//if (learning == true): return false
		return false; 
	}
};

var timeline = [trial];
timeline.push(instruction);
timeline.push(text_response);
timeline.push(slider);
timeline.push(learning_loop);

jsPsych.init({
	timeline: timeline
});