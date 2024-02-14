$(document).ready(() => {

    let root = "{{ my_variable }}";

    setTimeout(() => {
        $("#top").hide();
    }, 4000);

    $('#questiontype').on('change', function () {
        $('.bottom-section').toggle($(this).val() === 'multiple');
    }).trigger('change'); // Triggering the change event once to handle initial state


    $("span[id='#toggle-login-password']").addClass("fill");
    
    $('button.navbar-toggler').click(() => {
        $('#navbarToggle').slideToggle();
    });
    

    $('#popupButton').click(() => {
        // $('#btn').click(() => {
        //     $.ajax({
        //         url: root + '/users/,
        //         method: 'GET',
        //         dataType: 'json',
        //         success: function(response) {
        //             // Handle successful response
        //             console.log(response);
        //         },
        //         error: function(xhr, status, error) {
        //             // Handle errors
        //             console.error(status, error);
        //         }
        //     });
        // });
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
    
});
