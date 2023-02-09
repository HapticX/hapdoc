function toggleList(itemID) {
    // Finding elements by "itemID"
    const listElem = document.getElementById(`${itemID}-list`);
    const iconElem = document.getElementById(`${itemID}-icon`);

    function hide() {
        listElem.style.display = 'none';
        iconElem.style.transform = 'rotate(0deg)';
    }

    function show() {
        listElem.style.display = 'block';
        iconElem.style.transform = 'rotate(90deg)';
    }

    listElem.style.display === 'block' ? hide() : show(); // toggle
}