console.log("Sanity check!")

// # PRODUCTION: Change selector to .rentBtn for it to work!
let rentButtons = document.querySelectorAll(".rentBtn");

fetch("/tenant/stripe_config/")
.then((result) => { return result.json(); })
.then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    // Event handler
    for (let rentButton of rentButtons) {
        rentButton.addEventListener("click", e => {
            e.preventDefault();

            // Get Checkout Session ID
            fetch("/tenant/create-checkout-session/")
            .then((result) => { return result.json(); })
            .then((data) => {
                console.log(data);
                
                // Redirect to Stripe Checkout
                return stripe.redirectToCheckout({sessionId: data.sessionId})
            })
            .then((res) => {
                console.log(res);
            });
        });
    }
});  