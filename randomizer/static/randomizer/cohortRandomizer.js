document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded and parsed');
    setupEventListeners();  // Set up event listeners for buttons
    loadNames();  // Load names from the server
});

/**
 * Sets up event listeners for the buttons on the page.
 */
function setupEventListeners() {
    const buttons = [
        { id: 'addNameBtn', handler: addName, log: 'Add button clicked' }, 
        { id: 'deleteSelectedBtn', handler: deleteSelectedNames, log: 'Delete Selected button clicked' },
        { id: 'clearAllBtn', handler: clearNames, log: 'Clear All button clicked' }
    ];

    buttons.forEach(btn => {
        const element = document.getElementById(btn.id);
        if (element) {
            element.addEventListener('click', function (event) {
                event.preventDefault();  // Prevent default form submission
                console.log(btn.log);
                btn.handler();  // Call the respective handler function
            });
        } else {
            console.error(`${btn.id} not found`);
        }
    });
}

/**
 * Adds a new name to the list by sending a POST request to the server.
 */
function addName() {
    console.log('Adding name...');
    let nameInput = document.getElementById('nameInput').value.trim();
    if (nameInput === '') {
        alert('Please enter a name.');
        return;
    }

    fetch('/randomizer/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
        },
        body: new URLSearchParams({ 'name': nameInput })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            updateNameList(data.names);
        } else {
            alert('Error adding name.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error adding name');
    });

    document.getElementById('nameInput').value = '';  // Clear input field
}

/**
 * Deletes selected names by sending their IDs to the server.
 */
function deleteSelectedNames() {
    const selectedItems = document.querySelectorAll('.name-item.selected');
    const selectedIds = Array.from(selectedItems).map(item => item.dataset.id);

    if (selectedIds.length === 0) {
        alert('Please select at least one name to delete.');
        return;
    }

    fetch('/randomizer/delete_selected/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
        },
        body: `ids=${selectedIds.join(',')}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateNameList(data.names);  // Update the list after successful delete
        } else {
            alert('Error deleting names');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error deleting names');
    });
}

/**
 * Clears all names by sending a request to the server.
 */
function clearNames() {
    if (!confirm('Are you sure you want to clear all names?')) {
        return;
    }

    fetch('/randomizer/clear/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateNameList([]);  // Clear the name list after successful clear
        } else {
            alert('Error clearing names');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error clearing names');
    });
}

/**
 * Updates the name list in the DOM with the provided names.
 * @param {Array} names - Array of name objects to display.
 */
function updateNameList(names) {
    let nameList = document.getElementById('nameList');
    nameList.innerHTML = '';  // Clear existing names
    
    console.log('Updating name list with:', names);  // Debug log
    
    if (!names || names.length === 0) {
        nameList.innerHTML = '<p style="color: #fff;">No names added yet.</p>';
        return;
    }
    
    names.forEach(nameObj => {
        let nameItem = document.createElement('div');
        nameItem.className = 'name-item';
        nameItem.textContent = nameObj.name;
        nameItem.dataset.id = nameObj.id;
        nameItem.onclick = () => nameItem.classList.toggle('selected');
        nameList.appendChild(nameItem);
    });
}

/**
 * Retrieves the CSRF token from the DOM.
 * @returns {string} The CSRF token.
 */
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

/**
 * Loads names from the server and updates the name list.
 */
function loadNames() {
    fetch('/randomizer/names/')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Received names:', data.names);  // Debug log
        updateNameList(data.names);
    })
    .catch(error => {
        console.error('Error loading names:', error);
    });
}

/**
 * Sets the randomize mode and updates the UI accordingly.
 * @param {string} mode - The mode to set ('mode1' for Pair, 'mode2' for Groups).
 */
function setRandomizeMode(mode) {
    const mode1Label = document.getElementById('mode1Label');
    const mode2Label = document.getElementById('mode2Label');
    const groupSizeContainer = document.getElementById('groupSizeContainer');

    if (mode === 'mode1') {
        mode1Label.classList.add('active');
        mode2Label.classList.remove('active');
        groupSizeContainer.style.display = 'none';
    } else if (mode === 'mode2') {
        mode1Label.classList.remove('active');
        mode2Label.classList.add('active');
        groupSizeContainer.style.display = 'block';
    }
}
/**
 * Randomizes the cohort based on the selected mode and group size.
 */
function randomizeCohort() {
    const mode1Label = document.getElementById('mode1Label');
    const mode2Label = document.getElementById('mode2Label');
    const groupSizeInput = document.getElementById('groupSizeInput');
    const selectedItems = document.querySelectorAll('.name-item.selected');
    const names = Array.from(selectedItems).map(item => item.textContent);

    if (names.length === 0) {
        alert('Please select some names first.');
        return;
    }

    let result = [];
    if (mode1Label.classList.contains('active')) {
        // Pair mode
        while (names.length > 1) {
            const pair = [names.pop(), names.pop()];
            result.push(pair);
        }
        if (names.length === 1) { // If there's one name left
            result.push([names.pop()]);
        }
    } else if (mode2Label.classList.contains('active')) {
        // Group mode
        const groupSize = parseInt(groupSizeInput.value, 10);
        if (isNaN(groupSize) || groupSize <= 0) {
            alert('Please enter a valid group size.');
            return;
        }
        while (names.length > 0) {
            const group = names.splice(0, groupSize);
            result.push(group);
        }
    }

    displayResult(result);
}

/**
 * Displays the randomization result in the result div.
 * @param {Array} result - The randomization result.
 */
function displayResult(result) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';
    result.forEach(group => {  // Loop through each group
        const groupDiv = document.createElement('div');
        groupDiv.className = 'group';
        
        if (group.length === 1) { // If there's only one person in the group
            groupDiv.textContent = `${group[0]} solo`; // `$` is used for string interpolation, interpolation is when 
            // you insert a variable into a string. The variable is surrounded by curly braces ${variable} and is
            // preceded by a dollar sign $.
        } else {
            groupDiv.textContent = group.join(' with ');
        }
        
        resultDiv.appendChild(groupDiv);
    });
}
