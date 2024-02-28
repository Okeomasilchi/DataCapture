$(document).ready(function () {
    // alert("hello");

    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); // January is 0!
    var yyyy = today.getFullYear();
    today = yyyy + '-' + mm + '-' + dd;

    // Set the min attribute of the date input to today's date
    $("#exp_date").attr("min", today);

    function openNav() {
        let width = "400px"
        $("#mySidenav").css("width", width);
        $("#main").css("marginLeft", width);
        $(".sticky").hide();
    }

    function closeNav() {
        $("#mySidenav").css("width", "0");
        $("#main").css("marginLeft", "0");
        $(".sticky").show();
    }

    function openNavSmall() {
        $("#mySidenav").css("width", "350px");
        $(".sticky").hide();
    }

    function closeNavSmall() {
        $("#mySidenav").css("width", "0");
        $(".sticky").show();
    }


    if ($(window).width() <= 768) { // 768px is the Bootstrap medium breakpoint
        $("#openNav").click(openNavSmall);
        $("#closeNav").click(closeNavSmall);
        $("#openNav").click();
    } else {
        $("#openNav").click(openNav);
        $("#closeNav").click(closeNav);
        $("#openNav").click();
    }

    // Check screen width on window resize
    $(window).resize(() => {
        if ($(window).width() <= 768) {
            $("#openNav").click(openNavSmall);
            $("#closeNav").click(closeNavSmall);
        } else {
            $("#openNav").click(openNav);
            $("#closeNav").click(closeNav);
        }
    });

    $('#append').on('click', '#remove', function () {
        if ($('.border').length > 1) {
            // If there is more than one question block, remove the parent .border .row block
            $(this).closest('.border').remove();
        }
    });
    var questionCounter = 1;
    $("#add").click(() => {
        // Append the HTML code snippet to the #append element
        $('#append').append(`
        <div class="border row container my-3">
        <div class="col-md-7">
          <div class="top-section">
            <div class="heading d-flex justify-content-between m-3 align-items-center">
              <h2 class="m-0">Question</h2>
              <button type="button" id="remove"
                class="btn btn-3d btn-outline-danger p-20 text-center fa-solid fa-trash-can m-0"></button>
            </div>

            <div class="input-group mb-4">
              <textarea class="form-control questionTextarea" rows="5" placeholder="Type Question"></textarea>
            </div>
            <div class="input-group mb-4">
              <select class='form-control  questiontype-dropdown' name="questiontype" id="questiontype">
                <option value="" disabled selected>Question Type</option>
                <option value="multiple">Multiple Type</option>
                <option value="userdefined">User defined</option>
              </select>
            </div>

          </div>
        </div>
        <div class="col-md-5"> <!-- Adjusted to take 30% of the width -->
          <div class="bottom-section">
            <div class="heading m-3">
              <h2>Options</h2>
            </div>
            <div class="form-group" id="options">
              <input type="text" placeholder="Option 1" class="form-control option m-2">
              <input type="text" placeholder="Option 2" class="form-control option m-2">
            </div>
          </div>
          <div class="row">
            <div class="col-md-12"> <!-- Adjusted to take 100% of the width -->
                <div class="input-group text-center mx-auto mx-auto d-flex justify-content-center">
                    <button class="btn-3d btn btn-outline-success fa-solid fa-plus add-btn m-2 px-3"></button>
                    <button class="btn-3d btn btn-outline-danger fa-solid fa-minus remove-btn m-2 px-3"></button>
                </div>
            </div>
          </div>
        </div>
        </div>
        `);
        questionCounter++;
        // Scroll to the bottom of the page
        $('html, body').animate({
            scrollTop: $(document).height()
        }, 50);
    });

    let optionCounter = 1;

    function updatePlaceholders(optionsDiv) {
        optionsDiv.find('input[type="text"]').each(function (index) {
            $(this).attr('placeholder', 'Option ' + (index + 1));
        });
    }

    // Event listener for adding options dynamically
    $('#append').on('click', '.add-btn', function () {
        // Find the closest options within the same question block
        const optionsDiv = $(this).closest('.border').find('#options');

        // Append a new input field with an updated placeholder
        optionsDiv.append(`<input type="text" placeholder="Option ${optionCounter}" class="form-control option m-2">`);
        optionCounter++;

        // Scroll to the bottom of the options
        optionsDiv.scrollTop(optionsDiv.prop("scrollHeight"));

        // Update placeholders for all options within the same block
        updatePlaceholders(optionsDiv);
    });

    // Event listener for removing options dynamically
    $('#append').on('click', '.remove-btn', function () {
        // Find the closest options within the same question block
        const optionsDiv = $(this).closest('.border').find('#options');
        if (optionsDiv.find('input[type="text"]').length > 2) {
            // If there is more than one input field, remove the last input field
            optionsDiv.find('input[type="text"]').last().remove();
            optionCounter--;

            // Update placeholders for all options within the same block
            updatePlaceholders(optionsDiv);
        }
    });

    function saveSurvey(surveyData) {
        $("#loader").show();
        $("#dashboard-result").addClass("blurred-background");

        return new Promise((resolve, reject) => {
            $.ajax({
                url: "http://api.okeoma.tech/api/v1/survey/",
                method: 'POST',
                data: JSON.stringify(surveyData),
                contentType: 'application/json',
                success: function (response) {
                    $("#loader").hide();
                    $("#dashboard-result").removeClass("blurred-background");
                    resolve(response);
                },
                error: function (xhr) {
                    $("#loader").hide();
                    $("#dashboard-result").removeClass("blurred-background");
                    error = xhr.responseText
                    error.status = xhr.status
                    reject(new Error(error));
                }
            });
        });
    }

    function gatherQuestionDetails() {
        var questionDetails = [];

        // Survey details
        var title = $('.title').val();
        var description = $('.description').val();
        var expDate = $('#exp_date').val();
        var randomizeQuestions = $('#randomize-questions').is(':checked');
        var randomizeOptions = $('#randomize-options').is(':checked');
        var visibility = $('#visibility').is(':checked');

        console.log(expDate);
        user_id = $(".table-row").attr("id");
        // console.log(user_id);
        var surveyDetails = {
            'user_id': user_id,
            'title': title,
            'description': description,
            'expiry_date': expDate,
            'randomize': randomizeQuestions,
            "randomizeOptions": randomizeOptions,
            'visibility': visibility,
            'question_type': "Multiple Type"
        };

        // questionDetails.push(surveyDetails);

        // Loop through each question block
        $('.border.container').each(function () {
            var questionBlock = {};

            // Question details
            var questionText = $(this).find('.questionTextarea').val();
            var questionType = $(this).find('.questiontype-dropdown').val();

            questionBlock['question'] = questionText;

            // Options details
            var options = [];
            $(this).find('#options .option').each(function () {
                var optionText = $(this).val();
                options.push(optionText);
            });
            questionBlock['options'] = options;

            // Randomize options
            var random = randomizeOptions;
            questionBlock['random'] = random;

            questionDetails.push(questionBlock);
        });
        surveyDetails.questions = questionDetails;
        return surveyDetails;
    }

    $("#visibility").click();
    // Event listener for saving the survey
    $('#save').click(() => {
        var surveyData = gatherQuestionDetails();
        console.log(surveyData);
        saveSurvey(surveyData)
            .then((response) => {
                console.log(response);
                alert("Survey saved successfully");
            })
            .catch((error) => {
                console.error('Error:', error.message);
            });
    });

});