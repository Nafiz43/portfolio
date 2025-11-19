(function() {
  function updateButtonText(button, isDark) {
    if (!button) return;
    button.innerHTML = (isDark ? '<span aria-hidden="true">☀️</span> Light Mode' : '<span aria-hidden="true">🌙</span> Dark Mode');
    button.setAttribute('aria-pressed', isDark ? 'true' : 'false');
  }

  document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('theme-toggle');
    if (!toggleButton) {
      return;
    }

    const savedTheme = localStorage.getItem('preferred-theme');
    if (savedTheme === 'dark') {
      document.body.classList.add('dark-mode');
    }

    updateButtonText(toggleButton, document.body.classList.contains('dark-mode'));

    toggleButton.addEventListener('click', function() {
      document.body.classList.toggle('dark-mode');
      const isDark = document.body.classList.contains('dark-mode');
      localStorage.setItem('preferred-theme', isDark ? 'dark' : 'light');
      updateButtonText(toggleButton, isDark);
    });
  });
})();
