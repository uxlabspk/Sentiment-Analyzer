

let filterCheck = document.getElementById('filteredComment');
let allCommentsTable = document.getElementById('allCommentsTable');
let filteredCommentsTable = document.getElementById('filteredCommentsTable');


filterCheck.addEventListener('change', (event) => {
  if (event.target.checked) {
    allCommentsTable.classList.add('d-none');
    filteredCommentsTable.classList.remove('d-none');
  } else {
    allCommentsTable.classList.remove('d-none');
    filteredCommentsTable.classList.add('d-none');
  }
});