function capitalizeFirstLetters(obj) {
    if (typeof obj === 'string') {
        // Capitalize only if the value is a string
        newObj = obj.split(' ').map(word => word[0].toUpperCase() + word.slice(1)).join(' ');
    } else {
        newObj = obj;
    }
    return newObj;
}


$(document).ready(() => {
    const progressBar = document.getElementById("progressBar");

    // Function to update the progress bar
    function updateProgress() {
        // Count the number of answered questions
        var answeredQuestions = $('.question').filter(function () {
            return $(this).find('input[type="checkbox"]:checked').length > 0;
        }).length;
        // Update the value of the progress bar
        progressBar.value = answeredQuestions;
    }
    updateProgress()
    var currentYear = new Date().getFullYear();

    $('#copyright-year').text(currentYear);


    $(".entry-animation").each(function () {
        let element = $(this);
        if (!element.hasClass("animated")) {
            element.addClass("animated");
        }
    });

    $(".lead").each(function () {
        let element = $(this);
        if (!element.hasClass("animatedX")) {
            element.addClass("animatedX");
        }
    });
    var currentYear = new Date().getFullYear();

    $('#copyright-year').text(currentYear);


    $(".entry-animation").each(function () {
        let element = $(this);
        if (!element.hasClass("animated")) {
            element.addClass("animated");
        }
    });

    $(".lead").each(function () {
        let element = $(this);
        if (!element.hasClass("animatedX")) {
            element.addClass("animatedX");
        }
    });

    setTimeout(() => {

        $("#top").hide();
    }, 4000);

    $('#questiontype').on('change', function () {
        $('.bottom-section').toggle($(this).val() === 'multiple');
    }).trigger('change'); // Triggering the change event once to handle initial state


    $("span[id='#toggle-login-password']").addClass("fill");

    // Add hover event listener to dashboard-info section
    $('#dashboard-info').hover(
        function () {
            $(this).addClass('active');
        },
        function () {
            $(this).removeClass('active');
        }
    );

    $("#collapseButton").click(() => {
        $("#collapseButton").toggleClass("fa-chevron-left fa-chevron-right");
        $("#dashboard-info").animate({
            width: 'toggle'
        });
        var currentMarginLeft = $("#dashboard-result").css("marginLeft");
        var currentBtn = $("#collapseButton").css("left");

        // Toggle between the two values
        if (currentMarginLeft === "0px") {
            $("#dashboard-result").animate({ marginLeft: "400px" }); // Animate to 400px
        } else {
            $("#dashboard-result").animate({ marginLeft: "0px" }); // Animate back to 0px
        }

        if (currentBtn === "0px") {
            $("#collapseButton").animate({ left: "400px" }); // Animate to 400px
        } else {
            $("#collapseButton").animate({ left: "0px" }); // Animate back to 0px
        }
    });


    // $("#navbtn").click((e) => { 
    //     // e.preventDefault();
    //     $("#navcol-2").slideToggle()    
    // });

    $('#navbtn').click(function () {
        var target = $(this).data('bs-target');
        $(target).collapse('toggle');
    });


    if ($.userData) {
        let user = $.userData;
        let root = user.root;
        let originalValues = {
            first_name: user.first_name,
            last_name: user.last_name,
            email: user.email
        };

        $('#popupButton').click(() => {
            // $('div input[id="first_name"]').val(user.first_name);
            // $('div input[id="last_name"]').val(user.last_name);
            // $('div input[id="email"]').val(user.email);
            $('#popupContainer').fadeIn(150);
        });

        $('#popupContainer').click((e) => {
            if (e.target.id === 'popupContainer') {
                $('#popupContainer').fadeOut(150);
            }
        });

        $("#closeButton").click(() => {
            let updatedValues = {
                first_name: $('div input[id="first_name"]').val(),
                last_name: $('div input[id="last_name"]').val(),
                email: $('div input[id="email"]').val()
            };

            let changes = {};
            for (let key in updatedValues) {
                if (updatedValues[key] !== originalValues[key]) {
                    changes[key] = updatedValues[key];
                }
            }

            if (Object.keys(changes).length > 0) {
                fetch(root + 'users/' + user.id, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(changes)
                })
                    .then(response => {
                        // Check if response is successful
                        if (!response.ok) {
                            throw new Error('API error: ' + response.status + response.headers);
                        }

                        // Access status code
                        console.log('Status code:', response.status);

                        // Access other headers
                        console.log('Content-Type header:', response.headers.get('Content-Type'));

                        // Parse JSON response
                        return response.json();
                    })
                    .then(data => {
                        // Handle successful response
                        $('div input[id="first_name"]').val(data.first_name);
                        $('div input[id="last_name"]').val(data.last_name);
                        $('div input[id="email"]').val(data.email);
                        $('#popupContainer').fadeOut(150);
                    })
                    .catch(error => {
                        console.error('API error:', error.message);
                    });

            } else {
                $('#popupContainer').fadeOut(150);
            }
        });
    }

    $("button.add-btn").click(() => {
        $("div.choices").append(`
            <div class="form-group">
                <input type="text" placeholder="Option ..." class="form-control option">
            </div>
        `);
    });
    $("button.remove-btn").click(() => {
        $("div.choices").children(".form-group").last().remove();
    });

    $('#popup').show();

    $('#dashboard-info, #dashboard-result').addClass('blurred-background');

    // Remove the blur when the popup is closed
    $('#popup').on('hidden.bs.modal', () => {
        $('.section-container, #dashboard-result').removeClass('blurred-background');
    });

    let bio;

    $('#bioSubmit').click((event) => {
        event.preventDefault(); // Prevent default form submission

        // Input values
        const fullName = $('#full-name').val().trim();
        const selectedSex = $('#sex').val();

        // Validation
        let isValid = true;
        let errorMessage = '';

        if (fullName === '') {
            isValid = false;
            errorMessage += 'Please enter your full name.<br>';
        }

        const allowedSexValues = ['male', 'female', 'Prefer not to say'];
        if (!allowedSexValues.includes(selectedSex)) {
            isValid = false;
            errorMessage += `Please select a valid sex option.<br>`;
        }

        // Displaying errors or creating the JSON object
        if (isValid) {
            bio = {
                name: capitalizeFirstLetters(fullName),
                sex: selectedSex
            };

            // console.log(bio);
            $('#popup').hide();
            $('#dashboard-info, #dashboard-result').removeClass('blurred-background');
            $("#responder").text(bio.name);

        } else {
            $('#error-message').html(errorMessage);
        }
    });

    $('#collapseButton').click(function () {
        $('#dashboard-info').toggleClass('show');
        $('#dashboard-result').toggleClass('slide');
        $('#collapseButton').toggleClass('hide');
    });

    $('.options').click(function () {
        var checkbox = $(this).find('input[type="checkbox"]');
        checkbox.prop('checked', !checkbox.prop('checked'));
        updateProgress();
    });

    $("#commit, #commit1").click(function () {
        // Check if all questions have been answered
        var unansweredQuestions = $(".question").filter(function () {
            return $(this).find('input[type="checkbox"]:checked').length === 0;
        });

        if (unansweredQuestions.length > 0) {
            // If there are unanswered questions, display the Bootstrap modal alert
            // $("main").toggleClass("blurred-background");
            $('#confirmationModal').modal('show');

            // Handle the Continue Survey button click
            $('#continueBtn').click(function () {
                // If the user chooses to continue, close the modal and proceed
                $('#confirmationModal').modal('hide');
                submitResponses();
            });
        } else {
            // If all questions have been answered, proceed with submitting responses
            submitResponses();
        }
    });

    function submitResponses() {
        var responses = [];
        $(".question").each(function () {
            var questionId = $(this).attr("id");
            var selectedOptions = [];
            $(this).find("input[type='checkbox']:checked").each(function () {
                selectedOptions.push($(this).attr("name"));
            });
            responses.push({
                "question_id": questionId,
                "response": selectedOptions
            });
        });
        var data = {
            "bio": bio,
            "answers": responses
        };

        console.log(JSON.stringify(data));
    }

    
});
