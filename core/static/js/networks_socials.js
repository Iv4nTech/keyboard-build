const select = document.getElementsByName('social_networks')[0];
const inputUsername = document.getElementsByName('username_network')[0];
const inputUrl = document.getElementsByName('url')[0];
const ancoreDelete = document.createElement('a');
ancoreDelete.textContent = 'Delete network social';
ancoreDelete.classList.add('btn', 'btn-danger');

console.log(ancoreDelete);
console.log(inputUrl);
console.log(inputUsername);

inputUrl.disabled = true;
inputUsername.disabled = true;



select.addEventListener('change', (event) => {
    //Coger nombre red social
    let indexSelect = select.selectedIndex;
    let nameNetwork = select.children[indexSelect].textContent;
    
    //Averiguar la id
    try {
        const id = document.getElementById(`url-${nameNetwork}`).dataset.key;
        console.log(id);
        ancoreDelete.href = `/profile/networksocial/delete_socialnetwork/${id}`
    } catch (error) {
        console.log('No acces to id, becuase not selected option')
    }
    
    if (indexSelect != 0) {
        inputUrl.value = document.getElementById(`url-${nameNetwork}`).textContent;
        inputUsername.value = document.getElementById(`username-${nameNetwork}`).textContent;
        console.log(inputUsername);
        inputUrl.disabled = false;
        inputUsername.disabled = false;
        inputUrl.after(ancoreDelete);
    } else {
        inputUrl.value = "";
        inputUsername.value = "";
        inputUrl.disabled = true;
        inputUsername.disabled = true;
        ancoreDelete.remove();
    }
});

