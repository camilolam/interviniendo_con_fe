
let active = false;

function abrirModal(idModal,src,videoId) {
  console.log(src)
  const modal = document.getElementById(idModal);
  const video = document.getElementById(videoId);
  if (modal) {
    video.src = src;
    modal.classList.add('modal-open');
    
  }
}

function cerrarModal(idModal,videoId) {
  const modal = document.getElementById(idModal);
  const video = document.getElementById(videoId);
  if (modal) {
     video.src = "";
    modal.classList.remove('modal-open');
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