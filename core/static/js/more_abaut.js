const h2 = document.getElementById('more-abaut')
const ul = document.getElementById('detail-abaut')
console.log(h2)
console.log(ul)

if (ul) {
    h2.addEventListener('click', () => {
        ul.hidden = !ul.hidden;
    })
}