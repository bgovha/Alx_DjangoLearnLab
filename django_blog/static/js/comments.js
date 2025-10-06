// Comment system functionality
document.addEventListener("DOMContentLoaded", function () {
  // Character counter for comment textareas
  const textareas = document.querySelectorAll(
    ".comment-textarea, .reply-comment-form textarea"
  );
  textareas.forEach((textarea) => {
    const counter = textarea.closest("form").querySelector(".char-count");
    if (counter) {
      textarea.addEventListener("input", function () {
        counter.textContent = this.value.length;
      });
      // Initialize counter
      counter.textContent = textarea.value.length;
    }
  });

  // Like functionality
  document.querySelectorAll(".like-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const commentId = this.dataset.commentId;
      likeComment(commentId, this);
    });
  });

  // Reply functionality
  document.querySelectorAll(".reply-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const commentId = this.dataset.commentId;
      const authorName = this.dataset.authorName;
      showReplyForm(commentId, authorName);
    });
  });

  // Cancel reply
  document.querySelectorAll(".cancel-reply").forEach((button) => {
    button.addEventListener("click", function () {
      const form = this.closest(".reply-form");
      form.style.display = "none";
    });
  });

  // AJAX form submission
  document
    .querySelectorAll(".comment-form, .reply-comment-form")
    .forEach((form) => {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        submitCommentForm(this);
      });
    });
});

function likeComment(commentId, button) {
  const url = `/blog/comment/${commentId}/like/`;
  const csrfToken = getCookie("csrftoken");

  fetch(url, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Update like count and button state
        const likeCounts = document.querySelectorAll(
          `[data-comment-id="${commentId}"] .like-count`
        );
        likeCounts.forEach((span) => {
          span.textContent = data.like_count;
        });

        // Update button text and state
        const likeButtons = document.querySelectorAll(
          `[data-comment-id="${commentId}"] .like-btn`
        );
        likeButtons.forEach((btn) => {
          btn.dataset.liked = data.liked;
          const likeText = btn.querySelector(".like-text");
          if (likeText) {
            likeText.textContent = data.liked ? "Unlike" : "Like";
          }

          // Update button appearance
          if (data.liked) {
            btn.classList.remove("btn-outline-primary");
            btn.classList.add("btn-primary");
          } else {
            btn.classList.remove("btn-primary");
            btn.classList.add("btn-outline-primary");
          }
        });
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      showNotification("Error liking comment", "error");
    });
}

function showReplyForm(commentId, authorName) {
  // Hide all other reply forms
  document.querySelectorAll(".reply-form").forEach((form) => {
    form.style.display = "none";
  });

  // Show this reply form
  const replyForm = document.getElementById(`reply-form-${commentId}`);
  if (replyForm) {
    replyForm.style.display = "block";
    const textarea = replyForm.querySelector("textarea");
    textarea.value = `@${authorName} `;
    textarea.focus();

    // Update character counter
    const counter = replyForm.querySelector(".char-count");
    if (counter) {
      counter.textContent = textarea.value.length;
    }
  }
}

function submitCommentForm(form) {
  const url = form.action;
  const formData = new FormData(form);
  const csrfToken = getCookie("csrftoken");

  fetch(url, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        showNotification(data.message, "success");
        form.reset();

        // Reset character counter
        const counter = form.querySelector(".char-count");
        if (counter) counter.textContent = "0";

        // Hide reply form if it's a reply
        const replyForm = form.closest(".reply-form");
        if (replyForm) {
          replyForm.style.display = "none";
        }

        // Reload page to show new comment (or use AJAX to append)
        setTimeout(() => {
          window.location.reload();
        }, 1000);
      } else {
        showNotification("Error: " + JSON.stringify(data.errors), "error");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      showNotification("Error submitting comment", "error");
    });
}

// Utility functions
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function showNotification(message, type) {
  // Create notification element
  const notification = document.createElement("div");
  notification.className = `alert alert-${
    type === "success" ? "success" : "danger"
  } alert-dismissible fade show`;
  notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

  // Add to page
  document.body.appendChild(notification);

  // Auto remove after 5 seconds
  setTimeout(() => {
    notification.remove();
  }, 5000);
}
