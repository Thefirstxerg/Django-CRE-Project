document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded and parsed');
    
    // Add event listeners for the buttons
    const addButton = document.getElementById('addNameBtn');
    const deleteButton = document.getElementById('deleteSelectedBtn');
    const clearButton = document.getElementById('clearAllBtn');

    // Check if elements exist before attaching event listeners
    if (addButton) {
        addButton.addEventListener('click', function () {
            console.log('Add button clicked');
            addName();
        });
    } else {
        console.error('Add button not found');
    }

    if (deleteButton) {
        deleteButton.addEventListener('click', function () {
            console.log('Delete Selected button clicked');
            deleteSelectedNames();
        });
    } else {
        console.error('Delete button not found');
    }

    if (clearButton) {
        clearButton.addEventListener('click', function () {
            console.log('Clear All button clicked');
            clearNames();
        });
    } else {
        console.error('Clear button not found');
    }

    loadNames();
});


function addName() {
    console.log('Adding name...');
    let nameInput = document.getElementById('nameInput').value.trim();
    if (nameInput === '') {
        alert('Please enter a name.');
        return;
    }

    fetch('/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
        },
        body: new URLSearchParams({ 'name': nameInput })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateNameList(data.names);
        } else {
            alert('Error adding name.');
        }
    });

    document.getElementById('nameInput').value = '';  // Clear input field
}

function deleteSelectedNames() {
    const selectedItems = document.querySelectorAll('.name-item.selected');
    const selectedIds = Array.from(selectedItems).map(item => item.dataset.id);

    if (selectedIds.length === 0) {
        alert('Please select at least one name to delete.');
        return;
    }

    fetch('/delete_selected/', {
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

function clearNames() {
    if (!confirm('Are you sure you want to clear all names?')) {
        return;
    }

    fetch('/clear/', {
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

function updateNameList(names) {
    let nameList = document.getElementById('nameList');
    nameList.innerHTML = '';  // Clear existing names
    names.forEach(nameObj => {
        let nameItem = document.createElement('div');
        nameItem.className = 'name-item';
        nameItem.textContent = nameObj.name;
        nameItem.dataset.id = nameObj.id; // Assign database ID
        nameItem.onclick = () => nameItem.classList.toggle('selected');  // Toggle selected

        nameList.appendChild(nameItem);
    });
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function loadNames() {
    fetch('/names/')
    .then(response => response.json())
    .then(data => {
        updateNameList(data.names);
    });
}
