$(document).ready(function () {
  // alert("hello");

  // get and parse the survey id from the url on the browser
  var survey_id = String(window.location.href)
  survey_id = survey_id.substring(survey_id.lastIndexOf('/') + 1)
  survey_id = survey_id.replace(/\?$/, '')

  function openNav () {
    let width = '400px'
    $('#mySidenav').css('width', width)
    $('#main').css('marginLeft', width)
    $('.sticky').hide()
    $('#response-container').css('padding', '20px 80px')
  }

  function closeNav () {
    $('#mySidenav').css('width', '0')
    $('#main').css('marginLeft', '0')
    $('.sticky').show()
    $('#response-container').css('padding', '20px 40px')
  }

  function openNavSmall () {
    $('#mySidenav').css('width', '95%')
    $('.sticky').hide()
  }

  function closeNavSmall () {
    $('#mySidenav').css('width', '0')
    $('.sticky').show()
  }

  if ($(window).width() <= 768) {
    // 768px is the Bootstrap medium breakpoint
    $('#openNav').click(openNavSmall)
    $('#closeNav').click(closeNavSmall)
    $('#openNav').click()
  } else {
    $('#openNav').click(openNav)
    $('#closeNav').click(closeNav)
    $('#openNav').click()
  }

  // Check screen width on window resize
  $(window).resize(() => {
    if ($(window).width() <= 768) {
      $('#openNav').click(openNavSmall)
      $('#closeNav').click(closeNavSmall)
    } else {
      $('#openNav').click(openNav)
      $('#closeNav').click(closeNav)
    }
  })

  const progressBar = document.getElementById('progressBar')

  // Function to update the progress bar
  function updateProgress () {
    // Count the number of answered questions
    var answeredQuestions = $('.question').filter(function () {
      return $(this).find('input[type="checkbox"]:checked').length > 0
    }).length
    // Update the value of the progress bar
    progressBar.value = answeredQuestions
  }
  updateProgress()

  $('.options').click(function () {
    var checkbox = $(this).find('input[type="checkbox"]')
    checkbox.prop('checked', !checkbox.prop('checked'))
    updateProgress()
  })

  var currentYear = new Date().getFullYear()

  $('#popup').show()
  $('#main, #mySidenav').addClass('blurred-background')

  // Remove the blur when the popup is closed
  $('#popup').on('hidden.bs.modal', () => {
    $('#main, #mySidenav').removeClass('blurred-background')
  })

  let bio

  $('#bioSubmit').click(event => {
    event.preventDefault() // Prevent default form submission

    // Input values
    const fullName = $('#full-name').val().trim()
    const selectedSex = $('#sex').val()

    // Validation
    let isValid = true
    let errorMessage = ''

    if (fullName === '') {
      isValid = false
      errorMessage += 'Please enter your full name.<br>'
    } else if (!/^[a-zA-Z\s]+$/.test(fullName)) {
      isValid = false
      errorMessage += 'Name should only contain letters and spaces.<br>'
    }

    const allowedSexValues = [
      'male',
      'female',
      'trans-Gender',
      'Prefer not to say'
    ]
    if (!allowedSexValues.includes(selectedSex)) {
      isValid = false
      errorMessage += `Please select a valid sex option.<br>`
    }

    // Displaying errors or creating the JSON object
    if (isValid) {
      bio = {
        name: capitalizeFirstLetters(fullName),
        sex: selectedSex
      }

      // console.log(bio);
      $('#popup').hide()
      $('#main, #mySidenav').removeClass('blurred-background')
      $('#responder').text(bio.name)
    } else {
      $('#error-message').html(errorMessage)
    }
  })

  var fadeInTime = 400
  var fadeOutTime = 0
  $('#arrow').fadeOut(fadeOutTime)

  $('span#openNav').hover(
    function () {
      // Function to execute on hover in
      $('#arrow').fadeIn(fadeInTime)
      $('#long').fadeOut(fadeOutTime)
    },
    function () {
      // Function to execute on hover out
      $('#arrow').fadeOut(fadeOutTime)
      $('#long').fadeIn(fadeInTime)
    }
  )

  $('#commit, #commit1').click(function () {
    // Check if all questions have been answered
    var unansweredQuestions = $('.question').filter(function () {
      return $(this).find('input[type="checkbox"]:checked').length === 0
    })

    if (unansweredQuestions.length > 0) {
      // If there are unanswered questions, display the Bootstrap modal alert
      // $("main").toggleClass("blurred-background");
      $('#confirmationModal').modal('show')

      // Handle the Continue Survey button click
      $('#continueBtn').click(function () {
        // If the user chooses to continue, close the modal and proceed
        $('#confirmationModal').modal('hide')
        submitResponses()
      })
    } else {
      // If all questions have been answered, proceed with submitting answers
      submitResponses()
    }
  })

  function sendPostRequest (jsonData) {
    return new Promise(function (resolve, reject) {
      $.ajax({
        url: 'http://localhost:5000/api/v1/response/' + survey_id,
        type: 'POST',
        data: JSON.stringify(jsonData),
        contentType: 'application/json',
        success: function (response) {
          resolve(response)
        },
        error: function (xhr, status, error) {
          var errorMessage = xhr.responseText + xhr.status // Capture the server's error message
          reject(errorMessage) // Reject the promise with the error message
        }
      })
    })
  }

  function submitResponses () {
    let answers = []

    $('.question').each(function () {
      var questionId = $(this).attr('id')
      var selectedOptions = []
      $(this)
        .find("input[type='checkbox']:checked")
        .each(function () {
          selectedOptions.push($(this).attr('name'))
        })
      answers.push({
        question_id: questionId,
        response: selectedOptions
      })
    })

    var data = {
      bio,
      answers,
      survey_id
    }

    sendPostRequest(data)
      .then(() => {
        alert('Survey successfully submited!!!')
      })
      .then(() => {
        window.location.href = '/'
      })
      .catch(errorMessage => {
        console.log(errorMessage)
      })
  }

  // Capitalize the first letter of each word
  capitalizeFirstLetters = str =>
    str.toLowerCase().replace(/\b\w/g, l => l.toUpperCase())
})
