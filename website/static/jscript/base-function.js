document.addEventListener('DOMContentLoaded', function() {
  const sideBarBtn = document.getElementById('side-bar-button');
  const sideBar = document.getElementById('side-bar');
  const mainContent = document.getElementById('main-content');

  sideBarBtn.addEventListener('click', sideBarInteract);
  let isVisible = false;
  function sideBarInteract() {
    

    if (isVisible) {
      sideBarBtn.style.transform = 'rotate(0deg)';
      sideBar.style.transform = 'translateX(-250px)'; 
      mainContent.style.transform = 'translateX(0)';
      isVisible = false;     
    }
    else if (!isVisible) {
      sideBarBtn.style.transform = 'rotate(180deg)';
      sideBar.style.transform = 'translateX(0)';
      mainContent.style.transform = 'translateX(250px)';
      isVisible = true;
    }
  }
});