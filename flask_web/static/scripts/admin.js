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
        url: 'http://localhost:5000/api/v1/admin/c/data',
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

  // Function to build the table
  function renderTable (data) {
    const $table = $(
      '<table class="table table-striped table-responsive"></table>'
    )
    $table.append('<thead></thead>')
    let $headerRow = $('<tr class="bg-success-subtle"></tr>')

    // Define the specific order of columns
    const columnOrder = [
      'first_name',
      'last_name',
      'email',
      'id',
      'account_state'
    ]

    // Add headers in the desired order
    columnOrder.forEach(key => {
      $headerRow.append(
        `<th class="p-4" data-key="${key}">${key
          .replace('_', ' ')
          .toUpperCase()}</th>`
      )
    })
    $table.prepend($headerRow)

    // Add data rows (order will be maintained)
    $table.append('<tbody></tbody>')
    data.forEach(user => {
      let $row = $('<tr></tr>')
      columnOrder.forEach(key => {
        if (key === 'account_state') {
          // Add a button to the "account state" column
          $row.append(`
            <td class="class="d-flex justify-content-center align-items-center p-2"">
              <button class="view-user btn btn-3d btn-outline-success">View</button>
              <!--<div class="d-flex justify-content-center align-items-center p-2">
                <select class="custom-select p-2">
                    <option class="m-3" value="" disabled selected>Pick an action</option>
                    <option class="m-3 bg-danger" value="delete_user">Delete User</option>
                    <option class="m-3 bg-danger" value="suspend">Suspend User</option>
                    <option class="m-3" value="edit_user">Change Email</option>
                    <option class="m-3" value="view_profile">View Profile</option>
                    <option class="m-3" value="change_password">Change Password</option>
                </select>
              </div>-->
            </td>
          `)
        } else {
          $row.append(`<td>${user[key]}</td>`)
        }
      })

      $table.find('tbody').append($row)
    })

    // Target and append the table
    $('#table-container').empty().append($table) // Clear previous table before rendering new one

    // Add click event listener to table headers for sorting
    $table.find('th').on('click', function () {
      const $this = $(this)
      const key = $this.data('key')
      const sortDirection = $this.hasClass('ascending')
        ? 'descending'
        : 'ascending'
      $table.find('th').removeClass('ascending descending active')
      $this.addClass(sortDirection + ' active')
      sortTable(key, sortDirection)
      const inputValue = $('.input').val().trim() // Get input value after sorting
      if (inputValue) {
        filterTableRows(inputValue) // Reapply filtering after sorting
      }
    })
  }

  // Function to sort table based on the specified key and direction
  function sortTable (key, direction) {
    const $table = $('#table-container table')
    const $tbody = $table.find('tbody')
    const rows = $tbody.find('tr').get()

    rows.sort(function (a, b) {
      let A = $(a)
        .find(`td:eq(${getColumnIndex(key)})`)
        .text()
        .toUpperCase()
      let B = $(b)
        .find(`td:eq(${getColumnIndex(key)})`)
        .text()
        .toUpperCase()
      if (direction === 'descending') {
        ;[A, B] = [B, A] // Swap A and B for descending order
      }
      if (A < B) return -1
      if (A > B) return 1
      return 0
    })

    $tbody.empty().append(rows)
  }

  // Function to get the index of a column by its key
  function getColumnIndex (key) {
    const $table = $('#table-container table')
    return $table.find(`th[data-key="${key}"]`).index()
  }

  // Function to filter table rows based on input value
  function filterTableRows (inputValue) {
    const $table = $('#table-container table')
    const $tbody = $table.find('tbody')
    $tbody.find('tr').hide() // Hide all rows initially

    $tbody.find('tr').each(function () {
      $(this)
        .find('td')
        .each(function () {
          if ($(this).text().toUpperCase().includes(inputValue.toUpperCase())) {
            $(this).closest('tr').show() // Show row if any cell matches the input value
            return false // Exit loop once a match is found in this row
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
        .then(() => {
          getData()
            .then(data => {
              renderTable(data)
            })
            .catch(error => {
              console.error(error)
              $('#dashboard').append(`
              <div class="profile-info my-auto">
              <div class="d-flex flex-column justify-content-center align-items-center">
                <h2 style="background-color: red;">Failed to fetch Data</h2>
              </div>
            </div>
              `)
            })
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

  $('.input').on('input', function () {
    var inputValue = $(this).val().trim()
    // console.log('Input value:', inputValue)
    filterTableRows(inputValue) // Call function to filter table rows based on input value
  })

  $('#table-container').on('click', '.view-user', function () {
    // Find the closest row to the clicked button
    const $row = $(this).closest('tr')
    const id = $row.find('td').eq(3).text()
    // console.log(id)
    window.location.href = `/admin/user/?id=${id}`
  })

  $('#delete-user').click(() => {
    var id = $('#user').attr('name')

    $.ajax({
      type: 'DELETE',
      url: `http://localhost:5000/api/v1/users/${id}`,
      success: function (response) {
        window.location.href = '/admin/analytics/'
      },
      error: function (error) {
        alert("Couldn't delete user at the moment please try again later or contact support")
      }
    })
  })

  $('#view-user-survey').click(() => {
    var id = $('#user').attr('name')
    window.location.href = `/admin/user_surveys/?id=${id}`
  })
})
