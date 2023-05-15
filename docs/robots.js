const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("animated-shown");
            // entry.target.classList.remove("animated-hidden");
        // } else {
        //     entry.target.classList.remove("animated-shown");
        //     // entry.target.classList.add("animated-hidden");
        }
    });
});

const hiddenWidgets = document.querySelectorAll('.animated-hidden')
hiddenWidgets.forEach((element) => {
    observer.observe(element);
});

document.addEventListener("DOMContentLoaded", (event) => {
    document.querySelectorAll('img').forEach((img) => {
        img.onerror = () => {
            this.style.display = 'none';
        };
    })
});