particlesJS("particles-js", {
    "particles": {
        "number": {
            "value": 80,  // Particles ki sankhya
            "density": {
                "enable": true,
                "value_area": 800
            }
        },
        "color": {
            "value": "#ffffff"  // Particles ka rang (white)
        },
        "shape": {
            "type": "circle",  // Particles ka shape (circle, edge, triangle, polygon)
            "stroke": {
                "width": 0,
                "color": "#000000"
            },
            "polygon": {
                "nb_sides": 5  // Agar polygon shape ho toh kitne sides honge
            }
        },
        "opacity": {
            "value": 0.5,
            "random": false,
            "anim": {
                "enable": false,
                "speed": 1,
                "opacity_min": 0.1,
                "sync": false
            }
        },
        "size": {
            "value": 3,
            "random": true,
            "anim": {
                "enable": false,
                "speed": 40,
                "size_min": 0.1,
                "sync": false
            }
        },
        "line_linked": {
            "enable": true,  // Particles ke beech lines
            "distance": 150,
            "color": "#ffffff",
            "opacity": 0.4,
            "width": 1
        },
        "move": {
            "enable": true,  // Particles move karenge ya nahi
            "speed": 3,  // Speed of movement
            "direction": "none",  // Direction (none, top, top-right, right, etc.)
            "random": false,
            "straight": false,
            "out_mode": "out",  // Bahar jane par disappear ho ya bounce kare
            "bounce": false,
            "attract": {
                "enable": false,
                "rotateX": 600,
                "rotateY": 1200
            }
        }
    },
    "interactivity": {
        "detect_on": "canvas",
        "events": {
            "onhover": {
                "enable": true,
                "mode": "repulse"  // Cursor par hover hone par particles hatenge
            },
            "onclick": {
                "enable": true,
                "mode": "push"  // Click karne par naye particles add honge
            },
            "resize": true  // Window resize hone par adjust ho
        },
        "modes": {
            "grab": {
                "distance": 400,
                "line_linked": {
                    "opacity": 1
                }
            },
            "bubble": {
                "distance": 400,
                "size": 40,
                "duration": 2,
                "opacity": 8,
                "speed": 3
            },
            "repulse": {
                "distance": 100,
                "duration": 0.4
            },
            "push": {
                "particles_nb": 4
            },
            "remove": {
                "particles_nb": 2
            }
        }
    },
    "retina_detect": true
});
