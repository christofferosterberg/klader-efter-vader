
def createWindyNode(windy_clothes, not_windy_clothes):
    return {
        False : not_windy_clothes,
        True  : windy_clothes
    }

def createPrecipitationNode(no_precipitation, precipitation, much_precipitation):
    return {
        [0, 0.1]: createWindyNode(no_precipitation[0], no_precipitation[1]),
        [0.1, 1.0] : createWindyNode(precipitation[0], precipitation[1]),
        [1.1]: createWindyNode(much_precipitation[0], much_precipitation[1])
    }

def createCloudyNode(clear, cloudy):
    return {
        False: createPrecipitationNode(clear[0], clear[1], clear[2]),
        True: createPrecipitationNode(cloudy[0], cloudy[1], cloudy[2])
    }

def createTemperatureNode(cold,chilly,warm,hot):
    return {
        [-273, 0]: createCloudyNode(cold[0], cold[1]),
        [0, 10]: createCloudyNode(chilly[0], chilly[1]),
        [10, 20]: createCloudyNode(warm[0], warm[1]),
        [20, 100]: createCloudyNode(hot[0], hot[1])
    }

def createClothesStruct():
    return createTemperatureNode(
        [[[[],[]],[[],[]],[[],[]]],[[[],[]],[[],[]],[[],[]]]],
        [[[[],[]],[[],[]],[[],[]]],[[[],[]],[[],[]],[[],[]]]],
        [ # Warm
            [
                [
                    [
                        'ett par shorts eller en kjol och en skön tisha, det ska bli strålande sol och gassande värme'
                    ],
                    [
                        'ett par långbyxor och en skön tisha, det ska blåsa en del'
                    ]
                ],
                [
                    [
                        'en långtröja och kanske en keps eller hatt, lätt regn kan förekomma'
                    ],
                    [
                        'en långtröja och kanske en keps eller hatt, lätt regn kan förekomma'
                    ]
                ],
                [
                    [
                        'en kortärmad tröja men ta med ett paraply'
                    ],
                    [
                        'en långärmad tröja och paraply, det ska blåsa och regma'
                    ]
                ]
            ],
            [
                [
                    [
                        'ett par shorts eller kjol och en kortärmad tröja, det ska bli moligt men vara varmt och vindstilla'
                    ],
                    [
                        'långbyxor och långärmad tröja, det ska bli mulet och blåsa'
                    ]
                ],
                [
                    [
                        'långbyxor och långtröja, ta med något mot regn ifall att'
                    ],
                    [
                        'långbyxor och långtröja. Ta även med något mot regn ifall att'
                    ]
                ],
                [
                    [
                        'en tunn regnjacka eller paraply'
                    ],
                    [
                        'en tunn regnjacka, det ska regna mycket och blåsa'
                    ]
                ]
            ]
        ],
        [ # Hot
            [
                [
                    [
                        'ett par shorts eller en kjol och en skön tisha, det ska bli strålande sol och gassande värme'
                    ],
                    [
                        'ett par långbyxor och en skön tisha, det ska blåsa en del'
                    ]
                ],
                [
                    [
                        'en långtröja och kanske en keps eller hatt, lätt regn kan förekomma'
                    ],
                    [
                        'en långtröja och kanske en keps eller hatt, lätt regn kan förekomma'
                    ]
                ],
                [
                    [
                        'en kortärmad tröja men ta med ett paraply'
                    ],
                    [
                        'en långärmad tröja och paraply, det ska blåsa och regma'
                    ]
                ]
            ],
            [
                [
                    [
                        'ett par shorts eller kjol och en kortärmad tröja, det ska bli moligt men vara varmt och vindstilla'
                    ],
                    [
                        'långbyxor och långärmad tröja, det ska bli mulet och blåsa'
                    ]
                ],
                [
                    [
                        'långbyxor och långtröja, ta med något mot regn ifall att'
                    ],
                    [
                        'långbyxor och långtröja. Ta även med något mot regn ifall att'
                    ]
                ],
                [
                    [
                        'en tunn regnjacka eller paraply'
                    ],
                    [
                        'en tunn regnjacka, det ska regna mycket och blåsa'
                    ]
                ]
            ]
        ]
    )