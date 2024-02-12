document.addEventListener('DOMContentLoaded', (event) => {
    fetch('header.html')
        .then(response => response.text())
        .then(data => document.body.insertAdjacentHTML('afterbegin', data))
        .catch(error => console.error('Error fetching header:', error));

    // Get the select box and the bottom section
    var selectBox = document.getElementById('questiontype');
    var bottomSection = document.querySelector('.bottom-section');

    // Hide the bottom section initially
    bottomSection.style.display = 'none';

    // Listen for changes on the select box
    selectBox.addEventListener('change', function () {
        // If the selected value is 'multiple', show the bottom section
        if (this.value === 'multiple') {
            bottomSection.style.display = 'flex';
        } else {
            // Otherwise, hide it
            bottomSection.style.display = 'none';
        }
    });
});
