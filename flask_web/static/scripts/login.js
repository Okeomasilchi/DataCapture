$(document).ready(() => {
  $('#toggle-login-password').click(() => {
    $('input[name="password"]').attr(
      'type',
      $('input[name="password"]').attr('type') === 'password'
        ? 'text'
        : 'password'
    )
    $('#now').toggleClass('fa-eye fa-eye-slash')
  })

  $('#toggle-login-confirm_password').click(() => {
    $('input[name="confirm_password"]').attr(
      'type',
      $('input[name="confirm_password"]').attr('type') === 'password'
        ? 'text'
        : 'password'
    )
    $('#confirm_now').toggleClass('fa-eye fa-eye-slash')
  })
})
