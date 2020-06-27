/*
    core logic/payment flow from stripe documentation:
    https://stripe.com/docs/payments/accept-a-payment
    
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Open Sans", sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#542f34'
        }
    },
    invalid: {
        color: '#33266e',
        iconColor: '#33266e'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');

// validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// form submit from stripe documentation
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        if (result.error) {
        // shows error message to customer
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            // re enable to fix card error
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        } else {
        // shows payment success message 
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});