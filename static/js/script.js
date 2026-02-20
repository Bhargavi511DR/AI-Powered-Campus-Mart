// Main JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add to cart functionality
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            addToCart(productId);
        });
    });

    // Search functionality
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchTerm = this.querySelector('input[name="search"]').value;
            if (searchTerm.trim()) {
                window.location.href = `/products?search=${encodeURIComponent(searchTerm)}`;
            }
        });
    }

    // Category filter
    const categorySelect = document.getElementById('category-select');
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            const category = this.value;
            const currentUrl = new URL(window.location);
            
            if (category) {
                currentUrl.searchParams.set('category', category);
            } else {
                currentUrl.searchParams.delete('category');
            }
            
            window.location.href = currentUrl.toString();
        });
    }
});

// Add to cart function
async function addToCart(productId, quantity = 1) {
    try {
        const response = await fetch('/add_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `product_id=${productId}&quantity=${quantity}`
        });

        const data = await response.json();

        if (data.success) {
            showNotification('Product added to cart!', 'success');
            updateCartCount();
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        showNotification('Error adding product to cart', 'error');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const alertClass = type === 'success' ? 'alert-success' : 
                      type === 'error' ? 'alert-danger' : 'alert-info';

    const notification = document.createElement('div');
    notification.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
    `;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(notification);

    // Auto remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

// Update cart count in navbar
function updateCartCount() {
    // This would typically fetch the current cart count from the server
    const cartBadge = document.querySelector('.cart-count-badge');
    if (cartBadge) {
        // Increment count (you would get actual count from server in real implementation)
        const currentCount = parseInt(cartBadge.textContent) || 0;
        cartBadge.textContent = currentCount + 1;
    }
}

// Product search with AI suggestions
function setupProductSearch() {
    const searchInput = document.querySelector('input[name="search"]');
    const suggestionsContainer = document.createElement('div');
    suggestionsContainer.className = 'search-suggestions dropdown-menu';
    suggestionsContainer.style.cssText = 'width: 100%; max-height: 200px; overflow-y: auto;';
    
    if (searchInput) {
        searchInput.parentNode.appendChild(suggestionsContainer);

        searchInput.addEventListener('input', async function() {
            const query = this.value.trim();
            
            if (query.length < 2) {
                suggestionsContainer.style.display = 'none';
                return;
            }

            try {
                // Get AI-powered search suggestions
                const response = await fetch('/ai-search-suggestions', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query })
                });

                const suggestions = await response.json();
                showSearchSuggestions(suggestions, query);
            } catch (error) {
                console.error('Error getting search suggestions:', error);
            }
        });

        // Hide suggestions when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
                suggestionsContainer.style.display = 'none';
            }
        });
    }
}

function showSearchSuggestions(suggestions, query) {
    const container = document.querySelector('.search-suggestions');
    container.innerHTML = '';

    if (suggestions.length === 0) {
        container.style.display = 'none';
        return;
    }

    suggestions.forEach(suggestion => {
        const suggestionItem = document.createElement('a');
        suggestionItem.className = 'dropdown-item';
        suggestionItem.href = '#';
        suggestionItem.textContent = suggestion;
        suggestionItem.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector('input[name="search"]').value = suggestion;
            container.style.display = 'none';
            document.getElementById('search-form').submit();
        });
        container.appendChild(suggestionItem);
    });

    container.style.display = 'block';
}