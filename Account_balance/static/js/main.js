// const date = new Date();
// document.querySelector('.year').innerHTML = date.getFullYear();

setTimeout(function(){
    $('#message').fadeOut('slow');
}, 3000);

const updateClock = () => {
    document.getElementById('current-date').textContent = new Date().toLocaleDateString('fa-IR');
    document.getElementById('current-time').textContent = new Date().toLocaleTimeString('fa-IR');
};


updateClock();
setInterval(updateClock, 1000);