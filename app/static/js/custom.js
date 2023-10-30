const input = document.querySelector('input[id="link"]');
const author = document.querySelector('input[id="author"]');

input.addEventListener('input', update_value);

function update_value() {
    author.value = input.value
}
