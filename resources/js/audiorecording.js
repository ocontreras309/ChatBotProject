const CHAT_MODE_STATELESS = 1;
const CHAT_MODE_MEMORY = 2;

let mediaRecorder = null;
let btnStart, btnStop, audioPlay, textTranscription, textChat, grabar, cargando;
let dataArray = [];
let txtInputText;
let btnEnviar;
let chatWindow;
let chatMode;
let btnAudioInput;
let recording = false;
let micImage;

let executeStatelessChat = async(e) => {
    let human = document.createElement('div');
    human.className = 'item';
    human.innerHTML = `<div class="item">
        <div class="icon">
            <i class="fa fa-user"></i>
        </div>
        <div class="msg">
            <p>${txtInputText.value}</p>
        </div>
    </div>`

    chatWindow.appendChild(human);
    
    let br = document.createElement('br');
    br.clear = 'both';
    let prompt = txtInputText.value;
    txtInputText.value = '';

    chatWindow.appendChild(br);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    result = await axios.post('/chat', {
        data: prompt
    });    

    let ai = document.createElement('div');
    ai.innerHTML = `<div class="item right">
        <div class="msg">
            <p>${result.data.content}</p>
        </div>
    </div>`

    chatWindow.appendChild(ai);

    br = document.createElement('br');
    br.clear = 'both';

    chatWindow.appendChild(br);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

let executeStatefulChat = async(e) => {
    let human = document.createElement('div');
    human.className = 'item';
    human.innerHTML = `<div class="item">
        <div class="icon">
            <i class="fa fa-user"></i>
        </div>
        <div class="msg">
            <p>${txtInputText.value}</p>
        </div>
    </div>`

    chatWindow.appendChild(human);
    
    let br = document.createElement('br');
    br.clear = 'both';
    let prompt = txtInputText.value;
    txtInputText.value = '';

    chatWindow.appendChild(br);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    result = await axios.post('/chatmemory', {
        data: prompt
    });    

    let ai = document.createElement('div');
    ai.innerHTML = `<div class="item right">
        <div class="msg">
            <p>${result.data.text}</p>
        </div>
    </div>`

    chatWindow.appendChild(ai);

    br = document.createElement('br');
    br.clear = 'both';

    chatWindow.appendChild(br);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

let chatTextEvent = async (e) => {
    if (e.key === 'Enter' || e.keyCode === 13) {
        if (chatMode === CHAT_MODE_STATELESS) {
            executeStatelessChat();
        } else {
            executeStatefulChat();
        }
    }
}

let btnChatEvent = async (e) => {
    if (chatMode === CHAT_MODE_STATELESS) {
        executeStatelessChat();
    } else {
        executeStatefulChat();
    }
}

let startRecording = () => {
    grabar.style.display = 'block';
    navigator.mediaDevices.getUserMedia({ audio: true }).then((mediaStreamObject) => {
        mediaRecorder = new MediaRecorder(mediaStreamObject, {mimeType: "audio/webm"});
        mediaRecorder.start();

        mediaRecorder.ondataavailable = (ev) => {
            dataArray.push(ev.data);
        };
    }).catch((err) => {
        console.log(err.name, err.message);
    });
}

let stopRecording = () => {
    let mimeType = mediaRecorder.mimeType;
    mediaRecorder.stop();
    cargando.style.display = 'block';
    grabar.style.display = 'none';

    mediaRecorder.onstop = (ev) => {
        let audioData = new Blob(dataArray, { 'type': mimeType });
        let audioSrc = window.URL.createObjectURL(audioData);

        dataArray = [];

        audioPlay.src = audioSrc;
        audioPlay.play();

        let reader = new FileReader();
        reader.readAsDataURL(audioData);
        reader.onloadend = async () => {
            let base64audio = reader.result.split('base64,')[1];
            
            let result = await axios.post('/transcribe', {
                data: base64audio
            });

            let human = document.createElement('div');
            human.className = 'item';
            human.innerHTML = `<div class="item">
                <div class="icon">
                    <i class="fa fa-user"></i>
                </div>
                <div class="msg">
                    <p>${result.data.text}</p>
                </div>
            </div>`

            chatWindow.appendChild(human);
            
            let br = document.createElement('br');
            br.clear = 'both';
            let prompt = result.data.text;

            chatWindow.appendChild(br);
            chatWindow.scrollTop = chatWindow.scrollHeight;

            result = await axios.post('/chatmemory', {
                data: prompt
            });    

            let ai = document.createElement('div');
            ai.innerHTML = `<div class="item right">
                <div class="msg">
                    <p>${result.data.text}</p>
                </div>
            </div>`

            chatWindow.appendChild(ai);

            br = document.createElement('br');
            br.clear = 'both';

            chatWindow.appendChild(br);
            chatWindow.scrollTop = chatWindow.scrollHeight;
            cargando.style.display = 'none';
        }
    };

    mediaRecorder = null;
}

let recordAudio = () => {
    if (recording) {
        stopRecording();
    } else {
        startRecording();
    }

    recording = !recording;
    micImage.src = recording ? '/resources/img/mute.jpeg' : '/resources/img/mic1.webp';
}

window.onload = function() {
    let wrapperInterface = document.getElementById('wrapperInterface');
    wrapperInterface.style.height = document.body.clientHeight + 'px';

    chatWindow = document.getElementById('chatWindow');
    btnEnviar = document.getElementById('btnEnviar');
    btnAudioInput = document.getElementById('btnAudioInput');

    if (btnAudioInput) {
        audioPlay = document.getElementById('audioPlay');
        cargando = document.getElementById('cargando');
        grabar = document.getElementById('grabar');
        grabar.style.display = 'none';
        cargando.style.display = 'none';
        btnAudioInput.addEventListener('click', recordAudio);
        micImage = document.getElementById('micImage');
    } else {
        txtInputText = document.getElementById('txtInputText');
        txtInputText.addEventListener('keyup', chatTextEvent);
        btnEnviar.addEventListener('click', btnChatEvent);
    }
}

