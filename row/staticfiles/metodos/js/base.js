// Configuración de Tailwind
tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: '#4F46E5',
                secondary: '#10B981',
                dark: '#1F2937',
                light: '#F9FAFB'
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                logo: ['Poppins', 'sans-serif']
            }
        }
    }
};

// Menú móvil
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
});