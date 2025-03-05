//Variables
const carrito = document.querySelector('#carrito');
const listaProductos = document.querySelector('#lista-Productos');
const contenedorCarrito = document.querySelector('#lista-carrito tbody');
const vaciarCarritoBtn = document.querySelector('#vaciar-carrito');
let articulosCarrito = [];

//Listeners *****
cargarEventListeners();


function cargarEventListeners () {
    //Cuando agregas un producto presionando 'Agregar al carrito'
    if (listaProductos){
        listaProductos.addEventListener('click', agregarProducto);
    }
    //listaProductos.addEventListener('click', agregarProducto);
    //Elimina producto del carrito
    carrito.addEventListener("click", eliminarProducto);

    //muestra los productos del storage
    document.addEventListener('DOMContentLoaded', () => {
        // recuerda si no hay productos en el carrito se agrega un array vácio para que no de error.
        articulosCarrito = JSON.parse(localStorage.getItem("carrito")) || [];
        carritoHTML();
    })
    // Vaciar carrito
    vaciarCarritoBtn.addEventListener("click", () => {
        articulosCarrito = [];
        limpiarHTML();
        carritoHTML();
    });
}

// Funciones ****************************************

function agregarProducto (e) {
    //e.preventDefault();
    // Delegation para agregar-carrito
    if (e.target.classList.contains('agregar-carrito')) {

        const producto = e.target.parentElement.parentElement;
        // Enviamos el curso seleccionado para tomar sus datos
        //console.log(producto);
        leerDatosProducto(producto);
        //productoAgregado(producto);
    }
}
function productoAgregado(producto){
    //Crear una alerta
    const alert = document.createElement("H4");
    alert.style.cssText = "background-color: red; color: white; text-align: center;";
    alert.style.margin = "5px 20px";
    alert.textContent = 'Añadido al carrito'
    producto.appendChild(alert);
    setTimeout(() => {
        alert.remove();
    }, 2000);
}

function eliminarProducto (e) {
    if (e.target.classList.contains('borrar-Producto')) {
        const productoId = e.target.getAttribute("data-id");
        console.log(productoId);
        //Elimina del arreglo por el data-id
        articulosCarrito = articulosCarrito.filter(
            (producto) => producto.id !== productoId
          );
        //articulosCarrito = articulosCarrito.filter(producto => producto.id !== productoId);
        carritoHTML();
    }
}

//Lee el contenido del HTML al que le dimos click y extrae la información del curso.
function leerDatosProducto (producto) {
    //console.log(producto);
    //Crear un objeto con el contenido del curso actual
    const infoProducto = {
        imagen: producto.querySelector("img").src,
        titulo: producto.querySelector(".name").textContent,
        precio: producto.querySelector(".precio span").textContent,
        id: producto.querySelector("button").getAttribute("data-id"),
        cantidad: 1,
    }
    // Revisa si un elemento ya existe en el carrito
    const existe = articulosCarrito.some(producto => producto.id === infoProducto.id);
    if (existe) {
        // Creamos una copia del arreglo
        const productos = articulosCarrito.map(producto => {

            if (producto.id === infoProducto.id) {
                producto.cantidad++;
                return producto; // este retorna el objeto actualizado
            } else {
                return producto;// retorna los que no son duplicados
            }
        });
        articulosCarrito = [ ...productos ];

    } else {
        articulosCarrito = [ ...articulosCarrito, infoProducto ];
    }

    //Agregar elementos al carrito  
    carritoHTML();
}


// Muestra el carrito de compras en el HTML
function carritoHTML () {

    limpiarHTML();
    let cont = 1;
    let total = 0;
    articulosCarrito.forEach(producto => {
        cont += producto.cantidad;
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>  
                <img src="${ producto.imagen }" width="100">
            </td>
            <td>${ producto.titulo }</td>
            <td>${ producto.precio } €</td>
            <td>${ producto.cantidad } </td>
            <td>
                <a href="#" class="borrar-Producto" data-id="${ producto.id }">X</a>
            </td>
        `;
        total += producto.precio * producto.cantidad;
        contenedorCarrito.appendChild(row);
    });

    if (cont > 1) {
        document.getElementById("total").style.display = "block";
        document.getElementById("cart_menu_num").style.display = "block";
        document.getElementById("suma").innerHTML = `Total: ${total} €`;
        document.getElementById("cart_menu_num").innerHTML = cont - 1;
      } else {
        document.getElementById("total").style.display = "none";
        document.getElementById("cart_menu_num").style.display = "none";
        total = 0;
      }
    // Agregar el carrito de compras al storage
    sincronizarStorage();

}
function sincronizarStorage() {
    localStorage.setItem("carrito", JSON.stringify(articulosCarrito));
}
// Elimina los productos del tbody
function limpiarHTML () {

    //forma lenta
    //:contenedorCarrito.innerHTML = '';
    while (contenedorCarrito.firstChild) {
        contenedorCarrito.removeChild(contenedorCarrito.firstChild)
    }
}

/* gestion del token login */
async function checkAuth() {
    let token = localStorage.getItem("token");
    if (!token) {
        
        setTimeout(() => window.location.href = "/", 2000);
        return;
    }

    let response = await fetch("/v1/protected", {
        headers: { "Authorization": "Bearer " + token }
    });

    let result = await response.json();
    
    if (response.ok) {

        //document.getElementById("message").innerText = result.message;
    } else {
        //document.getElementById("message").innerText = "Token inválido. Redirigiendo...";
        localStorage.removeItem("token");
        setTimeout(() => window.location.href = "/", 2000);
    }
}



document.querySelector(".menu-btn").addEventListener("mouseover", function() {
    document.getElementById("menuContent").classList.toggle("show");
});
function updateMenu() {
    let token = localStorage.getItem("token");
    if (token) {
        document.getElementById("loginLink").style.display = "none";
        document.getElementById("logoutLink").style.display = "block";
        //document.getElementById("welcomeMessage").innerText = "Bienvenido, usuario autenticado.";
    } else {
        document.getElementById("loginLink").style.display = "block";
        document.getElementById("logoutLink").style.display = "none";
        //document.getElementById("welcomeMessage").innerText = "Por favor, inicia sesión.";
    }
}
document.getElementById("logoutLink").addEventListener("click", function() {
    localStorage.removeItem("token");
    //updateMenu();
    setTimeout(() => window.location.href = "/", 2000);
    alert("Has cerrado sesión.");
});

document.getElementById("loginLink").addEventListener("click", function() {
    window.location.href = "index.html";  // Redirige a la página de login
});
updateMenu();
//checkAuth();