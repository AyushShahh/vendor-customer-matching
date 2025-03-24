const searchForm = document.getElementById('search-form');
const filterPrice = document.getElementById('filter-price');
const filterRating = document.getElementById('filter-rating');
const filterArea = document.getElementById('filter-area');
const filterShop = document.getElementById('filter-shop');
const filterCategory = document.getElementById('filter-category');


searchForm.addEventListener('submit', event => {
    event.preventDefault();
    const query = searchForm.querySelector('input').value;
    console.log('Search query:', query);
    
});


[filterPrice, filterRating, filterArea, filterShop, filterCategory].forEach(filter => {
    filter.addEventListener('change', () => {
        console.log(`${filter.id} changed to:`, filter.value);
        
    });
});


document.querySelectorAll('.sidebar a:not(.profile-link)').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});
