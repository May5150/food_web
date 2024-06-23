fetch('http://127.0.0.1:5000/logout', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    }
})
.then(response => {
    if (!response.ok) {
        throw new Error('ログアウトに失敗しました。');
    }
    return response.json();
})
.then(data => {
    if (data.message === 'ログアウトに成功しました。') {
        window.location.href = 'login.html';
    } else {
        alert('ログアウトに失敗しました。');
    }
})
.catch(error => {
    console.error('ログアウト中にエラーが発生しました:', error);
    alert('ログアウト中にエラーが発生しました。');
});

