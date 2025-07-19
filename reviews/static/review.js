document.addEventListener("DOMContentLoaded", function () {
  const editBtn = document.getElementById("edit-review-btn");
  const editForm = document.getElementById("edit-review-form");
  const review = document.getElementById("user-review-card");
  if (editBtn && editForm && review) {
    editBtn.addEventListener("click", function () {
      editForm.style.display = "block";
      review.style.display = "none";
    });
    editForm.addEventListener("submit", function (e) {
      window.location.reload();
    });
  }
  const repliesBtn = document.getElementById("replies-btn");
  const replies = document.getElementById("replies");

  repliesBtn.addEventListener("click", () => {
    if (replies.style.display == "none") {
      replies.style.display = "block";
      repliesBtn.textContent = "Close";
      console.log(1);
    } else {
      console.log(0);
      repliesBtn.textContent = " Reply";
      icon = document.createElement("i");
      icon.classList = "fa-solid fa-reply";
      repliesBtn.prepend(icon);
      replies.style.display = "none";
    }
  });
});
