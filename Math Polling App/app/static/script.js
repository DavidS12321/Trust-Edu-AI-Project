const form = document.getElementById('poll-form');
const resultDiv = document.getElementById('results');

const buttons = document.querySelectorAll('.option');
buttons.forEach(button => {
    button.addEventListener('click', function() {

        const selectedAnswer = this.getAttribute('data-answer');
        document.getElementById('selected-answer').value = selectedAnswer;

        buttons.forEach(btn => btn.disabled = true);

        // immediate feedback 
        const correctAnswer = document.querySelector('input[name="correct_answer"]').value;
        const feedback = document.getElementById('feedback');
        if (selectedAnswer === correctAnswer) {
            feedback.textContent = 'Correct! Great job!';
            feedback.style.color = 'green';
        } else {
            feedback.textContent = 'Incorrect.';
            feedback.style.color = 'red';
        }

        form.submit();
    });
});


form.addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(form);
    
    const response = await fetch('/submit', {
        method: 'POST',
        body: formData
    });
    
    const result = await response.json();
    
    if (result.correct) {
        resultDiv.innerText = "Correct!";
    } else {
        resultDiv.innerText = "Try again!";
    }

});

document.addEventListener('DOMContentLoaded', function() {
    const feedback = document.getElementById('feedback');
    feedback.textContent = '';
});