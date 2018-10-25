document.addEventListener('DOMContentLoaded',  function () {
    //On content Load
    var user_signin_form = document.getElementById('user_sign_in_form')
    var admin_signin_form = document.getElementById('admin_sign_in_form')
    var user_sign_up_form = document.getElementById('user_sign_up_form')
    var admin_sign_up_form = document.getElementById('admin_sign_up_form')
    var show_menu_items = document.getElementById('show_menu_items')
    var user_show_menu_items = document.getElementById('user_show_menu_items')
    var submit_menu_form = document.getElementById('add_menu_form')
    var user_show_order_history = document.getElementById('user_show_order_history')
    var admin_show_new_orders = document.getElementById('admin_show_new_orders')
    var admin_show_order_history = document.getElementById('admin_show_order_new_order_history')
    var edit_menu_form = document.getElementById('edit_menu_form')
    if (submit_menu_form) {
        submit_menu_form.addEventListener('submit', function (event) {
            event.preventDefault()
            let title = document.getElementById('title').value
            let description = document.getElementById('description').value
            let price = parseInt(document.getElementById('price').value)
            emptyDivs(['title-error', 'description-error', 'price-error', 'display-info'])
            addMenu(title, description, price)
        })
    }
    if (user_signin_form) submit_signin_form('user')
    if (admin_signin_form) submit_signin_form('admin')
    if (user_sign_up_form) submit_register_form('user')
    if (admin_sign_up_form) submit_register_form('admin')
    if (show_menu_items) getMenus()
    if (user_show_menu_items) userGetMenuItems()
    if (user_show_order_history) showUserOrderHistory()
    if (admin_show_new_orders) adminGetOrders('new')
    if (admin_show_order_history) adminGetOrders('history')
    if (edit_menu_form) updateMenuDetails()
})

function submit_signin_form( user_type ) {
    var url = '/api/v1/users/login'
    if (user_type == 'admin') url = '/api/v1/admins/login'
    const form = document.getElementById(user_type + '_sign_in_form')
    form.addEventListener('submit', function(event) {
        event.preventDefault()
        emptyDivs(['email-error','password-error','login_info'])
        fetch(url, {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                email: form[0].value,
                password: form[1].value
            })
        })
        .then(function(response) {
            return response.json()
        })
        .then(function(jsonResponse) {
            //if response has errors
            var token = jsonResponse.user_token
            if ( user_type == 'admin') token = jsonResponse.admin_token
            if (jsonResponse.errors) {
                for (let error of jsonResponse.errors) {
                    //Display error messages
                    if (error['field'] == "email") displayInfo('email-error', '<span class="error">' + error['message'] +'</span>')
                    if (error['field'] == "password") displayInfo('password-error', '<span class="error">' + error['message'] +'</span>')
                    displayInfo('login-info', '<span class="alert-danger"> Ooops... ' + jsonResponse['message'] +'</span>')
                }
            } else if (jsonResponse.error) {
                //If response has an error
                displayInfo('login-info', '<span class="alert-danger"> Ooops... ' + jsonResponse.error +'</span>')
            } else if (token) {
                //Add token to cookie
                var redirectUrl = '/'
                if (user_type == 'admin') redirectUrl = '/admin/orders'
                createCookie('access_token', token, 30)
                displayInfo('login-info', '<span class="alert-success success">' + jsonResponse.message + ', redirecting...</span>')
                setTimeout(function () {
                    window.location.href = redirectUrl
                }, 1000)
            } else {
                //Return generic error message
                displayInfo('login-info', '<span class="alert-danger"> Ooops... Unable to process your request now</span>')
            }
        })
        .catch(function(error) {
            displayInfo('login-info', '<span class="alert-danger"> Oops, there was a problem: '+  error +'</span>')
        })
    }, false)
    //Disable multiple submit
    // form[2].setAttribute('disabled', 'disabled')
}

function submit_register_form ( user_type) {
    var url = '/api/v1/users/register'
    if (user_type == 'admin') url = '/api/v1/admins/register'
    const sign_up_form = document.getElementById(user_type + '_sign_up_form')
    sign_up_form.addEventListener('submit', function(event){
        event.preventDefault()
        //Empty all error divs
        emptyDivs(['first_name-error', 'last_name-error', 'email-error', 'password-error', 'register-info'])
        
        if (sign_up_form[3].value !== sign_up_form[4].value) {
            //If passwords don't match
            displayInfo('register-info', '<span class="alert-danger"> Oops, there was a problem:</span>')
            displayInfo('password-error',  "Passwords do not match")

        } else {
            //Post data to api endpoint
            fetch(url, {
                method: "POST",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    first_name: sign_up_form[0].value,
                    last_name: sign_up_form[1].value,
                    email: sign_up_form[2].value,
                    password: sign_up_form[3].value
                })
            })
            .then(function(response) {
                return response.json()
            })
            .then(function(jsonResponse) {
                var message = "User added successfully"
                if ( user_type == 'admin') token = "Admin registered successfully"
                if (jsonResponse.errors) {
                    for (let error of jsonResponse.errors) {
                        //Display error messages
                        if (error['field'] == "first_name") displayInfo('first_name-error', error['message'])
                        if (error['field'] == "last_name") displayInfo('last_name-error', error['message'])
                        if (error['field'] == "email") displayInfo('email-error', error['message'])
                        if (error['field'] == "password") displayInfo('password-error', error['message'])
                        displayInfo('register-info', '<span class="alert-danger"> Ooops... ' + jsonResponse['message'] +'</span>')
                    }
                } else if (jsonResponse.error) {
                    displayInfo('register-info', '<span class="alert-danger"> Ooops... ' + jsonResponse.error +'</span>')
                } else if (jsonResponse.field == 'email') {
                    displayInfo('register-info', '<span class="alert-danger"> Oops, there was a problem:</span>')
                    displayInfo('email-error', jsonResponse.message)
                } else if (jsonResponse.message == message) {
                    displayInfo('register-info', '<span class="alert-success success">Registration successful, Please wait while we redirect you...</span>')
                    var redirectUrl = '/user/login'
                    if (user_type == 'admin') redirectUrl = '/admin/login'
                    setTimeout(function () {
                        window.location.href = redirectUrl
                    }, 1000)
                } else {
                    displayInfo('register-info', '<span class="alert-danger"> Ooops... Unable to process your request now.</span>')
                }
            })
            .catch(function(error) {
                displayInfo('register-info', '<span class="error"> Oops, there was a problem: '+  error +'</span>')
            });
        }
    }, false)
    //Disable multiple submit
    // sign_up_form[5].setAttribute('disabled', 'disabled')
}

function addMenu (title, description, price) {
    let data = JSON.stringify({
        title: title,
        description: description,
        price: price
    })
    //Submit data to API
    var fetchedOrderData = fetchData('/api/v1/admins/menus', 'POST', data)
    fetchedOrderData.then (function (jsonResponse) {
        redirectUnautheneticated('admin', jsonResponse, 500)
        //If response contains errors
        if (jsonResponse.errors) {
            for (let error of jsonResponse.errors) {
                //Display error messages
                if (error['field'] == "title") displayInfo('title-error', error['message'])
                if (error['field'] == "description") displayInfo('description-error', error['message'])
                if (error['field'] == "price") displayInfo('price-error', error['message']) 
                displayInfo('display-info', '<div class="alert-danger"><span class="error"> Ooops... ' + jsonResponse['message'] +'</span></div>')
            }
        } else if (jsonResponse.message == "Menu added successfully") {
            emptyInputs(['title', 'description', 'price'])
            displayInfo(
                'display-info', '<div class="alert-success"><span class="success">' + jsonResponse.message + '</span></div>'
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
    var fetchedOrderData = fetchData('/api/v1/admins/menus', 'GET', '')
    fetchedOrderData.then (function (jsonResponse) {
        //If missing Authorization, Expired or invalid token
        redirectUnautheneticated('admin', jsonResponse, 500) 
        if (jsonResponse.menus) {
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
                    '<button type="submit" class="button delete" onclick="deleteMenuItem(' + item.id +')">Delete</button>' +
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
    var fetchedOrderData = fetchData('/api/v1/users/menus', 'GET', '')
    fetchedOrderData.then (function (jsonResponse) {
        //If missing Authorization, Expired or invalid token
        redirectUnautheneticated('user', jsonResponse, 500)
        if (jsonResponse.menus) {
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
                    menuItem.innerHTML += '<div class="order-image"><img src="/static/images/default.png" alt="default image"></div>' + 
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
        var fetchedOrderData = fetchData('/api/v1/users/orders', 'POST', data)
        fetchedOrderData.then (function (jsonResponse) {
            //If missing Authorization, Expired or invalid token
            redirectUnautheneticated('user', jsonResponse, 500) 
            if (jsonResponse.errors) {
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
    var fetchedOrderData = fetchData('/api/v1/users/orders', 'GET', '')
    fetchedOrderData.then (function (jsonResponse) {
        //If missing Authorization, Expired or invalid token
        redirectUnautheneticated('user', jsonResponse, 500)
        if (jsonResponse.order) {
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

function adminGetOrders ( order_type) {
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
    var fetchedOrderData = fetchData('/api/v1/admins/orders' + url, 'GET', '')
    fetchedOrderData.then (function (jsonResponse) {
        //If missing Authorization, Expired or invalid token
        redirectUnautheneticated('admin', jsonResponse, 500)
        if (jsonResponse.orders) {
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
    var data = JSON.stringify({status: status})
    var fetchedOrderData = fetchData('/api/v1/admins/orders/' + parseInt(order_id) + '/update', 'PUT', data)
    fetchedOrderData.then(function (jsonResponse) {
        console.log(jsonResponse)
        //If missing Authorization, Expired or invalid token
        redirectUnautheneticated('admin', jsonResponse, 500)
        if (jsonResponse.message) {
            loading.innerHTML = '<h4 class="success">Status updated successfuly...</h4>'
            emptyDivs(['admin_show_new_orders'])
            adminGetOrders('new')
        }
    })
    .catch(function(error) {
        console.log(error)
    })
}

function updateMenuDetails () {
    var menu_id = document.getElementById('menu_id').value
    var edit_menu_title = document.getElementById('edit_menu_title')
    var loading_text = document.getElementById('loading_text')
    loading_text.innerHTML = "Loading Menu details... please wait"

    var fetchedOrderData = fetchData('/api/v1/admins/menus/' + menu_id, 'GET', '')
    fetchedOrderData.then (function (jsonResponse) {
        emptyDivs(['loading_text'])
        redirectUnautheneticated('admin', jsonResponse, 500)
        if (jsonResponse.menus) {
            edit_menu_title.innerHTML = "Edit " + jsonResponse.menus[0].title + " details."
            document.getElementById('title').value = jsonResponse.menus[0].title
            document.getElementById('description').value = jsonResponse.menus[0].description
            document.getElementById('price').value = jsonResponse.menus[0].price
        }
    })
    .catch (function (error) {
        loading_text.innerHTML = "<span class='error'>Error while loading menu details " + error + "</span>" 
    })
    edit_menu_form.addEventListener('submit', function (event) {
        event.preventDefault()
        loading_text.innerHTML = "Updating menu details"
        var title = document.getElementById('title').value
        var description = document.getElementById('description').value
        var price = document.getElementById('price').value

        let data = JSON.stringify({
            title: title,
            description: description,
            price: parseInt(price)
        })
        //Update menu details
        var fetchedOrderData = fetchData('/api/v1/admins/menus/' + menu_id + '/update', 'PUT', data)
        fetchedOrderData.then (function (jsonResponse) {
            redirectUnautheneticated('admin', jsonResponse, 500)
            //If response contains errors
            if (jsonResponse.errors) {
                emptyDivs(['loading_text'])
                for (let error of jsonResponse.errors) {
                    if (error['field'] == "title") displayInfo('title-error', error['message'])
                    if (error['field'] == "description") displayInfo('description-error', error['message'])
                    if (error['field'] == "price") displayInfo('price-error', error['message'])
                    displayInfo('display-info', '<div class="alert-danger"><span class="error"> Ooops... ' + jsonResponse['message'] +'</span></div>')
                }
            } else if (jsonResponse.message) {
                emptyDivs(['display-info', 'title-error', 'description-error', 'price-error'])
                loading_text.innerHTML = "<span class='success'>Menu details updated successfuly</span> "
                edit_menu_title.innerHTML = "Edit " + title + " details."
            }
        })
        .catch (function (error) {
            loading_text.innerHTML = "Error while updating order details " + error
        })
    })
}

function deleteMenuItem(menu_id) {
    var delete_status = document.getElementById('delete_status')
    delete_status.innerHTML = "Deleting menu item... Please wait"
    var fetchedOrderData = fetchData('/api/v1/admins/menus/' + menu_id, 'DELETE', '')
    fetchedOrderData.then (function (jsonResponse) {
        emptyDivs(['delete_status'])
        redirectUnautheneticated('admin', jsonResponse, 500)
        if (jsonResponse.not_found_error) {
            delete_status.innerHTML = "Error  while Deleting menu item... " + jsonResponse.not_found_error
        } else if (jsonResponse.message) {
            emptyDivs(['show_menu_items'])
            delete_status.innerHTML = "<span class='success'>Menu item deleted successfuly</span>"
            //Reload menu items
            getMenus()
        }
    })
    .catch (function (error) {
        delete_status.innerHTML = "<span class='error'>Error while loading menu details " + error + "</span>" 
    })
}

function fetchData( url, method, body) {
    var append =''
    if (body) {
        append = {
            method: method,
            body: body,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': "Bearer " + readCookie('access_token')
            }
        }
    } else {
        append = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': "Bearer " + readCookie('access_token')
            }
        }
    }
    return fetch(url, append)
    .then( function (response) {
        return response.json()
    })
    .then ( function(jsonResponse) {
        return jsonResponse
    })
    .catch( function (error) {
        return error
    })
}

function redirectUnautheneticated(type, data, timeOut){
    var url = '/user/login'
    if ( type == 'admin') url = '/admin/login'
    if (data.msg) {
        alert("Ooops Authorization error \n\n" + data.msg)
        setTimeout(function () {
            window.location.href = url
        }, timeOut)
    } else if (data.error) {
        alert("Ooops Authorization error \n\n" + data.error)
        setTimeout(function () {
            window.location.href = url
        }, timeOut)
    }
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

function readCookie (name) {
    // Read cookie
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

// Create cookie
function createCookie(name, value, days) {
    var expires;
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        expires = "; expires="+date.toGMTString();
    }
    else {
        expires = "";
    }
    document.cookie = name+"="+value+expires+"; path=/";
}
