// Google Maps functionality for polling locations

let map;
let markers = [];
let userMarker;
let geocoder;
let directionsService;
let directionsRenderer;

// Initialize map when page loads
function initMap() {
    // Default to North Carolina center
    // const ncCenter = { lat: 35.7596, lng: -79.0193 };
    
    // map = new google.maps.Map(document.getElementById('map'), {
    //     zoom: 8,
    //     center: ncCenter,
    //     mapTypeControl: true,
    //     mapTypeControlOptions: {
    //         style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
    //         position: google.maps.ControlPosition.TOP_CENTER,
    //     },
    //     zoomControl: true,
    //     zoomControlOptions: {
    //         position: google.maps.ControlPosition.RIGHT_CENTER,
    //     },
    //     scaleControl: true,
    //     streetViewControl: true,
    //     streetViewControlOptions: {
    //         position: google.maps.ControlPosition.RIGHT_TOP,
    //     },
    //     fullscreenControl: false,
    // });
    
    // geocoder = new google.maps.Geocoder();
    // directionsService = new google.maps.DirectionsService();
    // directionsRenderer = new google.maps.DirectionsRenderer();
    // directionsRenderer.setMap(map);
    
    initializeEventListeners();
}

// Initialize event listeners
function initializeEventListeners() {
    // Address search
    document.getElementById('search-btn').addEventListener('click', handleAddressSearch);
    document.getElementById('address-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleAddressSearch();
        }
    });
    
    // Current location button
    document.getElementById('location-btn').addEventListener('click', handleCurrentLocation);
}

// Handle address search
async function handleAddressSearch() {
    const address = document.getElementById('address-input').value.trim();
    if (!address) {
        showError('Please enter an address');
        return;
    }
    
    // Validate North Carolina address
    if (!MyNCRep.isValidNCAddress(address)) {
        showError('Please enter a North Carolina address for accurate polling information.');
        return;
    }
    
    showLoadingState();
    
    try {
        // Geocode the address
        const location = await geocodeAddress(address);
        
        // Get polling locations
        const pollingData = await MyNCRep.makeAPIRequest(`/api/polling-locations?address=${encodeURIComponent(address)}`);
        
        if (pollingData.success) {
            displayPollingLocations(pollingData, location);
            updateMapView(location);
        } else {
            showError(pollingData.error || 'Unable to find polling locations for this address.');
        }
        
    } catch (error) {
        console.error('Error searching for polling locations:', error);
        showError('An error occurred while searching. Please try again.');
    } finally {
        hideLoadingState();
    }
}

// Handle current location request
async function handleCurrentLocation() {
    showLoadingState();
    
    try {
        const position = await MyNCRep.getCurrentLocation();
        console.log(position);
        
        // Reverse geocode to get address
        const address = await reverseGeocode(position);
        
        // Update address input
        document.getElementById('address-input').value = address;
        
        // Get polling locations
        const pollingData = await MyNCRep.makeAPIRequest(`/api/polling-locations?address=${encodeURIComponent(address)}`);
        console.log(pollingData);
        
        if (pollingData.success) {
            displayPollingLocations(pollingData, position);
            updateMapView(position);
        } else {
            showError(pollingData.error || 'Unable to find polling locations for your current location.');
        }
        
    } catch (error) {
        console.error('Error getting current location:', error);
        showError(error.message || 'Unable to get your current location.');
    } finally {
        hideLoadingState();
    }
}

// Geocode address to coordinates
function geocodeAddress(address) {
    return new Promise((resolve, reject) => {
        geocoder.geocode({ address: address }, (results, status) => {
            if (status === 'OK') {
                const location = results[0].geometry.location;
                resolve({
                    lat: location.lat(),
                    lng: location.lng()
                });
            } else {
                reject(new Error('Unable to find the specified address.'));
            }
        });
    });
}

// Reverse geocode coordinates to address
function reverseGeocode(position) {
    return new Promise((resolve, reject) => {
        geocoder.geocode({ location: position }, (results, status) => {
            if (status === 'OK' && results[0]) {
                resolve(results[0].formatted_address);
            } else {
                reject(new Error('Unable to determine address from your location.'));
            }
        });
    });
}

// Display polling locations on map and in sidebar
function displayPollingLocations(pollingData, userLocation) {
    // Clear existing markers
    clearMarkers();
    
    // Add user location marker
    addUserMarker(userLocation);
    
    // Add polling location markers
    const allLocations = [
        ...(pollingData.polling_locations || []),
        ...(pollingData.early_vote_sites || [])
    ];
    
    allLocations.forEach((location, index) => {
        addPollingMarker(location, index);
    });
    
    // Update sidebar results
    updateSidebarResults(pollingData);
    
    // Show results
    document.getElementById('results').classList.remove('d-none');
}

// Add user location marker
function addUserMarker(location) {
    userMarker = new google.maps.Marker({
        position: location,
        map: map,
        title: 'Your Location',
        icon: {
            url: 'data:image/svg+xml;base64,' + btoa(`
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#007bff">
                    <circle cx="12" cy="12" r="8" stroke="#fff" stroke-width="2"/>
                    <circle cx="12" cy="12" r="3" fill="#fff"/>
                </svg>
            `),
            scaledSize: new google.maps.Size(24, 24),
            anchor: new google.maps.Point(12, 12)
        }
    });
    
    const infoWindow = new google.maps.InfoWindow({
        content: `
            <div class="p-2">
                <h6><i class="fas fa-user me-2"></i>Your Location</h6>
                <p class="mb-0 small">This is your entered location</p>
            </div>
        `
    });
    
    userMarker.addListener('click', () => {
        infoWindow.open(map, userMarker);
    });
}

// Add polling location marker
function addPollingMarker(location, index) {
    // Geocode the location address
    geocoder.geocode({ address: location.address }, (results, status) => {
        if (status === 'OK') {
            const position = results[0].geometry.location;
            const isEarlyVoting = location.type === 'early_voting';
            
            const marker = new google.maps.Marker({
                position: position,
                map: map,
                title: location.name,
                icon: {
                    url: 'data:image/svg+xml;base64,' + btoa(`
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="${isEarlyVoting ? '#28a745' : '#dc3545'}">
                            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" fill="white"/>
                        </svg>
                    `),
                    scaledSize: new google.maps.Size(32, 32),
                    anchor: new google.maps.Point(16, 32)
                }
            });
            
            const infoWindow = new google.maps.InfoWindow({
                content: createMarkerInfoWindow(location, position)
            });
            
            marker.addListener('click', () => {
                infoWindow.open(map, marker);
            });
            
            markers.push(marker);
        }
    });
}

// Create info window content for marker
function createMarkerInfoWindow(location, position) {
    const isEarlyVoting = location.type === 'early_voting';
    
    return `
        <div class="p-2" style="max-width: 300px;">
            <h6>
                <i class="fas fa-${isEarlyVoting ? 'clock' : 'vote-yea'} me-2"></i>
                ${location.name}
            </h6>
            <p class="mb-2"><strong>Address:</strong><br>${location.address}</p>
            <p class="mb-2"><strong>Hours:</strong><br>${location.hours}</p>
            ${location.notes ? `<p class="mb-2"><strong>Notes:</strong><br>${location.notes}</p>` : ''}
            <div class="d-flex gap-2">
                <button class="btn btn-sm btn-primary" onclick="getDirections('${location.address}')">
                    <i class="fas fa-directions me-1"></i>Directions
                </button>
                <a href="https://maps.google.com/?q=${encodeURIComponent(location.address)}" target="_blank" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-external-link-alt me-1"></i>Google Maps
                </a>
            </div>
        </div>
    `;
}

// Update sidebar results
function updateSidebarResults(pollingData) {
    const pollingContainer = document.getElementById('polling-locations');
    const earlyVotingContainer = document.getElementById('early-voting-sites');
    
    // Display polling locations
    if (pollingData.polling_locations && pollingData.polling_locations.length > 0) {
        pollingContainer.innerHTML = pollingData.polling_locations.map(location => `
            <div class="card mb-2">
                <div class="card-body py-2">
                    <h6 class="card-title mb-1">${location.name}</h6>
                    <p class="small text-muted mb-1">${location.address}</p>
                    <p class="small mb-0"><strong>Hours:</strong> ${location.hours}</p>
                    ${location.notes ? `<p class="small text-info mb-0">${location.notes}</p>` : ''}
                </div>
            </div>
        `).join('');
    } else {
        pollingContainer.innerHTML = '<p class="text-muted small">No Election Day polling locations found.</p>';
    }
    
    // Display early voting sites
    if (pollingData.early_vote_sites && pollingData.early_vote_sites.length > 0) {
        earlyVotingContainer.innerHTML = pollingData.early_vote_sites.map(site => `
            <div class="card mb-2">
                <div class="card-body py-2">
                    <h6 class="card-title mb-1">${site.name}</h6>
                    <p class="small text-muted mb-1">${site.address}</p>
                    <p class="small mb-0"><strong>Hours:</strong> ${site.hours}</p>
                    ${site.notes ? `<p class="small text-info mb-0">${site.notes}</p>` : ''}
                </div>
            </div>
        `).join('');
    } else {
        earlyVotingContainer.innerHTML = '<p class="text-muted small">No early voting sites found.</p>';
    }
}

// Update map view to show all markers
function updateMapView(userLocation) {
    if (markers.length === 0) {
        map.setCenter(userLocation);
        map.setZoom(12);
        return;
    }
    
    const bounds = new google.maps.LatLngBounds();
    bounds.extend(userLocation);
    
    markers.forEach(marker => {
        bounds.extend(marker.getPosition());
    });
    
    map.fitBounds(bounds);
    
    // Ensure minimum zoom level
    google.maps.event.addListenerOnce(map, 'bounds_changed', function() {
        if (map.getZoom() > 15) {
            map.setZoom(15);
        }
    });
}

// Get directions to a location
function getDirections(destination) {
    if (!userMarker) {
        alert('Please search for your address first to get directions.');
        return;
    }
    
    const request = {
        origin: userMarker.getPosition(),
        destination: destination,
        travelMode: google.maps.TravelMode.DRIVING
    };
    
    directionsService.route(request, (result, status) => {
        if (status === 'OK') {
            directionsRenderer.setDirections(result);
        } else {
            console.error('Directions request failed:', status);
            alert('Unable to get directions to this location.');
        }
    });
}

// Clear all markers from map
function clearMarkers() {
    markers.forEach(marker => {
        marker.setMap(null);
    });
    markers = [];
    
    if (userMarker) {
        userMarker.setMap(null);
        userMarker = null;
    }
    
    directionsRenderer.setDirections({ routes: [] });
}

// Show loading state
function showLoadingState() {
    document.getElementById('loading').classList.remove('d-none');
    document.getElementById('results').classList.add('d-none');
    document.getElementById('error-message').classList.add('d-none');
}

// Hide loading state
function hideLoadingState() {
    document.getElementById('loading').classList.add('d-none');
}

// Show error message
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.classList.remove('d-none');
    hideLoadingState();
}

// Initialize map when Google Maps API is loaded
window.initMap = initMap;

// Initialize map if Google Maps is already loaded
// if (typeof google !== 'undefined' && google.maps) {
    initMap();
// }
