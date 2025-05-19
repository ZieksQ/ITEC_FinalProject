// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
  //----------------------variables---------------------//
  const editProfile = document.getElementById('edit-profile');
  const modalEditContainer = document.getElementById('modal-edit-container');
  const cancelButton = document.getElementById('cancel-edit-button');
  const closeButton = document.querySelector('.modal-header svg');
  const submitButton = document.getElementById('submit-edit-button');

  //variables of the input function

  // //userEmail
  // const editEmailInput = document.getElementById('edit-email')
  // const userEmaildisplay = document.getElementById('user-email-display');

  // //username
  // const editUsernameInput = document.getElementById('edit-username');
  // const usernameDisplay = document.getElementById('username-display');

  // //firstname
  // const editfirstNameInput = document.getElementById('edit-firstname');
  // const firstNameDisplay = document.getElementById('firstname-display');

  // //lastname
  // const editlastnameInput = document.getElementById('edit-lastname');
  // const lastnameDisplay = document.getElementById('lastname-display');

  // //password
  // const editPasswordInput = document.getElementById('edit-password');
  // const passwordDisplay = document.getElementById('password-display');

  //user Role
  const userRoleDisplay = document.getElementById('user-role');
  const roleForm = document.querySelector('.role-form');

  function updateRole(role) {
    userRoleDisplay.textContent = role.charAt(0).toUpperCase() + role.slice(1);
  }

  // Add event listeners to all radio buttons
  const roleRadios = document.querySelectorAll('input[name="role"]');
  roleRadios.forEach(radio => {
    radio.addEventListener('change', (e) => {
      if (e.target.checked) {
        updateRole(e.target.value);
      }
    });
  });

  //-------------------------functions----------------------------//
  function showEditModal() {
    // Set the current name in the input field when opening the modal

    // editEmailInput.value = userEmaildisplay.textContent;
    // editUsernameInput.value = usernameDisplay.textContent;
    // editPasswordInput.value = passwordDisplay.textContent;
    // editfirstNameInput.value = firstNameDisplay.textContent;
    // editlastnameInput.value = lastnameDisplay.textContent;

    modalEditContainer.style.display = 'flex';
  }

  function hideEditModal() {
    modalEditContainer.style.display = 'none';
  }

  // Event listeners
  editProfile.addEventListener('click', showEditModal);
  cancelButton.addEventListener('click', hideEditModal);
  closeButton.addEventListener('click', hideEditModal);

  // Close modal when clicking outside
  modalEditContainer.addEventListener('click', (e) => {
    if (e.target === modalEditContainer) {
      hideEditModal();
    }
  });

  // Handle form submission
  submitButton.addEventListener('click', function () {
    // Update the displayed name with the new value

    // const newEmail = editEmailInput.value.trim();
    // if (newEmail) {
    //   userEmaildisplay.textContent = newEmail;
    // }

    // const newUsername = editUsernameInput.value.trim();
    // if (newUsername) {
    //   usernameDisplay.textContent = newUsername;
    // }

    // const newPassword = editPasswordInput.value.trim();
    // if (newPassword) {
    //   passwordDisplay.textContent = newPassword;
    // }

    // const newfirstname = editfirstNameInput.value.trim();
    // if (newfirstname) {
    //   firstNameDisplay.textContent = newfirstname;
    // }

    // const newlatname = editlastnameInput.value.trim();
    // if (newlatname) {
    //   lastnameDisplay.textContent = newlatname;
    // }
    hideEditModal();
  });
});
