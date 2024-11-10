function deleteStudent(studentId, element) {
    if (confirm('Are you sure you want to delete this student?')) {
        fetch(`/delete/${studentId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token() }}'  // Include CSRF token if you're using CSRF protection
            }
        })
        .then(response => {
            if (response.ok) {
                const row = element.closest('tr');  // Find the closest <tr> (table row) to the clicked button
                row.parentNode.removeChild(row);  // Remove the row from the table
                updateSerialNumbers();            // Update serial numbers
            } else {
                response.json().then(data => alert('Failed to delete student: ' + (data.message || 'Unknown error')));
            }
        })
        .catch(error => alert('Error: ' + error));
    }
}

function updateSerialNumbers() {
    const rows = document.querySelectorAll('table tbody tr');
    rows.forEach((row, index) => {
        const serialNumberCell = row.querySelector('td:first-child');  // Assuming the serial number is in the first column
        if (serialNumberCell) {
            serialNumberCell.textContent = index + 1;  // Update the serial number to match the row index
        }
    });
}