const audio = document.querySelector('#audio');
const fileInput = document.querySelector('#fileInput');
const playButton = document.querySelector('#playButton');
const seekBar = document.querySelector('#seekBar');
const currentTime = document.querySelector('#currentTime');
const totalTime = document.querySelector('#totalTime');
const canvas = document.querySelector('#visualizer');
const ctx = canvas.getContext('2d');
const eqCanvas = document.querySelector('#eqCanvas');
const eqCtx = eqCanvas.getContext('2d');
let audioContext, analyser, source, stream, animationId, usingMic = false;

const formatTime = seconds => !Number.isFinite(seconds) ? '00:00' : `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(Math.floor(seconds % 60)).padStart(2, '0')}`;
function setupAudio(node) { if (!audioContext) audioContext = new AudioContext(); if (source) source.disconnect(); source = audioContext.createMediaElementSource(node); analyser = audioContext.createAnalyser(); analyser.fftSize = 128; source.connect(analyser); analyser.connect(audioContext.destination); draw(); }
function draw() { const rect = canvas.getBoundingClientRect(); canvas.width = rect.width * devicePixelRatio; canvas.height = rect.height * devicePixelRatio; ctx.scale(devicePixelRatio, devicePixelRatio); const w = rect.width, h = rect.height; const values = analyser ? new Uint8Array(analyser.frequencyBinCount) : null; const paint = () => { animationId = requestAnimationFrame(paint); ctx.clearRect(0, 0, w, h); if (values) analyser.getByteFrequencyData(values); for (let x = 0; x < w; x += 8) { const v = values ? values[Math.floor((x / w) * values.length)] / 255 : .08 + Math.sin(x / 25) * .03; const bar = Math.max(2, v * h * .75); const gradient = ctx.createLinearGradient(0,h,0,h-bar); gradient.addColorStop(0,'rgba(114,230,210,.08)'); gradient.addColorStop(1,'rgba(200,239,76,.72)'); ctx.fillStyle = gradient; ctx.fillRect(x, h - bar, 3, bar); } }; cancelAnimationFrame(animationId); paint(); }
function drawEq() { const controls = [...document.querySelectorAll('.eq-control')].map(control => Number(control.value)); const w = eqCanvas.width, h = eqCanvas.height; eqCtx.clearRect(0, 0, w, h); eqCtx.strokeStyle = '#2f3944'; eqCtx.lineWidth = 1; for (let y = 18; y < h; y += 22) { eqCtx.beginPath(); eqCtx.moveTo(0, y); eqCtx.lineTo(w, y); eqCtx.stroke(); } eqCtx.beginPath(); eqCtx.moveTo(0, h / 2 - controls[0] * 2); eqCtx.bezierCurveTo(w * .18, h / 2 - controls[0] * 2, w * .28, h / 2 - controls[1] * 2, w * .5, h / 2 - controls[1] * 2); eqCtx.bezierCurveTo(w * .72, h / 2 - controls[1] * 2, w * .82, h / 2 - controls[2] * 2, w, h / 2 - controls[2] * 2); eqCtx.strokeStyle = '#c8ef4c'; eqCtx.lineWidth = 2; eqCtx.stroke(); }
function updateTrackTitle(file) { document.querySelector('#trackTitle').textContent = file.name.replace(/\.[^/.]+$/, ''); document.querySelector('#trackSubtitle').textContent = 'Загруженный файл · HTML5 Audio'; }
document.querySelector('#uploadButton').onclick = () => fileInput.click();
fileInput.onchange = e => { const file = e.target.files[0]; if (!file) return; audio.src = URL.createObjectURL(file); setupAudio(audio); updateTrackTitle(file); audio.play(); };
playButton.onclick = async () => { if (!audio.src) return fileInput.click(); if (audio.paused) { await audioContext?.resume(); audio.play(); } else audio.pause(); };
audio.onplay = () => playButton.textContent = '❚❚'; audio.onpause = () => playButton.textContent = '▶';
audio.ontimeupdate = () => { seekBar.value = audio.duration ? audio.currentTime / audio.duration * 100 : 0; currentTime.textContent = formatTime(audio.currentTime); };
audio.onloadedmetadata = () => totalTime.textContent = formatTime(audio.duration);
seekBar.oninput = () => { if (audio.duration) audio.currentTime = audio.duration * seekBar.value / 100; };
document.querySelector('#rewindButton').onclick = () => { audio.currentTime = 0; };
document.querySelector('#volumeControl').oninput = e => { audio.volume = e.target.value / 100; document.querySelector('.track-volume').value = e.target.value; };
document.querySelector('.track-volume').oninput = e => { audio.volume = e.target.value / 100; document.querySelector('#volumeControl').value = e.target.value; };
document.querySelector('.mute').onclick = e => { audio.muted = !audio.muted; e.currentTarget.classList.toggle('on', audio.muted); };
document.querySelector('#micButton').onclick = async () => { try { if (usingMic) { stream.getTracks().forEach(t => t.stop()); usingMic = false; document.querySelector('#micButton').style.color = ''; return; } stream = await navigator.mediaDevices.getUserMedia({audio:true}); if (!audioContext) audioContext = new AudioContext(); analyser = audioContext.createAnalyser(); analyser.fftSize = 128; audioContext.createMediaStreamSource(stream).connect(analyser); usingMic = true; document.querySelector('#micButton').style.color = '#c8ef4c'; document.querySelector('#trackTitle').textContent = 'Микрофон активен'; document.querySelector('#trackSubtitle').textContent = 'Прямой мониторинг · нажмите ◉ для остановки'; draw(); } catch { document.querySelector('#trackSubtitle').textContent = 'Не удалось получить доступ к микрофону'; } };
document.querySelectorAll('.toggle').forEach(button => button.onclick = () => button.classList.toggle('active'));
document.querySelectorAll('.eq-control').forEach(control => control.oninput = drawEq);
document.querySelector('#reverbControl').oninput = event => document.querySelector('#reverbValue').textContent = `${event.target.value}%`;
document.querySelector('#tempoButton').onclick = () => { const value = document.querySelector('#tempoValue'); value.textContent = value.textContent === '120' ? '128' : '120'; };
document.querySelector('#addTrack').onclick = () => { const count = document.querySelectorAll('.track').length + 1; const item = document.querySelector('.track').cloneNode(true); item.querySelector('.track-num').textContent = String(count).padStart(2, '0'); item.querySelector('.track-info strong').textContent = `Новая дорожка ${count}`; document.querySelector('#trackList').append(item); };
document.querySelector('#exportButton').onclick = () => { const button = document.querySelector('#exportButton'); button.textContent = 'Проект сохранён ✓'; setTimeout(() => button.innerHTML = 'Экспорт <span>↗</span>', 1600); };
draw();
drawEq();
