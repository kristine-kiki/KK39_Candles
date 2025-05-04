var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);

// Initialize Stripe object
var stripe = Stripe(stripePublicKey);

// Initialize Elements (Stripe's UI library)
var elements = stripe.elements();

// Define basic styling for the Card Element
// Matches Bootstrap's form control styling mostly
var style = {
    base: {
        color: '#333333', // Dark text
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4' // Placeholder color
        }
    },
    invalid: {
        color: '#dc3545', // Bootstrap danger color for errors
        iconColor: '#dc3545'
    }
};

// Create an instance of the Card Element
var card = elements.create('card', {style: style});

// Mount the Card Element to the div '#card-element' in your form
card.mount('#card-element');


card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>`;
        $(errorDiv).html(html); // Use jQuery to set HTML content
    } else {
        errorDiv.textContent = ''; // Clear errors if valid
    }
});

var form = document.getElementById('payment-form');
var submitButton = document.getElementById('submit-button');
var loadingOverlay = $('#loading-overlay'); // Use jQuery selector for overlay

form.addEventListener('submit', function(ev) {
    ev.preventDefault(); // Prevent the default form submission

    // Disable card element and submit button, show overlay
    card.disable();
    $(submitButton).attr('disabled', true);
    loadingOverlay.fadeToggle(100); // Show loading overlay

    // --- Pre-payment step: Cache checkout data ---
    // Create a FormData object with necessary data for caching
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val(); // Get CSRF token using jQuery
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        // Optional: Include save_info if you want to cache that decision too
        // 'save_info': Boolean($('#id-save-info').is(':checked')),
    };
    var url = '/checkout/cache_checkout_data/'; // The URL for your caching view

    // Use jQuery's $.post for simplicity here
    $.post(url, postData).done(function () {
        // If caching is successful, proceed to confirm payment with Stripe
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address:{
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        country: $.trim(form.country.value),
                        state: $.trim(form.county.value), // Stripe uses 'state' for county/province
                        postal_code: $.trim(form.postcode.value), // Ensure this matches form field name
                    }
                }
            },
            shipping: { // Include shipping details if different or required by Stripe settings
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value), // Ensure this matches form field name
                    state: $.trim(form.county.value),
                }
            },
        }).then(function(result) {
            // Handle result from Stripe
            if (result.error) {
                // Show error to your customer (e.g., insufficient funds)
                var errorMsg = `
                    <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(errorMsg);

                // Hide overlay, re-enable card element and submit button
                loadingOverlay.fadeToggle(100);
                card.enable();
                $(submitButton).attr('disabled', false);

            } else {
                // The payment has been processed!
                if (result.paymentIntent.status === 'succeeded') {
                    // Payment successful, submit the form to the Django backend
                    // to save the order details.
                    form.submit();
                }
            }
        });
    });
}) 
