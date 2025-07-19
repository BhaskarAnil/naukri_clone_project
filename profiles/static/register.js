document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".register-form");
  const btn = document.querySelector(".register-submit");
  if (form && btn) {
    form.addEventListener("submit", function () {
      btn.disabled = true;
      btn.textContent = "Registering...";
    });

    if (document.querySelector(".register-error")) {
      btn.disabled = false;
      btn.textContent = "Register now";
    }
  }
});
