document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const data = {
        email: email,
        password: password
    };

    fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        credentials: 'include'  // セッションを維持するためにクッキーを含める
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.token) {
            localStorage.setItem('token', data.token); // ログイン成功時にトークンを保存
            alert('ログインに成功しました。');
            window.location.href = 'dashboard.html'; // ダッシュボードにリダイレクト
        } else {
            throw new Error('Token not received');
        }
    })
    .catch(error => {
        console.error('ログインエラー:', error);
        alert('ログイン中にエラーが発生しました。');
    });
});

