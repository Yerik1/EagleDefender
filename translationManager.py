# translationManager.py
class TranslationManager:
    def __init__(self):
        self.translations = {
            'English': {
                'testLbl': ' Hello',
                'testBtn': ' Goodbye',
                'wallsLb': ' Walls',
                'powersLb': ' Powers',
                'pointsDefender': ' Points',
                'pointsAttacker': ' Points',
                'userDefender': ' User',
                'userAttacker': ' User',
                'musicDefender': ' Music',
                'musicAttacker': ' Music',
                'funFactDefender': ' Fun Facts: ...',
            },
            'Español': {
                'testLbl': ' Hola',
                'testBtn': ' Adiós',
                'wallsLb': ' Paredes',
                'powersLb': ' Poderes',
                'pointsDefender': ' Puntos',
                'pointsAttacker': ' Puntos',
                'userDefender': ' Usuario',
                'userAttacker': ' Usuario',
                'musicDefender': ' Música',
                'musicAttacker': ' Música',
                'funFactDefender': ' Datos Curiosos: ...',
            },
        }
        self.currentLanguage = 'English'

    def loadTranslations(self):
        # Carga las traducciones desde algún archivo o base de datos si es necesario
        pass

    def setLanguage(self, language):
        self.currentLanguage = language

    def updateWidgets(self, widgetDict):
        language = self.currentLanguage
        for widgetId, translation in self.translations[language].items():
            widget = widgetDict.get(widgetId)
            if widget:
                widget.config(text=translation)
