document.addEventListener('DOMContentLoaded', function () {
    const revealItems = Array.from(document.querySelectorAll('.pf-reveal'));

    function revealElement(element, delay) {
        window.setTimeout(() => {
            element.classList.add('pf-reveal--visible');
        }, delay);
    }

    if ('IntersectionObserver' in window && revealItems.length) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    const index = revealItems.indexOf(entry.target);
                    const delay = Math.min(index * 100, 300);
                    revealElement(entry.target, delay);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.15,
        });

        revealItems.forEach((item) => observer.observe(item));
    } else {
        revealItems.forEach((item, index) => {
            revealElement(item, Math.min(index * 100, 300));
        });
    }
});
