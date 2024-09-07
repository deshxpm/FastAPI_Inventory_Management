document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('token');

    fetch('/items/create', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    }).then(response => {
        if (response.ok) {
            console.log("Authorized and fetched data");
        } else {
            console.error("Failed to authenticate");
        }
    }).catch(error => {
        console.error("Error:", error);
    });
});
