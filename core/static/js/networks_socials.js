const select = document.getElementsByName('social_networks')[0];
const inputUsername = document.getElementsByName('username_network')[0];
const inputUrl = document.getElementsByName('url')[0];

inputUrl.disabled = true;
inputUsername.disabled = true;
select.addEventListener('change', (event) => {
    const indexSelect = select.selectedIndex;
    if (indexSelect != 0) {
        const nameNetwork = select.children[indexSelect].textContent;
        inputUrl.value = document.getElementById(`url-${nameNetwork}`).textContent;
        inputUsername.value = document.getElementById(`username-${nameNetwork}`).textContent;
        console.log(inputUsername);
        inputUrl.disabled = false;
        inputUsername.disabled = false;
    } else {
        inputUrl.value = "";
        inputUsername.value = "";
        inputUrl.disabled = true;
        inputUsername.disabled = true;
    }
});
