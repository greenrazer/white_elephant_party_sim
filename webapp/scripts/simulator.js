function shuffle(a) {
  var j, x, i;
  for (i = a.length - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i + 1));
      x = a[i];
      a[i] = a[j];
      a[j] = x;
  }
  return a;
}

class Simulator {

  constructor(numberOfParticipants, numberOfSteals) {
    this.revealedPresents = [];
    this.unrevealedPresents = [];
    this.presents = [];
    this.people = [];

    this.turn = 0;
    this.stealStack = [];
    this.cantSteal = [];

    this.numberOfSteals = numberOfSteals;
    this.numberOfParticipants = numberOfParticipants;

    this.generateParticipants();
  }

  generateParticipants() {
    const values = shuffle(Array.from(Array(this.numberOfParticipants).keys()));
    for(let i = 0; i < values.length; i++){
      this.presents.push({
        'value': values[i],
        'steals': 0,
        'belongs_to': -1,
      });
      this.people.push({
        'threshold': values[i]
      });
      this.unrevealedPresents.push(i);
    }
  }

  run() {
    while (this.stealStack.length > 0 || this.turn < this.numberOfParticipants){
      this.step();
    }
  }

  step(){
    let turnUser = this.turn;

    if (this.stealStack.length){
      turnUser = this.stealStack.pop();
    }
    else {
      this.cantSteal = [];
      this.turn += 1;
    }

    const pickOrSteal = this.pickOrSteal(turnUser);

    if (pickOrSteal > -1){
      this.stealPresent(turnUser, pickOrSteal);
    }
    else{
      this.pickFromPile(turnUser);
    }
  }

  pickFromPile(toId){
    const picked = this.unrevealedPresents.pop();
    this.presents[picked]['belongs_to'] = toId;
    this.revealedPresents.push(picked);

    return picked
  }

  stealPresent(userId, presentId) {
    const newTurn = this.presents[presentId]['belongs_to'];
    this.presents[presentId]['belongs_to'] = userId;
    this.presents[presentId]['steals'] += 1;
    this.cantSteal.push(presentId);
    this.stealStack.push(newTurn);
  }

  pickOrSteal(userId){
    const threshold = this.people[userId]['threshold'];
    let currMax = null;
    let maxInd = -1;
    for (let p of this.revealedPresents) {
      const val = this.presents[p]['value'];
      if (val > threshold && (currMax === null || val > currMax)){
        if (this.presents[p]['steals'] < this.numberOfSteals){
          if (!this.cantSteal.includes(p)){
            currMax = val;
            maxInd = p;
          }
        }
      }
    }

    return maxInd;
  }

  getRelativeValues(){
    let out = Array(this.numberOfParticipants);
    for (let present of this.presents) {
      let person = present['belongs_to'];
      out[person] = present['value']/(this.numberOfParticipants-1) - this.people[person]['threshold']/(this.numberOfParticipants-1);
    }
    return out;
  }

  getValues(){
    let out = Array(this.numberOfParticipants);
    for (let present of this.presents){
      let person = present['belongs_to'];
      out[person] = present['value']/(this.numberOfParticipants-1);
    }
    return out;
  }

  getPeoplePresentPairs(){
    let out = [];
    for (let i = 0; i < this.presents.length; i++){
      out.push([this.presents[i]['belongs_to'], i]);
    } 
    return out;
  }

}

function getSimulatedValuesForParticipants(participants, steals, usingRelativeValues){
  whiteElephantSim = new Simulator(parseInt(participants), parseInt(steals));
  whiteElephantSim.run();
  if(usingRelativeValues){
    return whiteElephantSim.getRelativeValues();
  }
  else {
    return whiteElephantSim.getValues();
  }
}