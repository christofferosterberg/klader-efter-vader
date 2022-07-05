const host = 'http://localhost:3000/'
var position = null

var map
var allCities
var marker
$('document').ready(function(){
    map = L.map('map').setView([61.34, 12.88], 5)
    map.on('click', updateMarker)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(map)
    marker = L.marker()
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
    $('#see-clothes').click(viewCityPicker)
    $('#cancel-city-btn').click(hideCityPicker)
    $("#chosen-city").change(showClothes)
    $('#submit-city-btn').click(showClothes) 
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

function viewCityPicker() {
    $('#see-clothes').addClass('d-none')
    $('#select-city').removeClass('d-none')
    setTimeout(function () {
        window.dispatchEvent(new Event('resize'));
    }, 10)
    $.ajax({
        url: host + 'cities',
        type: 'GET',
        success: autofillCity
    })
}

function hideCityPicker(){
    $('#see-clothes').removeClass('d-none')
    $('#select-city').addClass('d-none')
    $('#all-cities-choice').val('')
    $('#clothes-info').empty()
}

function autofillCity(cities){
    allCities = cities
    for (const city of cities){
        $('#cities-options').append($('<option>').attr('value', city.name))
    }
    if (position != null){
        closestCity = findClosestCity(position['latitude'], position['longitude'])
        $('#all-cities-choice').val(closestCity.name)
        pinOnMap(closestCity.latitude, closestCity.longitude)
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

function pinOnMap(latitude, longitude){
    marker.setLatLng([latitude, longitude])
    marker.addTo(map)
}

function updateMarker(e){
    pinOnMap(e.latlng.lat, e.latlng.lng)
    closestCity = findClosestCity(e.latlng.lat, e.latlng.lng)
    $('#all-cities-choice').val(closestCity.name)
}

function showClothes(){
    var selectedCity = $('#all-cities-choice').val()
    $.ajax({
        url: host + 'clothes-info/'+ selectedCity,
        type: 'GET',
        success: showTheText
    })
}

function showTheText(resp){
    $('#clothes-info').empty()
    $('#clothes-info').append($('<p></p>').text(resp))
}
