const host = 'http://localhost:3000/'
var position = null

// var map
var allCities
// var marker
$('document').ready(function(){
    // map = L.map('map').setView([61.34, 12.88], 5)
    // map.on('click', updateMarker)
    // L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //     maxZoom: 19,
    //     attribution: '© OpenStreetMap'
    // }).addTo(map)
    // marker = L.marker()
    $('#all-cities-choice').val('')
    navigator.geolocation.getCurrentPosition((pos) => {
        position = {
            'longitude': pos.coords.longitude,
            'latitude' : pos.coords.latitude
        }
    })
    viewStart()
})

function viewStart(){
    $.ajax({
        url: host + 'weather',
        contentType: "application/json",
        type: 'POST',
        data: JSON.stringify(citiesOnMap),
        success: fillHomeWeather
    })
    $.ajax({
        url: host + 'cities',
        type: 'GET',
        success: autofillCity
    })
    $("#chosen-city").change(showClothes)

    $('#see-clothes').click(showClothes)
    $('#update-clothes-btn').click(fetchClothes)
    $('#cancel-clothes-btn').click(hideClothes)

    $('#see-pollen').click(showPollen)
    $('#update-pollen-btn').click(fetchPollen)
    $('#cancel-pollen-btn').click(hidePollen)

    $('#see-uv').click(showUV)
    $('#update-uv-btn').click(fetchUV)
    $('#cancel-uv-btn').click(hideUV)
    
    // $('#submit-city-btn').click(showClothes) 
}

function fillHomeWeather(resp){
    fillMap(resp)
    stockholm  = findWeatherInfo(resp, 'Stockholm')
    gothenburg = findWeatherInfo(resp, 'Göteborg')
    malmo      = findWeatherInfo(resp, 'Malmö')

    $('#weather-now-header').append(' (' + stockholm.hour + ':00)')
    $('#stockholm-home').append($('<p></p>').text(stockholm.description))
    $('#gothenburg-home').append($('<p></p>').text(gothenburg.description))
    $('#malmo-home').append($('<p></p>').text(malmo.description))
}

function fillMap(weatherData){
    for (const weather of weatherData){
        icon = $('<p></p>').addClass('map-icon')
        icon.attr('id', weather.city_name + '-map')
        theIcon = $('<i></i>').attr('id', weather.city_name + '-icon')
        theIcon.addClass('fa-solid ' + icons[weather.value-1]) // the class for correct icon
        icon.css('position', 'absolute')
        icon.append(theIcon)
        // Coordinates
        icon.css('margin-left', coordinatesForMap[weather.city_name][0])
        icon.css('margin-top', coordinatesForMap[weather.city_name][1])

        $('#my-map').append(icon)
    }
}

function findWeatherInfo(allWeathers, targetCity){
    for (const weather of allWeathers){
        if(weather.city_name == targetCity){return weather}
    }
}

// function viewCityPicker() {
//     $('#see-clothes').addClass('d-none')
//     $('#select-city').removeClass('d-none')
//     setTimeout(function () {
//         window.dispatchEvent(new Event('resize'));
//     }, 10)
// }

function autofillCity(cities){
    allCities = cities
    for (const city of cities){
        $('#cities-options').append($('<option>').attr('value', city.name))
    }
    if (position != null){
        closestCity = findClosestCity(position['latitude'], position['longitude'])
        $('#all-cities-choice').val(closestCity.name)
        // pinOnMap(closestCity.latitude, closestCity.longitude)
    } else {L.marker([61.34, 13.88]).addTo(map)}
}

function findClosestCity(latitude, longitude){
    closestCity = allCities[0]
        closestDistance = Math.sqrt((allCities[0].latitude-latitude)**2 + (allCities[0].longitude-longitude)**2)
        for (const city of allCities){
            distance = Math.sqrt(((city.latitude-latitude)**2) + ((city.longitude-longitude)**2))
            if (distance < closestDistance){
                closestCity = city
                closestDistance = distance
            }
        }
        return closestCity
}

// function pinOnMap(latitude, longitude){
//     marker.setLatLng([latitude, longitude])
//     marker.addTo(map)
// }

// function updateMarker(e){
//     pinOnMap(e.latlng.lat, e.latlng.lng)
//     closestCity = findClosestCity(e.latlng.lat, e.latlng.lng)
//     $('#all-cities-choice').val(closestCity.name)
// }

// CLOTHES //

function showClothes(){
    $('#see-clothes').addClass('d-none')
    $('#clothes-div').removeClass('d-none')
    fetchClothes()
}

function hideClothes(){
    $('#see-clothes').removeClass('d-none')
    $('#clothes-div').addClass('d-none')
    $('#clothes-info').empty()
}

function fetchClothes(){
    var selectedCity = $('#all-cities-choice').val()
    $.ajax({
        url: host + 'clothes-info/'+ selectedCity,
        type: 'GET',
        success: showClothesText
    })
}

function showClothesText(resp){
    $('#clothes-info').empty()
    $('#clothes-info').append($('<p></p>').text(resp))
}

// POLLEN //

function showPollen(){
    $('#see-pollen').addClass('d-none')
    $('#pollen-div').removeClass('d-none')
    fetchClothes()
}

function hidePollen(){
    $('#see-pollen').removeClass('d-none')
    $('#pollen-div').addClass('d-none')
    $('#pollen-info').empty()
}

function fetchPollen(){
    var selectedCity = $('#all-cities-choice').val()
    $.ajax({
        url: host + 'pollen-info/'+ selectedCity,
        type: 'GET',
        success: showPollenText
    })
}

function showPollenText(resp){
    $('#pollen-info').empty()
    $('#pollen-info').append($('<p></p>').text(resp))
}

// POLLEN //

function showUV(){
    $('#see-uv').addClass('d-none')
    $('#uv-div').removeClass('d-none')
    fetchClothes()
}

function hideUV(){
    $('#see-uv').removeClass('d-none')
    $('#uv-div').addClass('d-none')
    $('#uv-info').empty()
}

function fetchUV(){
    var selectedCity = $('#all-cities-choice').val()
    $.ajax({
        url: host + 'uv-info/'+ selectedCity,
        type: 'GET',
        success: showUVText
    })
}

function showUVText(resp){
    $('#uv-info').empty()
    $('#uv-info').append($('<p></p>').text(resp))
}