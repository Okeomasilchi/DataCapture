$(document).ready(function() {
    $('#popupButton').click(function() {
        $('#popupContainer').show();
    });

    $('#closeButton').click(function() {
        $('#popupContainer').hide();
    });

    $("body").css("background-color", "green");
});
