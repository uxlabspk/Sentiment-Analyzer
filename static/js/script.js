const ourProjects = ["All", "Video", "Audio", "Content"];

const btn = document.querySelector(".btn-container");

window.addEventListener("DOMContentLoaded", function () {
  displayButtons(ourProjects);
});

function displayButtons(proj) {
  const category = proj
    .map((item) => {
      return `<button class="filter-btn btn btn-outline-primary text-uppercase m-1 " data-id=${item}>${item}</button>`;
    })
    .join("");
  btn.innerHTML = category;
}
