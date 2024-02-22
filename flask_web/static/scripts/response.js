function updateProgress() {
    var questions = document.querySelectorAll('.questions .question');
    var answeredQuestions = Array.from(questions).filter(question => {
        return question.querySelector('input[type="checkbox"]:checked') !== null;
    });
    var progress = document.getElementById('progress');
    var percentage = (answeredQuestions.length / questions.length) * 100;
    progress.style.width = percentage + '%';
}
