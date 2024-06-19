function submitAnswer(questionId, choice) {
    fetch('/check_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question_id: questionId, answer: choice })
    })
    .then(response => response.json())
    .then(data => {
        alert('Your answer is ' + (data.correct ? 'correct!' : 'incorrect.'));
    })
    .catch(error => console.error('Error:', error));
}
