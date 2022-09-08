$(document).ready(function() {
    document.documentElement.setAttribute('data-theme', localStorage.getItem('SQLeasy'));
});

function changeTheme(theme) {
    localStorage.setItem('SQLeasy', theme);
    document.documentElement.setAttribute('data-theme', localStorage.getItem('SQLeasy'));
}

function toggleDiv(divId) {
    $('#' + divId).fadeToggle(150);
}

function newColumn() {
    x = document.getElementById('newCol');
    y = x.cloneNode(true);
    x.parentNode.appendChild(y);
}