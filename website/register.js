// フォームの送信時の処理
const registerForm = document.getElementById('registerForm');

registerForm.addEventListener('submit', function(event) {
  event.preventDefault();

  // 入力値を取得
  const email = document.getElementById('email').value;
  const username = document.getElementById('newUsername').value;
  const password = document.getElementById('newPassword').value;

  // サーバーに送信するデータの準備
  const data = {
    email: email,
    username: username,
    password: password
  };

  // サーバーへのHTTPリクエストの実装（例としてfetchを使用）
  fetch('http://127.0.0.1:5000/api/register', { // サーバーのURLを適宜変更
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json().then(data => ({status: response.status, body: data})))
  .then(({status, body}) => {
    if (status !== 200) {
      throw new Error(body.message || 'Unknown error');
    }
    console.log('アカウントが正常に作成されました。', body);
    window.location.href = 'login.html'; // 例：登録後はログインページにリダイレクト
  })
  .catch(error => {
    console.error('アカウント作成中にエラーが発生しました: ', error.message);
    alert('アカウント作成中にエラーが発生しました: ' + error.message);
  });
});



