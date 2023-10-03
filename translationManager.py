# translationManager.py
class TranslationManager:
    def __init__(self):
        self.translations = {
            'English': {
                'wallsLb': ' Walls:',
                'powersLb': ' Powers',
                'pointsDefender': ' Points',
                'pointsAttacker': ' Points',
                'userDefender': ' User',
                'userAttacker': ' User',
                'musicDefender': ' Music',
                'musicAttacker': ' Music',
                'funFactDefender': ' Fun Facts: ...',
                'funFactAttacker': ' Fun Facts: ...',
                'rolDefender': ' Defender',
                'rolAttacker': ' Attacker',
                'profilePicDefender': ' Profile Pic',
                'profilePicAttacker': ' Profile Pic',
            },
            'Español': {
                'wallsLb': ' Paredes',
                'powersLb': ' Poderes',
                'pointsDefender': ' Puntos',
                'pointsAttacker': ' Puntos',
                'userDefender': '      Usuario',
                'userAttacker': ' Usuario',
                'musicDefender': '      Música',
                'musicAttacker': ' Música',
                'funFactDefender': ' Datos Curiosos: ...',
                'funFactAttacker': ' Datos Curiosos: ...',
                'rolDefender': ' Defensor',
                'rolAttacker': ' Atacante',
                'profilePicDefender': ' Foto de Perfil',
                'profilePicAttacker': ' Foto de Perfil',
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
