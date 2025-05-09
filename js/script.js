document.addEventListener('DOMContentLoaded', function () {
  const addBtn = document.getElementById('add-button');
  const tbody = document.getElementById('table-tbody');
  const modal = document.getElementById('modal-background');
  const modalContent = document.getElementById('modal-add-container');
  const closeBtn = document.querySelector('.close');
  const modalCancel = document.getElementById('modal-cancel');
  const modalAdd = document.getElementById('modal-add');

  addBtn.onclick = function () {
    modal.style.display = 'block';
  };

  closeBtn.onclick = function () {
    modal.style.display = 'none';
  };

  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = 'none';
    }
  };

  modalCancel.onclick = () => {
    modal.style.display = 'none';
  };

  modalAdd.addEventListener('click', addContent);

  function addContent() {
    const productName = document.getElementById('product-name').value;
    const productManufacturer = document.getElementById('product-manufacturer').value;
    const productCategory = document.getElementById('product-category').value;
    const productStock = document.getElementById('product-stock').value;
    const productPrice = document.getElementById('product-price').value;

    if (!productName || !productPrice) {
      alert('Product name and price are required!');
      return;
    }

    const dateCreated = new Date().toLocaleDateString();
    const newRow = document.createElement('tr');
    const rowNumber = tbody.rows.length + 1;

    newRow.innerHTML = `
      <td>${rowNumber}</td>
      <td>${productName}</td>
      <td>${productPrice}</td>
      <td>${productStock}</td>
      <td>${productCategory}</td>
      <td>${productManufacturer}</td>
      <td>${dateCreated}</td>
      <td>${dateCreated}</td>
      <td>
        <button class="edit-button">Edit</button>
        <button class="delete-button">Delete</button>
      </td>
    `;

    tbody.appendChild(newRow);
    clearFormInputs();
    modal.style.display = 'none';

    addEditDeleteListeners(newRow);
    updateRowNumbers();
  }

  function clearFormInputs() {
    document.getElementById('product-name').value = '';
    document.getElementById('product-manufacturer').value = '';
    document.getElementById('product-category').value = '';
    document.getElementById('product-stock').value = '';
    document.getElementById('product-price').value = '';
  }

  function addEditDeleteListeners(row) {
    row.querySelector('.delete-button').addEventListener('click', function () {
      if (confirm('Are you sure you want to delete this table?')) {
        row.remove();
        updateRowNumbers();
      }
    });

    row.querySelector('.edit-button').addEventListener('click', function () {
      const cells = row.cells;
      const currentData = {
        name: cells[1].textContent,
        price: cells[2].textContent,
        stock: cells[3].textContent,
        category: cells[4].textContent,
        manufacturer: cells[5].textContent,
      };

      document.getElementById('product-name').value = currentData.name;
      document.getElementById('product-price').value = currentData.price;
      document.getElementById('product-stock').value = currentData.stock;
      document.getElementById('product-category').value = currentData.category;
      document.getElementById('product-manufacturer').value = currentData.manufacturer;

      document.getElementById('modal-header').textContent = 'Edit Product';
      modalAdd.textContent = 'Update';
      modal.style.display = 'block';

      modalAdd.dataset.editingRow = row.rowIndex;

      modalAdd.onclick = function () {
        updateContent(row);
      };
    });
  }

  function updateContent(row) {
    const productName = document.getElementById('product-name').value;
    const productManufacturer = document.getElementById('product-manufacturer').value;
    const productCategory = document.getElementById('product-category').value;
    const productStock = document.getElementById('product-stock').value;
    const productPrice = document.getElementById('product-price').value;
    document.getElementById('modal-header').textContent = 'Add Product';
    modalAdd.textContent = 'Add';

    if (!productName || !productPrice) {
      alert('Product name and price are required!');
      return;
    }

    // Remove the old row (the one being edited)
    row.remove();

    // Add the new row with updated data
    const newRow = document.createElement('tr');
    const rowNumber = tbody.rows.length + 1;  // new row number
    const dateCreated = new Date().toLocaleDateString(); // dateCreated can be updated if needed

    newRow.innerHTML = `
      <td>${rowNumber}</td>
      <td>${productName}</td>
      <td>${productPrice}</td>
      <td>${productStock}</td>
      <td>${productCategory}</td>
      <td>${productManufacturer}</td>
      <td>${dateCreated}</td>
      <td>${dateCreated}</td>
      <td>
        <button class="edit-button">Edit</button>
        <button class="delete-button">Delete</button>
      </td>
    `;

    tbody.appendChild(newRow);
    clearFormInputs();
    delete modalAdd.dataset.editingRow;
    modalAdd.onclick = addContent;

    modal.style.display = 'none';

    addEditDeleteListeners(newRow);
    updateRowNumbers();
  }

  function updateRowNumbers() {
    const rows = tbody.querySelectorAll('tr');
    rows.forEach((row, index) => {
      row.cells[0].textContent = index + 1;
    });
  }
});
