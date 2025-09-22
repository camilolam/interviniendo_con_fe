const video = document.querySelector(".video-modal");


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