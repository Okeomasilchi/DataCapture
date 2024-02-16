document.addEventListener('DOMContentLoaded', (event) => {
    fetch('header.html')
        .then(response => response.text())
        .then(data => document.body.insertAdjacentHTML('afterbegin', data))
        .catch(error => console.error('Error fetching header:', error));

    // Get the select box and the bottom section
    
});
