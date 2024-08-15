document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const autocompleteResults = document.getElementById('autocomplete-results');

    searchInput.addEventListener('input', function() {
        const query = searchInput.value;

        if (query.length < 2) {
            autocompleteResults.innerHTML = '';
            return;
        }

        fetch(`/api/autocomplete?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                autocompleteResults.innerHTML = '';
                data.forEach(item => {
                    const resultDiv = document.createElement('div');
                    resultDiv.className = 'autocomplete-result';
                    resultDiv.textContent = item.title;
                    resultDiv.addEventListener('click', () => {
                        searchInput.value = item.title;
                        autocompleteResults.innerHTML = '';
                        document.getElementById('searchForm').submit();
                    });
                    autocompleteResults.appendChild(resultDiv);
                });
            })
            .catch(error => console.error('Error fetching autocomplete results:', error));
    });

    document.addEventListener('click', (e) => {
        if (!autocompleteResults.contains(e.target) && e.target !== searchInput) {
            autocompleteResults.innerHTML = '';
        }
    });

    // Handle Cast Modal
    $('#castModal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget); // Button that triggered the modal
        const castId = button.data('id'); // Extract info from data-* attributes

        fetch(`/api/cast/${castId}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('castName').textContent = data.name;
                document.getElementById('castRole').textContent = data.role;
                document.getElementById('castBday').textContent = data.bday;
                document.getElementById('castPlace').textContent = data.place;
                document.getElementById('castBio').textContent = data.bio;
            })
            .catch(error => console.error('Error fetching cast details:', error));
    });
});
