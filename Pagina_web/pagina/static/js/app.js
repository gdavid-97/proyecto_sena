// inicializamos un objeto de reconocimiento de voz en español
var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.lang = "es";

recognition.onstart = function () {
  // acciones a realizar cuando el reconocimiento de voz empieza
};

recognition.onspeechend = function () {
  // acciones a realizar cuando el reconocimiento de voz termina
  recognition.stop();
};

recognition.onresult = function (event) {
  // obtener los resultados del reconocimiento de voz
  const transcript = event.results[0][0].transcript.toLowerCase();
  const confidence = event.results[0][0].confidence;

  // realizar acciones basadas en la transcripción y confianza
};


let speech = new SpeechSynthesisUtterance();
speech.lang = "es";
speech.text = "This is the text to read.";
//window.speechSynthesis.speak(speech);