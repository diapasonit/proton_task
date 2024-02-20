const list_url = "http://localhost:5000/orders/";
const details_url = "http://localhost:5000/orders/";
const follow_up_list_url = "http://localhost:5000/orders/follow-up/";
const unfollow_up_list_url = "http://localhost:5000/orders/unfollow-up/";

const post_header = {
    method: 'POST',
    headers:
        {
            Accept: 'application/json',
            'Content-Type':
                'application/json',
        }
}

async function get_list(url) {
    const response = await fetch(url);
    var data = await response.json();
    console.log(data);
    if (response) {
        hideloader();
    }
    show(data);
}

async function sync_state() {
    await get_list(list_url);
    await get_follow_up_list(follow_up_list_url);
}

async function get_follow_up_list(url) {
    const response = await fetch(url);
    var data = await response.json();
    console.log(data);
    if (response) {
        hideloader();
    }
    show_follow_up(data);
}

// Calling that async function
sync_state()

// Function to hide the loader
function hideloader() {
    document.getElementById('loading').style.display = 'none';
}

async function show_details(order_id) {
    const response = await fetch(details_url + order_id);
    let data = await response.json();
    let tab =
        `<tr> <th>Name</th> <th>Price</th> <th>Quantity</th></tr>`;

    for (let r of data.items) {
        tab += `<tr> <td>${r.name} </td> <td>${r.price.toFixed(2)}</td> <td>${r.quantity}</td></tr>`;
    }
    document.getElementById("details").innerHTML = tab;

}

async function move_to_follow_up(order_id) {
    const response = await fetch(follow_up_list_url + order_id, post_header);
    await sync_state()
}


async function move_to_unfollow_up(order_id) {
    const response = await fetch(unfollow_up_list_url + order_id, post_header);
    await sync_state()
}

// Function to define innerHTML for HTML table
function unfollow_up_button(order_id) {
    return `<button onclick="move_to_unfollow_up(${order_id})">UnFollow-up</button>`
}

function follow_up_button(order_id) {
    return `<button onclick="move_to_follow_up(${order_id})">Follow-up</button>`
}

function get_place_holder_list() {
    return `<tr>Add something to this list</tr>`
}

function details_button(order_id) {
    return `<button onclick="show_details(${order_id})">Details</button>`
}

function show_follow_up(data) {
    let tab = `<tr><th>Name</th><th>Total price</th><th>Date</th><th>Details</th><th>UnFollow-up</th></tr>`;
    let amount = 0.0
    // Loop to access all rows
    let present = false
    for (let r of data.order_list) {
        tab += `<tr><td>${r.customer_name} </td><td>${r.total_price.toFixed(2)}</td><td>${r.date}</td> <td>${details_button(r.id)}</td><td>${unfollow_up_button(r.id)}</td> </tr>`;
        amount += r.total_price
        present = true
    }
    if (!present) {
        tab += get_place_holder_list()
    }
    tab += `<tr> <td>Total amount</td><td>${amount.toFixed(2)}</td></tr>`
    document.getElementById("orders_followup").innerHTML = tab;
}


function show(data) {
    let tab = `<tr><th>Name</th><th>Total price</th><th>Date</th><th>Details</th><th>Follow-up</th></tr>`;
    // Loop to access all rows
    let present = false
    for (let r of data.order_list) {
        present = true
        tab += `<tr><td>${r.customer_name} </td><td>${r.total_price.toFixed(2)}</td><td>${r.date}</td> <td>${details_button(r.id)}</td><td>${follow_up_button(r.id)}</td> </tr>`;
    }
    if (!present) {
        tab += get_place_holder_list()
    }
    // Setting innerHTML as tab variable
    document.getElementById("orders").innerHTML = tab;
}