$(document).ready(function () {

  function openNav() {
      let width = "400px"
      $("#mySidenav").css("width", width);
      $("#main").css("marginLeft", width);
      $(".sticky").hide();
      $("#response-container").css("padding", "20px 80px");
  }

  function closeNav() {
      $("#mySidenav").css("width", "0");
      $("#main").css("marginLeft", "0");
      $(".sticky").show();
      $("#response-container").css("padding", "20px 40px");
  }

  function openNavSmall() {
      $("#mySidenav").css("width", "95%");
      $(".sticky").hide();
  }

  function closeNavSmall() {
      $("#mySidenav").css("width", "0");
      $(".sticky").show();
  }

  if ($(window).width() <= 768) { // 768px is the Bootstrap medium breakpoint
      $("#openNav").click(openNavSmall);
      $("#closeNav").click(closeNavSmall);
      $("#openNav").click();
  } else {
      $("#openNav").click(openNav);
      $("#closeNav").click(closeNav);
      $("#openNav").click();
  }

  // Check screen width on window resize
  $(window).resize(() => {
      if ($(window).width() <= 768) {
          $("#openNav").click(openNavSmall);
          $("#closeNav").click(closeNavSmall);
      } else {
          $("#openNav").click(openNav);
          $("#closeNav").click(closeNav);
      }
  });

//   const progressBar = document.getElementById("progressBar");

//   // Function to update the progress bar
//   function updateProgress() {
//       // Count the number of answered questions
//       var answeredQuestions = $('.question').filter(function () {
//           return $(this).find('input[type="checkbox"]:checked').length > 0;
//       }).length;
//       // Update the value of the progress bar
//       progressBar.value = answeredQuestions;
//   }
//   updateProgress();

  var fadeInTime = 400;
  var fadeOutTime = 0;
  $("#arrow").fadeOut(fadeOutTime);

  $("span#openNav").hover(
      function () { // Function to execute on hover in
          $("#arrow").fadeIn(fadeInTime);
          $("#long").fadeOut(fadeOutTime);
      },
      function () { // Function to execute on hover out
          $("#arrow").fadeOut(fadeOutTime);
          $("#long").fadeIn(fadeInTime);
      }
  );

});