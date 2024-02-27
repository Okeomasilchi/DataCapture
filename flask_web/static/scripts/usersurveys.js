$(document).ready(() => {
    // alert("hello")
    // const navLinks = document.querySelectorAll('.nav-link')

    // navLinks.forEach((link) => {
    //     link.addEventListener('click', (event) => {
    //         // Remove 'active' class from other links
    //         navLinks.forEach((link) => link.classList.remove('active'))

    //         // Add 'active' class to the clicked link
    //         event.currentTarget.classList.add('active')
    //     })
    // })

    $('.link').on('click', function () {
        // Remove 'active' class from all links
        $('.link').removeClass('active');

        // Add 'active' class to the clicked link
        $(this).addClass('active');
    });

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


    if ($(window).width() <= 768) {
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
        if (!id) {
            return Promise.reject(new Error('Invalid ID'));
        }

        return new Promise((resolve, reject) => {
            $.ajax({
                type: "GET",
                url: "http://localhost:5000/api/v1/survey/" + id,
                success: (response) => {
                    // const responseData = JSON.stringify(response);
                    resolve(response);
                },
                error: (error) => {
                    reject(new Error('API call failed'));
                }
            });
        });
    }


    $(".bottom-section").hide();

    data = { "description": "Description for Survey 3", "expiry_date": "2024-03-01", "randomize": true, "id": "70900d07-1d40-4bf0-a587-abe4e4487ce8", "updated_at": "2024-01-31 14:06:05", "title": "Survey 3 for User 1", "user_id": "08c2c669-15b5-4e0a-951b-92d17c27a370", "visibility": true, "question_type": "Multiple Choice", "created_at": "2024-01-31 14:06:05", "__class__": "Survey", "questions": [{ "random": false, "survey_id": "70900d07-1d40-4bf0-a587-abe4e4487ce8", "created_at": "2024-01-31 14:50:07", "question": "Question for 70900d07-1d40-4bf0-a587-abe4e4487ce8?", "options": ["Option 1", "Option 2", "Option 3"], "id": "47006707-11f3-4fad-8d61-a61b5594dea1", "updated_at": "2024-01-31 14:50:07", "__class__": "Question" }, { "random": true, "survey_id": "70900d07-1d40-4bf0-a587-abe4e4487ce8", "created_at": "2024-01-31 14:50:07", "question": "Question for 70900d07-1d40-4bf0-a587-abe4e4487ce8?", "options": ["Option 1", "Option 2", "Option 3"], "id": "8128d9be-8552-4bc8-88db-8e642f7531f1", "updated_at": "2024-01-31 14:50:07", "__class__": "Question" }, { "random": false, "survey_id": "70900d07-1d40-4bf0-a587-abe4e4487ce8", "created_at": "2024-01-31 14:50:08", "question": "Question for 70900d07-1d40-4bf0-a587-abe4e4487ce8?", "options": ["Option 1", "Option 2", "Option 3", "Option 4"], "id": "d9dc836b-6204-490a-bd21-9a9c189b8771", "updated_at": "2024-01-31 14:50:08", "__class__": "Question" }, { "random": true, "survey_id": "70900d07-1d40-4bf0-a587-abe4e4487ce8", "created_at": "2024-01-31 14:50:08", "question": "Question for 70900d07-1d40-4bf0-a587-abe4e4487ce8?", "options": ["Option 1", "Option 2", "Option 3"], "id": "dd1edcad-a136-4f69-ac65-bb20c1dd7ab9", "updated_at": "2024-01-31 14:50:08", "__class__": "Question" }, { "random": false, "survey_id": "70900d07-1d40-4bf0-a587-abe4e4487ce8", "created_at": "2024-01-31 14:50:07", "question": "Question for 70900d07-1d40-4bf0-a587-abe4e4487ce8?", "options": ["Option 1", "Option 2", "Option 3", "Option 4"], "id": "e896c4bb-3e2c-4524-a0c7-629d0198ab78", "updated_at": "2024-01-31 14:50:07", "__class__": "Question" }] }

    $("a.link").click(function () {
        var id = $(this).attr("id");

        $("#populate").children(".row").empty();
        const questions = data.questions;
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
                                <h4 class="m-0 mb-3">Question</h4>
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
        $(".bottom-section").hide();
        // apiCall(id)
        //     .then((data) => {
        //         // console.log(data)
        //         $("#populate").children(".row").empty();
        //         const questions = data.questions;
        //         questions.forEach((question) => {
        //             let optionsHTML = ''; // Variable to store options HTML
        //             // Loop through each option and concatenate input elements
        //             for (let i = 0; i < question.options.length; i++) {
        //                 optionsHTML += `<p class="form-control option m-2"><strong><em>${String.fromCharCode(i + 65)}</em>.</strong>&Tab;${question.options[i]}</p>`;
        //             }
        //             // Append question and options to the 'populate' element
        //             $("#populate").children(".row").append(`
        //             <div class="col-lg-4 col-md-6 col-sm-12 question-block p-3 m-2">
        //                 <div class="top-section">
        //                     <div class="form-group d-flex justify-content-between align-items-center">
        //                         <h4 class="m-0 mb-3">Question</h4>
        //                         <button class="option-tag btn btn-outline-success btn-3d m-0 py-0"><i class="fa-solid fa-arrow-down-short-wide"></i></button>
        //                     </div>
        //                     <div class="input-group mb-4">
        //                         <p class="questionTextarea" rows="5" placeholder="Type Question">${question.question}</p>
        //                     </div>
        //                 </div>
        //                 <div class="px-3 bottom-section">
        //                     <div class="py-2">
        //                         ${optionsHTML}
        //                     </div>
        //                 </div>
        //             </div>
        //         `);
        //         });
        //     })
        //     .then(() => {
        //         $(".bottom-section").hide();
        //     })
        //     .catch((error) => {
        //         console.error('Error:', error.message);
        //     });
    });

    $("a.link:first").click();

    $(document).on("click", ".option-tag", function () {
        var bottomSection = $(this).closest(".question-block").find(".bottom-section");
        $(".bottom-section").not(bottomSection).slideUp(1);
        bottomSection.slideToggle();
    });

    // Add your existing JavaScript logic here, such as handling the copy button click event
    // $('.copy-button').click(() => {
    //     // Your copy functionality code here
    //     var copyText = $(this).siblings('.survey-title').text()
    //     navigator.clipboard.writeText(copyText)
    // });

    $('button.copy-t').click(() => {
        alert("Copied the text")
        console.log("clicked")
        // Retrieve the survey ID from the closest table-data element
        var copyText = $(this).closest('.table-data');

        copyText.select();
        copyText.setSelectionRange(0, 99999); // For mobile devices

        //Copy the text inside the text field
        navigator.clipboard.writeText(copyText.value);

        //Alert the copied text
        alert("Copied the text: " + copyText.value);
    });
});
