class App {
    init () {
        this.render ()
    }

    render () {
        var show_menu_items = document.getElementById('show_menu_items')
        var user_show_menu_items = document.getElementById('user_show_menu_items')
        var submit_menu_form = document.getElementById('add_menu_form')
        var user_show_order_history = document.getElementById('user_show_order_history')
        var admin_show_new_orders = document.getElementById('admin_show_new_orders')
        var admin_show_order_history = document.getElementById('admin_show_order_new_order_history')

        if (submit_menu_form) {
            submit_menu_form.addEventListener('submit', function (event) {
                event.preventDefault()
                let title = document.getElementById('title').value
                let description = document.getElementById('description').value
                let price = parseInt(document.getElementById('price').value)
                //Empty error message divs
                emptyDivs(['title-error', 'description-error', 'price-error', 'display-info'])
                //Post daat through API
                addMenu(title, description, price)
            })
        }
        if (show_menu_items) {
            getMenus()
        }

        if (user_show_menu_items) {
            userGetMenuItems()
        }

        if (user_show_order_history) {
            showUserOrderHistory()
        }

        if (admin_show_new_orders) {
            adminGetOrders('new')
        }

        if (admin_show_order_history) {
            adminGetOrders('history')
        }
    }
}

let app = new App()
app.init()

function addMenu (title, description, price) {
    let data = JSON.stringify({
        title: title,
        description: description,
        price: price
    })
    //Submit data to API
    fetch("/api/v1/admins/menus", {
        method: "POST",
        body: data,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + this.readCookie('access_token')
        }
    })
    .then (function(response) {
        return response.json()
    })
    .then (function (jsonResponse) {
        //If response contains errors
        if (jsonResponse.errors) {
            for (let error of jsonResponse.errors) {
                //Display error messages
                if (error['field'] == "title"){
                    displayInfo('title-error', error['message'])
                }
                if (error['field'] == "description"){
                    displayInfo('description-error', error['message'])
                }
                if (error['field'] == "price"){
                    displayInfo('price-error', error['message'])
                } 
                displayInfo('display-info', '<div class="alert-danger"><span class="error"> Ooops... ' + jsonResponse['message'] +'</span></div>')
            }
        } else if (jsonResponse.msg || jsonResponse.error) {
            //If missing Authorization, Expired or invalid token
            alert("Ooops Authorization error \n\n" + jsonResponse.msg)
            setTimeout(function () {
                window.location.href = "/admin/login"
            }, 500)
        } else if (jsonResponse.message == "Menu added successfully") {
            emptyInputs(['title', 'description', 'price'])
            displayInfo(
                'display-info', '<div class="alert-success"><span class="success">' + 
                jsonResponse.message +
                '</span></div>'
            )
        } else {
            displayInfo('display-info', '<div class="alert-danger"><span class="error"> Ooops... Unable to process ur request</span></div>')
        }
    })
    .catch (function (error) {
        displayInfo('display-info', '<div class="alert-danger"><span class="error"> Ooops... ' + error +'</span></div>')
    })
}

function getMenus() {
    var menu_items_element = document.getElementById('show_menu_items')
    var loading_div = document.createElement('div')
    loading_div.setAttribute('class', 'loading-text')
    loading_div.setAttribute('id', 'loading-text')
    loading_div.innerHTML = '<h4>Loading Menu Items....... Please wait!</h4>'
    menu_items_element.appendChild(loading_div)
    //Fetch menu data from API
    fetch("/api/v1/admins/menus", {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + this.readCookie('access_token')
        }
    })
    .then (function(response) {
        return response.json()
    })
    .then (function (jsonResponse) {
        //If missing Authorization, Expired or invalid token
        if (jsonResponse.msg) {
            alert("Ooops Authorization error \n\n" + jsonResponse.msg)
            setTimeout(function () {
                window.location.href = "/admin/login"
            }, 500)
        } else if (jsonResponse.error) {
            alert("Ooops Authorization error \n\n" + jsonResponse.error)
            setTimeout(function () {
                window.location.href = "/admin/login"
            }, 500)
        } else if (jsonResponse.menus) {
            if (jsonResponse.menus.length > 0) {
                emptyDivs(['loading-text'])
                //If response contains menus, display items
                var titleDiv  = document.getElementById('menu_title')
                titleDiv.innerHTML = "<strong>Menu Items [" + jsonResponse.menus.length + "]</strong>"
                var fragment = document.createDocumentFragment()
                for (let item of jsonResponse.menus) {
                    let menuItem = document.createElement('div')
                    menuItem.classList.add('order-item')
                    menuItem.innerHTML += '<div class="order-image">' +
                    '<img src="/static/images/default.png" alt="default image">' +
                    '</div>' + 
                    '<div class="order-content">' +
                    '<div class="title">' + item.title +' - <span class="price">' + 
                    Intl.NumberFormat('en-US', { style: 'currency', currency: 'UGX' }).format(item.price) +
                    '</span> </div>' + 
                    '<div class="description">' + 
                    '<p>' + item.description + '</p>' +
                    '</div>' + 
                    '<p><small class="date">Date Created: ' + 
                    item.created_at +
                    ' - By: ' + item.first_name + ' ' + item.last_name + '</small></p>' +
                    '</div>'+
                    '<div class="order-button">' +
                    '<a href="/admin/menus/' + item.id + '/edit" class="button">Edit</a>' +
                    '<button type="submit" class="button delete">Delete</button>' +
                    '</div>'
                    fragment.appendChild(menuItem)
                }
                menu_items_element.appendChild(fragment)
            } else {
                loading_div.innerHTML = '<h4 class="error">No menu items found... Please <a href="/admin/menus/create">create one</a> !</h4>'
            }
        }
    })
    .catch (function (error) {
        console.log("Error " + error)
    })
}

function userGetMenuItems () {
    var menu_items_element = document.getElementById('user_show_menu_items')
    var loading_div = document.createElement('div')
    loading_div.setAttribute('class', 'loading-text')
    loading_div.setAttribute('id', 'loading-text')
    loading_div.innerHTML = '<h4>Loading Menu Items....... Please wait!</h4>'
    menu_items_element.appendChild(loading_div)
    //Fetch menu data from API
    fetch("/api/v1/users/menus", {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + this.readCookie('access_token')
        }
    })
    .then (function(response) {
        return response.json()
    })
    .then (function (jsonResponse) {
        //If missing Authorization, Expired or invalid token
        if (jsonResponse.msg) {
            alert("Ooops Authorization error \n\n" + jsonResponse.msg)
            setTimeout(function () {
                window.location.href = "/user/login"
            }, 500)
        } else if (jsonResponse.error) {
            alert("Ooops Authorization error \n\n" + jsonResponse.error)
            setTimeout(function () {
                window.location.href = "/user/login"
            }, 500)
        } else if (jsonResponse.menus) {
            if (jsonResponse.menus.length > 0) {
                emptyDivs(['loading-text'])
                //If response contains menus, display items
                var titleDiv  = document.getElementById('menu_title')
                titleDiv.innerHTML = "<strong>Today's Menu Items [" + jsonResponse.menus.length + "]</strong>"
                var fragment = document.createDocumentFragment()
                for (let item of jsonResponse.menus) {
                    let menuItem = document.createElement('form')
                    menuItem.classList.add('order-item')
                    menuItem.setAttribute('onSubmit', 'makeOrder(' + item.id + ')')
                    menuItem.setAttribute('id', 'make_order_form_' + item.id)
                    menuItem.innerHTML += '<div class="order-image">' +
                    '<img src="/static/images/default.png" alt="default image">' +
                    '</div>' + 
                    '<div class="order-content">' +
                    '<div class="title">' + item.title +' - <span class="price">' + 
                    Intl.NumberFormat('en-US', { style: 'currency', currency: 'UGX' }).format(item.price) +
                    '</span> </div>' + 
                    '<div class="description">' + 
                    '<p>' + item.description + '</p>' +
                    '</div>' + 
                    '<div class="field">' +
                    '<input type="text" placeholder="Location" id="location_' + item.id + '" required>' +
                    '<select id="quantity_' + item.id + '">' +
                    '<option value="1">1</option>' +
                    '<option value="2">2</option>' +
                    '<option value="3">3</option>' +
                    '<option value="4">4</option>' +
                    '<option value="5">5</option>' +
                    '</select>' +
                    '</div>' +
                    '<p><small class="date">Date Created: ' + 
                    item.created_at +
                    ' - By: ' + item.first_name + ' ' + item.last_name + '</small></p>' +
                    '</div>'+
                    '<div class="order-button">' +
                    '<button type="submit" class="button">Order Now</button>' +
                    '</div>'
                    fragment.appendChild(menuItem)
                }
                menu_items_element.appendChild(fragment)
            } else {
                loading_div.innerHTML = '<h4 class="error">No menu items found... Please wait while admin creates them!</h4>'
            }
        }
    })
    .catch (function (error) {
        loading_div.innerHTML = "Error " + error
    })
}

function makeOrder(menu_id) {
    var form = document.getElementById('make_order_form_' + menu_id)
    document.addEventListener('submit', function (event) {
        event.preventDefault()
        var loading_element = document.getElementById('show_loading_status')
        var loading_div = document.createElement('div')
        loading_div.setAttribute('class', 'loading-text')
        loading_div.setAttribute('id', 'loading-text')
        loading_div.innerHTML = '<h4>Submitting order....... Please wait!</h4>'
        loading_element.appendChild(loading_div)
        emptyDivs(['show_loading_status'])

        var location = document.getElementById('location_' + menu_id).value
        var quantity = document.getElementById('quantity_' + menu_id).value

        var data = JSON.stringify({
            menu_id: menu_id,
            location: location,
            quantity: parseInt(quantity)
        })
        //Post order to API endpoint
        fetch("/api/v1/users/orders", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': "Bearer " + readCookie('access_token')
            },
            body: data
        })
        .then (function(response) {
            return response.json()
        })
        .then (function (jsonResponse) {
            //If missing Authorization, Expired or invalid token
            if (jsonResponse.msg) {
                alert("Ooops Authorization error \n\n" + jsonResponse.msg)
                setTimeout(function () {
                    window.location.href = "/user/login"
                }, 500)
            } else if (jsonResponse.error) {
                if (jsonResponse.error == "This menu item doesn't exist in the menu list"){
                    alert("Menu Item Not Found \n" + jsonResponse.error)
                } else {
                    alert("Ooops Authorization error \n\n" + jsonResponse.error)
                    setTimeout(function () {
                        window.location.href = "/user/login"
                    }, 500)
                }
            } else if (jsonResponse.errors) {
                errorMessage = ""
                for (let error of jsonResponse.errors){
                    errorMessage += error.message + "\n"
                }
                alert("Ooops Validation error. \n\n" + errorMessage)
            } else if (jsonResponse.data) {
                emptyDivs(['show_loading_status'])
                loading_div.innerHTML = '<h4>Kudos, Order placed successfully!</h4>'
                loading_element.appendChild(loading_div)
                emptyInputs(['location_' + menu_id, 'quantity_' + menu_id])
            }
        })
        .catch (function (error) {
            emptyDivs(['show_loading_status'])
            loading_div.innerHTML = '<h4>Error! ' + error + '</h4>'
            loading_element.appendChild(loading_div)
        })

    })
}

function showUserOrderHistory () {
    var order_history_element = document.getElementById('user_show_order_history')
    var loading_div = document.createElement('div')
    loading_div.setAttribute('class', 'loading-text')
    loading_div.setAttribute('id', 'loading-text')
    loading_div.innerHTML = '<h4>Loading Order history....... Please wait!</h4>'
    order_history_element.appendChild(loading_div)
    //Fetch menu data from API
    fetch("/api/v1/users/orders", {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + this.readCookie('access_token')
        }
    })
    .then (function(response) {
        return response.json()
    })
    .then (function (jsonResponse) {
        //If missing Authorization, Expired or invalid token
        if (jsonResponse.msg) {
            alert("Ooops Authorization error \n\n" + jsonResponse.msg)
            setTimeout(function () {
                window.location.href = "/user/login"
            }, 500)
        } else if (jsonResponse.error) {
            alert("Ooops Authorization error \n\n" + jsonResponse.error)
            setTimeout(function () {
                window.location.href = "/user/login"
            }, 500)
        } else if (jsonResponse.order) {
            if (jsonResponse.order.length > 0) {
                emptyDivs(['loading-text'])
                 //If response contains menus, display items
                 var titleDiv  = document.getElementById('order_title')
                 titleDiv.innerHTML = "<strong>Your order history [" + jsonResponse.order.length + "]</strong>"
                 var fragment = document.createDocumentFragment()
                 for (let item of jsonResponse.order) {
                     var status = "pending"
                     if (item.status == 'Complete') {
                         status = 'completed'
                     } else if (item.status == 'Cancelled') {
                         status = 'declined'
                     }
                     let orderItem = document.createElement('form')
                     orderItem.classList.add('order-item')
                     orderItem.setAttribute('onSubmit', 'makeOrder(' + item.id + ')')
                     orderItem.setAttribute('id', 'make_order_form_' + item.id)
                     orderItem.innerHTML += '<div class="order-image">' +
                     '<img src="/static/images/default.png" alt="default image">' +
                     '</div>' + 
                     '<div class="order-content">' +
                     '<div class="title">' + item.title +' - <span class="price">' + 
                     Intl.NumberFormat('en-US', { style: 'currency', currency: 'UGX' }).format(item.price) +
                     '</span> </div>' + 
                     '<div class="description">' + 
                     '<p>' + item.description + '</p>' +
                     '</div>' + 
                     '<div class="field"><strong>Location:</strong> ' + item.location + '<strong> Quantity:</strong> ' + item.quantity + ' ' +
                     '<strong>Total cost:</strong> ' +Intl.NumberFormat('en-US', { style: 'currency', currency: 'UGX' }).format(item.price * item.quantity) + '</div>' +
                     '<p><small class="date">Date Created: ' + item.created_at + '</small></p>' +
                     '</div>'+
                     '<div class="order-button">' +
                     '<button type="button" class="button ' + status + '">' + item.status + '</button>' +
                     '</div>'
                     fragment.appendChild(orderItem)
                 }
                 order_history_element.appendChild(fragment)
            } else {
                loading_div.innerHTML = '<h4 class="error">No orders found... Please make your first order.</4>'
            }
        }
    })
    .catch (function (error) {
        loading_div.innerHTML = '<h4 class="error">Error while loading orders.... ' + error +'.</4>'
    })
}

function adminGetOrders (order_type) {
    //Get all Orders acccording to type
    var elementID = 'admin_show_new_orders'
    var url = ''
    var loading_text = "Loading New orders..."
    var title_text = "Clients Pending orders"
    if (order_type == 'history') {
        elementID = 'admin_show_order_new_order_history'
        url = '/history'
        loading_text = "Loading Order History..."
        title_text = "Processed Order History"
    }
    var admin_show_order_orders = document.getElementById(elementID)
    var loading_div = document.createElement('div')
    loading_div.setAttribute('class', 'loading-text')
    loading_div.setAttribute('id', 'loading-text')
    loading_div.innerHTML = '<h4>' + loading_text + ' Please wait!</h4>'
    admin_show_order_orders.appendChild(loading_div)
    //Fetch menu data from API
    fetch("/api/v1/admins/orders" + url, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + this.readCookie('access_token')
        }
    })
    .then (function(response) {
        return response.json()
    })
    .then (function (jsonResponse) {
        //If missing Authorization, Expired or invalid token
        if (jsonResponse.msg) {
            alert("Ooops Authorization error \n\n" + jsonResponse.msg)
            setTimeout(function () {
                window.location.href = "/admin/login"
            }, 500)
        } else if (jsonResponse.error) {
            alert("Ooops Authorization error \n\n" + jsonResponse.error)
            setTimeout(function () {
                window.location.href = "/admin/login"
            }, 500)
        } else if (jsonResponse.orders) {
            if (jsonResponse.orders.length > 0) {
                emptyDivs(['loading-text'])
                 //If response contains menus, display items
                 var titleDiv  = document.getElementById('order_title')
                 titleDiv.innerHTML = "<strong>" + title_text + " - [" + jsonResponse.orders.length + "]</strong>"
                 var fragment = document.createDocumentFragment()
                 for (let item of jsonResponse.orders) {
                     var status = "pending"
                     var button = '<button type="button" class="button completed" onclick="updateOrderStatus('+ item.id + ', \'Processing\' )">Accept</button>'+
                    '<button type="button" class="button declined" onclick="updateOrderStatus('+ item.id + ', \'Cancelled\' )">X Decline</button>'
                    
                     if (item.status == 'Complete') {
                        status = 'completed'
                        button = '<span class="button ' + status + '">' + item.status + '</span>'
                     } else if (item.status == 'Cancelled') {
                        status = 'declined'
                        button = '<span class="button ' +status +'">' + item.status + '</span>'
                     } else if (item.status == 'Processing') {
                        status = 'pending'
                        button = '<span class="button ' +status +'">' + item.status + '</span>' +
                        '<button type="button" class="button completed" onclick="updateOrderStatus('+ item.id + ', \'Complete\' )"> Mark as Complete</button>'
                     }
                     let orderItem = document.createElement('div')
                     orderItem.classList.add('order-item')
                     orderItem.innerHTML += '<div class="order-image">' +
                     '<img src="/static/images/default.png" alt="default image">' +
                     '</div>' + 
                     '<div class="order-content">' +
                     '<div class="title">' + item.title +' - <span class="price">' + 
                     Intl.NumberFormat('en-US', { style: 'currency', currency: 'UGX' }).format(item.price) +
                     '</span> </div>' + 
                     '<div class="description">' + 
                     '<p>' + item.description + '</p>' +
                     '</div>' + 
                     '<div class="field"><strong>Location:</strong> ' + item.location + '<strong> Quantity:</strong> ' + item.quantity + ' ' +
                     '<strong>Total cost:</strong> ' +Intl.NumberFormat('en-US', { style: 'currency', currency: 'UGX' }).format(item.price * item.quantity) + '</div>' +
                     '<p><small class="date">Date Created: ' + 
                     item.created_at + 
                     ' - By: ' + item.first_name + ' ' + item.last_name + ' Email: ' + item.email + '</small></p>' +
                     '</small></p>' +
                     '</div>'+
                     '<div class="order-button">' +
                     button + 
                     '</div>'
                     fragment.appendChild(orderItem)
                 }
                 admin_show_order_orders.appendChild(fragment)
            } else {
                loading_div.innerHTML = '<h4 class="error">No orders found... Please wait while customers make orders.</4>'
            }
        }
    })
    .catch (function (error) {
        loading_div.innerHTML = '<h4 class="error">Error while loading orders.... ' + error +'.</4>'
    })
}

function updateOrderStatus(order_id, status) {
    var loading = document.getElementById('loading-text')
    loading.innerHTML = '<h4>Updating status...</h4>'
    fetch('/api/v1/admins/orders/' + parseInt(order_id) + '/update', {
        method: "PUT",
        body: JSON.stringify({status: status}),
        headers: {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + this.readCookie('access_token')
        }
    })
    .then(function(response) {
        return response.json()
    })
    .then(function (jsonResponse) {
        console.log(jsonResponse)
        //If missing Authorization, Expired or invalid token
        if (jsonResponse.msg) {
            alert("Ooops Authorization error \n\n" + jsonResponse.msg)
            setTimeout(function () {
                window.location.href = "/user/login"
            }, 500)
        } else if (jsonResponse.error) {
            alert("Ooops Authorization error \n\n" + jsonResponse.error)
            setTimeout(function () {
                window.location.href = "/user/login"
            }, 500)
        } else if (jsonResponse.message) {
            loading.innerHTML = '<h4 class="success">Status updated successfuly...</h4>'
            emptyDivs(['admin_show_new_orders'])
            adminGetOrders('new')
        }
    })
    .catch(function(error) {
        console.log(error)
    })
}

function displayInfo (divName, error) {
    //Function to display error messages
    let element = document.getElementById(divName)
    if (element) element.innerHTML = '<span class="error">' + error +'</span>'
    return true
}

function emptyDivs (divNames) {
    //Function to empty all div contents
    for (let div of divNames) {
        let element = document.getElementById(div)
        if (element) while (element.firstChild) element.removeChild(element.firstChild)
    }
    return true
}

function emptyInputs(fieldNames) {
    //Function to empty all input fields
    for (let field of fieldNames) {
       let element =  document.getElementById(field)
       if (element) element.value = ''
    }
    return true
}

// Read cookie
function readCookie (name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1,c.length);
        }
        if (c.indexOf(nameEQ) === 0) {
            return c.substring(nameEQ.length,c.length);
        }
    }
    return null;
}