changes = {"first_name": "John", "last_name": "Doe"}
fetch('http://0.0.0.0:5000/api/v1/users/05c712a8-84d0-42ce-a3d7-cc0797bfa4f8', {
    method: 'PUT',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(changes)
})
.then(response => {
    // Check if response is successful
    if (!response.ok) {
        throw new Error('API error: ' + response.status);
    }

    // Access status code
    console.log('Status code:', response.status);

    // Access other headers
    console.log('Content-Type header:', response.headers.get('Content-Type'));
    
    // Parse JSON response
    return response.json();
})
.then(data => {
    // Handle successful response
    $('div input[id="first_name"]').val(data.first_name);
    $('div input[id="last_name"]').val(data.last_name);
    $('div input[id="email"]').val(data.email);
    $('#popupContainer').fadeOut(150);
})
.catch(error => {
    console.error('API error:', error);
});
