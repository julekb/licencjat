const N = 1;
const TIME_STIM = 500;
const TIME_RESP = 10000;
const entry_questions = ['Proszę podać adres e-mail. Posłuży on do kontaktu w celu umówienia się na dalszą część badania', 'Podaj wiek'];
const TRAINING = ['103', '145', '142', '013', '010', '127', '139', '154', '007', '163', '079', '130', '172', '133', '031', '178', '193', '184', '061', '037', '085', '121', '196', '112', '052', '019', '169', '088', '055', '151', '160'];
const GROUP_ID = 'G1';//G1-grupa kontrolna  lub G2-grupa eksperymentalna


jsPsych.data.addProperties({
	subject: GROUP_ID,
	phase: "F1",
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


var entry_instruction = {
	type: 'instructions',
	pages: ['Witaj w eksperymencie. Jest to pilotaż pierwszego etapu mojego badania nt. systemów poprawiających komunikację między ludźmi. Proszę jednak o rzetelne podejście do testu, ma on na celu zweryfikować, czy stawiane przeze mnie hipotezy mają jakiś sens'+
	' oraz czy świat jest w rzeczywistości taki, jaki zdaje się być. Badanie zajmie ok. 10 minut. Prawdopodobnie będę się również odzywał mailowo w sprawie pilotażu do drugiego etapu badania. Z góry dziękuję za poświęcony czas ;)',
	' Udział w eksperymencie jest dowolny, a wyniki będą analizowane grupowo i nie będą skojarzone z adresem e-mail. W tym momencie bierze Pani/Pan udział w pierwszej fazie eksperymentu. Proszę o podanie prawdziwego adresu e-mail. Umożliwi to dalszy kontakt w celu umówienia się na drugi etap badania, który zostanie przeprowadzony również za pośrednictwem internetu.',
	'Jeśli zgadza sie Pani/Pan na wzięcie udziału w badaniu, proszę nacisnąć przycisk DALEJ. W przeciwnym wypadku proszę zamknąć stronę.'],
	show_clickable_nav: true,
};

var final_instruction = {
	type: 'instructions',
	pages: ['To już koniec, dziękuję. Wszelkie pytania lub wątpliwości dotyczące eksperymentu proszę kierować na adres juliusz.baranski@student.uw.edu.pl'],
};

var instruction = {
	type: 'instructions',
	pages: ['<b> INSTRUKCJA:</b> <p>Badanie polega na szacowaniu liczby kropek, która pojawi się na rysunku. Za chwilę pojawi się seria obrazków oraz zaraz po każdym z nich suwak, za pomocą którego udziela się odpowiedzi. '+
	'Przesunięcie suwaka w lewo jest oznacza mniejszą liczbę kropek, a w prawo większą. Dwa obrazki pod suwakiem oznaczają minimalną(maksymalne wychylenie suwaka w lewo) i maksymalną(maksymalne wychylenie suwaka w prawo) liczbę kropek. '+
	'Uwaga, obrazki będą wyświetlane przez pół sekundy. Będą poprzedzone obrazkiem z krzyżykiem,a po nich pojawi się kratownica. Eksperyment składa sie z 30 obrazków. </p> Naciśnij przycisk aby rozpocząć.'],
	show_clickable_nav: true
}


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
var additional_text_response = {
	type: 'survey-text',
	questions: ["Dziękuję za udział. Czy masz jakieś uwagi odnośnie badania? Czy coś było niejasne, nieprawidłowe?</p> <b> ważne:</b> naciśnij 'Submit Answers' aby dodać swoje odpowiedzi"]
};
var choice_response = {
	type: 'survey-multi-choice',
	questions: ['Płeć:'],
	options: [['kobieta', 'mężczyzna']],
	//required: [true],
	horizontal: true,
};


var timeline = [];
// timeline.push(entry_instruction);
// timeline.push(instruction);
// timeline.push(text_response);
// timeline.push(choice_response);

//adding learnig stimuli
var training_stim = [];
for (i = 0; i < TRAINING.length; i++) {
	training_stim.push(['img/dots/dots_'+TRAINING[i]+'.png']);
};


// adding learning phase

for ( i = 0; i < training_stim.length; i++) {
	var similarity_b = {
		type: 'similarity',
		stimuli: training_stim[i],
		//prompt: "Suwak:",
		show_response: "POST_STIMULUS",
		labels: ['7', '200'],
		img_labels: ['img/dots/dots_007.png', 'img/dots/dots_200.png'], //img labels

		//2 faza client.send_message(peer_id, "RESPONSE", $("#text_input").val());
        
		timing_first_stim: TIME_STIM,
		timing_image_gap: 100,
	};
	timeline.push(similarity_b);
};
timeline.push(additional_text_response);


jsPsych.init({
	timeline: timeline,
	on_finish: function(data) { saveData_csv("pilotaz", jsPsych.data.dataAsCSV()) }
});

timeline.push(final_instruction);