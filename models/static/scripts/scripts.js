document.addEventListener('DOMContentLoaded', (event) => {
  document.getElementById('add-ingredient').addEventListener('click', function() {
    let newDiv = document.createElement('div');
    newDiv.className = 'form-group mt-2';

    let newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.name = 'ingredients[]';
    newInput.className = 'form-control form-control-md';

    newDiv.appendChild(newInput);

    document.getElementById('ingredients-container').appendChild(newDiv);
  });

  document.getElementById('add-instruction').addEventListener('click', function() {
    let newDiv = document.createElement('div');
    newDiv.className = 'form-group mt-2';

    let newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.name = 'instructions[]';
    newInput.className = 'form-control form-control-md';

    newDiv.appendChild(newInput);

    document.getElementById('instructions-container').appendChild(newDiv);
  });
});


button = document.getElementById("searchButton")
input = document.getElementById("searchBox")
button.disabled = true;
input.addEventListener("input", function() {
  if (input.value.length > 0) {
    button.disabled = false;
  }
});

function showForm() {
  document.getElementById('formContainer').style.display = 'block';
  document.getElementById('buttonContainer').style.display = 'none';
}
