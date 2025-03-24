let shops = JSON.parse(localStorage.getItem('shops') || '[]');
let products = JSON.parse(localStorage.getItem('products') || '[]');

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
}

function addShop() {
    const shopName = document.getElementById('shopName').value;
    if (shopName) {
        shops.push({ name: shopName, id: Date.now() });
        updateShopList();
        updateShopSelect();
        updateOverview();
        document.getElementById('shopName').value = '';
        syncWithCustomer();
        showToast('Shop added successfully!');
    } else {
        showToast('Please enter a shop name.');
    }
}

function editShop(shopId) {
    const shop = shops.find(s => s.id === shopId);
    const newName = prompt('Enter new shop name:', shop.name);
    if (newName) {
        shop.name = newName;
        updateShopList();
        updateShopSelect();
        updateOverview();
        syncWithCustomer();
        showToast('Shop updated successfully!');
    }
}

function deleteShop(shopId) {
    if (confirm('Are you sure you want to delete this shop? All associated products will also be deleted.')) {
        shops = shops.filter(s => s.id !== shopId);
        products = products.filter(p => p.shopId !== shopId);
        updateShopList();
        updateShopSelect();
        updateOverview();
        syncWithCustomer();
        showToast('Shop deleted successfully!');
    }
}

function addProduct() {
    const shopId = document.getElementById('shopSelect').value;
    const productName = document.getElementById('productName').value;
    const quantity = document.getElementById('quantity').value;
    const price = document.getElementById('price').value;
    const category = document.getElementById('category').value;
    const imageInput = document.getElementById('productImage');
    let imageData = null;

    if (shopId && productName && quantity && price) {
        if (imageInput.files && imageInput.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imageData = e.target.result;
                products.push({ shopId, name: productName, quantity: parseInt(quantity), price: parseInt(price), category, image: imageData, id: Date.now() });
                updateProductList();
                updateOverview();
                updateAnalytics();
                resetProductForm();
                syncWithCustomer();
                showToast('Product added successfully!');
            };
            reader.readAsDataURL(imageInput.files[0]);
        } else {
            products.push({ shopId, name: productName, quantity: parseInt(quantity), price: parseInt(price), category, image: null, id: Date.now() });
            updateProductList();
            updateOverview();
            updateAnalytics();
            resetProductForm();
            syncWithCustomer();
            showToast('Product added successfully!');
        }
    } else {
        showToast('Please fill in all required fields.');
    }
}

function editProduct(productId) {
    const product = products.find(p => p.id === productId);
    const newName = prompt('Enter new product name:', product.name);
    const newQuantity = prompt('Enter new quantity:', product.quantity);
    const newPrice = prompt('Enter new price:', product.price);
    if (newName && newQuantity && newPrice) {
        product.name = newName;
        product.quantity = parseInt(newQuantity);
        product.price = parseInt(newPrice);
        updateProductList();
        updateOverview();
        updateAnalytics();
        syncWithCustomer();
        showToast('Product updated successfully!');
    }
}

function deleteProduct(productId) {
    if (confirm('Are you sure you want to delete this product?')) {
        products = products.filter(p => p.id !== productId);
        updateProductList();
        updateOverview();
        updateAnalytics();
        syncWithCustomer();
        showToast('Product deleted successfully!');
    }
}

function resetProductForm() {
    document.getElementById('productName').value = '';
    document.getElementById('quantity').value = '';
    document.getElementById('price').value = '';
    document.getElementById('productImage').value = '';
}

function updateShopList() {
    const shopList = document.getElementById('shopList');
    const searchQuery = document.getElementById('shopSearch').value.toLowerCase();
    shopList.innerHTML = shops
        .filter(shop => shop.name.toLowerCase().includes(searchQuery))
        .map(shop => `
            <div class="list-item">
                <div>${shop.name}</div>
                <div>
                    <a href="#" onclick="editShop(${shop.id})">Edit</a>
                    <button onclick="deleteShop(${shop.id})">Delete</button>
                </div>
            </div>
        `).join('');
}

function updateShopSelect() {
    const shopSelect = document.getElementById('shopSelect');
    shopSelect.innerHTML = '<option value="">Select Shop</option>' + 
        shops.map(shop => `<option value="${shop.id}">${shop.name}</option>`).join('');
}

function updateProductList() {
    const productList = document.getElementById('productList');
    const searchQuery = document.getElementById('productSearch').value.toLowerCase();
    productList.innerHTML = products
        .filter(product => product.name.toLowerCase().includes(searchQuery))
        .map(product => {
            const shop = shops.find(s => s.id == product.shopId);
            return `
                <div class="list-item ${product.quantity <= 5 ? 'low-stock' : ''}">
                    <div>
                        ${product.image ? `<img src="${product.image}" alt="${product.name}">` : '📦'}
                        ${product.name} - ${shop ? shop.name : 'Unknown Shop'} (Qty: ${product.quantity}, ₹${product.price.toLocaleString()})
                    </div>
                    <div>
                        <a href="#" onclick="editProduct(${product.id})">Edit</a>
                        <button onclick="deleteProduct(${product.id})">Delete</button>
                    </div>
                </div>`;
        }).join('');
}

function updateOverview() {
    document.getElementById('totalStores').textContent = shops.length;
    document.getElementById('totalProducts').textContent = products.length;
    document.getElementById('lowStock').textContent = products.filter(p => p.quantity <= 5).length;
    document.getElementById('outOfStock').textContent = products.filter(p => p.quantity === 0).length;

    const recentStores = document.getElementById('recentStores');
    recentStores.innerHTML = shops.slice(-2).map(shop => {
        const shopProducts = products.filter(p => p.shopId == shop.id);
        return `
            <div class="list-item">
                <div>
                    🏪 ${shop.name}
                    <small>${shopProducts.length} products</small>
                </div>
                <a href="#" onclick="showSection('stores')">View</a>
            </div>`;
    }).join('');

    const recentProducts = document.getElementById('recentProducts');
    recentProducts.innerHTML = products.slice(-4).map(product => {
        return `
            <div class="list-item ${product.quantity <= 5 ? 'low-stock' : ''}">
                <div>
                    ${product.image ? `<img src="${product.image}" alt="${product.name}">` : '📦'}
                    ${product.name}
                    <small>₹${product.price.toLocaleString()}</small>
                </div>
                <a href="#" onclick="showSection('products')">View</a>
            </div>`;
    }).join('');
}

function updateAnalytics() {
    const ctx = document.getElementById('analyticsChart').getContext('2d');
    const categories = ['Electronics', 'Fashion', 'Home', 'Other'];
    const data = categories.map(category => 
        products.filter(p => p.category === category).length
    );

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: categories,
            datasets: [{
                label: 'Products by Category',
                data: data,
                backgroundColor: 'rgba(26, 26, 26, 0.7)',
                borderColor: 'rgba(26, 26, 26, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function syncWithCustomer() {
    localStorage.setItem('shops', JSON.stringify(shops));
    localStorage.setItem('products', JSON.stringify(products));
}

function showSection(section) {
    document.getElementById('overviewSection').style.display = 'none';
    document.getElementById('storesSection').style.display = 'none';
    document.getElementById('productsSection').style.display = 'none';
    document.getElementById('analyticsSection').style.display = 'none';
    document.getElementById(`${section}Section`).style.display = 'block';

    document.querySelectorAll('.sidebar a').forEach(link => link.classList.remove('active'));
    document.querySelector(`.sidebar a[onclick="showSection('${section}')"]`).classList.add('active');

    if (section === 'analytics') {
        updateAnalytics();
    }
}

function searchShops() {
    updateShopList();
}

function searchProducts() {
    updateProductList();
}

updateShopSelect();
updateShopList();
updateProductList();
updateOverview();
