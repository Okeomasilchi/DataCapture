        fetch('header.html')
            .then(response => response.text())
            .then(data => document.body.insertAdjacentHTML('afterbegin', data))
            .catch(error => console.error('Error fetching header:', error));
    function populateDropdown() {
        var optiontype = ['A, B, C, ...', 'a, b, c, ...', '1, 2, 3, ...', 'I, II, III, ...', 'i, ii, iii, ...', 'α, β, γ, ...', 'Α, Β, Γ, ...', 'a, b, c, ...', 'A, B, C, ...', '1, 2, 3, ...', 'I, II, III, ...', 'i, ii, iii, ...', 'α, β, γ, ...', 'Α, Β, Γ, ...', 'a, b, c, ...', 'A, B, C, ...', '1, 2, 3, ...', 'I, II, III, ...', 'i, ii, iii, ...', 'α, β, γ, ...', 'Α, Β, Γ, ...', 'a, b, c, ...', 'A, B, C, ...', '1, 2, 3, ...', 'I, II, III, ...', 'i, ii, iii, ...', 'α, β, γ, ...', 'Α, Β, Γ, ...', 'a, b, c, ...', 'A, B, C, ...', '1, 2, 3, ...', 'I, II, III, ...', 'i, ii, iii, ...', 'α, β, γ, ...', 'Α, Β, Γ, ...', 'a, b, c, ...', 'A, B, C, ...', '1, 2, 3, ...', 'I, II, III, ...', 'i, ii, iii, ...', 'α, β, γ, ...', 'Α, Β, Γ, ...', 'a, b, c, ...', 'A, B, C, ...', '1, 2, 3, ...', 'I, II, III, ...', 'i, ii, iii, ...', 'α, β, γ, ...', 'Α, Β, Γ, ...', 'a, b, c, ...', 'A, B, C, ...', '1, 2, 3, ...', 'i, ii, iii, ...', '...'];
        var dropdown = document.getElementById('dropdown');
        for (var i = 0; i < optiontype.length; i++) {
            var option = document.createElement('option');
            option.text = optiontype[i];
            dropdown.appendChild(option);
        }
        //fetch('index.optiontype.html')
         //   .then(response => response.text())
         //   .then(data => document.getElementById('dropdown').insertAdjacentHTML('afterbegin', data))
         //   .catch(error => console.error('Error fetching dropdown:', error));
    }