const image = document.getElementById('image-profile')
const nav = document.getElementById('nav-user')

if (image) {
    image.addEventListener('click', () => {
        nav.hidden = !nav.hidden;
    })
}