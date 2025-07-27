import random
import os

def load_words(language='russian'):
    if language == 'russian':
        filepath = 'words_rus.txt'
        default_words = ['программирование', 'компьютер', 'разработка', 'алгоритм', 'функция']
    else:  
        filepath = 'words_eng.txt'
        default_words = ['programming', 'computer', 'development', 'algorithm', 'function']
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            words = [line.strip().lower() for line in file if line.strip()]
        
        # Слова с менее чем 4 буквами и менее чем 2 уникальными буквами не добавляются
        words = [word for word in words if len(word) >= 4 and len(set(word)) >= 2]
        
        if not words:
            print(f"В файле {filepath} нет подходящих слов. Используется встроенный список.")
            return default_words
        
        return words
    except FileNotFoundError:
        print(f"Файл {filepath} не найден. Используется встроенный список слов.")
        return default_words

def choose_language():
    print("\nВыберите язык для игры:")
    print("1. Русский")
    print("2. English")
    
    while True:
        choice = input("Введите номер (1 или 2): ").strip()
        if choice == '1':
            return 'russian'
        elif choice == '2':
            return 'english'
        else:
            print("Пожалуйста, введите 1 для русского или 2 для английского языка.")

def initialize_game(word_list):
    secret_word = random.choice(word_list)
    attempts_left = 7 
    display_word = ['_'] * len(secret_word)
    guessed_letters = set()
    wrong_letters = set()
    
    unique_letters = list(set(secret_word))
    if len(unique_letters) >= 3:
        revealed_letters = random.sample(unique_letters, 2)
    elif len(unique_letters) == 2:
        revealed_letters = random.sample(unique_letters, 1)
    
    for letter in revealed_letters:
        for i, char in enumerate(secret_word):
            if char == letter:
                display_word[i] = letter
        guessed_letters.add(letter)
    
    return {
        'secret_word': secret_word,
        'attempts_left': attempts_left,
        'display_word': display_word,
        'guessed_letters': guessed_letters,
        'wrong_letters': wrong_letters
    }

def display_hangman(attempts_left):
    stages = [
        # 0
        """
        ______
        |    |
        |    O
        |   /|\\
        |   / \\
        |
        """,
        # 1
        """
        ______
        |    |
        |    O
        |   /|\\
        |   /
        |
        """,
        # 2
        """
        ______
        |    |
        |    O
        |   /|\\
        |
        |
        """,
        # 3
        """
        ______
        |    |
        |    O
        |   /|
        |
        |
        """,
        # 4
        """
        ______
        |    |
        |    O
        |    |
        |
        |
        """,
        # 5
        """
        ______
        |    |
        |    O
        |
        |
        |
        """,
        # 6
        """
        ______
        |    |
        |
        |
        |
        |
        """,
        # 7
        """
        
        |
        |
        |
        |
        |
        """
    ]
    return stages[attempts_left]

def display_game_state(display_word, attempts_left, wrong_letters):
    print("\n" + "="*50)
    print(display_hangman(attempts_left))
    print(f"Слово: {' '.join(display_word)}")
    print(f"Осталось попыток: {attempts_left}")
    if wrong_letters:
        print(f"Неверные буквы: {', '.join(sorted(wrong_letters))}")
    print("="*50)

def get_player_input(guessed_letters, secret_word_length):
    while True:
        try:
            user_input = input("Введите букву или целое слово: ").strip().lower()
            
            if not user_input:
                print("Пожалуйста, введите букву или слово!")
                continue
            
            if not user_input.isalpha():
                print("Пожалуйста, используйте только буквы!")
                continue
            
            # попытка угадать целое слово
            if len(user_input) == secret_word_length:
                return {'type': 'word', 'value': user_input}
            
            elif len(user_input) == 1:
                letter = user_input
                if letter in guessed_letters:
                    print(f"Вы уже называли букву '{letter}'. Попробуйте другую!")
                    continue
                return {'type': 'letter', 'value': letter}
            
            else:
                print(f"Введите либо одну букву, либо слово из {secret_word_length} букв!")
                print("(Защита от случайных нажатий)")
                continue
            
        except KeyboardInterrupt:
            print("\nИгра прервана пользователем.")
            return None

def update_display_word(secret_word, display_word, letter):
    updated = False
    for i, char in enumerate(secret_word):
        if char == letter:
            display_word[i] = letter
            updated = True
    return updated

def check_win(secret_word, display_word):
    return '_' not in display_word

def check_loss(attempts_left):
    return attempts_left <= 0

def play_again():
    while True:
        answer = input("Хотите сыграть еще раз? (да/нет): ").strip().lower()
        if answer in ['да', 'д', 'yes', 'y']:
            return True
        elif answer in ['нет', 'н', 'no', 'n']:
            return False
        else:
            print("Пожалуйста, введите 'да' или 'нет'.")

def run_game():
    print("Добро пожаловать в игру 'Виселица'!")
    print("Попробуйте угадать загаданное слово, называя буквы по одной.")
    
    language = choose_language()
    
    word_list = load_words(language)
    
    if language == 'russian':
        print("Играем на русском языке!")
    else:
        print("Playing in English!")
    
    while True:
        game_data = initialize_game(word_list)
        secret_word = game_data['secret_word']
        attempts_left = game_data['attempts_left']
        display_word = game_data['display_word']
        guessed_letters = game_data['guessed_letters']
        wrong_letters = game_data['wrong_letters']
        
        print(f"\nНовая игра! Загадано слово из {len(secret_word)} букв.")
        print("Для облегчения игры уже раскрыты две (или одна) случайные буквы!")

        while True:
            display_game_state(display_word, attempts_left, wrong_letters)
            
            user_input = get_player_input(guessed_letters, len(secret_word))
            
            # попытка угадать слово
            if user_input['type'] == 'word':
                guessed_word = user_input['value']
                if guessed_word == secret_word:
                    display_word = list(secret_word)  
                    print(f"🎉 ПРЕВОСХОДНО! Вы угадали слово '{secret_word}' целиком!")
                else:
                    attempts_left -= 1
                    print(f"❌ Неверно! Это не слово '{guessed_word}'.")
            
            elif user_input['type'] == 'letter':
                letter = user_input['value']
                
                guessed_letters.add(letter)
                
                if update_display_word(secret_word, display_word, letter):
                    print(f"Отлично! Буква '{letter}' есть в слове!")
                else:
                    wrong_letters.add(letter)
                    attempts_left -= 1
                    print(f"К сожалению, буквы '{letter}' нет в слове.")
            
            if check_win(secret_word, display_word):
                display_game_state(display_word, attempts_left, wrong_letters)
                print("🎉 ПОЗДРАВЛЯЕМ! Вы угадали слово!")
                print(f"Загаданное слово: {secret_word}")
                break
            elif check_loss(attempts_left):
                display_game_state(display_word, attempts_left, wrong_letters)
                print("💀 Игра окончена! Вы проиграли.")
                print(f"Загаданное слово было: {secret_word}")
                break
        
        if not play_again():
            break
    
    print("Спасибо за игру! До свидания!")

def main():
    try:
        run_game()
    except KeyboardInterrupt:
        print("\n\nИгра прервана. До свидания!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main() 