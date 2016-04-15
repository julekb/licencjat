const N = 1;
const TIME_STIM = 500;
const TIME_RESP = 10000;
const STIMULI = ['bardzomalo', 'malo', 'srednio', 'duzo', 'bardzoduzo','mnostwo'];
const entry_questions = ['Podaj adres e-mail', 'Podaj wiek'];
const TRAINING = ['103', '145', '142', '013', '010', '127', '139', '154', '007', '163', '079', '130', '172', '133', '031', '178', '193', '184', '061', '037', '085', '121', '196', '112', '052', '019', '169', '088', '055', '151', '160'];
const GROUP_ID = 'G1';//G1-grupa kontrolna  lub G2-grupa eksperymentalna


jsPsych.data.addProperties({
	subject: GROUP_ID,
});

function saveData_csv(filename, filedata){
	$.ajax({
		type:'post',
		cache: false,
		url: 'save_data_csv.php',
		data: {filename: filename, filedata: filedata},
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
};

var trial = {
	type: 'text',
	text: 'czesc lic. nacisnij przycisk'
};

var instruction = {
	type: 'instructions',
	pages: ['Witaj w eksperymencie. Nacisnij dalej',
	'Udział w eksperymencie jest dowolny, a wyniki będą analizowane anonimowo.'],
	show_clickable_nav: true,
};

var final_instruction = {
	type: 'instructions',
	pages: ['To już koniec, dziękuję.'],
};


var text_response = {
	type: 'survey-text',
	questions: entry_questions
};
var text_response_loop = {
	type: 'single-stim',
	timeline: ['text_response'],
	loop_function: function(){
		if (jsPsych.data.getData() =='')//if data.response == empty
			return false;
		return true;
	}
};

var choice_response = {
	type: 'survey-multi-choice',
	questions: ['Płeć:'],
	options: [['kobieta', 'mężczyzna']],
	//required: [true],
	horizontal: true,
};


var timeline = [trial];
timeline.push(instruction);
timeline.push(text_response);
timeline.push(choice_response);

//adding learnig stimuli
var training_stim = [];
for (i = 0; i < TRAINING.length; i++) {
	training_stim.push(['img/dots/dots_'+TRAINING[i]+'.png']);
};


// adding learning phase

for ( i = 0; i < training_stim.length-25; i++) {
	var similarity_b = {
		type: 'similarity',
		stimuli: training_stim[i],
		//prompt: "Suwak:",
		show_response: "POST_STIMULUS",
		labels: ['7', '100'],
		timing_first_stim: TIME_STIM,
		timing_image_gap: 100,
	};
	timeline.push(similarity_b);
};


jsPsych.init({
	timeline: timeline,
	on_finish: function(data) { saveData_csv("filename.csv", jsPsych.data.dataAsCSV()) }
});