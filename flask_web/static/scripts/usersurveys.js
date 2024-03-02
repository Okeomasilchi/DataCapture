$(document).ready(() => {
    // alert("hello")
    $("#loader").hide();

    $('.link-click').on('click', function () {
        // Remove 'active' class from all links
        // $(this).parent('.n-link').removeClass('active');
        $(".link").removeClass('active');

        // Add 'active' class to the clicked link
        // $(this).parent('.n-link').addClass('active');
        $(this).addClass('active');
        $("#closeNav").click()
    });

    function formatDate(dateString) {
        // Split the date and time parts
        var parts = dateString.split(' ');

        // Keep only the date part (i.e., the first part)
        var datePart = parts[0];

        // Format the date
        var date = new Date(datePart);
        var options = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
        var formattedDate = date.toLocaleDateString('en-US', options);

        return formattedDate;
    }

    function openNav() {
        let width = "350px"
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


    if ($(window).width() <= 992) {
        $("#openNav").click(openNavSmall);
        $("#closeNav").click(closeNavSmall);
    } else {
        $("#openNav").click(openNav);
        $("#closeNav").click(closeNav);
        $("#openNav").click();
    }

    $(window).resize(() => {
        if ($(window).width() <= 768) {
            $("#openNav").click(openNavSmall);
            $("#closeNav").click(closeNavSmall);
        } else {
            $("#openNav").click(openNav);
            $("#closeNav").click(closeNav);
        }
    });

    function apiCall(id) {
        $("#loader").show();
        $("#dashboard-result").addClass("blurred-background")
        if (!id) {
            return Promise.reject(new Error('Invalid ID'));
        }
        return new Promise((resolve, reject) => {
            $.ajax({
                type: "GET",
                url: "https://www.okeoma.tech/api/v1/survey/" + id,
                success: (response) => {
                    // const responseData = JSON.stringify(response);
                    $("#loader").hide();
                    $("#dashboard-result").removeClass("blurred-background")
                    resolve(response);
                },
                error: (xhr, status, error) => {
                    $("#loader").hide();
                    $("#dashboard-result").removeClass("blurred-background")
                    reject(new Error(xhr.responseText + " " + xhr.status + " " + xhr.statusText));
                }
            });
        });
    }


    $(".bottom-section").hide();

    $(".link-click").click(function () {
        var id = $(this).attr('id');;

        apiCall(id)
            .then((data) => {
                console.log(data)
                $("#populate").children(".row").empty();
                $("#title").text(data.title);
                $("#created_at").text(formatDate(data.created_at));
                $("#expiration").text(formatDate(data.expiry_date));
                $("#delete-survey").attr("name", data.id);
                if (data.visibility) {
                    $("#visibility").click();
                }
                if (data.randomize) {
                    $("#randomize").click();
                }
                // console.log(data.questions)
                const questions = data.questions;
                var questionNumber = 0;
                questions.forEach((question) => {
                    let optionsHTML = ''; // Variable to store options HTML
                    // Loop through each option and concatenate input elements
                    for (let i = 0; i < question.options.length; i++) {
                        optionsHTML += `<p class="form-control option m-2"><strong><em>${String.fromCharCode(i + 65)}</em>.</strong>&Tab;${question.options[i]}</p>`;
                    }
                    // Append question and options to the 'populate' element
                    $("#populate").children(".row").append(`
                    <div class="col-lg-4 col-md-6 col-sm-12 question-block p-3 m-2">
                        <div class="top-section">
                            <div class="form-group d-flex justify-content-between align-items-center">
                                <h4 class="m-0 mb-3">Question ${++questionNumber}</h4>
                                <button class="option-tag btn btn-outline-success btn-3d m-0 py-0"><i class="fa-solid fa-arrow-down-short-wide"></i></button>
                            </div>
                            <div class="input-group mb-4">
                                <p class="questionTextarea" rows="5" placeholder="Type Question">${question.question}</p>
                            </div>
                        </div>
                        <div class="px-3 bottom-section">
                            <div class="py-2">
                                ${optionsHTML}
                            </div>
                        </div>
                    </div>
                `);
                });
            })
            .then(() => {
                $(".bottom-section").hide();
            })
            .catch((error) => {
                console.error('Error:', error.message);
            });

    });

    $(".link-click:first").click();

    $(document).on("click", ".option-tag", function () {
        var bottomSection = $(this).closest(".question-block").find(".bottom-section");
        $(".bottom-section").not(bottomSection).slideUp(1);
        bottomSection.slideToggle();
    });

    $('#copy-t').click(function () {
        var id = $(this).closest('a').attr('id');
        // var currentURL = window.location.href;
        var homeLink = window.location.origin;
        response_link = homeLink + "/app/survey/respond/" + id;
        navigator.clipboard.writeText(response_link);

        var tooltip = document.getElementById("myTooltip");
        tooltip.innerHTML = "Copied: " + copyText.value;

        var popup = $(this).siblings('.popup'); // Find the sibling popup of the clicked button
        popup.show(); // Show the popup
        setTimeout(function() {
            popup.hide(); // Hide the popup after 2 seconds
        }, 2000);
    });

    $("#delete-survey").click(function () {
        var id = $(this).attr("name");
        var url = "https://www.okeoma.tech/api/v1/survey/" + id;
        // Show confirmation modal
        $('#confirmationModal').modal('show');

        // Change modal content and button text according to requirements
        $('#confirmationModal .modal-body').html("Are you sure you want to delete the survey?");
        $('#continueBtn').text('Delete Survey').removeClass('btn-outline-success').addClass('btn-danger');

        // Continue commit button action
        $('#continueBtn').off('click').on('click', function () {
            $.ajax({
                type: "DELETE",
                url: url,
                success: function (response) {
                    // console.log(response);
                    alert("Survey Deleted");
                    window.location.reload();
                },
                error: function (xhr, status, error) {
                    // console.log(xhr.responseText + " " + xhr.status + " " + xhr.statusText);
                    alert("An error occurred");
                }
            });
            // Hide the modal after deletion
            $('#confirmationModal').modal('hide');
        });
    });

    $("#no-create_survey").click(function () {
        window.location.href = "/app/survey/new";
    });

});
