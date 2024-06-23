document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('foodForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const foodName = document.getElementById('foodName').value;
        const expiryDate = document.getElementById('expiryDate').value;

        fetch('http://127.0.0.1:5000/api/add_food', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ foodName: foodName, expiryDate: expiryDate })
        })
        .then(response => response.json())
        .then(data => {
            alert('食品が正常に登録されました。');
        })
        .catch(error => {
            console.error('Error occurred while adding food:', error);
            alert('食品の登録中にエラーが発生しました。');
        });
    });
});





