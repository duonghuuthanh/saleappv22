function addToCart(id, name, price) {
    fetch('/api/cart', {
        "method": "POST",
        "body": JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
        var info = document.getElementById("cart-stats");
        info.innerText = `${data.total_quantity} - ${data.total_amount} VNĐ`;
    })
}

function pay() {
    fetch('/payment', {
        "method": "POST",
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
        alert(data.message);
    }).catch(res => console.log(res))
}
