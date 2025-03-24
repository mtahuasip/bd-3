document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".tab-link").forEach((tab) => {
    tab.addEventListener("click", function () {
      document.querySelectorAll(".tab-link").forEach((el) => {
        el.classList.remove(
          "is-active",
          "has-background-primary",
          "has-text-white"
        );
      });

      this.classList.add(
        "is-active",
        "has-background-primary",
        "has-text-white"
      );

      document.querySelectorAll(".tab-content").forEach((section) => {
        section.classList.add("is-hidden");
      });

      const targetSection = document.getElementById(this.dataset.target);
      if (targetSection) {
        targetSection.classList.remove("is-hidden");
      }
    });
  });

  const activeTab = document.querySelector(".tab-link.is-active");
  if (activeTab) {
    activeTab.classList.add("has-background-primary", "has-text-white");
    document
      .getElementById(activeTab.dataset.target)
      .classList.remove("is-hidden");
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const burger = document.querySelector(".navbar-burger");
  const menu = document.querySelector("#navbarMenu");

  burger.addEventListener("click", function () {
    menu.classList.toggle("is-active");
    burger.classList.toggle("is-active");
  });
});

function showEditForm(id, title, content, username) {
  document.getElementById("edit-title").value = title;
  document.getElementById("edit-content").value = content;
  document.getElementById("edit-username").value = username;
  document.getElementById("edit-form").action = `/edit/${id}`;
  document.getElementById("edit-modal").classList.add("is-active");
}

function closeEditForm() {
  document.getElementById("edit-modal").classList.remove("is-active");
}

function showCommentForm(postId) {
  document.getElementById("commentPostId").value = postId;
  document.getElementById("commentModal").classList.add("is-active");
}

function closeCommentModal() {
  document.getElementById("commentModal").classList.remove("is-active");
}

function showEditCommentForm(postId, commentId, username, commentText) {
  document.getElementById("editCommentPostId").value = postId;
  document.getElementById("editCommentId").value = commentId;
  document.getElementById("editCommentUsername").value = username;
  document.getElementById("editCommentText").value = commentText;
  document.getElementById("editCommentModal").classList.add("is-active");
}

function closeEditCommentModal() {
  document.getElementById("editCommentModal").classList.remove("is-active");
}
