//Variables
const carrito = document.querySelector('#carrito');
const listaProductos = document.querySelector('#lista-Productos');
const contenedorCarrito = document.querySelector('#lista-carrito tbody');
const vaciarCarritoBtn = document.querySelector('#vaciar-carrito');
let articulosCarrito = [];

//Listeners *****
cargarEventListeners();

function cargarEventListeners() {
    //Cuando agregas un producto presionando 'Agregar al carrito'
    if (listaProductos) {
        console.log("entra");
        
        document.querySelectorAll('.agregar_all').forEach((card) => {
            card.addEventListener('click', agregarProducto);
        });
    }

    // Para la página de detalles del producto
    const agregarDetalleBtn = document.querySelector('.agregar-detalle');
    if (agregarDetalleBtn) {
        agregarDetalleBtn.addEventListener('click', agregarProductoDesdeDetalle);
    }

    //Elimina producto del carrito
    carrito.addEventListener("click", eliminarProducto);

    //muestra los productos del storage
    document.addEventListener('DOMContentLoaded', () => {
        articulosCarrito = JSON.parse(localStorage.getItem("carrito")) || [];
        carritoHTML();
    });

    // Vaciar carrito
    vaciarCarritoBtn.addEventListener("click", () => {
        articulosCarrito = [];
        limpiarHTML();
        carritoHTML();
    });
}

// Funciones ****************************************

function agregarProducto(e) {
    if (e.target.classList.contains('agregar-carrito')) {
        const producto = e.target.closest('.card');
        leerDatosProducto(producto);
    }
}

function agregarProductoDesdeDetalle(e) {
    const producto = document.querySelector('.agregar-detalle');
    leerDatosProducto(producto);
}

function eliminarProducto(e) {
    if (e.target.classList.contains('borrar-Producto')) {
        const productoId = e.target.getAttribute("data-id");
        articulosCarrito = articulosCarrito.filter(producto => producto.product_id !== productoId);
        carritoHTML();
    }
}

//Lee el contenido del HTML al que le dimos click y extrae la información del curso.
function leerDatosProducto(producto) {
    const infoProducto = {
        imagen: producto.querySelector("img").src,
        titulo: producto.querySelector(".name").textContent,
        precio: parseFloat(producto.querySelector(".precio span").textContent),
        product_id: producto.querySelector("button").getAttribute("data-id"),
        cantidad: 1
    };

    const existe = articulosCarrito.some(producto => producto.product_id === infoProducto.product_id);
    if (existe) {
        const productos = articulosCarrito.map(producto => {
            if (producto.product_id === infoProducto.product_id) {
                producto.cantidad++;
                return producto;
            } else {
                return producto;
            }
        });
        articulosCarrito = [...productos];
    } else {
        articulosCarrito = [...articulosCarrito, infoProducto];
    }

    carritoHTML();
}

// Muestra el carrito de compras en el HTML
function carritoHTML() {
    limpiarHTML();
    let total = 0;
    let cont = 0;

    articulosCarrito.forEach(producto => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><img src="${producto.imagen}" width="100"></td>
            <td>${producto.titulo}</td>
            <td>${producto.precio} €</td>
            <td>${producto.cantidad}</td>
            <td><a href="#" class="borrar-Producto" data-id="${producto.product_id}">X</a></td>
        `;
        total += producto.precio * producto.cantidad;
        cont += producto.cantidad;
        contenedorCarrito.appendChild(row);
    });

    if (cont > 0) {
        document.getElementById("total").style.display = "block";
        document.getElementById("cart_menu_num").style.display = "block";
        document.getElementById("suma").innerHTML = `Total: ${total.toFixed(2)} €`;
        document.getElementById("cart_menu_num").innerHTML = cont;
    } else {
        document.getElementById("total").style.display = "none";
        document.getElementById("cart_menu_num").style.display = "none";
    }

    sincronizarStorage();
}

function sincronizarStorage() {
    localStorage.setItem("carrito", JSON.stringify(articulosCarrito));
}

// Elimina los productos del tbody
function limpiarHTML() {
    while (contenedorCarrito.firstChild) {
        contenedorCarrito.removeChild(contenedorCarrito.firstChild);
    }
}


document.querySelector(".menu-btn").addEventListener("mouseover", function() {
    document.getElementById("menuContent").classList.toggle("show");
});
async function updateMenu() {
    let token = localStorage.getItem("token");
    let response = await fetch("/v1/protected", {
        headers: { "Authorization": "Bearer " + token }
    });
    const userImage = document.getElementById("userImage");
    console.log(response);
    if (response.ok) {
        document.getElementById("loginLink").style.display = "none";
        document.getElementById("logoutLink").style.display = "block";
        userImage.src = "/v1/static/img/exit.png";
        
    } else {
        document.getElementById("loginLink").style.display = "block";
        document.getElementById("logoutLink").style.display = "none";
        userImage.src = "/v1/static/img/user.png";
        
    }
}

document.getElementById("logoutLink").addEventListener("click", function() {
    localStorage.removeItem("token");
    
    setTimeout(() => window.location.href = "/logout", 500);
    
});

document.getElementById("loginLink").addEventListener("click", function() {

    window.location.href = "/login";  
});
updateMenu();

async function enviarDatos() {
    if (document.getElementById("logoutLink").style.display !== "block") {
        window.location.href = "/register";
    } else {
        const token = localStorage.getItem("token");
        const carrito = JSON.parse(localStorage.getItem("carrito"));
        console.log(carrito);
        if (!carrito || carrito.length === 0) {
            alert("El carrito está vacío.");
            return;
        }

        try {
            const response = await fetch("/v1/buy", {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ carrito })
            });

            if (response.ok) {
                
                articulosCarrito = [];
                localStorage.removeItem("carrito");
                
                setTimeout(() => window.location.href = "/invoice", 1000);
            } else {
                alert("Error al realizar la compra.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Hubo un problema al procesar la compra.");
        }
    }
}
document.getElementById("buy").addEventListener("click", function() {
    enviarDatos(); 
});
