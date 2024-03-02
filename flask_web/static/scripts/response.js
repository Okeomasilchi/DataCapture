$(document).ready(function () {
    // alert("hello");

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


    function saveSurvey(surveyData) {
        $("#loader").show();
        $("#dashboard-result").addClass("blurred-background");

        return new Promise((resolve, reject) => {
            $.ajax({
                url: "https://www.okeoma.tech/api/v1/survey/",
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

});