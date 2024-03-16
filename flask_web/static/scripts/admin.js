$(document).ready(function () {
  $('#loader').hide()

  function openNav () {
    let width = '400px'
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

  function fetchUser () {
    return new Promise((resolve, reject) => {
      $.ajax({
        url: 'https://randomuser.me/api/',
        dataType: 'json',
        success: function (data) {
          resolve(data)
        },
        error: function (error) {
          reject(error)
        }
      })
    })
  }

  function getApiStatus () {
    return new Promise((resolve, reject) => {
      $.ajax({
        url: 'http://localhost:5000/api/v1/status',
        dataType: 'json',
        success: function (data) {
          resolve(data)
        },
        error: function (error) {
          reject(error)
        }
      })
    })
  }

  function getData () {
    return new Promise((resolve, reject) => {
      $.ajax({
        url: 'http://localhost:5000/api/v1/users',
        dataType: 'json',
        success: function (data) {
          resolve(data)
        },
        error: function (error) {
          reject(error)
        }
      })
    })
  }

  function formatDate (dateString) {
    const months = [
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December'
    ]
    const days = [
      'Sunday',
      'Monday',
      'Tuesday',
      'Wednesday',
      'Thursday',
      'Friday',
      'Saturday'
    ]

    const date = new Date(dateString)
    const dayName = days[date.getDay()]
    const dayOfMonth = date.getDate()
    const monthName = months[date.getMonth()]
    const year = date.getFullYear()

    return `${dayName}, ${dayOfMonth}-${monthName} ${year}`
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

  $('#closeNav').click()
  getApiStatus()
    .then(data => {
      $('#api-status').prepend(`
      <div class="api-status bg-success">
        <div class="d-flex flex-column justify-content-center align-items-center">
          <h2>API Status: ${data.status} <i class="fa-regular fa-circle-check"></i></h2>
        </div>
      </div>
    `)
    })
    .then(() => {
      fetchUser()
        .then(data => {
          const { name, email, id, picture, dob, login } = data.results[0]
          // console.log(name, id, email, picture)
          $('#profile').append(`
        <div class="profile-info pt-4 mt-3">
          <div class="d-flex flex-column justify-content-center align-items-center">
            <img src="${
              picture.large
            }" alt="${email}" class="rounded-circle profile-photo" />
            <div class="profile-details p-5">
              <p class="username"><strong>Username:</strong> <em>${
                login.username
              }</em></p>
              <p class="account-level"><strong>Account Level:</strong> <em>${
                id.name
              }-${id.value}</em></p>
              <p class="full-name"><strong>Full Name:</strong> <em>${
                name.first
              } ${name.last}</em></p>
              <p class="email"><strong>Email:</strong> <em>${email}</em></p>
              <p class="DOB"><strong>DOB:</strong> <em>${formatDate(
                dob.date
              )}</em></p>
            </div>
          </div>
          
        </div>
      `)
        })
        .catch(error => {
          console.error(error)
          $('#profile').append(`
            <div class="profile-info my-auto">
              <div class="d-flex flex-column justify-content-center align-items-center">
                <h2 style="background-color: red;">Failed to fetch user</h2>
              </div>
            </div>
          `)
        })
    })
    .catch(error => {
      // console.error(error)
      $('#api-status').append(`
      <div class="api-status bg-danger pt-2">
        <div class="d-flex flex-column justify-content-center align-items-center">
        ${
          error.status === 500
            ? `<h2>Api Status: <i class="fa-solid fa-triangle-exclamation"></i></h2>`
            : `<h2>Api Status: ${
                error.status === 503
                  ? `<i class="fa-solid fa-screwdriver-wrench"></i>`
                  : `Offline`
              }</h2>`
        }
        </div>
      </div>
    `)
    $('#dashboard').append(`
      <div class="api-status bg-danger p-5 my-auto mx-5">
        <div class="d-flex flex-column justify-content-center align-items-center">
        ${
          error.status === 500
            ? `<h2>Api Status: <i class="fa-solid fa-triangle-exclamation"></i></h2>`
            : `<h2>Api Status: ${
                error.status === 503
                  ? `<i class="fa-solid fa-screwdriver-wrench"></i>`
                  : `Offline`
              }</h2>`
        }
        </div>
      </div>
    `)
    
    })
})
