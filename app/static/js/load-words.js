let currentWordId = null;

// Hàm gọi API lấy từ mới từ Flask
async function loadNewWord() {
    document.getElementById('user-input').value = '';
    document.getElementById('result').innerText = '';
    
    const response = await fetch('/api/get-quiz');
    const data = await response.json();
    
    currentWordId = data.id;
    document.getElementById('word-meaning').innerText = data.meaning;
    document.getElementById('word-scrambled').innerText = data.scrambled.toUpperCase();
}

// Hàm gửi câu trả lời lên Flask kiểm tra
async function checkAnswer() {
    const userAnswer = document.getElementById('user-input').value;
    
    const response = await fetch('/api/check-answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: currentWordId, answer: userAnswer })
    });
    
    const data = await response.json();
    const resultDiv = document.getElementById('result');
    
    if(data.is_correct) {
        resultDiv.style.color = "green";
        resultDiv.innerText = data.message;
    } else {
        resultDiv.style.color = "red";
        resultDiv.innerText = data.message;
    }
}

// Tự động tải từ đầu tiên khi mở web
window.onload = loadNewWord; 