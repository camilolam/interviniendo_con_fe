const video = document.querySelector(".video-modal");
let active = false;

function abrirModal(idModal) {
  const modal = document.getElementById(idModal);
  if (modal) {
    modal.classList.add('modal-open');
    video.src = "https://www.youtube.com/embed/UnY6bGhSLRo?si=Gg4eLF8k_aF7_AMY";
  }
}

function cerrarModal(idModal) {
  const modal = document.getElementById(idModal);
  
  if (modal) {
    modal.classList.remove('modal-open');
    video.src = "";
  }
}

document.addEventListener('DOMContentLoaded', () => {
    // 1. Seleccionar los elementos
    const menuBtn = document.querySelector('.main_nav-btn');
    const navLinksContainer = document.querySelector('.main_nav-links');

    const MOBILE_BREAKPOINT = 768;
    let isMobile = window.innerWidth <= MOBILE_BREAKPOINT;
    

    if(isMobile){
      if (menuBtn && navLinksContainer) {
          // 2. Asignar el evento al botón
          menuBtn.addEventListener('click', () => {
            console.log(active)
              // 3. Alternar la clase 'active' para mostrar/ocultar el menú
              if(navLinksContainer.style.display == "flex"){
                navLinksContainer.style.display = "none";
                console.log("estoy oprimiendo el botón");
                
              }else{
                navLinksContainer.style.display = "flex";
                console.log("estoy oprimiendo el botón");
              }
          });
      }
    }
});