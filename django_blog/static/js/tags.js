// Tag management functionality
document.addEventListener("DOMContentLoaded", function () {
  // Tag autocomplete
  const tagInputs = document.querySelectorAll(
    'input[name="new_tags"], #id_tags_search'
  );
  tagInputs.forEach((input) => {
    input.addEventListener("input", function () {
      const query = this.value;
      if (query.length >= 2) {
        fetch(`/blog/autocomplete/tags/?q=${encodeURIComponent(query)}`)
          .then((response) => response.json())
          .then((tags) => {
            showTagSuggestions(tags, this);
          });
      }
    });
  });

  // Tag color picker enhancement
  const colorInputs = document.querySelectorAll('input[type="color"]');
  colorInputs.forEach((input) => {
    input.addEventListener("change", function () {
      this.style.backgroundColor = this.value;
    });
    // Initialize background color
    if (input.value) {
      input.style.backgroundColor = input.value;
    }
  });

  // Tag cloud interactions
  document.querySelectorAll(".tag-cloud-item").forEach((tag) => {
    tag.addEventListener("mouseenter", function () {
      this.style.transform = "scale(1.1)";
      this.style.transition = "transform 0.2s ease";
    });

    tag.addEventListener("mouseleave", function () {
      this.style.transform = "scale(1)";
    });
  });
});

function showTagSuggestions(tags, input) {
  // Remove existing suggestions
  const existingSuggestions =
    input.parentNode.querySelector(".tag-suggestions");
  if (existingSuggestions) {
    existingSuggestions.remove();
  }

  if (tags.length > 0) {
    const suggestions = document.createElement("div");
    suggestions.className = "tag-suggestions list-group mt-2";
    suggestions.style.position = "absolute";
    suggestions.style.zIndex = "1000";
    suggestions.style.width = "100%";

    tags.forEach((tag) => {
      const suggestion = document.createElement("button");
      suggestion.type = "button";
      suggestion.className = "list-group-item list-group-item-action";
      suggestion.innerHTML = `
                <strong>${tag.name}</strong>
                <small class="text-muted float-end">${tag.post_count} posts</small>
            `;
      suggestion.addEventListener("click", function () {
        addTagToInput(tag.name, input);
        suggestions.remove();
      });
      suggestions.appendChild(suggestion);
    });

    input.parentNode.appendChild(suggestions);
  }
}

function addTagToInput(tagName, input) {
  if (input.name === "new_tags") {
    const currentValue = input.value;
    const tags = currentValue
      ? currentValue.split(",").map((t) => t.trim())
      : [];

    if (!tags.includes(tagName)) {
      tags.push(tagName);
      input.value = tags.join(", ");
    }
  }
}
