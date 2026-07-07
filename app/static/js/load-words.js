let currentWord = null;
const API_BASE = '/api';

async function loadNewWord() {
    document.getElementById('user-input').value = '';
    document.getElementById('result').innerText = '';
    const response = await fetch(`${API_BASE}/words`);
    const words = await response.json();
    const randomIndex = Math.floor(Math.random() * words.length);
    currentWord = words[randomIndex];

    document.getElementById('word-meaning').innerText = currentWord.meaning;
    document.getElementById('word-scrambled').innerText = shuffleWord(currentWord.word).toUpperCase();
}

function shuffleWord(word) {
    const chars = word.split('');
    for (let i = chars.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [chars[i], chars[j]] = [chars[j], chars[i]];
    }
    return chars.join('');
}

function checkAnswer() {
    const userAnswer = document.getElementById('user-input').value.trim().toLowerCase();
    const resultDiv = document.getElementById('result');

    if (!currentWord) {
        resultDiv.style.color = 'red';
        resultDiv.innerText = 'Chưa có từ nào để kiểm tra. Vui lòng nhấn Từ mới.';
        return;
    }

    if (userAnswer === currentWord.word.toLowerCase()) {
        resultDiv.style.color = 'green';
        resultDiv.innerText = 'Chính xác! Bạn thật tuyệt vời!';
    } else {
        resultDiv.style.color = 'red';
        resultDiv.innerText = `Sai rồi. Đáp án đúng là: ${currentWord.word}`;
    }
}

window.onload = loadNewWord;
