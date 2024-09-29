document.addEventListener('DOMContentLoaded', function() {
    const stateSelect = document.getElementById('state');
    const townSelect = document.getElementById('town');
    const houseTypeSelect = document.getElementById('house_type');

    // Get the states and house types from the backend when the page loads
    fetch('/states')
        .then(response => response.json())
        .then(data => {
            data.states.forEach(state => {
                const option = document.createElement('option');
                option.value = state;
                option.textContent = state;
                stateSelect.appendChild(option);
            });
        });

    fetch('/house-types')
        .then(response => response.json())
        .then(data => {
            data.house_types.forEach(type => {
                const option = document.createElement('option');
                option.value = type;
                option.textContent = type;
                houseTypeSelect.appendChild(option);
            });
        });

    // When the state changes, update the town dropdown
    stateSelect.addEventListener('change', function() {
        const selectedState = stateSelect.value;
        townSelect.innerHTML = '';  // Clear the existing options

        fetch(`/towns/${selectedState}`)
            .then(response => response.json())
            .then(data => {
                data.towns.forEach(town => {
                    const option = document.createElement('option');
                    option.value = town;
                    option.textContent = town;
                    townSelect.appendChild(option);
                });
            });
    });

    // Prevent negative numbers for bedrooms, bathrooms, toilets, and parking space
    const numericInputs = ['bedrooms', 'bathrooms', 'toilets', 'parking_space'];
    numericInputs.forEach(id => {
        document.getElementById(id).addEventListener('input', function() {
            if (this.value < 0) {
                this.value = 0;
            }
        });
    });

    // Handle the form submission
    const form = document.getElementById('prediction-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();  // Prevent default form submission

        const data = {
            bedrooms: document.getElementById('bedrooms').value,
            bathrooms: document.getElementById('bathrooms').value,
            toilets: document.getElementById('toilets').value,
            parking_space: document.getElementById('parking_space').value,
            house_type: houseTypeSelect.value,
            town: townSelect.value,
            state: stateSelect.value
        };

        // Send the form data to the backend
        fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').textContent = `Predicted Price: ₦${data.predicted_price}`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
