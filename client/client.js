const host = 'http://localhost:3000/'

$('document').ready(function(){
    $('#nav-logo').click(viewStart)
    $('#nav-home').click(viewStart)
    viewStart()
})

function loadContainer(src, viewToLoad){
    $('#container').load('html/' + src, viewToLoad)
}

function viewStart(){
    loadContainer('home.html', function(){
        $.ajax({
            url: host + 'weather',
            contentType: "application/json",
            type: 'POST',
            data: JSON.stringify(citiesOnMap),
            success: fillHomeWeather
        })
        $('#see-clothes').click(viewCityPicker)
        $("#chosen-city").change(showClothes)
    })
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

        $('#map').append(icon)
    }
}

function findWeatherInfo(allWeathers, targetCity){
    for (const weather of allWeathers){
        if(weather.city_name == targetCity){return weather}
    }
}

function viewCityPicker(){
    $('#see-clothes').addClass('d-none')
    $('#select-city').removeClass('d-none')
    $('#submit-city-btn').click(showClothes)
    $.ajax({
        url: host + 'city-names',
        type: 'GET',
        success: function(resp){
            for (const city of resp){
                $('#cities-options').append($('<option>').attr('value', city))
            }
        }
    })
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
