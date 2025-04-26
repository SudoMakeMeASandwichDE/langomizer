import random
import hashlib
from itertools import groupby

word_lengths = {
    'noun': (4, 7),
    'verb': (3, 5), # Plus two letter ending
    'adjective': (3, 6),
    'preposition': (2, 4),
    'pronoun': (1, 3),
    'conjunction': (1, 3),
    'particle': (2, 3)
}

class SimpleLanguage:
    def __init__(self, seed=None, consonants=['m', 'n', 'p', 't', 'k'], vowels=['a', 'i', 'u']):
        self.seed = seed
        if seed is not None:
            random.seed(seed)
            self.randomseed = False
        else:
            self.seed = random.randint(-10000, 10000)
            self.randomseed = True
        self.word_map = {}
        self.consonants = consonants
        self.vowels = vowels
        self.verb_ending = random.choice(self.vowels) + random.choice(self.consonants)

    def generate_syllable(self, word_type, wordseed):
        min_len, max_len = word_lengths[word_type]
        random.seed(wordseed)
        length = random.randint(min_len, max_len)
        structure = random.choice(['CV', 'VC', 'CVC'])
        syllable = ''
        if length == 1:
            syllable += random.choice(self.vowels)
            return syllable
        while True:
            if structure.startswith('CV'):
                syllable += random.choice(self.consonants)
                length -= 1
                if length == 0:
                    if word_type == 'verb':
                        syllable += self.verb_ending
                    return syllable
                syllable += random.choice(self.vowels)
                length -= 1
                if length == 0:
                    if word_type == 'verb':
                        syllable += self.verb_ending
                    return syllable
            elif structure.startswith('VC'):
                syllable += random.choice(self.vowels)
                length -= 1
                if length == 0:
                    if word_type == 'verb':
                        syllable += self.verb_ending
                    return syllable
                syllable += random.choice(self.consonants)
                length -= 1
                if length == 0:
                    if word_type == 'verb':
                        syllable += self.verb_ending
                    return syllable
            if structure == 'CVC':
                syllable += random.choice(self.consonants)
                length -= 1
                if length == 0:
                    if word_type == 'verb':
                        syllable += self.verb_ending
                    return syllable

    def translate(self, word, word_type):
        key = (word.lower(), word_type.lower())
        wordseed = int(str(self.seed) + str(int(hashlib.sha256(word.encode()).hexdigest(), 16)))
        random.seed(wordseed)
        if key not in self.word_map:
            self.word_map[key] = self.generate_syllable(word_type.lower(), wordseed=wordseed)
        random.seed(self.seed)
        translation = self.word_map[key]
        no_repeat = ''.join(k for k, _ in groupby(translation))
        return no_repeat
    
    def generate_grammar_basics(self):
        plural_ending = random.choice(self.vowels)
        verb_ending = self.verb_ending
        question_particle = self.generate_syllable(word_type='particle', wordseed=self.seed)
        question_particle_position = random.choice(['beginning', 'end'])
        negation = self.generate_syllable(word_type='particle', wordseed=self.seed+1)
        negation_position = random.choice(['before', 'after'])
        past_particle = self.generate_syllable(word_type='particle', wordseed=self.seed+2)
        future_particle = self.generate_syllable(word_type='particle', wordseed=self.seed+3)
        word_order = random.choice(['SVO', 'SOV', 'VSO'])
        return {'word_order': word_order, 'plural_ending': plural_ending, 'verb_ending': verb_ending, 'question_particle': question_particle, 'question_particle_position': question_particle_position, 'negation': negation, 'negation_position': negation_position, 'past_particle': past_particle, 'future_particle': future_particle}
    
    def describe_grammar_basics(self):
        grammar_basics = self.generate_grammar_basics()
        output = "There are no cases and no articles and no use of 'to be' to connect adjectives with nouns (so 'The ball is red' becomes 'Ball red')\n"
        output += f"The basic word order is '{grammar_basics['word_order']}'\n"
        output += f"Plural ending is always '{grammar_basics['plural_ending']}'\n"
        output += f"The ending of a verb is always '{grammar_basics['verb_ending']}'\n"
        output += f"If you want to pose a question, use the questoin particle '{grammar_basics['question_particle']}'. Place it at the {grammar_basics['question_particle_position']} of the question sentence\n"
        output += f"If you want to deny a statement, use the negation particle '{grammar_basics['negation']}'. Place it {grammar_basics['negation_position']} the verb or adjective you want to deny\n"
        output += f"To say something in the past, put '{grammar_basics['past_particle']}' before the word or other particle (if exisiting) and if you want to say something in the future, do the same thing with '{grammar_basics['future_particle']}'"
        return output

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, help='Seed for language generation')
    parser.add_argument('--showbasics', action='store_true', help='Show other basic grammar functions')
    parser.add_argument('word', type=str, help='Word to translate')
    parser.add_argument('type', type=str, choices=['noun', 'verb', 'adjective', 'preposition', 'pronoun'], help='Part of speech')
    args = parser.parse_args()

    lang = SimpleLanguage(seed=args.seed)
    translation = lang.translate(args.word, args.type)
    print(f"Word: {args.word}\nType: {args.type}\nTranslation: {translation}")
    if lang.randomseed:
        print(f"Seed: {lang.seed}")
    if args.showbasics:
        print()
        print(lang.describe_grammar_basics())

