// JavaScript code to dynamically populate the table
document.addEventListener("DOMContentLoaded", function() {
    // Get the <tbody> element
    var tableBody = document.querySelector('tbody');
  
    // Data for the table (dummy data for example)
    var data = [
      ['Data 1', 'Data 2', 'Data 3', 'Data 4', 'Data 5', 'Data 6'],
      ['Data 1', 'Data 2', 'Data 3', 'Data 4', 'Data 5', 'Data 6'],
      ['Data 1', 'Data 2', 'Data 3', 'Data 4', 'Data 5', 'Data 6'],
      ['Data 1', 'Data 2', 'Data 3', 'Data 4', 'Data 5', 'Data 6'],
      ['Data 1', 'Data 2', 'Data 3', 'Data 4', 'Data 5', 'Data 6'],
      ['Data 1', 'Data 2', 'Data 3', 'Data 4', 'Data 5', 'Data 6']
    ];
  
    // Loop through each row of the data and create table rows and cells
    data.forEach(function(rowData) {
      var row = document.createElement('tr');
      rowData.forEach(function(cellData) {
        var cell = document.createElement('td');
        cell.textContent = cellData;
        row.appendChild(cell);
      });
      tableBody.appendChild(row);
    });
  });
  