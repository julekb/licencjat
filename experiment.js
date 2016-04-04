const N = 1;
const TIME_RESP = 10000;
const STIMULI = ['bardzomalo', 'malo', 'srednio', 'duzo', 'bardzoduzo','mnostwo'];
const ID;

var trial = {
	type: 'text',
	text: 'czesc lic. nacisnij przycisk'
};

var instruction = {
	type: 'text',
	text: ' raz dwa </p> czy cztery' +
	'pięć sześć </p> witaj w ekeperymencie',
	timing_post_trial: 20
};



var block = [
	{
		stimulus: 'img/blue.png',
		data: { response: 'b' },
		choices: ['b']
	},
	{
		stimulus: 'img/orange.png',
		data: { response: 'o' },
		choices: ['o']
	}];
var multiple_stim = jsPsych.randomization.repeat(block, N);
var multiple_block = {
	type: 'single-stim',
	//choices: ['o', 'b'],
	timing_response: TIME_RESP,
	on_finish: function(data){
		var correct = false;
		if (data.response == 'b' && data.rt == -1){
			correct = true;
		}
		jsPsych.data.addDataToLastTrial({correct: correct});
	},
	timeline: multiple_stim
};

function getSubjectData() {
	var trials = jsPsych.data.getTrialsOfType('single-stim');
	var sum_rt = 0;
	var correct_trial_count = 0;
	var correct_rt_count = 0;
	for (var i=0; i<trials.length; i++) {
		if (trials[i].correct == true) {
			correct_trial_count++;
			if (trials[i].rt > -1) {
				sum_rt += trials[i].rt;
				correct_rt_count++;
			}
		}
	};
	return {
		rt: Math.floor(sum_rt/correct_rt_count),
		accuracy: Math.floor(correct_trial_count/trials.length*100)
	}
}
var debrief_block = {
	type: 'text',
	text: function() {
		var subject_data = getSubjectData();
		return "poprawność odpowiedzi: "+subject_data.accuracy+
		"</p>średni czas odpowiedzi: "+subject_data.rt+"</p></p>"+
		jsPsych.data.getTrialsOfType('single-stim');
	}
};

// ################
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
		return true; 
	}
};

var timeline = [trial];
//timeline.push(instruction);
//timeline.push(multiple_block);
//timeline.push(debrief_block);
timeline.push(learning_loop);

jsPsych.init({
	timeline: timeline
});