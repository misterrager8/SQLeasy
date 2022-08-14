function toggleDiv(divId) {
    $('#' + divId).fadeToggle(150);
}

function newColumn() {
    x = document.getElementById('newCol');
    y = x.cloneNode(true);
    x.parentNode.appendChild(y);
}