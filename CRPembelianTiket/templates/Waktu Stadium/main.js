const hamburger = document.querySelector('.hamburger');
const hamburger_icon = hamburger.querySelector('span');
const mobile_menu = document.querySelector('.mobile-menu')

hamburger.addEventListener('click', function() {
    this.classList.toggle('is-active');

    hamburger_icon.innerText = hamburger_icon.innerText === 'menu'
            ? 'close'
            : 'menu';
    
    mobile_menu.classList.toggle('is-open')
})

function nextAction() {
    // Add your code here to handle the next action
    console.log("Next button clicked");
}