$(document).ready(() => {

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



    if ($.userData) {
        let user = $.userData;
        let root = user.root;
        let originalValues = {
            first_name: user.first_name,
            last_name: user.last_name,
            email: user.email
        };

        $('#popupButton').click(() => {
            $('div input[id="first_name"]').val(user.first_name);
            $('div input[id="last_name"]').val(user.last_name);
            $('div input[id="email"]').val(user.email);
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
                $.ajax({
                    url: root + 'users/' + user.id,
                    type: 'PUT',
                    contentType: 'application/json',
                    data: JSON.stringify(changes),
                    success: (response) => {
                        // Handle successful response
                        $('div input[id="first_name"]').val(response.first_name);
                        $('div input[id="last_name"]').val(response.last_name);
                        $('div input[id="email"]').val(response.email);            
                        console.log('API response:', response);
                    },
                    error: function (jqXHR, textStatus, errorThrown) {
                        console.error('API error:', textStatus, errorThrown);
                    }
                });
            } else {
                $('#popupContainer').fadeOut(150);
            }
        });
    }


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
