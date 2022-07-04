const host = 'http://localhost:3000/'
var position = null

var map
$('document').ready(function(){
    map = L.map('map').setView([61.34, 12.88], 5)
    var marker = L.marker([61.34, 13.88]).addTo(map)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(map)
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
    $("#chosen-city").change(showClothes)
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
    // map.invalidateSize()
    $('#map').removeClass('d-none')
    $('#see-clothes').addClass('d-none')
    $('#select-city').removeClass('d-none')
    $('#submit-city-btn').click(showClothes)
    $.ajax({
        url: host + 'cities',
        type: 'GET',
        success: autofillCity
    })
}

function autofillCity(cities){
    for (const city of cities){
        $('#cities-options').append($('<option>').attr('value', city.name))
    }
    if (position != null){
        closestCity = cities[0]
        closestDistance = Math.sqrt((cities[0].latitude-position['latitude'])**2 + (cities[0].longitude-position['longitude'])**2)
        for (const city of cities){
            distance = Math.sqrt(((city.latitude-position['latitude'])**2) + ((city.longitude-position['longitude'])**2))
            if (distance < closestDistance){
                closestCity = city
                closestDistance = distance
            }
        }
        $('#all-cities-choice').val(closestCity.name)
    }
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
