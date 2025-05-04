$(document).ready(function() {
    console.log("Stripe JS: Initializing payment system...");

    // 1. Get Stripe configuration from template
    var stripePublicKey = $('#id_stripe_public_key').text().trim();
    var clientSecret = $('#id_client_secret').text().trim();
    
    // 2. Validate configuration
    if (!stripePublicKey || !clientSecret) {
        console.error("Stripe configuration missing!");
        $('#card-errors').html(`
            <span class="icon"><i class="fas fa-exclamation-triangle"></i></span>
            <span>Payment system configuration error. Please refresh the page.</span>
        `);
        return;
    }

    // 3. Initialize Stripe
    var stripe = Stripe(stripePublicKey);
    var elements = stripe.elements();
    
    // 4. Card element styling
    var style = {
        base: {
            color: '#32325d',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#fa755a',
            iconColor: '#fa755a'
        }
    };

    // 5. Create and mount card element
    var card = elements.create('card', {style: style});
    try {
        card.mount('#card-element');
        console.log("Card element mounted successfully");
    } catch (err) {
        console.error("Failed to mount card element:", err);
        return;
    }

    // 6. Real-time validation
    card.addEventListener('change', function(event) {
        var displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.innerHTML = `
                <span class="icon"><i class="fas fa-times"></i></span>
                <span>${event.error.message}</span>
            `;
        } else {
            displayError.textContent = '';
        }
    });

    // 7. Form submission handler
    var form = document.getElementById('payment-form');
    if (!form) {
        console.error("Payment form not found!");
        return;
    }

    form.addEventListener('submit', function(ev) {
        ev.preventDefault();
        console.log("Form submission intercepted");

        // UI State Management
        var submitButton = $('#submit-button');
        var loadingOverlay = $('#loading-overlay');
        
        submitButton.attr('disabled', true);
        loadingOverlay.fadeIn(100);
        card.update({disabled: true});

        // 8. Cache checkout data first
        var cacheData = {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'client_secret': clientSecret,
            'save_info': $('#id-save-info').is(':checked')
        };

        $.ajax({
            url: '/checkout/cache_checkout_data/',
            type: 'POST',
            data: cacheData,
            success: function() {
                console.log("Checkout data cached successfully");
                processPayment();
            },
            error: function(xhr) {
                handleError("Failed to cache checkout data", xhr);
            }
        });

        function processPayment() {
            // 9. Confirm card payment with Stripe
            stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: getBillingDetails()
                },
                shipping: getShippingDetails()
            }).then(function(result) {
                if (result.error) {
                    handleStripeError(result.error);
                } else {
                    handlePaymentSuccess(result.paymentIntent);
                }
            });
        }

        function getBillingDetails() {
            return {
                name: $.trim(form.full_name.value),
                email: $.trim(form.email.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    state: $.trim(form.county.value),
                    postal_code: $.trim(form.postcode.value),
                    country: $.trim(form.country.value)
                }
            };
        }

        function getShippingDetails() {
            return {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    state: $.trim(form.county.value),
                    postal_code: $.trim(form.postcode.value),
                    country: $.trim(form.country.value)
                }
            };
        }

        function handleStripeError(error) {
            console.error("Stripe error:", error);
            $('#card-errors').html(`
                <span class="icon"><i class="fas fa-times"></i></span>
                <span>${error.message}</span>
            `);
            resetFormState();
        }

        function handlePaymentSuccess(paymentIntent) {
            if (paymentIntent.status === 'succeeded') {
                console.log("Payment succeeded, submitting form");
                form.submit();
            } else {
                handleError("Unexpected payment status: " + paymentIntent.status);
            }
        }

        function handleError(message, xhr) {
            console.error(message, xhr);
            $('#card-errors').html(`
                <span class="icon"><i class="fas fa-exclamation-triangle"></i></span>
                <span>${message}. Please try again.</span>
            `);
            resetFormState();
        }

        function resetFormState() {
            loadingOverlay.fadeOut(100);
            submitButton.attr('disabled', false);
            card.update({disabled: false});
        }
    });

    console.log("Stripe payment system initialized successfully");
});