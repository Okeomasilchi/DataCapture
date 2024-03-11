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
    setTimeout(() => {

        $("#top").hide();
    }, 3000);

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

    logo

    //     $('#copyright-year').text(currentYear);


    //     // $(".entry-animation").each(function () {
    //     //     let element = $(this);
    //     //     if (!element.hasClass("animated")) {
    //     //         element.addClass("animated");
    //     //     }
    //     // });

    //     // $(".lead").each(function () {
    //     //     let element = $(this);
    //     //     if (!element.hasClass("animatedX")) {
    //     //         element.addClass("animatedX");
    //     //     }
    //     // });
    //     var currentYear = new Date().getFullYear();

    //     $('#copyright-year').text(currentYear);


    //     // $(".entry-animation").each(function () {
    //     //     let element = $(this);
    //     //     if (!element.hasClass("animated")) {
    //     //         element.addClass("animated");
    //     //     }
    //     // });

    //     // $(".lead").each(function () {
    //     //     let element = $(this);
    //     //     if (!element.hasClass("animatedX")) {
    //     //         element.addClass("animatedX");
    //     //     }
    //     // });



    //     $('#questiontype').on('change', function () {
    //         $('.bottom-section').toggle($(this).val() === 'multiple');
    //     }).trigger('change'); // Triggering the change event once to handle initial state


    //     $("span[id='#toggle-login-password']").addClass("fill");

    //     // Add hover event listener to dashboard-info section
    //     $('#dashboard-info').hover(
    //         function () {
    //             $(this).addClass('active');
    //         },
    //         function () {
    //             $(this).removeClass('active');
    //         }
    //     );

    //     $("#collapseButton").click(() => {
    //         $("#collapseButton").toggleClass("fa-chevron-left fa-chevron-right");
    //         $("#dashboard-info").animate({
    //             width: 'toggle'
    //         });
    //         var currentMarginLeft = $("#dashboard-result").css("marginLeft");
    //         var currentBtn = $("#collapseButton").css("left");

    //         // Toggle between the two values
    //         if (currentMarginLeft === "0px") {
    //             $("#dashboard-result").animate({ marginLeft: "400px" }); // Animate to 400px
    //         } else {
    //             $("#dashboard-result").animate({ marginLeft: "0px" }); // Animate back to 0px
    //         }

    //         if (currentBtn === "0px") {
    //             $("#collapseButton").animate({ left: "400px" }); // Animate to 400px
    //         } else {
    //             $("#collapseButton").animate({ left: "0px" }); // Animate back to 0px
    //         }
    //     });


    //     // $("#navbtn").click((e) => {
    //     //     // e.preventDefault();
    //     //     $("#navcol-2").slideToggle()
    //     // });

    //     $('#navbtn').click(function () {
    //         var target = $(this).data('bs-target');
    //         $(target).collapse('toggle');
    //     });


    //     if ($.userData) {
    //         let user = $.userData;
    //         let root = user.root;
    //         let originalValues = {
    //             first_name: user.first_name,
    //             last_name: user.last_name,
    //             email: user.email
    //         };



    //         $("#closeButton").click(() => {
    //             let updatedValues = {
    //                 first_name: $('div input[id="first_name"]').val(),
    //                 last_name: $('div input[id="last_name"]').val(),
    //                 email: $('div input[id="email"]').val()
    //             };

    //             let changes = {};
    //             for (let key in updatedValues) {
    //                 if (updatedValues[key] !== originalValues[key]) {
    //                     changes[key] = updatedValues[key];
    //                 }
    //             }

    //             if (Object.keys(changes).length > 0) {
    //                 fetch(root + 'users/' + user.id, {
    //                     method: 'PUT',
    //                     headers: {
    //                         'Content-Type': 'application/json'
    //                     },
    //                     body: JSON.stringify(changes)
    //                 })
    //                     .then(response => {
    //                         // Check if response is successful
    //                         if (!response.ok) {
    //                             throw new Error('API error: ' + response.status + response.headers);
    //                         }

    //                         // Access status code
    //                         console.log('Status code:', response.status);

    //                         // Access other headers
    //                         console.log('Content-Type header:', response.headers.get('Content-Type'));

    //                         // Parse JSON response
    //                         return response.json();
    //                     })
    //                     .then(data => {
    //                         // Handle successful response
    //                         $('div input[id="first_name"]').val(data.first_name);
    //                         $('div input[id="last_name"]').val(data.last_name);
    //                         $('div input[id="email"]').val(data.email);
    //                         $('#popupContainer').fadeOut(150);
    //                     })
    //                     .catch(error => {
    //                         console.error('API error:', error.message);
    //                     });

    //             } else {
    //                 $('#popupContainer').fadeOut(150);
    //             }
    //         });
    //     }

    //     $("button.add-btn").click(() => {
    //         $("div.choices").append(`
    //             <div class="form-group">
    //                 <input type="text" placeholder="Option ..." class="form-control option">
    //             </div>
    //         `);
    //     });
    //     $("button.remove-btn").click(() => {
    //         $("div.choices").children(".form-group").last().remove();
    //     });


    //     $('#collapseButton').click(function () {
    //         $('#dashboard-info').toggleClass('show');
    //         $('#dashboard-result').toggleClass('slide');
    //         $('#collapseButton').toggleClass('hide');
    //     });

});
