// Get DOM elements
const addItemButton = document.getElementById('add-item');
const addModal = document.getElementById('add-modal');
const closeModalButtons = document.querySelectorAll('.close-modal');
const cancelButton = document.getElementById('cancel-button');
const submitButton = document.getElementById('submit-button');
const tableBody = document.querySelector('tbody');
const modalTitle = document.querySelector('.modal-header p');

// Variables for edit mode
let isEditMode = false;
let currentEditRow = null;

// Function to show add modal
function showAddModal() {
    addModal.style.display = 'flex';
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
    modalTitle.textContent = 'Add Product';
    submitButton.textContent = 'Add Product';
    isEditMode = false;
    currentEditRow = null;
}

// Function to hide add modal
function hideAddModal() {
    addModal.style.display = 'none';
    document.body.style.overflow = 'auto'; // Restore background scrolling
    // Clear form inputs
    document.querySelectorAll('.modal-input-container input, .modal-input-container select').forEach(input => {
        input.value = '';
    });
}

// Function to show edit modal
function showEditModal(productId) {
    const editModal = document.getElementById('formContainer-' + productId);
    if (editModal) {
        editModal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

// Function to hide edit modal
function hideEditModal(productId) {
    const editModal = document.getElementById('formContainer-' + productId);
    if (editModal) {
        editModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Function to get current date in YYYY-MM-DD format
function getCurrentDate() {
    const now = new Date();
    return now.toISOString().split('T')[0];
}

// Function to format price to PHP format
function formatPrice(price) {
    return '₱' + parseFloat(price).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

// Function to add new row to table
function addTableRow(formData) {
    const rowCount = tableBody.children.length + 1;
    const currentDate = getCurrentDate();

    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td>${rowCount}</td>
        <td>${formData.name}</td>
        <td>${formatPrice(formData.price)}</td>
        <td>${formData.stock}</td>
        <td>${formData.category}</td>
        <td>${formData.manufacturer}</td>
        <td>${currentDate}</td>
        <td>${currentDate}</td>
        <td class="action-buttons">
            <button class="edit-btn" onclick="editRow(this)">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                </svg>
            </button>
            <button class="delete-btn" onclick="deleteRow(this)">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                </svg>
            </button>
        </td>
    `;

    tableBody.appendChild(newRow);
}

// Function to edit row
function editRow(button) {
    const row = button.closest('tr');
    const cells = row.cells;

    // Set edit mode
    isEditMode = true;
    currentEditRow = row;

    // Update modal title and button
    modalTitle.textContent = 'Edit Product';
    submitButton.textContent = 'Save Changes';

    // Fill form with current values
    document.querySelector('input[placeholder="Enter product name"]').value = cells[1].textContent;
    document.querySelector('input[placeholder="Enter price"]').value = cells[2].textContent.replace('₱', '').replace(/,/g, '');
    document.querySelector('input[placeholder="Enter stock quantity"]').value = cells[3].textContent;
    document.querySelector('select').value = cells[4].textContent.toLowerCase().replace(/\s+/g, '');
    document.querySelector('input[placeholder="Enter manufacturer name"]').value = cells[5].textContent;

    // Show modal
    showEditModal(cells[0].textContent);
}

// Function to delete row
function deleteRow(button) {
    if (confirm('Are you sure you want to delete this item?')) {
        const row = button.closest('tr');
        row.remove();
        // Update row numbers
        updateRowNumbers();
    }
}

// Function to update row numbers after deletion
function updateRowNumbers() {
    const rows = tableBody.querySelectorAll('tr');
    rows.forEach((row, index) => {
        row.cells[0].textContent = index + 1;
    });
}

// Event Listeners
addItemButton.addEventListener('click', showAddModal);

// Close modal when clicking outside
addModal.addEventListener('click', (e) => {
    if (e.target === addModal) {
        hideAddModal();
    }
});

// Add event listeners for all close buttons
closeModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = button.closest('.modal-background');
        if (modal.id === 'add-modal') {
            hideAddModal();
        } else {
            const productId = modal.id.split('-')[1];
            hideEditModal(productId);
        }
    });
});

// Add event listeners for all edit modals
document.querySelectorAll('.modal-background').forEach(modal => {
    if (modal.id !== 'add-modal') {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                const productId = modal.id.split('-')[1];
                hideEditModal(productId);
            }
        });
    }
});

// Cancel button event listener
if (cancelButton) {
    cancelButton.addEventListener('click', hideAddModal);
}

// Form validation
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
        } else {
            input.classList.remove('error');
        }
    });

    return isValid;
}

// Add form submission handler
const addForm = document.querySelector('#add-modal form');
if (addForm) {
    addForm.addEventListener('submit', (e) => {
        if (!validateForm(addForm)) {
            e.preventDefault();
            alert('Please fill in all required fields');
        }
    });
}

// Edit form submission handler
document.querySelectorAll('.formContainer-form').forEach(form => {
    form.addEventListener('submit', (e) => {
        if (!validateForm(form)) {
            e.preventDefault();
            alert('Please fill in all required fields');
        }
    });
});

