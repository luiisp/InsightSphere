
const username = userData.username;
const apelido = userData.apelido;
const channel_id = userData.chatId;
const creator = userData.creator;

const socket = new WebSocket(`ws://127.0.0.1:8000/ws/c/${creator}/${channel_id}/`);
socket.onopen = () => {
  console.warn('Conectado ao Servidor!');
 
};
  

socket.addEventListener('close', () => {
  socket.close();
});

function hr() {
  const data = new Date();
  const hora = ('0' + data.getHours()).slice(-2);
  const minutos = ('0' + data.getMinutes()).slice(-2);
  const dia = ('0' + data.getDate()).slice(-2);
  const mes = ('0' + (data.getMonth() + 1)).slice(-2);
  return `${hora}:${minutos} ${dia}/${mes}`;
}

const form = document.getElementById('input');
const rms = document.getElementById('msg-send');
document.addEventListener('keydown', (event) => {
  const keyCode = event.keyCode;

  if ((keyCode >= 48 && keyCode <= 57) ||   
      (keyCode >= 65 && keyCode <= 90) ||   
      (keyCode >= 97 && keyCode <= 122)) {    
    document.querySelector('form').querySelector('input').focus();
  }
});

const spawnUserMsg = (apelido, username, hrs, msg) => {
  const divMensagem = document.createElement('div');
  divMensagem.id = 'msg';

  const divCabecalho = document.createElement('div');
  divCabecalho.id = 'head-msg';

  const h1Apelido = document.createElement('h1');
  h1Apelido.id = 'apelidoo';
  

  const linkUsuario = document.createElement('a');
  linkUsuario.id = 'usern';
  linkUsuario.href = `/@${username}`; 
  linkUsuario.textContent = '@' + username;

  const pTime = document.createElement('p');
  pTime.id = 'time';
  pTime.textContent = hrs;

  const divConteudo = document.createElement('div');
  divConteudo.id = 'content';

  const pConteudo = document.createElement('p');
  pConteudo.id = 'content-msg';
  pConteudo.textContent = msg;

  divCabecalho.appendChild(h1Apelido);
  divCabecalho.appendChild(linkUsuario);
  divCabecalho.appendChild(pTime);

  divConteudo.appendChild(pConteudo);

  divMensagem.appendChild(divCabecalho);
  divMensagem.appendChild(divConteudo); 
  
  if(username == userData.username ){
    divMensagem.className = 'msg-user';
    h1Apelido.textContent = 'Você';
  }
  else{
    h1Apelido.textContent = apelido;
    divMensagem.className = 'msg-r';
  }

  const msgsCallDiv = document.getElementById('msgs-call');
  msgsCallDiv.appendChild(divMensagem);
};

const ServerMsg = v =>{
  textt = document.createElement('p');
  textt.id = 'msg-serve';
  textt.textContent = v
  const msgsCallDiv = document.getElementById('msgs-call');
  msgsCallDiv.appendChild(textt);
}


socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type == 'msg.server'){
    const msgServe = data.msgserver;
    ServerMsg(msgServe)
    


  }
  else{
  const apelido = JSON.parse(event.data).apelido;
  const username = JSON.parse(event.data).username;
  const hrs = JSON.parse(event.data).hora;
  const msg = JSON.parse(event.data).message;
  spawnUserMsg(apelido,username,hrs,msg)};
  }



const send = (apelido,username,hrs,msg) => {
  const obj = { message: msg,
                          apelido:apelido,
                          username:username,
                          hora:hrs
  };
  socket.send(JSON.stringify(obj));
};

const sendbtn = document.getElementById('send')
const minD = 768;
rms.addEventListener('blur', () => {
  if (window.innerWidth >= minD) {
    sendbtn.style.display = 'none';
  }
  else{
    sendbtn.style.display = 'flex';
  }
});
rms.addEventListener('focus', function(event) {
  if (window.innerWidth >= minD) {
    sendbtn.style.display = 'flex';
  }
  else{
    sendbtn.style.display = 'flex';
  }
});




form.addEventListener('submit', function(event) {
  msg = rms.value;

  if(msg != ''){
    const hrs = hr();
    event.preventDefault();
    this.reset();
    send(apelido,username,hrs,msg)
  }
  else{
    event.preventDefault();
  }
  
});

const removerDiv = (divId) => {
  const divParaRemover = document.getElementById(divId);
  if (divParaRemover) {
    divParaRemover.parentNode.removeChild(divParaRemover);
  } else {
    console.error(`div não encontrada! ${divId}`);
  }
};

function init(){
  sendbtn.style.display = 'none';


}

window.onload = init;

document.addEventListener('DOMContentLoaded', () => {


setTimeout(() => {
  removerDiv('load')
}, 1500);
});

console.log('kldok')