import re
from typing import Optional

class English:

    def pluralize(self, noun: 'str') -> 'str':
        noun = noun.lower()
        if self.is_plural(noun):
            return noun
        
        # irregular nouns
        i_noun = English.irregular_noun(noun)
        if i_noun:
            return i_noun
        
        # noun ending in: s, sh, ch, x, z
        if re.search(r'[a-z]+(s|sh|ch|x|z)$', noun):
            return noun + 'es'
        
        reg = re.search(r'[a-z]+(?P<before>[a-z])(?P<end>o|y)$', noun)
        if reg:
            result = reg.groupdict()
            if result['end'] == 'o': # noun ending in: o
                return noun + 's' if re.search(r'[aeiou]', result['before']) else 'es' 
            else: # noun ending in: y
                return noun + 's' if re.search(r'[aeiou]', result['before']) else noun[:len(noun) - 1] + 'ies'
        
        # noun ending in: fe or f but not ff
        if re.search(r'[a-z]+[^f]f(e)?$', noun):
            return re.sub(r'f(e)?$', 'ves', noun)
        
        # general pluralization: add 's'
        return noun + 's'

    def singularize(self, noun: 'str') -> 'str':
        if self.is_singular(noun):
            return noun
        
        # irregular nouns
        result = self.irregular_noun(noun, False)
        if result:
            return result 
        
        # removing in nouns with end in s, sh, ch, x, z
        # removing in nouns with end in o
        if re.search(r'[a-z]+(s|sh|ch|x|z)es$|[a-z]+[^aeiou]oes$', noun):
            return noun.removesuffix('es')
        
        # removing in nouns with end in y
        if re.search(r'[a-z]+[^aeiou]ies$', noun):
            return noun.removesuffix('ies') + 'y'
        
        # removing in nouns with end in fe
        # NOTE: Because can't possible detects when noun must end in f, nouns ending in f will be added
        #   like irregular nouns
        # TODO [future] add heuristic for detect singular noun that end in f
        if re.search(r'[a-z]+ves$', noun):
            return noun.removesuffix('ves') + 'fe'

        # normal pluralization
        return noun.removesuffix('s')
    
    def is_plural(self, noun: 'str'):
        noun = noun.lower()

        rule1 = r'\w+fe?s$'
        rule2 = r'\w+(ch|sh|z|x|s|i|o|v)es$' #rule for s, ch, sh, x, z, y, fe
        rule3 = r'\w+i$' # rule for stranger english words 
        rule4 = r'\w+[^aeiou]s$'

        # warning: order in conditions is important!
        return English.irregular_noun(noun, False) \
            or re.search(f'{rule1}|{rule2}|{rule3}|{rule4}', noun) #TODO: agregar restricciones para comprobar la pluralidad cuando terminan en s
        
        return False # by default
    
    def is_singular(self, noun):
        return not self.is_plural(noun)
    
    @staticmethod
    def irregular_noun(noun: 'str', compare_singular: 'bool' = True) -> Optional['str']:
        # singular, plural
        _nouns = [
            ('analysis', 'analyses'), ('axis', 'axes'),
            ('basis', 'bases'),
            ('child', 'children'), ('crisis', 'crises'), ('criterion', 'criteria'), 
            ('datum', 'data'), ('deer', 'deer'),
            ('fish', 'fishes'), ('focus', 'foci'), ('foot', 'feet'), ('formula', 'formulae'), 
            ('genus', 'genera'), ('goose', 'geese'), 
            ('ice', 'ice'), ('index', 'indices'),
            ('louse', 'lice'), 
            ('man', 'men'), ('medium', 'media'), ('moose', 'moose'), ('mouse', 'mice'),
            ('nucleus', 'nuclei'), 
            ('oasis', 'oases'), ('octopus', 'octopuses'), ('opus', 'opera'), ('ox', 'oxen'),
            ('person', 'people'), ('people', 'people'), ('phenomenon', 'phenomena'),
            ('radius', 'radii'), 
            ('scarf', 'scarves'), ('self', 'selves'), ('series', 'series'), ('sheep', 'sheep'), ('species', 'species'), ('stadium', 'stadia'), 
            ('thesis', 'theses'), ('tooth', 'teeth'),  
            ('stimulus', 'stimuli'), ('vertex', 'vertices'), 
            ('woman', 'women')  
        ]

        for singular, plural in _nouns:
            if compare_singular:
                if singular == noun:
                    return plural
            else:
                if plural == noun:
                    return singular
                
        return None # there was not matches
    
if __name__ == '__main__':
    e = English()
    w = input('Ingrese una palabra en plural: ')
    print(e.singularize(w))
    
