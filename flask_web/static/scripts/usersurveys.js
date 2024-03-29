$(document).ready(() => {
  // alert("hello")
  $('#loader').hide()
  
  $(".survey-title").on("click", function() {
    // Remove 'active' class from all links
    $('.link').removeClass('active')
    $(this).parent('.link').addClass('active')
  })

  function formatDate (dateString) {
    // Split the date and time parts
    var parts = dateString.split(' ')

    // Keep only the date part (i.e., the first part)
    var datePart = parts[0]

    // Format the date
    var date = new Date(datePart)
    var options = {
      weekday: 'long',
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    }
    var formattedDate = date.toLocaleDateString('en-US', options)

    return formattedDate
  }

  function openNav () {
    let width = '350px'
    $('#mySidenav').css('width', width)
    $('#main').css('marginLeft', width)
    $('.sticky').hide()
  }

  function closeNav () {
    $('#mySidenav').css('width', '0')
    $('#main').css('marginLeft', '0')
    $('.sticky').show()
  }

  function openNavSmall () {
    $('#mySidenav').css('width', '350px')
    $('.sticky').hide()
  }

  function closeNavSmall () {
    $('#mySidenav').css('width', '0')
    $('.sticky').show()
  }

  if ($(window).width() <= 992) {
    $('#openNav').click(openNavSmall)
    $('#closeNav').click(closeNavSmall)
  } else {
    $('#openNav').click(openNav)
    $('#closeNav').click(closeNav)
    $('#openNav').click()
  }

  $(window).resize(() => {
    if ($(window).width() <= 768) {
      $('#openNav').click(openNavSmall)
      $('#closeNav').click(closeNavSmall)
    } else {
      $('#openNav').click(openNav)
      $('#closeNav').click(closeNav)
    }
  })

  function apiCall (id) {
    $('#loader').show()
    $('#dashboard-result').addClass('blurred-background')
    if (!id) {
      return Promise.reject(new Error('Invalid ID'))
    }
    return new Promise((resolve, reject) => {
      $.ajax({
        type: 'GET',
        url: 'http://localhost:5000/api/v1/survey/' + id,
        success: response => {
          // const responseData = JSON.stringify(response);
          $('#loader').hide()
          $('#dashboard-result').removeClass('blurred-background')
          resolve(response)
        },
        error: (xhr, status, error) => {
          $('#loader').hide()
          $('#dashboard-result').removeClass('blurred-background')
          reject(
            new Error(
              xhr.responseText + ' ' + xhr.status + ' ' + xhr.statusText
            )
          )
        }
      })
    })
  }

  $('.bottom-section').hide()

  $('.survey-title').click(function () {
    var id = $(this).parent().attr('id');

    apiCall(id)
      .then(data => {
        // console.log(data)
        $('#populate').children('.grid-container').empty()
        $('#title').text(data.title)
        $('#created_at').text(formatDate(data.created_at))
        $('#response').text(data.numberOfResponse)
        $('#expiration').text(formatDate(data.expiry_date))
        $('#delete-survey').attr('name', data.id)
        if (data.visibility) {
          $('#visibility').click()
        }
        if (data.randomize) {
          $('#randomize').click()
        }
        // console.log(data.questions)
        const questions = data.questions
        var questionNumber = 0
        questions.forEach(question => {
          let optionsHTML = '' // Variable to store options HTML
          // Loop through each option and concatenate input elements
          for (let i = 0; i < question.options.length; i++) {
            optionsHTML += `<p class="form-control option m-2"><strong><em>${String.fromCharCode(
              i + 65
            )}</em>.</strong>&Tab;${question.options[i]}</p>`
          }
          // Append question and options to the 'populate' element
          $('#populate').children('.grid-container').append(`
                    <div class="grid-item question-block p-3 m-2 hope">
                        <div class="top-section">
                            <div class="form-group d-flex justify-content-between align-items-center">
                                <h4 class="m-0 mb-3">Question ${++questionNumber}</h4>
                                <button data-bs-container="body" data-bs-toggle="tooltip" data-bs-placement="right" title="View Options" class="option-tag btn btn-outline-success btn-3d m-0 py-0"><i class="fa-solid fa-arrow-down-short-wide"></i></button>
                            </div>
                            <div class="input-group mb-4">
                                <p class="questionTextarea" rows="5" placeholder="Type Question">${
                                  question.question
                                }</p>
                            </div>
                        </div>
                        <div class="px-3 bottom-section">
                            <div class="py-2">
                                ${optionsHTML}
                            </div>
                        </div>
                    </div>
                `)
        })
      })
      .then(() => {
        $('.bottom-section').hide()
      })
      .catch(error => {
        console.error('Error:', error.message)
      })
  })

  $('.survey-title:first').click()
  $('.popup').hide()

  $(document).on('click', '.option-tag', function () {
    var questionBlock = $(this).closest('.question-block')
    var bottomSection = questionBlock.find('.bottom-section')

    // Check if the bottom section is hidden
    if (questionBlock.hasClass('hope')) {
      // Add the 'hope' class only if the bottom section is hidden
      questionBlock.removeClass('hope')
    } else {
      questionBlock.addClass('hope')
      // Remove the 'hope' class if the bottom section is visible
    }

    // Toggle the visibility of the bottom section
    $('.bottom-section').not(bottomSection).slideUp(1)
    bottomSection.slideToggle()
  })

  $('.copy-button').click(function () {
    var id = $(this).parent().attr('id')
    var homeLink = window.location.origin
    response_link = homeLink + '/app/survey/respond/' + id
    navigator.clipboard.writeText(response_link)

    var popup = $(this).siblings('.popup') // Find the sibling popup of the clicked button
    popup.show() // Show the popup
    setTimeout(function () {
      popup.hide() // Hide the popup after 2 seconds
    }, 2000)
  })

  $('#delete-survey').click(function () {
    let id = $(this).attr('name')
    // Show confirmation modal
    // console.log("http://localhost:5000/api/v1/survey/" + id)
    $('#confirmationModal').modal('show')

    // Change modal content and button text according to requirements
    $('#confirmationModal .modal-body').html(
      'Are you sure you want to delete the survey?'
    )
    $('#continueBtn')
      .text('Delete Survey')
      .removeClass('btn-outline-success')
      .addClass('btn-danger')

    $('#continueBtn')
      .off('click')
      .on('click', () => {
        $.ajax({
          url: 'http://localhost:5000/api/v1/survey/' + id,
          type: 'DELETE',
          success: function (response) {
            alert('Survey Deleted')
            window.location.reload()
          },
          error: function (xhr, status, error) {
            var errorMessage = xhr.responseText + ' ' + xhr.status // Capture the server's error message
            alert(errorMessage)
          }
        })
        $('#confirmationModal').modal('hide')
      })
  })

  $('#no-create_survey').click(function () {
    window.location.href = '/app/survey/new'
  })

  $('#survey-dashboard').click(() => {
    let id = $('a.active').attr('id')
    // console.log(window.location.origin + "/app/dashboard/" + id)
    window.location.href = '/app/dashboard/' + id
  })
})
