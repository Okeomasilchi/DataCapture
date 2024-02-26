$(document).ready(() => {
    const navLinks = document.querySelectorAll('.nav-link')

    navLinks.forEach((link) => {
        link.addEventListener('click', (event) => {
            // Remove 'active' class from other links
            navLinks.forEach((link) => link.classList.remove('active'))

            // Add 'active' class to the clicked link
            event.currentTarget.classList.add('active')
        })
    })

    function updateUI(data) {
        // Update the UI with the JSON data
        // For example, manipulate the DOM to display the data
    }

    function showError(errorMessage) {
        // Display the error message to the user
        // For example, show an alert with the error message
        alert(errorMessage);
    }

    function apiCall(id) {
        if (!id) {
            return Promise.reject(new Error('Invalid ID'));
        }

        return new Promise((resolve, reject) => {
            $.ajax({
                type: "GET",
                url: "http://localhost:5000/api/v1/survey/" + id,
                success: (response) => {
                    const responseData = JSON.stringify(response);
                    resolve(response); // Resolving with the extracted data
                },
                error: (error) => {
                    reject(new Error('API call failed'));
                }
            });
        });
    }


    function openNav() {
        document.getElementById('mySidenav').style.width = '500px'
    }

    function closeNav() {
        document.getElementById('mySidenav').style.width = '0'
    }

    $("#open").click(() => {
        document.getElementById('mySidenav').style.width = '500px'
    });

    $(".closebtn").click(() => {
        document.getElementById('mySidenav').style.width = '0'
    });


    // $(".table-row a:first").click();
    let id = $(".table-row a:first").attr("id");
    $(".bottom-section").hide();

    // Show options container on hover of options button
    $("button [class='options-button']").hover(
        function () {
            // Show options container using slide down animation
            $(this).closest(".question-block").find(".bottom-section").slideDown();
        },
        function () {
            // Hide options container using slide up animation
            $(this).closest(".question-block").find(".bottom-section").slideUp();
        }
    );
    apiCall(id)
        .then((data) => {
            const questions = data.questions;
            questions.forEach((question) => {
                let optionsHTML = ''; // Variable to store options HTML
                // Loop through each option and concatenate input elements
                for (let i = 0; i < question.options.length; i++) {
                    optionsHTML += `<p class="form-control option m-2"><strong>${String.fromCharCode(i + 65)}</strong>&Tab;${question.options[i]}</p>`;
                }
                // Append question and options to the 'populate' element
                $("#populate").append(`
                    <div class="col-lg-3 col-md-4 col-sm-12 question-block">
                        <div class="top-section">
                            <div class="form-group">
                                <h4 class="m-0 mb-3">Question</h4>
                                <button class="options-button m-0">Options</button>
                            </div>
                            <div class="input-group mb-4">
                                <p class="questionTextarea" rows="5" placeholder="Type Question">${question.question}</p>
                            </div>
                        </div>
                        <div class="bottom-section">
                            <h4 mb-3>Options</h4>
                            <div class="options-container py-2">
                                ${optionsHTML}
                            </div>
                        </div>
                    </div>
                `);
            });
        })
        .catch((error) => {
            console.error('Error:', error.message);
        });



    // Add your existing JavaScript logic here, such as handling the copy button click event
    $('.copy-button').click(function () {
        // Your copy functionality code here
        var copyText = $(this).siblings('.survey-title').text()
        navigator.clipboard.writeText(copyText)
    });
});
