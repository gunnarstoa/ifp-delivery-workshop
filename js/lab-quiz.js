// Today's date — replaces every .lab-today-date placeholder with YYYYMMDD
// (no separators, matches the model-naming convention) so the participant
// reads the literal value to type instead of substituting a placeholder.
(function () {
  var d = new Date();
  var today = d.getFullYear() +
              String(d.getMonth() + 1).padStart(2, '0') +
              String(d.getDate()).padStart(2, '0');
  document.querySelectorAll('.lab-today-date').forEach(function (el) {
    el.textContent = today;
  });
})();

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

// Check my work — simulated API validation. Click the button, see a short
// "checking" delay, then the success panel reveals. When we wire up the real
// Anaplan API later, the setTimeout becomes a fetch() to the workshop backend
// proxy that returns the live list of models from the participant's tenant.
(function () {
  function bindCheck(check) {
    var btn = check.querySelector('.lab-check-button');
    var results = check.querySelector('.lab-check-results');
    if (!btn || !results) return;
    btn.addEventListener('click', function () {
      btn.disabled = true;
      btn.innerHTML = '<span class="lab-check-spinner" aria-hidden="true"></span>Checking with Anaplan…';
      setTimeout(function () {
        results.hidden = false;
        btn.style.display = 'none';
      }, 1200);
    });
  }
  document.querySelectorAll('.lab-check').forEach(bindCheck);
})();

