console.log("Prueba de inicio")

/* Navigation */

function homePage() {
    console.log('Home');

    // Muestra la entrada de correo electrónico y el botón falso de suscripción
    titleTracker1.classList.remove('inactive');
    emailSelectionDiv.classList.remove('inactive');

    // Oculta la selección de monedas y el botón real de suscripción
    titleTracker2.classList.add('inactive');
    currencySelectionDiv.classList.add('inactive');
}

function currencySelection() {
    // Oculta la entrada de correo electrónico y el botón falso de suscripción
    emailSelectionDiv.classList.add('inactive');
    banner.classList.add('inactive');
    titleTracker1.classList.add('inactive');

    // Muestra la selección de monedas y el botón real de suscripción
    currencySelectionDiv.classList.remove('inactive');
    submitBtn.classList.remove('inactive');
    titleTracker2.classList.remove('inactive');

    // Actualiza el texto del botón según la cantidad de checkboxes seleccionados
    updateButtonCount();
}

/* Email Verification */

function checkEmailValidity() {
    // Verificar si el correo electrónico es válido
    if (!emailInput.checkValidity()) {
        alert('Please enter a valid email address.');
        return;
    }
    checkEmailExistence(window.location.origin, emailInput.value);
}

async function checkEmailExistence(domain, email) {
    try {
        const response = await fetch(`${domain}/api/check-email/`, {
            method: 'POST',
            body: JSON.stringify({ email: email }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            }
        });
        if (response.status !== 200) {
            throw new Error(
                `An error ocurred: ${response.status} ${response.statusText}`
            );
        }

        const data = await response.json()

        if (data.emailExists) {
            // Mostrar mensaje de error si el correo electrónico ya existe
            alert('This email is already registered.');
        } else {
            // Continuar con la selección de monedas si el correo electrónico no existe
            currencySelection();
        }

    } catch (error) {
        console.error(error.message);
    }

}

function getCsrfToken() {
    return document.querySelector('[name="csrfmiddlewaretoken"]').value;
}
    

/* Utils */

// Función para actualizar el texto del botón de envío según la cantidad de checkboxes seleccionados
function updateButtonCount() {
    const selectedCount = checkboxes.length ? `Track ${document.querySelectorAll('input[name="assets"]:checked').length} Currencies` : 'Select Currencies';
    submitBtn.textContent = selectedCount;
}

/* Event Listeners */

// Añade un evento de cambio a cada checkbox para actualizar el conteo al cambiar su estado
checkboxes.forEach((checkbox) => {
    checkbox.addEventListener('change', () => {
        // Actualizar el conteo de checkboxes seleccionados
        updateButtonCount();
        
        // Cambiar la visibilidad de los SVGs
        const uncheckedSVG = checkbox.nextElementSibling.querySelector('.unchecked');
        const checkedSVG = checkbox.nextElementSibling.querySelector('.checked');
        const currencyItem = checkbox.closest('.currency-item');
        
        if (checkbox.checked) {
            uncheckedSVG.classList.add('inactive');
            checkedSVG.classList.remove('inactive');
            currencyItem.classList.add('selected');
        } else {
            uncheckedSVG.classList.remove('inactive');
            checkedSVG.classList.add('inactive');
            currencyItem.classList.remove('selected');
        }
    });
});

// Manejar el evento submit del formulario
subscribeForm.addEventListener('submit', (event) => {
    // Verificar si la selección de monedas está oculta y si el campo de correo electrónico tiene el foco
    if (currencySelectionDiv.classList.contains('inactive') && document.activeElement === emailInput) {
        event.preventDefault(); // Prevenir que el formulario se envíe (cuando se presiona enter en el campo de correo electrónico)
        checkEmailValidity(); // Verificar email
    }
    // No es necesario un else aquí, si el display no está none, el formulario se enviará normalmente???
});

let itemsToShow = 2; // Número inicial de elementos a mostrar

// Inicialmente oculta todos los elementos excepto los dos primeros
allCurrencyItems.forEach((item, index) => {
    if (index >= itemsToShow) {
        item.classList.add('inactive');
    }
});

loadMoreButton.addEventListener('click', () => {
    // Incrementa la cantidad de elementos a mostrar
    itemsToShow += 2; // Ajusta este número según tus necesidades
    // Muestra los elementos según el nuevo límite
    allCurrencyItems.forEach((item, index) => {
        if (index < itemsToShow) {
            item.classList.remove('inactive');
        }
    });
    // Ocultar el botón mismo
    loadMoreButton.classList.add('inactive');
});

searchInput.addEventListener('input', () => {
    const searchText = searchInput.value.toLowerCase();

    allCurrencyItems.forEach((item) => {
        const assetName = item.querySelector('label').textContent.toLowerCase();
        if (assetName.includes(searchText)) {
            item.classList.remove('inactive');
        } else {
            item.classList.add('inactive');
        }
    });
});

emailBtn.addEventListener('click', checkEmailValidity);

window.addEventListener('DOMContentLoaded', homePage, false);



// Script to menu toggle

// MENU-TOGGLE
_toggle.onclick = () =>{
    console.log("toggle")
    _items.classList.toggle("open")
    _toggle.classList.toggle("close")
}
// Nuevo código para cerrar el menú al hacer clic fuera del #header_navbar
const _headerNavbar = document.getElementById('header_navbar');  // Asumiendo que este es el ID de tu navbar

document.addEventListener('click', function(event) {
  // Si el clic no fue en el navbar ni en el botón toggle
  if (!_headerNavbar.contains(event.target) && !_toggle.contains(event.target)) {
    _items.classList.remove("open");
    _toggle.classList.remove("close");
  }
});