// JavaScript code for dynamically updating progress bars
document.addEventListener("DOMContentLoaded", function() {
    var forms = document.querySelectorAll('form');

    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent form submission

            var responses = this.querySelectorAll('input[type="radio"]:checked');

            responses.forEach(function(response) {
                var progress = response.nextElementSibling.querySelector('.progress');
                progress.style.width = parseInt(progress.style.width) + 25 + '%';
            });
        });
    });
});
