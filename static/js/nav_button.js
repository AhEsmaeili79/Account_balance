
document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.querySelector('.toggle-button');
    const userActions = document.querySelector('.user-actions');

    toggleButton.addEventListener('click', function () {
        userActions.classList.toggle('active');
    });
});
