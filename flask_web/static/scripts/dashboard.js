$(document).ready(function () {
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

  var currentView = 'histogram' // Initial view mode is histogram

  // Function to toggle between pie chart and histogram
  function toggleView () {
    if (currentView === 'histogram') {
      showPieCharts()
      $('#toggle-view').text('View Histogram')
      currentView = 'pie'
    } else {
      showHistograms()
      $('#toggle-view').text('View Pie Chart')
      currentView = 'histogram'
    }
  }

  // Initially show histograms
  showHistograms()

  // Event listener for the toggle view button
  $('#toggle-view').click(function () {
    toggleView()
  })

  // Function to show pie charts
  function showPieCharts () {
    $('[id^="chart_"]').show()
    $('[id^="histogram-"]').hide()
  }

  // Function to show histogram charts
  function showHistograms () {
    $('[id^="histogram-"]').show()
    $('[id^="chart_"]').hide()
  }

  $('[id^="chart_"]').css('width', '100%')
  $('[id^="histogram-"]').css('width', '100%')
})
