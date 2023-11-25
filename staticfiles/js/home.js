const newAcc = document.getElementById('new-acc');
const anonim = document.getElementById('anonim');

console.log('Não compartilhe a ninguém as informações desta pagina!');



newAcc.addEventListener('click', () =>{
    window.location.href = 'login'


});

anonim.addEventListener('click', () =>{
    window.location.href = 'anonim'


});