const ENTER_KEY = 13;

const DEFAULT_SLIDER_MAX_PARTICIPANTS = 100;
const DEFAULT_SLIDER_MIN_PARTICIPANTS = 3;
const DEFAULT_SLIDER_MIN_STEALS = 0;
const DEFAULT_SLIDER_STEP = 1;

const SUMULATION_INTERVAL_MS = 100;

const participantSlider = document.getElementById("participantSlider");
const participantSliderInput = document.getElementById("participantSliderInput");

const maxStealsSlider = document.getElementById("maxStealsSlider");
const maxStealsSliderInput = document.getElementById("maxStealsSliderInput");

const typeContainer = document.getElementById("typeContainer");

const usingRelativeValues = document.getElementById("relativeValues");

const ctx = document.getElementById('myChart').getContext('2d');
const lineChart = new Chart(ctx, {type: 'line', options: {
  animation: false,
  legend: {
    display:false
  },
  scales: {
    yAxes: [{
      scaleLabel: {
        display: true,
        labelString: 'Normalized Expected Value (0=Worst Gift, 1=Best Gift)'
      },
      ticks: {
          min: 0,
          max: 1
      }
    }],
    xAxes: [{
      scaleLabel: {
        display: true,
        labelString: 'Participant Order Number'
      },
    }]
  }
}
});


let currentLooper = null;
let currentData = null;
let currentSims = 0;

function updateData(data){
  labels = Array.from(Array(data.length + 1).keys()).slice(1);

  lineChart.data = {
    labels: labels,
    datasets: [{
      data: data,
      "fill":false,
      "borderColor":"rgb(75, 192, 192)",
      "lineTension":0.1
    }]
  }
  lineChart.update() 
}


function changeTypeContainer(precomputed){
  typeContainer.innerHTML = precomputed ? "Precomputed": "Simulated";
}

function init() {
  participantSlider.min = DEFAULT_SLIDER_MIN_PARTICIPANTS;
  participantSliderInput.min = DEFAULT_SLIDER_MIN_PARTICIPANTS;
  maxStealsSlider.min = DEFAULT_SLIDER_MIN_STEALS;
  maxStealsSliderInput.min = DEFAULT_SLIDER_MIN_STEALS;
  
  participantSlider.value = DEFAULT_SLIDER_MIN_PARTICIPANTS;
  participantSliderInput.value = DEFAULT_SLIDER_MIN_PARTICIPANTS;
  maxStealsSlider.value = DEFAULT_SLIDER_MIN_STEALS;
  maxStealsSliderInput.value = DEFAULT_SLIDER_MIN_STEALS;
  
  participantSlider.max = DEFAULT_SLIDER_MAX_PARTICIPANTS;
  participantSliderInput.max = DEFAULT_SLIDER_MAX_PARTICIPANTS;
  maxStealsSlider.max = participantSlider.value-1;
  maxStealsSliderInput.max = participantSlider.value-1;
  
  participantSlider.step = DEFAULT_SLIDER_STEP;
  participantSliderInput.step = DEFAULT_SLIDER_STEP;
  maxStealsSlider.step = DEFAULT_SLIDER_STEP;
  maxStealsSliderInput.step = DEFAULT_SLIDER_STEP;
  
  changeTypeContainer(true);
  
  updateData(getPrecomputedExpectedValuesForParticipants(participantSlider.value, maxStealsSlider.value, usingRelativeValues.checked));
}

init();

function updateAxes(){
  if(usingRelativeValues.checked){
    lineChart.options.scales.yAxes[0].ticks.min = -1;
    lineChart.options.scales.yAxes[0].ticks.max = 1;
    lineChart.options.scales.yAxes[0].scaleLabel.labelString = 'Relative Expected Value Of Recieved Present'
  }
  else {
    lineChart.options.scales.yAxes[0].ticks.min = 0;
    lineChart.options.scales.yAxes[0].ticks.max = 1;
    lineChart.options.scales.yAxes[0].scaleLabel.labelString = 'Normalized Expected Value (0=Worst Gift, 1=Best Gift)'
  }
}

let updateGraph = function () {

  if(currentLooper !== null){
    clearInterval(currentLooper);
    currentData = null;
    currentSims = 0;
  }

  const data = getPrecomputedExpectedValuesForParticipants(participantSlider.value, maxStealsSlider.value, usingRelativeValues.checked);
  
  changeTypeContainer(data);

  if(data){
    updateData(data);
  }
  else {

    currentLooper = setInterval(function() {
      let data = getSimulatedValuesForParticipants(participantSlider.value, maxStealsSlider.value, usingRelativeValues.checked);

      if(currentData === null){
        currentData = data;
        currentSims = 1;
      }
      else {
        for(let i = 0; i < currentData.length; i++){
          currentData[i] += data[i];
        }
        currentSims += 1;
      }
      
      display_data = Array(currentData.length);
      for(let i = 0; i < currentData.length; i++){
        display_data[i] = currentData[i]/currentSims;
      }

      updateData(display_data)
    }, SUMULATION_INTERVAL_MS)
  }
}


let participantsSliderInputFunc = function (self) {
  let val = !self.value ? DEFAULT_SLIDER_MIN_PARTICIPANTS : parseInt(self.value);
  
  if(val < DEFAULT_SLIDER_MIN_PARTICIPANTS){
    participantSliderInput.value = DEFAULT_SLIDER_MIN_PARTICIPANTS;
    participantSlider.value = participantSliderInput.value;
    return;
  }
  
  participantSlider.value = val;
  
  if(val >= DEFAULT_SLIDER_MAX_PARTICIPANTS){
    // participantSlider.max = val+10;
    participantSlider.value = DEFAULT_SLIDER_MAX_PARTICIPANTS;
  }
  else {
    participantSlider.max = DEFAULT_SLIDER_MAX_PARTICIPANTS;
  }
  
  maxStealsSlider.max = val-1;
  maxStealsSliderInput.max = val-1;

  updateGraph();
}

let maxStealsSliderInputFunc = function (self) {
  let val = !self.value ? DEFAULT_SLIDER_MIN_STEALS : parseInt(self.value);

  if(DEFAULT_SLIDER_MIN_STEALS <= val && val < participantSlider.value){
    maxStealsSlider.value = val;
  }
  else {
    maxStealsSliderInput.value = DEFAULT_SLIDER_MIN_STEALS > val ? 0 : participantSlider.value-1;
    maxStealsSlider.value = maxStealsSliderInput.value;
  }

  updateGraph();
}

// Update Slider Based On Input From Textbox
participantSliderInput.addEventListener("focusout", function() {
  participantsSliderInputFunc(this);
}) 

participantSliderInput.addEventListener("keyup", function(event) {
  if (event.keyCode === ENTER_KEY) {
    participantsSliderInputFunc(this);
  }
});

// Update Slider Based On Input From Textbox
participantSlider.oninput = function() {
  let val = parseInt(this.value);
  participantSliderInput.value = val;
  maxStealsSlider.max = val-1;
  maxStealsSliderInputFunc(maxStealsSliderInput);
}

maxStealsSliderInput.addEventListener("focusout", function() {
  maxStealsSliderInputFunc(this)
});

maxStealsSliderInput.addEventListener("keyup", function(event) {
  if (event.keyCode === ENTER_KEY) {
    maxStealsSliderInputFunc(this);
  }
});

maxStealsSlider.oninput = function() {
  maxStealsSliderInput.value = this.value;

  updateGraph();
}

usingRelativeValues.oninput = function() {
  updateAxes();
  updateGraph();
}

