document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.card, .tariff-card, .review-card');
    cards.forEach((card, index) => {
        card.style.opacity = 0;
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = 1;
            card.style.transform = 'translateY(0)';
        }, index * 150);
    });

    const shopBtn = document.querySelector('button[onclick*="shop.html"]');
    const supportBtn = document.querySelector('button[onclick*="support.html"]');
    const reviewsBtn = document.querySelector('button[onclick*="reviews.html"]');

    if (shopBtn) {
        shopBtn.addEventListener('click', () => window.location.href = 'shop.html');
    }
    if (supportBtn) {
        supportBtn.addEventListener('click', () => window.location.href = 'Support/support.html');
    }
    if (reviewsBtn) {
        reviewsBtn.addEventListener('click', () => window.location.href = 'reviews.html');
    }
});