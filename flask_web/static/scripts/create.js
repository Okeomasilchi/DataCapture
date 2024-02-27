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
              <div class="input-group mb-4">
                <button class="btn-3d btn btn-outline-success fa-solid fa-plus add-btn m-1"></button>
                <button class="btn-3d btn btn-outline-danger fa-solid fa-minus remove-btn m-1"></button>
                <select class="form-control optiontype m-1" name="optiontype" id="optiontype">
                  <option value="" disabled selected>Option Type</option>
                  <option value="A">A, B, C, ...</option>
                  <option value="a">a, b, c, ...</option>
                  <option value="1">1, 2, 3, ...</option>
                  <option value="i">i, ii, iii, ...</option>
                </select>
              </div>
              <div class="checkbox-wrapper-35 mb-4">
                <input class="switch" type="checkbox" id="randomize-options-${questionCounter}" name="switch" value="private">
                <label for="randomize-options-${questionCounter}">
                    <span class="switch-x-text">
                        Randomize options
                    </span>
                    <span class="switch-x-toggletext">
                        <span class="switch-x-unchecked">
                            <span class="switch-x-hiddenlabel">
                                Unchecked: 
                            </span>
                            Off
                        </span>
                        <span class="switch-x-checked">
                            <span class="switch-x-hiddenlabel">
                                Checked: 
                            </span>
                            On
                        </span>
                    </span>
                </label>
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
        if (optionsDiv.find('input[type="text"]').length > 1) {
            // If there is more than one input field, remove the last input field
            optionsDiv.find('input[type="text"]').last().remove();
            optionCounter--;

            // Update placeholders for all options within the same block
            updatePlaceholders(optionsDiv);
        }
    });


    function gatherQuestionDetails() {
        var questionDetails = [];

        // Survey details
        var title = $('.title').val();
        var description = $('.description').val();
        var expDate = $('#exp_date').val();
        var randomizeQuestions = $('#randomize-questions').is(':checked');
        var visibility = $('#visibility').is(':checked');

        var surveyDetails = {
            'title': title,
            'description': description,
            'expirationDate': expDate,
            'randomizeQuestions': randomizeQuestions,
            'visibility': visibility
        };

        questionDetails.push(surveyDetails);

        // Loop through each question block
        $('.border.container').each(function () {
            var questionBlock = {};

            // Question details
            var questionText = $(this).find('.questionTextarea').val();
            var questionType = $(this).find('.questiontype-dropdown').val();

            questionBlock['questionText'] = questionText;
            questionBlock['questionType'] = questionType;

            // Options details
            var options = [];
            $(this).find('#options .option').each(function () {
                var optionText = $(this).val();
                options.push(optionText);
            });
            questionBlock['options'] = options;

            // Option type
            var optionType = $(this).find('.optiontype').val();
            questionBlock['optionType'] = optionType;

            // Randomize options
            var randomizeOptions = $(this).find('#randomize-options').is(':checked');
            questionBlock['randomizeOptions'] = randomizeOptions;

            questionDetails.push(questionBlock);
        });

        return questionDetails;
    }

    $("#visibility").click();
    // Event listener for saving the survey
    $('#save').click(() => {
        var surveyData = gatherQuestionDetails();
        console.log(surveyData); // You can use this data for further processing, such as sending it to the server
    });

});