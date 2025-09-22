"""
Генератор файлов с японскими символами
"""

import os
from japanese_data import QUIZ_TYPES


class JapaneseSymbolGenerator:
    def __init__(self):
        pass
        
    def generate_symbol_file(self, symbol, symbol_data, quiz_type, folder):
        """Генерирует файл с данными о символе"""
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        filename = f"{symbol}.txt"
        filepath = os.path.join(folder, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Символ: {symbol}\n")
            
            if quiz_type == "kanji":
                f.write(f"Значение: {symbol_data['meaning']}\n")
                f.write(f"Чтение: {symbol_data['reading']}\n")
                f.write(f"Romaji: {symbol_data['romaji']}\n")
            else:  # hiragana или katakana
                f.write(f"Romaji: {symbol_data['romaji']}\n")
                f.write(f"Звук: {symbol_data['sound']}\n")
        
        return filepath
    
    def generate_all_files(self):
        """Генерирует файлы для всех типов символов"""
        all_generated_files = {}
        
        for quiz_type, quiz_info in QUIZ_TYPES.items():
            generated_files = []
            data = quiz_info['data']
            folder = quiz_info['folder']
            
            for symbol, symbol_data in data.items():
                filepath = self.generate_symbol_file(symbol, symbol_data, quiz_type, folder)
                generated_files.append(filepath)
                
            all_generated_files[quiz_type] = generated_files
            print(f"Сгенерировано {len(generated_files)} файлов для {quiz_info['name']}")
            
        return all_generated_files


if __name__ == "__main__":
    generator = JapaneseSymbolGenerator()
    files = generator.generate_all_files()
    total_files = sum(len(file_list) for file_list in files.values())
    print(f"Всего сгенерировано {total_files} файлов")
