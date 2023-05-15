const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("animated-shown");
        }
    });
});

const hiddenWidgets = document.querySelectorAll('.animated-hidden')
hiddenWidgets.forEach((element) => {
    observer.observe(element);
});
