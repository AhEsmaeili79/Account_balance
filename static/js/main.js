setTimeout(function(){
    $('#message').fadeOut('slow');
}, 3000);

const updateClock = () => {
    document.getElementById('current-date').textContent = new Date().toLocaleDateString('fa-IR');
    document.getElementById('current-time').textContent = new Date().toLocaleTimeString('fa-IR');
};

console.log('main.js is loaded');
