// Wait for the DOM to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', () => {
    // Get all the necessary elements from the DOM
    const openBasketBtn = document.getElementById('open-basket-btn');
    const basketSidebar = document.getElementById('basket-sidebar');
    const basketOverlay = document.getElementById('basket-overlay');

    // Function to open the basket
    const openBasket = () => {
        basketSidebar.classList.add('is-active');
        basketOverlay.classList.add('is-active');
        document.body.classList.add('basket-open'); // Prevent background scrolling
    };

    // Function to close the basket
    const closeBasket = () => {
        basketSidebar.classList.remove('is-active');
        basketOverlay.classList.remove('is-active');
        document.body.classList.remove('basket-open');
    };

    // Event listener for the floating button
    openBasketBtn.addEventListener('click', openBasket);

    // Event listener for the overlay (to close when clicking outside)
    basketOverlay.addEventListener('click', closeBasket);

    // Optional: Close the basket with the 'Escape' key
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && basketSidebar.classList.contains('is-active')) {
            closeBasket();
        }
    });
});