ScrollReveal({
    delay: 200,
    interval: 400,
    //reset: true
});

ScrollReveal().reveal(".section-1, .section-2, .section-4, .footer-animation", {
    interval: 500,
    distance: '50px',
    origin: 'bottom',
    duration: '400',
    easing: 'ease-in'
});

ScrollReveal().reveal(".feature-block", {interval: 300, distance: '50px', origin: 'bottom', duration: '300', easing: 'ease-in'});

ScrollReveal().reveal(".sec-4-text", {distance: '50px', origin: 'left', duration: '400', easing: 'ease-in'});