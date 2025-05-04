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