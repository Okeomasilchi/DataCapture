$(document).ready(function() {
  $("#role, #verification_pin").hide();
  $(document).keydown(function(event) {
    if (event.ctrlKey && event.shiftKey && event.altKey && event.key === "Enter") {
      $("#role, #verification_pin").toggle();
    }
  });
});
