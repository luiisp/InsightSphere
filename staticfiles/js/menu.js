hamburger = document.querySelector(".hamburger");
nav = document.querySelector("nav");
hamburger.onclick = function() {
nav.classList.toggle("active");
}
document.addEventListener('DOMContentLoaded', () => {
    const divsVerificadas = document.querySelectorAll('#verific');
    divsVerificadas.forEach(div => {
        let parentElement = div.parentElement.parentElement.parentElement;
        let parentParentElement = parentElement.parentElement;

        parentParentElement.insertBefore(parentElement, parentParentElement.firstChild);
    });
});

