/* Main JavaScript for portal functionality */

// CSRF token helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Modal functionality
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

// Close modal when clicking outside
document.addEventListener('click', function (event) {
    const modals = document.querySelectorAll('.modal.active');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.classList.remove('active');
        }
    });
});

// Create department
function createDepartment() {
    const name = document.getElementById('departmentName').value.trim();
    const description = document.getElementById('departmentDescription').value.trim();

    if (!name) {
        alert('Please enter a department name');
        return;
    }

    fetch('/create-department/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ name, description })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                hideModal('createDepartmentModal');
                alert('Department created successfully!');
                location.reload();
            } else {
                alert('Error: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to create department');
        });
}

// Create tab
function createTab(departmentId) {
    const name = document.getElementById('tabName').value.trim();
    const description = document.getElementById('tabDescription').value.trim();

    if (!name) {
        alert('Please enter a tab name');
        return;
    }

    fetch(`/create-tab/${departmentId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ name, description })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                hideModal('createTabModal');
                alert('Tab created successfully!');
                location.reload();
            } else {
                alert('Error: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to create tab');
        });
}

// Rename tab
function renameTab(tabId) {
    const newName = prompt('Enter new tab name:');
    if (!newName || !newName.trim()) {
        return;
    }

    fetch(`/rename-tab/${tabId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ name: newName.trim() })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Tab renamed successfully!');
                location.reload();
            } else {
                alert('Error: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to rename tab');
        });
}

// Delete tab
function deleteTab(tabId, tabName) {
    if (!confirm(`Are you sure you want to delete the tab "${tabName}"?`)) {
        return;
    }

    fetch(`/delete-tab/${tabId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Tab deleted successfully!');
                location.reload();
            } else {
                alert('Error: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to delete tab');
        });
}

// Delete record
function deleteRecord(recordId) {
    if (!confirm('Are you sure you want to delete this record?')) {
        return;
    }

    fetch(`/record/${recordId}/delete/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Record deleted successfully!');
                location.reload();
            } else {
                alert('Error: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to delete record');
        });
}

// Validate JSON input
function validateJSON(textareaId) {
    const textarea = document.getElementById(textareaId);
    if (!textarea) return;

    textarea.addEventListener('blur', function () {
        try {
            JSON.parse(this.value);
            this.style.borderColor = '#28a745';
        } catch (e) {
            this.style.borderColor = '#dc3545';
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
    // Validate JSON on data input fields
    const dataFields = document.querySelectorAll('textarea[name="data"]');
    dataFields.forEach(field => {
        field.addEventListener('blur', function () {
            try {
                JSON.parse(this.value);
                this.style.borderColor = '#28a745';
            } catch (e) {
                this.style.borderColor = '#dc3545';
            }
        });
    });
});
