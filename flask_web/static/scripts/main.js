$(document).ready(() => {

    $("span[id='#toggle-login-password']").addClass("fill");

    $('#popupButton').click(() => {
        $('#popupContainer').fadeIn(150);
    });

    $('#popupContainer').click((e) => {
        if (e.target.id === 'popupContainer') {
            $('#popupContainer').fadeOut(150);
        }
    });

    $("#closeButton").click(() => {
        $('#popupContainer').fadeOut(150);
    });

    $('#toggle-login-password').click(() => {
        $('input[name="password"]').attr('type', $('input[name="password"]').attr('type') === 'password' ? 'text' : 'password');
        $("#now").toggleClass('fa-eye fa-eye-slash');
    });

    $('#toggle-login-confirm_password').click(() => {
        $('input[name="confirm_password"]').attr('type', $('input[name="confirm_password"]').attr('type') === 'password' ? 'text' : 'password');
        $("#confirm_now").toggleClass('fa-eye fa-eye-slash');
    });

});
