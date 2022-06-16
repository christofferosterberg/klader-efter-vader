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
            type: 'GET',
            success: fillHomeWeather
        })
        $('#see-clothes').click(viewCityPicker)
        $("#chosen-city").change(showClothes)
    })
}

function fillHomeWeather(resp){
    stockholm  = findWeatherInfo(resp, 'Stockholm')
    gothenburg = findWeatherInfo(resp, 'Göteborg')
    malmo      = findWeatherInfo(resp, 'Malmö')

    $('#stockholm-home').append($('<p></p>').text(stockholm.description))
    $('#stockholm-icon').addClass('fa-solid ' + getIcon(stockholm.value))
    $('#gothenburg-home').append($('<p></p>').text(gothenburg.description))
    $('#gothenburg-icon').addClass('fa-solid ' + getIcon(gothenburg.value))
    $('#malmo-home').append($('<p></p>').text(malmo.description))
    $('#malmo-icon').addClass('fa-solid ' + getIcon(malmo.value))
    $('#weather-now-header').append(' (' + stockholm.datetime.slice(17,22) + ')')
}

function getIcon(value){
    icons = ['fa-sun',
            'fa-cloud-sun',
            'fa-cloud-sun',
            'fa-cloud-sun',
            'fa-cloud-sun',
            'fa-cloud',
            'fa-cloud-smog',
            'fa-droplet',
            'fa-cloud-rain',
            'fa-cloud-showers-heavy',
            'fa-cloud-bolt',
            'fa-droplet',
            'fa-cloud-rain',
            'fa-cloud-showers-heavy',
            'fa-snowflake',
            'fa-snowflake',
            'fa-snowflake',
            'fa-droplet',
            'fa-cloud-rain',
            'fa-cloud-showers-heavy',
            'fa-cloud-bolt',
            'fa-snowflake',
            'fa-snowflake',
            'fa-snowflake',
            'fa-snowflake',
            'fa-snowflake',
            'fa-snowflake',
            ]
    return icons[value-1]
}

function findWeatherInfo(allWeathers, targetCity){
    for (const weather of allWeathers){
        if(weather.city_name == targetCity){return weather}
    }
}

function viewCityPicker(){
    $('#see-clothes').addClass('d-none')
    $('#select-city').removeClass('d-none')
}

function showClothes(){
    var selectedCity = $("#chosen-city option:selected").val();
    console.log('du valde ' + selectedCity)
    $.ajax({
        url: host + 'clothes-info/'+ selectedCity,
        type: 'GET',
        success: showTheText
    })
}

function showTheText(resp){
    
}

// function viewQuestions(){
//     loadContainer('questions.html', function(){
//         const questions = $('#questions').children()
//         var questionQueue = createQuestions(questions)
//         questionQueue.shift()()
//         var answers = []

//         function createQuestions(questions){
//             var questionQueue = []
//             for (const question of questions){
//                 questionQueue.push(function(){
//                     $(question).removeClass('d-none')
//                     $(question).find('button').click(function (event) {
//                         saveAnswer(event.currentTarget)
//                         $(question).find('button').off()
//                         $(question).addClass('d-none')
//                         if (questionQueue.length > 0) {questionQueue.shift()()}
//                         else {saveAnswers()}
//                     })
//                 })
//             }
//             return questionQueue
//         }
//         function saveAnswer(answer){
//             answers.push($(answer).attr('answerNo'))
//         }
//         function saveAnswers(){
//             console.log('alla frågor är svarade!')
//             console.log(answers)
//         }
//     })
// }




