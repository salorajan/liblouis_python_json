import os
from pathlib import Path
from typing import List, Dict, Optional

class Hyphenator:
    """
    Handles hyphenation rules for liblouis.
    Liblouis uses a modified TeX hyphenation algorithm.
    """
    def __init__(self, table):
        self.table = table
        self.patterns: Dict[str, List[int]] = {}
        self.exceptions: Dict[str, List[int]] = {}

    def load_hyphen_file(self, file_path: Path):
        """
        Parses a .dic or .ctb hyphenation section.
        """
        if not file_path.exists():
            return

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.split('#')[0].strip()
                if not line: continue
                
                # Basic TeX pattern parsing (simplified)
                # patterns look like: .a1b2c.
                if any(c.isdigit() for c in line):
                    self._add_pattern(line)
                else:
                    self._add_exception(line)

    def _add_pattern(self, pattern_str: str):
        # Extract digits and positions
        clean_pattern = ""
        levels = []
        i = 0
        while i < len(pattern_str):
            if pattern_str[i].isdigit():
                levels.append(int(pattern_str[i]))
                i += 1
            else:
                levels.append(0)
                clean_pattern += pattern_str[i]
                i += 1
        levels.append(0) # Trailing level
        self.patterns[clean_pattern] = levels

    def _add_exception(self, exception_str: str):
        # Exceptions look like: hy-phen-ation
        parts = exception_str.split('-')
        clean = "".join(parts)
        levels = [0] * (len(clean) + 1)
        curr = 0
        for part in parts[:-1]:
            curr += len(part)
            levels[curr] = 1 # Hyphen possible
        self.exceptions[clean] = levels

    def hyphenate(self, word: str) -> List[int]:
        """
        Returns a list of hyphenation levels for each inter-character position.
        """
        if word in self.exceptions:
            return self.exceptions[word]
            
        word_folded = word.lower()
        padded = "." + word_folded + "."
        levels = [0] * (len(padded) + 1)
        
        for i in range(len(padded)):
            for j in range(i + 1, len(padded) + 1):
                sub = padded[i:j]
                if sub in self.patterns:
                    p_levels = self.patterns[sub]
                    for k, val in enumerate(p_levels):
                        if i + k < len(levels):
                            levels[i + k] = max(levels[i + k], val)
        
        # Strip padding levels
        return levels[2:-2]

    def get_hyphenated_word(self, word: str, hyphen_char: str = "-") -> str:
        levels = self.hyphenate(word)
        result = []
        for i, char in enumerate(word):
            result.append(char)
            if i < len(levels) and levels[i] % 2 != 0:
                result.append(hyphen_char)
        return "".join(result)
