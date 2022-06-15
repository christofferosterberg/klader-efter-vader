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
        $('#see-clothes').click(viewQuestions)
    })
}

function fillHomeWeather(resp){
    stockholm  = findWeatherInfo(resp, 'Stockholm')
    gothenburg = findWeatherInfo(resp, 'Göteborg')
    malmo      = findWeatherInfo(resp, 'Malmö')

    $('#stockholm-home').append($('<p></p>').text(stockholm.description))
    $('#gothenburg-home').append($('<p></p>').text(gothenburg.description))
    $('#malmo-home').append($('<p></p>').text(malmo.description))
}

function findWeatherInfo(allWeathers, targetCity){
    for (const weather of allWeathers){
        if(weather.city_name == targetCity){return weather}
    }
}

function viewQuestions(){
    loadContainer('questions.html', function(){
        const questions = $('#questions').children()
        var questionQueue = createQuestions(questions)
        questionQueue.shift()()
        var answers = []

        function createQuestions(questions){
            var questionQueue = []
            for (const question of questions){
                questionQueue.push(function(){
                    $(question).removeClass('d-none')
                    $(question).find('button').click(function (event) {
                        saveAnswer(event.currentTarget)
                        $(question).find('button').off()
                        $(question).addClass('d-none')
                        if (questionQueue.length > 0) {questionQueue.shift()()}
                        else {saveAnswers()}
                    })
                })
            }
            return questionQueue
        }
        function saveAnswer(answer){
            answers.push($(answer).attr('answerNo'))
        }
        function saveAnswers(){
            console.log('alla frågor är svarade!')
            console.log(answers)
        }
    })
}




