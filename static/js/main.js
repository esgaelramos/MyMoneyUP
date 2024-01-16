console.log("Prueba de inicio")

document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector('#subscribeForm');
    var emailInput = document.querySelector('#emailSelection input[type=email]');
    var currencySelectionDiv = document.getElementById('currencySelection');
    var submitBtn = document.getElementById('submitBtn');
    var checkboxes = document.querySelectorAll('input[name="assets"]');
    var titleTracker2 = document.getElementById('titleTracker2');

    // Función para mostrar la selección de monedas y ocultar la selección de correo electrónico
    window.showCurrencySelection = function() {
        var email = emailInput.value;
        // Verificar si el correo electrónico es válido
        if (!emailInput.checkValidity()) {
            alert('Please enter a valid email address.');
            return;
        }

        // Hacer la llamada AJAX
        var domain = window.location.origin;
        fetch( domain + '/api/check-email/', {
            method: 'POST',
            body: JSON.stringify({ email: email }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.emailExists) {
                // Mostrar mensaje de error si el correo electrónico ya existe
                alert('This email is already registered.');
            } else {
                // Continuar con la selección de monedas si el correo electrónico no existe
                proceedToShowCurrencySelection();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function getCsrfToken() {
        return document.querySelector('[name="csrfmiddlewaretoken"]').value;
    }
    
    function proceedToShowCurrencySelection() {
        // Oculta la entrada de correo electrónico y el botón falso de suscripción
        document.getElementById('emailSelection').style.display = 'none';
        document.getElementById('banner').style.display = 'none';
        document.getElementById('titleTracker1').style.display = 'none';
    
        // Muestra la selección de monedas y el botón real de suscripción
        currencySelectionDiv.style.display = 'block';
        submitBtn.style.display = 'block';
        titleTracker2.style.display = 'block';
    
        // Actualiza el texto del botón según la cantidad de checkboxes seleccionados
        updateButtonCount();
    }
    

    // Función para actualizar el texto del botón de envío según la cantidad de checkboxes seleccionados
    function updateButtonCount() {
        var selectedCount = checkboxes.length ? `Track ${document.querySelectorAll('input[name="assets"]:checked').length} Currencies` : 'Select Currencies';
        submitBtn.textContent = selectedCount;
    }

    // Añade un evento de cambio a cada checkbox para actualizar el conteo al cambiar su estado
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            // Actualizar el conteo de checkboxes seleccionados
            updateButtonCount();
            
            // Cambiar la visibilidad de los SVGs
            var uncheckedSVG = checkbox.nextElementSibling.querySelector('.unchecked');
            var checkedSVG = checkbox.nextElementSibling.querySelector('.checked');
            var currencyItem = checkbox.closest('.currency-item');
            
            if (checkbox.checked) {
                uncheckedSVG.style.display = 'none';
                checkedSVG.style.display = 'block';
                currencyItem.classList.add('selected');
            } else {
                uncheckedSVG.style.display = 'block';
                checkedSVG.style.display = 'none';
                currencyItem.classList.remove('selected');
            }
        });
    });

    // Manejar el evento submit del formulario
    form.addEventListener('submit', function(event) {
        // Verificar si la selección de monedas está oculta y si el campo de correo electrónico tiene el foco
        if (currencySelectionDiv.style.display === 'none' && document.activeElement === emailInput) {
            event.preventDefault(); // Prevenir que el formulario se envíe (cuando se presiona enter en el campo de correo electrónico)
            showCurrencySelection(); // Mostrar la selección de monedas
        }
        // No es necesario un else aquí, si el display no está none, el formulario se enviará normalmente???
    });

    var loadMoreButton = document.getElementById('loadMoreButton');
    var allCurrencyItems = document.querySelectorAll('.currency-item');
    var itemsToShow = 2; // Número inicial de elementos a mostrar

    // Inicialmente oculta todos los elementos excepto los dos primeros
    allCurrencyItems.forEach(function(item, index) {
        if (index >= itemsToShow) {
            item.style.display = 'none';
        }
    });

    loadMoreButton.addEventListener('click', function() {
        // Incrementa la cantidad de elementos a mostrar
        itemsToShow += 2; // Ajusta este número según tus necesidades
        // Muestra los elementos según el nuevo límite
        allCurrencyItems.forEach(function(item, index) {
            if (index < itemsToShow) {
                item.style.display = 'block';
            }
        });
        // Ocultar el botón mismo
        loadMoreButton.style.display = 'none'

    });

    var searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', function() {
        var searchText = searchInput.value.toLowerCase();

        allCurrencyItems.forEach(function(item) {
            var assetName = item.querySelector('label').textContent.toLowerCase();
            if (assetName.includes(searchText)) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });

    // Inicializa el estado del botón de envío
    updateButtonCount();
});

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