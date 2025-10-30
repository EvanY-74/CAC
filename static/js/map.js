let map;
let userMarker;
let markers = [];

// Initialize the map
function initMap() {
    map = L.map('map').setView([35.7596, -79.0193], 7); // North Carolina center
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    initializeEventListeners();
}

// Listen for address search & current location
function initializeEventListeners() {
    document.getElementById('search-btn').addEventListener('click', handleAddressSearch);
    document.getElementById('location-btn').addEventListener('click', handleCurrentLocation);
}

// Handle address search
async function handleAddressSearch() { //! test using this address: 1600 Amphitheatre Parkway, Mountain View, CA
    const address = document.getElementById('address-input').value.trim();
    if (!address) {
        showError('Please enter an address.');
        return;
    }
    
    showLoadingState();
    
    try {
        // Geocode address via Nominatim (OpenStreetMap)
        const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`);
        const data = await response.json();
        if (!data.length) throw new Error('Address not found.');
        
        const location = {
            lat: parseFloat(data[0].lat),
            lng: parseFloat(data[0].lon)
        };
        
        // Get polling locations from your Flask/Civi API
        const pollingData = await MyNCRep.makeAPIRequest(`/api/polling-locations?address=${encodeURIComponent(address)}`);
        
        if (pollingData.success) {
            displayPollingLocations(pollingData, location);
        } else {
            showError('Unable to find polling locations.');
        }
        
    } catch (err) {
        console.error(err);
        showError(err.message);
    } finally {
        hideLoadingState();
    }
}

// Handle current location
async function handleCurrentLocation() {
    showLoadingState();
    try {
        const pos = await MyNCRep.getCurrentLocation();
        const { latitude, longitude } = pos.coords;
        const userLoc = { lat: latitude, lng: longitude };
        
        // Get polling locations
        const pollingData = await MyNCRep.makeAPIRequest(`/api/polling-locations?lat=${latitude}&lng=${longitude}`);
        
        if (pollingData.success) {
            displayPollingLocations(pollingData, userLoc);
        } else {
            showError('Unable to find polling locations.');
        }
    } catch (err) {
        showError(err.message);
    } finally {
        hideLoadingState();
    }
}

// Display user & polling location markers
function displayPollingLocations(pollingData, userLocation) {
    clearMarkers();
    
    // Center on user location
    map.setView([userLocation.lat, userLocation.lng], 11);
    
    // Add user marker
    userMarker = L.marker([userLocation.lat, userLocation.lng], {
        icon: L.icon({
            iconUrl: 'https://cdn-icons-png.flaticon.com/512/64/64113.png', // black marker icon
            iconSize: [32, 32],
            iconAnchor: [16, 32]
        })
    }).addTo(map).bindPopup('<b>Your Location</b>').openPopup();
    
    // Add polling places
    const allLocations = [
        ...(pollingData.polling_locations || []),
        ...(pollingData.early_vote_sites || [])
    ];
    
    allLocations.forEach(loc => {
        if (!loc.address) return;
        
        const marker = L.marker([loc.lat, loc.lon], {
            icon: L.icon({
                iconUrl: loc.type === 'early_voting'
                    ? 'https://cdn-icons-png.flaticon.com/512/190/190411.png' // check mark
                    : 'https://cdn-icons-png.flaticon.com/512/684/684908.png', // red marker icon
                iconSize: [30, 30],
                iconAnchor: [15, 30]
            })
        })
        .addTo(map)
        .bindPopup(`
            <b>${loc.name}</b><br>
            ${loc.address}<br>
            <small>${loc.hours || ''}</small>
        `);
        
        markers.push(marker);
    });
}
    
    // Clear all markers
    function clearMarkers() {
        markers.forEach(m => map.removeLayer(m));
        markers = [];
        if (userMarker) {
            map.removeLayer(userMarker);
            userMarker = null;
        }
    }
    
    // UI helpers
    function showLoadingState() {
        document.getElementById('loading').classList.remove('d-none');
    }
    function hideLoadingState() {
        document.getElementById('loading').classList.add('d-none');
    }
    function showError(msg) {
        const err = document.getElementById('error-message');
        err.textContent = msg;
        err.classList.remove('d-none');
    }
    
    // Initialize
    initMap();
