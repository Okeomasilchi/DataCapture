// Make a GET request to the API endpoint
const $ = require('jquery');

$.ajax({
  url: "http://0.0.0.0:5000/api/v1/stats",
  method: "GET",
  success: function(response) {
    console.log(response);
  },
  error: function(error) {
    console.error(error);
  }
});

