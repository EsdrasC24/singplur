from singplur.english import English

class Noun:
    def __init__(self, lang = 'en'):
        self.obj = self._factory(lang)

    def pluralize(self, noun: 'str') -> 'str':
        return self.obj.pluralize(noun)
    
    def singularize(self, noun: 'str') -> 'str':
        return self.obj.singularize(noun)
    
    def _factory(self, lang):
        obj = English()
        if lang == 'es':
            pass
        # default
        return obj