document.addEventListener('DOMContentLoaded', (event) => {
    const table = document.getElementById('assetTable');
    const addAssetButton = document.getElementById('addAssetButton');

    addAssetButton.addEventListener('click', () => {
        const newRow = table.insertRow();
        const tickerCell = newRow.insertCell(0);
        const assetCell = newRow.insertCell(1);
        const weightCell = newRow.insertCell(2);
        const deleteCell = newRow.insertCell(3);

        tickerCell.innerHTML = '<input type="text" class="form-control" placeholder="Ticker">';
        assetCell.innerHTML = '<input type="text" class="form-control" placeholder="Asset">';
        weightCell.innerHTML = '<input type="text" class="form-control" placeholder="Weight">';
        deleteCell.innerHTML = '<button class="btn btn-danger" onclick="deleteRow(this)">Delete</button>';
    });
});

function deleteRow(button) {
    const row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
}