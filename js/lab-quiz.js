// Lab quiz handler — Trailhead-style inline mini-quizzes.
// Each .lab-quiz block carries data-correct (the right answer letter); two
// pre-baked feedback elements (.lab-quiz-feedback-correct / -wrong) hold the
// explanation copy. On submit we lock the inputs, mark the correct option
// green, mark the user's wrong choice red, and reveal the matching feedback.
(function () {
  function bindQuiz(quiz) {
    var btn = quiz.querySelector('.lab-quiz-check');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var correct = (quiz.getAttribute('data-correct') || '').trim();
      var selected = quiz.querySelector('input[type=radio]:checked');
      if (!selected) {
        btn.classList.add('lab-quiz-shake');
        setTimeout(function () { btn.classList.remove('lab-quiz-shake'); }, 350);
        return;
      }
      var opts = quiz.querySelectorAll('.lab-quiz-option');
      opts.forEach(function (opt) {
        var input = opt.querySelector('input[type=radio]');
        input.disabled = true;
        opt.classList.add('lab-locked');
        if (input.value === correct) {
          opt.classList.add('lab-quiz-correct');
        } else if (input === selected) {
          opt.classList.add('lab-quiz-wrong');
        }
      });
      var isCorrect = selected.value === correct;
      var feedback = quiz.querySelector(isCorrect ? '.lab-quiz-feedback-correct' : '.lab-quiz-feedback-wrong');
      if (feedback) feedback.classList.add('show');
      btn.disabled = true;
      btn.textContent = isCorrect ? 'Correct' : 'Checked';
    });
  }
  document.querySelectorAll('.lab-quiz').forEach(bindQuiz);
})();
