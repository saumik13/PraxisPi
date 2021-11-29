#  ----------------------------------------------------------------------------
#   Copyright (c) PraxisPi Group. All rights reserved.
#  ----------------------------------------------------------------------------

IMAGE_PATH = 'image.jpg'

CARDBOARD = 'cardboard'
GLASS = 'glass'
KEYBOARD = 'keyboard'
LAPTOP = 'laptop'
METAL = 'metal'
MOBILE = 'mobile'
MONITOR = 'monitor'
MOUSE = 'mouse'
PAPER = 'paper'
PLASTIC = 'plastic'
TRASH = 'trash'
E_WASTE = 'e-waste'

LABELS = {
    CARDBOARD: CARDBOARD,
    GLASS: GLASS,
    KEYBOARD: E_WASTE,
    LAPTOP: E_WASTE,
    METAL: METAL,
    MOBILE: E_WASTE,
    MONITOR: E_WASTE,
    MOUSE: E_WASTE,
    PAPER: PAPER,
    PLASTIC: PLASTIC,
    TRASH: TRASH,
}

PINS = {
    CARDBOARD: 27,
    GLASS: 22,
    METAL: 16,
    E_WASTE: 17,
    PAPER: 6,
    PLASTIC: 18,
    TRASH: 5,
}

BUTTON_PIN = 24

LED_ACTIVATION_TIME = 10
