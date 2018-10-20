class Menu {
    init () {
        this.render ()
    }

    render () {
        var show_menu_items = document.getElementById('show_menu_items')
        let submit_menu_form = document.getElementById('add_menu_form')

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
    }
}

let menu = new Menu()
menu.init()

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
        //If missing Authorization, Expired or invalid token
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
            alert("Ooops Authorization error \n\n" + jsonResponse.msg)
            setTimeout(function () {
                window.location.href = "/admin/login"
            }, 1000)
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
            }, 1000)
        } else if (jsonResponse.error) {
            alert("Ooops Authorization error \n\n" + jsonResponse.error)
            setTimeout(function () {
                window.location.href = "/admin/login"
            }, 1000)
        } else if (jsonResponse.menus) {
            emptyDivs(['loading-text'])
            //If response contains menus, display items
            var titleDiv  = document.getElementById('menu_title')
            titleDiv.innerHTML = "Menu Items [" + jsonResponse.menus.length + "]"
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
                '</div>'
                fragment.appendChild(menuItem)
            }
            menu_items_element.appendChild(fragment)
        }
    })
    .catch (function (error) {
        console.log("Error " + error)
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