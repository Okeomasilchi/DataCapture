$(document).ready(() => {
    $('#popupButton').click(() => {
        $('#popupContainer').fadeIn(150);
    });

    $('#popupContainer').click((e) => {
        if (e.target.id === 'popupContainer') {
            $('#popupContainer').fadeOut(150);;
        }
    });

    // $('#closeButton').click(() => {
    //     $('#popupContainer').hide();
    // });

});
