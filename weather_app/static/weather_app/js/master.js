 // Navbar scroll effect
 window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Add active class based on current page
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.parentElement.classList.add('active');
        }
    });
});





document.addEventListener('DOMContentLoaded', function() {
    const weatherForm = document.querySelector('.search-form');
    const weatherResults = document.querySelector('.weather-card-container');
    const errorDisplay = document.querySelector('.error-display');
    
    if (weatherForm) {
        weatherForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(weatherForm);
            const searchParams = new URLSearchParams(formData);
            
            // Show loading state
            const submitButton = weatherForm.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="bi bi-hourglass me-2"></i> Searching...';
            
            axios.get(`?${searchParams.toString()}`)
                .then(response => {
                    // Parse the HTML response
                    const parser = new DOMParser();
                    const htmlDoc = parser.parseFromString(response.data, 'text/html');
                    
                    // Extract the weather card or error message
                    const newWeatherCard = htmlDoc.querySelector('.weather-card');
                    const newError = htmlDoc.querySelector('.error-message');
                    
                    // Clear previous results
                    if (weatherResults) weatherResults.innerHTML = '';
                    if (errorDisplay) errorDisplay.innerHTML = '';
                    
                    // Update the DOM
                    if (newWeatherCard) {
                        weatherResults.innerHTML = newWeatherCard.outerHTML;
                    } else if (newError) {
                        errorDisplay.innerHTML = newError.outerHTML;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    if (errorDisplay) {
                        errorDisplay.innerHTML = `
                            <div class="error-message">
                                <i class="bi bi-exclamation-triangle-fill"></i> 
                                Failed to fetch weather data. Please try again.
                            </div>
                        `;
                    }
                })
                .finally(() => {
                    // Reset button state
                    submitButton.disabled = false;
                    submitButton.innerHTML = '<i class="bi bi-search me-2"></i> Search';
                });
        });
    }
});