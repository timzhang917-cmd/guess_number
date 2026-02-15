const maxAttempts = 5;
let secret = 0;
let attempts = 0;
let ended = false;

const input = document.getElementById('guessInput');
const btn = document.getElementById('guessBtn');
const feedback = document.getElementById('feedback');
const leftCount = document.getElementById('leftCount');
const progressBar = document.getElementById('progressBar');
const restartBtn = document.getElementById('restartBtn');
const overlay = document.getElementById('overlay');
const overlayContent = document.getElementById('overlayContent');
const app = document.querySelector('.app');

function rndSecret(){ return Math.floor(Math.random() * 100) + 1; }

function init(){
  secret = rndSecret();
  attempts = 0;
  ended = false;
  input.value = '';
  input.disabled = false;
  btn.disabled = false;
  restartBtn.disabled = true;
  leftCount.textContent = String(maxAttempts - attempts);
  progressBar.style.width = '0%';
  feedback.textContent = '开始吧！';
  overlay.classList.add('hidden');
  overlayContent.className = 'overlay-content';
  app.classList.remove('success','failure');
}

function knockFeedback(){
  input.classList.add('pressed');
  setTimeout(()=>input.classList.remove('pressed'), 60);
  try{
    if(!('AudioContext' in window || 'webkitAudioContext' in window)) return;
    const AC = window.AudioContext || window.webkitAudioContext;
    const ctx = knockFeedback._ctx || (knockFeedback._ctx = new AC());
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'square';
    osc.frequency.setValueAtTime(440, ctx.currentTime);
    gain.gain.setValueAtTime(0.03, ctx.currentTime);
    osc.connect(gain).connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.05);
  }catch(e){}
}

function showOverlaySuccess(){
  overlayContent.classList.add('success');
  overlayContent.innerHTML = `
    <div class="emoji-burst">🎉🎉🎉</div>
    <div class="overlay-title">猜对了！</div>
    <div class="overlay-sub">用时 ${attempts} 次</div>
  `;
  overlay.classList.remove('hidden');
  app.classList.add('success');
}
function showOverlayFailure(){
  overlayContent.classList.add('failure');
  overlayContent.innerHTML = `
    <div class="emoji-burst">💥💥💥</div>
    <div class="overlay-title">失败了</div>
    <div class="overlay-sub">正确答案是 ${secret}</div>
  `;
  overlay.classList.remove('hidden');
  app.classList.add('failure');
}

function onGuess(){
  if(ended) return;
  knockFeedback();
  const v = Number(input.value);
  if(!Number.isInteger(v) || v < 1 || v > 100){
    feedback.textContent = '输入无效（需 1-100 的整数）';
    input.classList.add('invalid');
    setTimeout(()=>input.classList.remove('invalid'), 250);
    return;
  }
  attempts++;
  leftCount.textContent = String(maxAttempts - attempts);
  progressBar.style.width = `${attempts / maxAttempts * 100}%`;
  if(v < secret){
    feedback.textContent = '小了';
  }else if(v > secret){
    feedback.textContent = '大了';
  }else{
    feedback.textContent = '猜对了！';
    ended = true;
    input.disabled = true;
    btn.disabled = true;
    restartBtn.disabled = false;
    showOverlaySuccess();
    return;
  }
  if(attempts >= maxAttempts){
    ended = true;
    input.disabled = true;
    btn.disabled = true;
    restartBtn.disabled = false;
    showOverlayFailure();
  }
}

btn.addEventListener('click', onGuess);
input.addEventListener('keydown', (e)=>{
  if(e.key === 'Enter') onGuess();
});
restartBtn.addEventListener('click', init);

init();
