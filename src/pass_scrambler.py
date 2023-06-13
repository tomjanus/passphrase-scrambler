""" """
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Sequence


class WrongShiftValueException(Exception):
    """ """

class PermutationPatternError(Exception):
    """ """


@dataclass
class PassPhrase:
    """ """
    words: List[str]

    def __len__(self) -> int:
        return len(self.words)

    @classmethod
    def from_string(
            cls, word_sequence: str, delimiter: str = ",") -> PassPhrase:
        """Instantiate passphrase from a string of words deliminated by a
        common delimiter"""
        return cls(words = [c.strip() for c in word_sequence.split(delimiter)])
    
    def as_string(self, delimiter: str = ", ") -> str:
        """ """
        return delimiter.join(self.words)
        
        
@dataclass
class Permutation:
    """ """
    digits: List[int]
    _index: int = 0

    def __len__(self) -> int:
        return len(self.digits)
        
    def __iter__(self) -> Permutation:
        self._index=0
        return self
        
    def __next__(self):
        if self._index >= len(self.digits):
            raise StopIteration
        item = self.digits[self._index]
        self._index += 1
        return item

    @classmethod
    def from_string(
            cls, digit_sequence: str, delimiter: str = ",") -> PassPhrase:
        """Instantiate permutation sequence from a string of numbers deliminated by a
        common delimiter"""
        return cls(digits = [int(c.strip()) for c in digit_sequence.split(delimiter)])
    
    def as_string(self, delimiter: str = ", ") -> str:
        """ """
        digits: List[str] = list(map(str, self.digits))
        return delimiter.join(digits)


@dataclass
class PassPhraseScrambler:
    """ """
    passphrase: PassPhrase
    permutation_pattern: Permutation
    shift: int
    
    @classmethod
    def from_txt_file(cls, filename: str, delimiter: str = ",") -> PassPhraseScrambler:
        """ """
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        passphrase = PassPhrase.from_string(lines[0], delimiter)
        permutation = Permutation.from_string(lines[1], delimiter)
        shift = int(lines[2].strip())
        
        return cls(passphrase, permutation, shift)

    def __post_init__(self) -> None:
        """Validate attributes"""
        if not 1 <= self.shift <=26:
            raise WrongShiftValueException(
                "Shift value %d outside the permitted 1-26 range." % self.shift)
        
        if len(set(self.permutation_pattern.digits)) != len(self.permutation_pattern.digits) or \
                set(self.permutation_pattern.digits) != set(range(0, len(self.passphrase))):
            raise PermutationPatternError(
                "Permutation pattern needs to contain numbers between 0 and " +
                "the passphrase length and have no repeated values")

    @staticmethod
    def _permute(
            passphrase: PassPhrase,
            permutation_pattern: Permutation, direction: str = "forward") -> PassPhrase:
        """ """
        if direction == "forward":
            new_passphrase = PassPhrase([passphrase.words[index] for index in permutation_pattern])
        if direction == "reverse":
            reversed_words: List[str] = passphrase.words.copy()
            # Sort using indices of the permutation index
            for _ix, value in enumerate(permutation_pattern):
                reversed_words[value] = passphrase.words[_ix]
            new_passphrase = PassPhrase(reversed_words)
        return new_passphrase
    
    @staticmethod
    def _shift_letters(word: str, shift: int, direction: str) -> str:
        """ """
        shifted_word = ''
        word = word.strip()
        for char in word:
            if direction == "forward":
                shifted_char = chr((ord(char) - 97 + shift) % 26 + 97)
            elif direction == "reverse":
                shifted_char = chr((ord(char) - 97 - shift) % 26 + 97)
            else:
                raise ValueError(
                    "Letter shifting method unrecognized. Supported methods: forward/reverse.")
            shifted_word += shifted_char
        return shifted_word
    
    def encode(self) -> PassPhrase:
        """ """
        permuted_passphrase = self._permute(self.passphrase, self.permutation_pattern, "forward")
        scrambled_words = []
        for word in permuted_passphrase.words:
            scrambled_words.append(self._shift_letters(word, self.shift, "forward"))
        return PassPhrase(scrambled_words)
    
    def decode(self) -> PassPhrase:
        """ """
        unpermuted_words = self._permute(self.passphrase, self.permutation_pattern, "reverse")
        unscrambled_words = []
        for word in unpermuted_words.words:
            unscrambled_words.append(self._shift_letters(word, self.shift, "reverse"))
        return PassPhrase(unscrambled_words)


if __name__ == "__main__": 
    
    passphrase = PassPhrase(["first", "second", "third", "fourth", "fifth"])
    permutation_pattern = Permutation([2,1,0,4,3])
    shift = 25

    scrambler = PassPhraseScrambler(
        passphrase, 
        permutation_pattern, 
        shift)
    scrambled_passphrase = scrambler.encode()
    print(scrambled_passphrase)
    unscrambler = PassPhraseScrambler(
        scrambled_passphrase, permutation_pattern, shift)
    unscrambled_passphrase = unscrambler.decode()
    print(unscrambled_passphrase.as_string())
    
