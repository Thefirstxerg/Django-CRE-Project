// Wait for the DOM to be fully loaded before executing any code
document.addEventListener('DOMContentLoaded', initializeApp);

// Object to store DOM elements
const elements = {
    addBtn: null,
    deleteBtn: null,
    clearBtn: null,
    nameInput: null,
    nameList: null,
    darkModeSwitch: null // Add dark mode switch element
};

// Initialize the application
function initializeApp() {
    console.log('DOM fully loaded and parsed');
    
    // Initialize element references
    elements.addBtn = document.getElementById('addNameBtn');
    elements.deleteBtn = document.getElementById('deleteSelectedBtn');
    elements.clearBtn = document.getElementById('clearAllBtn');
    elements.nameInput = document.getElementById('nameInput');
    elements.nameList = document.getElementById('nameList');
    elements.darkModeSwitch = document.getElementById('darkModeSwitch'); // Add dark mode switch element

    // Set up event listeners
    setupEventListeners();
    
    // Load initial names from server
    loadNames();
}

// Set up all event listeners
function setupEventListeners() {
    // Add name button
    if (elements.addBtn) {
        elements.addBtn.addEventListener('click', (e) => {
            e.preventDefault();
            addName();
        });
    }

    // Delete selected button
    if (elements.deleteBtn) {
        elements.deleteBtn.addEventListener('click', (e) => {
            e.preventDefault();
            deleteSelectedNames();
        });
    }

    // Clear all button
    if (elements.clearBtn) {
        elements.clearBtn.addEventListener('click', (e) => {
            e.preventDefault();
            clearNames();
        });
    }

    // Dark mode switch
    if (elements.darkModeSwitch) {
        elements.darkModeSwitch.addEventListener('change', toggleDarkMode);
    }
}

// Add a new name to the list
function addName() {
    const nameInput = elements.nameInput.value.trim();
    
    if (nameInput === '') {
        alert('Please enter a name.');
        return;
    }

    // Send POST request to server
    sendRequest('/add/', { name: nameInput })
        .then(data => {
            if (data.success) {
                updateNameList(data.names);
                elements.nameInput.value = ''; // Clear input field
            } else {
                alert('Error adding name.');
            }
        });
}

// Delete selected names from the list
function deleteSelectedNames() {
    const selectedItems = document.querySelectorAll('.name-item.selected');
    const selectedIds = Array.from(selectedItems).map(item => item.dataset.id);

    if (selectedIds.length === 0) {
        alert('Please select at least one name to delete.');
        return;
    }

    sendRequest('/delete_selected/', { ids: selectedIds.join(',') })
        .then(data => {
            if (data.success) {
                updateNameList(data.names);
            } else {
                alert('Error deleting names');
            }
        });
}

// Clear all names from the list
function clearNames() {
    if (!confirm('Are you sure you want to clear all names?')) {
        return;
    }

    sendRequest('/clear/')
        .then(data => {
            if (data.success) {
                updateNameList([]);
            } else {
                alert('Error clearing names');
            }
        });
}

// Update the UI with the current list of names
function updateNameList(names) {
    elements.nameList.innerHTML = '';
    names.forEach(nameObj => {
        const nameItem = document.createElement('div');
        nameItem.className = 'name-item';
        nameItem.textContent = nameObj.name;
        nameItem.dataset.id = nameObj.id;
        nameItem.onclick = () => nameItem.classList.toggle('selected');
        elements.nameList.appendChild(nameItem);
    });
}

// Helper function to send requests to the server
async function sendRequest(url, data = null) {
    try {
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken()
            }
        };

        if (data) {
            options.body = new URLSearchParams(data);
        }

        const response = await fetch(url, options);
        return await response.json();
    } catch (error) {
        console.error('Request error:', error);
        throw error;
    }
}

// Get CSRF token from the page
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Load names from server
function loadNames() {
    fetch('/names/')
        .then(response => response.json())
        .then(data => updateNameList(data.names))
        .catch(error => console.error('Error loading names:', error));
}

// Toggle dark mode
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
}
