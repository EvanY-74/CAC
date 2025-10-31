let map;
let userMarker;
let markers = [];

// Initialize the map
function initMap() {
    map = L.map('map').setView([36.7783, -119.4179], 6); // California center
    
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
    // Reset valid address flag
    isValidAddress = false;
    
    // Clear any previous successful search state
    clearMarkers();
    
    const address = document.getElementById('address-input').value.trim();
    
    // Basic input validation
    if (!address) {
        showError('Please enter an address.');
        return;
    }

    // Check for minimum address components
    const addressParts = address.split(',').map(part => part.trim());
    
    // Validate address format
    if (addressParts.length < 3) {
        showError(`
            Your address is incomplete. Please include:
            1. Street address (e.g., 555 Market Street)
            2. City (e.g., San Francisco)
            3. State and ZIP (e.g., CA 94105)
            
            Example: 555 Market Street, San Francisco, CA 94105
        `);
        return;
    }

    // Validate street address
    const streetAddress = addressParts[0];
    if (!streetAddress.match(/\d+/)) {
        showError('Please include a street number in your address.\nExample: 555 Market Street, San Francisco, CA 94105');
        return;
    }

    // Validate state
    const lastPart = addressParts[addressParts.length - 1].toLowerCase();
    if (!lastPart.includes('ca') && !lastPart.includes('california')) {
        showError('Please enter a California address with ZIP code.\nExample: 555 Market Street, San Francisco, CA 94105');
        return;
    }

    // Validate ZIP code
    if (!address.match(/\d{5}/)) {
        showError('Please include a 5-digit ZIP code.\nExample: 555 Market Street, San Francisco, CA 94105');
        return;
    }
    
    // Clear any existing error messages since the address format is valid
    clearError();
    showLoadingState();
    
    try {
        // Geocode address via Nominatim (OpenStreetMap)
        const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}&countrycodes=us`);
        const data = await response.json();
        console.log('Geocoding response:', data);
        
        if (!data.length) throw new Error('Address not found. Please make sure to include the full address with zip code.');
        
        // Verify the result is in California
        if (!data[0].display_name.toLowerCase().includes('california')) {
            throw new Error('Address found but not in California. Please enter a California address.');
        }
        
        const location = {
            lat: parseFloat(data[0].lat),
            lng: parseFloat(data[0].lon)
        };
        console.log('Location coordinates:', location);
        
        // Get polling locations from your Flask/Civic API
        const pollingData = await MyNCRep.makeAPIRequest(`/api/polling-locations?address=${encodeURIComponent(address)}`);
        console.log('Polling data response:', pollingData);
        
        if (pollingData && pollingData.success) {
            if ((!pollingData.polling_locations || pollingData.polling_locations.length === 0) &&
                (!pollingData.early_vote_sites || pollingData.early_vote_sites.length === 0)) {
                showError('No polling locations found for this address. Try adding a zip code or using a more specific address.');
            } else {
                isValidAddress = true;
                clearError();
                displayPollingLocations(pollingData, location);
            }
        } else {
            showError('Unable to find polling locations. Please use format: Street Address, City, CA Zip (e.g., 1600 Amphitheatre Parkway, Mountain View, CA 94043)');
        }
        
    } catch (err) {
        console.error(err);
        showError(err.message || 'An error occurred while searching for the address. Please try again with a valid California address.');
    } finally {
        hideLoadingState();
    }
    
    // If we reach this point without finding polling locations, keep the error visible
    if (!document.getElementById('error-message').classList.contains('d-none')) {
        return;
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
    // map.setView([userLocation.lat, userLocation.lng], 11);
    
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
    
    console.log('Processing locations:', allLocations);
    
    if (allLocations.length === 0) {
        // At least show the user's location on the map
        map.setView([userLocation.lat, userLocation.lng], 13);
        return;
    }
    
    allLocations.forEach(loc => {
        if (!loc.address) return;
        
        // Skip if no coordinates
        if (!loc.lat || !loc.lon) return;
        
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
let isValidAddress = false;

function showError(msg) {
    const err = document.getElementById('error-message');
    if (err) {
        console.error(msg);
        err.innerHTML = msg.replace(/\n/g, '<br>');
        err.classList.remove('d-none');
        err.style.display = 'block';
        isValidAddress = false;
    }
}

function clearError() {
    // Only clear error if we have a valid address
    if (isValidAddress) {
        const err = document.getElementById('error-message');
        if (err) {
            err.classList.add('d-none');
            err.innerHTML = '';
            err.style.display = 'none';
        }
    }
}

// Initialize
initMap();
