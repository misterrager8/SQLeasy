


$(document).ready(function() {{
    localStorage.getItem('SQLeasy') === 'dark' ? setDark() : setLight();
}});

function setDark() {{
    localStorage.setItem('SQLeasy', 'dark');
    document.documentElement.setAttribute('data-theme', localStorage.getItem('SQLeasy'));
    $('#dark').show();
    $('#light').hide();
}}

function setLight() {{
    localStorage.setItem('SQLeasy', 'light');
    document.documentElement.setAttribute('data-theme', localStorage.getItem('SQLeasy'));
    $('#light').show();
    $('#dark').hide();
}}

function toggleDiv(divId) {
    $('#' + divId).fadeToggle(150);
}

function newColumn() {
    x = document.getElementById('newCol');
    y = x.cloneNode(true);
    x.parentNode.appendChild(y);
}