"""
Телеграм-бот для изучения японских иероглифов
"""

from collections import defaultdict
from math import log, atan
import numpy as np
import os
import random
import logging
from typing import Dict, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from dotenv import load_dotenv

from japanese_data import QUIZ_TYPES
from image_generator import JapaneseSymbolGenerator

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class JapaneseBotState:
    def __init__(self):
        self.user_sessions: Dict[int, Dict[str, Any]] = {}
        self.symbol_generator = JapaneseSymbolGenerator()
        
    def get_user_session(self, user_id: int) -> Dict[str, Any]:
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                'current_symbol': None,
                'current_quiz_type': None,
                'score': 0,
                'total_questions': 0,
                'waiting_for_answer': False,
                'quiz_started': False,
                'current_question_message_id': None,
                'user_answer_message_id': None,
                'stats_message_id': None,
                'main_menu_message_id': None,
                'submenu_message_id': None,
                # Списки для хранения всех ID сообщений
                'all_question_message_ids': [],
                'all_user_answer_message_ids': [],
                'all_stats_message_ids': [],
                'all_main_menu_message_ids': [],
                'all_submenu_message_ids': [],
                # История ответов пользователя по иероглифам
                'symbols_stats': defaultdict(int)
            }
        return self.user_sessions[user_id]


bot_state = JapaneseBotState()


def generate_wrong_answers(correct_symbol: str, quiz_type: str, count: int = 3) -> list:
    """Генерирует неправильные варианты ответов для викторины с кнопками"""
    if quiz_type == "romaji_to_hiragana":
        data = QUIZ_TYPES["hiragana_to_romaji"]["data"]
    elif quiz_type == "romaji_to_katakana":
        data = QUIZ_TYPES["katakana_to_romaji"]["data"]
    else:
        return []
    
    # Получаем все символы кроме правильного
    all_symbols = [symbol for symbol in data.keys() if symbol != correct_symbol]
    
    # Выбираем случайные неправильные варианты
    import random
    wrong_answers = random.sample(all_symbols, min(count, len(all_symbols)))
    
    return wrong_answers


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    user_id = user.id
    
    session = bot_state.get_user_session(user_id)
    session['score'] = 0
    session['total_questions'] = 0
    session['waiting_for_answer'] = False
    session['quiz_started'] = False
    session['current_question_message_id'] = None
    session['user_answer_message_id'] = None
    session['stats_message_id'] = None
    session['main_menu_message_id'] = None
    session['submenu_message_id'] = None
    # Очищаем списки всех ID сообщений
    session['all_question_message_ids'] = []
    session['all_user_answer_message_ids'] = []
    session['all_stats_message_ids'] = []
    session['all_main_menu_message_ids'] = []
    session['all_submenu_message_ids'] = []
    # Очищаем статистику по иероглифам
    session['symbols_stats'] = defaultdict(int)
    
    welcome_message = (
        f"Привет, {user.first_name}! 👋\n\n"
        "Добро пожаловать в бот для изучения японского языка! 🇯🇵\n\n"
        "Выбери тип викторины:\n\n"
        "🈳 **Кандзи** - иероглифы и их значения (12 символов)\n"
        "🈶 **Хирагана** - основная слоговая азбука (46 символов)\n"
        "🈯 **Катакана** - азбука для заимствованных слов (46 символов)\n\n"
        "Для каждой азбуки доступны два режима:\n"
        "• Символ → Romaji\n"
        "• Romaji → Символ"
    )
    
    keyboard = [
        [InlineKeyboardButton("🈳 Кандзи", callback_data="quiz_kanji")],
        [InlineKeyboardButton("🈶 Хирагана", callback_data="menu_hiragana")],
        [InlineKeyboardButton("🈯 Катакана", callback_data="menu_katakana")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')
    session['main_menu_message_id'] = message.message_id
    session['all_main_menu_message_ids'].append(message.message_id)


async def show_quiz_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает меню выбора типа викторины"""
    query = update.callback_query
    if query:
        await query.answer()
    
    selection_message = (
        "Выбери тип викторины:\n\n"
        "🈳 **Кандзи** - иероглифы и их значения (12 символов)\n"
        "🈶 **Хирагана** - основная слоговая азбука (46 символов)\n"
        "🈯 **Катакана** - азбука для заимствованных слов (46 символов)\n\n"
        "Для каждой азбуки доступны два режима:\n"
        "• Символ → Romaji\n"
        "• Romaji → Символ"
    )
    
    keyboard = [
        [InlineKeyboardButton("🈳 Кандзи", callback_data="quiz_kanji")],
        [InlineKeyboardButton("🈶 Хирагана", callback_data="menu_hiragana")],
        [InlineKeyboardButton("🈯 Катакана", callback_data="menu_katakana")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.message.reply_text(selection_message, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(selection_message, reply_markup=reply_markup, parse_mode='Markdown')


async def show_hiragana_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает меню выбора режима хираганы"""
    query = update.callback_query
    user_id = query.from_user.id
    session = bot_state.get_user_session(user_id)
    await query.answer()
    
    menu_message = (
        "🈶 **Хирагана**\n\n"
        "Выбери набор символов:\n\n"
        "**Базовая хирагана** (46 символов) - основные символы\n"
        "**Тэнтэн и мару** (25 символов) - символы с ゛ и ゜\n"
        "**Полная хирагана** (71 символ) - все символы вместе"
    )
    
    keyboard = [
        [InlineKeyboardButton("🈶 Базовая хирагана", callback_data="hiragana_basic_menu")],
        [InlineKeyboardButton("🈶゛゜ Тэнтэн и мару", callback_data="hiragana_dakuten_menu")],
        [InlineKeyboardButton("🈶📖 Полная хирагана", callback_data="hiragana_full_menu")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = await query.message.reply_text(menu_message, reply_markup=reply_markup, parse_mode='Markdown')
    session['submenu_message_id'] = message.message_id
    session['all_submenu_message_ids'].append(message.message_id)


async def show_hiragana_basic_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает меню базовой хираганы"""
    query = update.callback_query
    user_id = query.from_user.id
    session = bot_state.get_user_session(user_id)
    await query.answer()
    
    menu_message = (
        "🈶 **Базовая хирагана** (46 символов)\n\n"
        "Выбери режим викторины:\n\n"
        "**Символ → Romaji**: Видишь символ хираганы, пишешь его чтение латиницей\n"
        "**Romaji → Символ**: Видишь чтение латиницей, выбираешь правильный символ из кнопок"
    )
    
    keyboard = [
        [InlineKeyboardButton("🈶 → 🔤 Символ → Romaji", callback_data="quiz_hiragana_to_romaji")],
        [InlineKeyboardButton("🔤 → 🈶 Romaji → Символ", callback_data="quiz_romaji_to_hiragana")],
        [InlineKeyboardButton("🔙 Назад", callback_data="menu_hiragana")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = await query.message.reply_text(menu_message, reply_markup=reply_markup, parse_mode='Markdown')
    session['submenu_message_id'] = message.message_id
    session['all_submenu_message_ids'].append(message.message_id)


async def show_hiragana_dakuten_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает меню хираганы с тэнтэн и мару"""
    query = update.callback_query
    user_id = query.from_user.id
    session = bot_state.get_user_session(user_id)
    await query.answer()
    
    menu_message = (
        "🈶゛゜ **Тэнтэн и мару** (25 символов)\n\n"
        "Символы хираганы с диакритическими знаками:\n"
        "• **Тэнтэн** (゛) - озвончение: が, ざ, だ\n"
        "• **Мару** (゜) - придыхание: ぱ, ぴ, ぷ, ぺ, ぽ\n\n"
        "Выбери режим викторины:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🈶゛゜ → 🔤 Символ → Romaji", callback_data="quiz_hiragana_dakuten_to_romaji")],
        [InlineKeyboardButton("🔤 → 🈶゛゜ Romaji → Символ", callback_data="quiz_romaji_to_hiragana_dakuten")],
        [InlineKeyboardButton("🔙 Назад", callback_data="menu_hiragana")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = await query.message.reply_text(menu_message, reply_markup=reply_markup, parse_mode='Markdown')
    session['submenu_message_id'] = message.message_id
    session['all_submenu_message_ids'].append(message.message_id)


async def show_hiragana_full_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает меню полной хираганы"""
    query = update.callback_query
    user_id = query.from_user.id
    session = bot_state.get_user_session(user_id)
    await query.answer()
    
    menu_message = (
        "🈶📖 **Полная хирагана** (71 символ)\n\n"
        "Все символы хираганы:\n"
        "• Базовые символы (46)\n"
        "• Символы с тэнтэн (20)\n"
        "• Символы с мару (5)\n\n"
        "Выбери режим викторины:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🈶📖 → 🔤 Символ → Romaji", callback_data="quiz_hiragana_full_to_romaji")],
        [InlineKeyboardButton("🔤 → 🈶📖 Romaji → Символ", callback_data="quiz_romaji_to_hiragana_full")],
        [InlineKeyboardButton("🔙 Назад", callback_data="menu_hiragana")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = await query.message.reply_text(menu_message, reply_markup=reply_markup, parse_mode='Markdown')
    session['submenu_message_id'] = message.message_id
    session['all_submenu_message_ids'].append(message.message_id)


async def show_katakana_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает меню выбора режима катаканы"""
    query = update.callback_query
    user_id = query.from_user.id
    session = bot_state.get_user_session(user_id)
    await query.answer()
    
    menu_message = (
        "🈯 **Катакана** (46 символов)\n\n"
        "Выбери режим викторины:\n\n"
        "**Символ → Romaji**: Видишь символ катаканы, пишешь его чтение латиницей\n"
        "**Romaji → Символ**: Видишь чтение латиницей, выбираешь правильный символ из кнопок"
    )
    
    keyboard = [
        [InlineKeyboardButton("🈯 → 🔤 Символ → Romaji", callback_data="quiz_katakana_to_romaji")],
        [InlineKeyboardButton("🔤 → 🈯 Romaji → Символ", callback_data="quiz_romaji_to_katakana")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = await query.message.reply_text(menu_message, reply_markup=reply_markup, parse_mode='Markdown')
    session['submenu_message_id'] = message.message_id
    session['all_submenu_message_ids'].append(message.message_id)

def get_weight(delta: float) -> float:
    if delta >= 0:
        return 1.0 / (log(delta + 1)**2 + 1)
    return atan(-delta) + 1

def sample_symbol(stats: dict, symbols: list[str]) -> str:
    deltas = [float(stats[symbol]) for symbol in symbols]
    weights = [get_weight(delta) for delta in deltas]
    sum_weights = sum(weights)
    probas = [weight / sum_weights for weight in weights]
    return np.random.choice(symbols, p=probas)


async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE, quiz_type: str = None) -> None:
    """Начинает новый вопрос викторины"""
    query = update.callback_query
    if query:
        await query.answer()
        user_id = query.from_user.id
    else:
        user_id = update.effective_user.id
    
    session = bot_state.get_user_session(user_id)
    
    # Если передан тип викторины, устанавливаем его
    if quiz_type:
        session['current_quiz_type'] = quiz_type
        session['quiz_started'] = True
    
    # Проверяем, что тип викторины установлен
    if not session.get('current_quiz_type'):
        await show_quiz_selection(update, context)
        return
    
    current_quiz_type = session['current_quiz_type']
    quiz_info = QUIZ_TYPES[current_quiz_type]
    data = quiz_info['data']
    
    # Выбираем случайный символ
    symbol = sample_symbol(session['symbol_stats'], data.keys())
    session['current_symbol'] = symbol
    session['waiting_for_answer'] = True
    
    # Формируем текст вопроса в зависимости от типа викторины
    if quiz_info['show_symbol']:
        question_text = (
            f"❓ Вопрос {session['total_questions'] + 1} ({quiz_info['name']})\n"
            f"📊 Счет: {session['score']}/{session['total_questions']}\n\n"
            f"Символ: **{symbol}**\n\n"
            f"{quiz_info['question']}"
        )
        
        if current_quiz_type == "kanji":
            question_text += " Напиши значение на русском языке:"
        else:
            question_text += " Напиши в латинице (romaji):"
    else:
        # Для обратных викторин показываем romaji
        romaji = data[symbol]['romaji']
        question_text = (
            f"❓ Вопрос {session['total_questions'] + 1} ({quiz_info['name']})\n"
            f"📊 Счет: {session['score']}/{session['total_questions']}\n\n"
            f"Чтение: **{romaji}**\n\n"
            f"{quiz_info['question']} Напиши символ:"
        )
    
    # Создаем клавиатуру в зависимости от типа викторины
    if quiz_info['answer_type'] == "symbol":
        # Для режимов Romaji→Символ создаем кнопки с вариантами ответов
        wrong_answers = generate_wrong_answers(symbol, current_quiz_type, 3)
        all_answers = [symbol] + wrong_answers
        random.shuffle(all_answers)
        
        # Создаем кнопки с вариантами ответов (по 2 в ряд)
        keyboard = []
        for i in range(0, len(all_answers), 2):
            row = []
            for j in range(2):
                if i + j < len(all_answers):
                    answer = all_answers[i + j]
                    row.append(InlineKeyboardButton(answer, callback_data=f"answer_{answer}"))
            keyboard.append(row)
        
        # Добавляем кнопки навигации
        keyboard.append([InlineKeyboardButton("🔙 Выбрать другой тип", callback_data="back_to_menu")])
    else:
        # Для остальных режимов обычные кнопки
        keyboard = [
            [InlineKeyboardButton("🔄 Следующий вопрос", callback_data=f"next_{current_quiz_type}")],
            [InlineKeyboardButton("🔙 Выбрать другой тип", callback_data="back_to_menu")]
        ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Если есть предыдущее сообщение с вопросом, редактируем его
    if session.get('current_question_message_id') and query:
        try:
            await query.edit_message_text(
                text=question_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        except Exception:
            # Если не удалось отредактировать, отправляем новое
            message = await query.message.reply_text(
                question_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            session['current_question_message_id'] = message.message_id
            session['all_question_message_ids'].append(message.message_id)
    else:
        # Отправляем новое сообщение
        if query:
            message = await query.message.reply_text(
                question_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            message = await context.bot.send_message(
                chat_id=user_id,
                text=question_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        session['current_question_message_id'] = message.message_id
        session['all_question_message_ids'].append(message.message_id)


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает ответ пользователя"""
    user_id = update.effective_user.id
    session = bot_state.get_user_session(user_id)
    
    if not session['waiting_for_answer'] or not session.get('quiz_started'):
        await update.message.reply_text(
            "Сначала выбери тип викторины командой /start!"
        )
        return
    
    # Сохраняем ID сообщения пользователя для последующего удаления
    session['user_answer_message_id'] = update.message.message_id
    session['all_user_answer_message_ids'].append(update.message.message_id)
    
    current_quiz_type = session.get('current_quiz_type')
    if current_quiz_type:
        quiz_info = QUIZ_TYPES[current_quiz_type]
        # Если это режим с кнопками, игнорируем текстовые сообщения
        if quiz_info['answer_type'] == "symbol":
            await update.message.reply_text(
                "Для этого режима используй кнопки с вариантами ответов! 👆"
            )
            return
    
    user_answer = update.message.text.lower().strip()
    current_symbol = session['current_symbol']
    current_quiz_type = session['current_quiz_type']
    
    if not current_symbol or not current_quiz_type:
        await update.message.reply_text("Произошла ошибка. Начни заново с /start")
        return
    
    quiz_info = QUIZ_TYPES[current_quiz_type]
    symbol_data = quiz_info['data'][current_symbol]
    
    # Определяем правильный ответ в зависимости от типа викторины
    if quiz_info['answer_type'] == "meaning":
        correct_answer = symbol_data['meaning'].lower()
        is_correct = user_answer in correct_answer or correct_answer in user_answer
    elif quiz_info['answer_type'] == "romaji":
        correct_answer = symbol_data['romaji'].lower()
        is_correct = user_answer == correct_answer
    else:  # answer_type == "symbol"
        correct_answer = current_symbol
        is_correct = user_answer == correct_answer
    
    session['total_questions'] += 1
    session['waiting_for_answer'] = False
    
    if is_correct:
        session['score'] += 1
        session['symbol_stats'][current_symbol] += 1
        response = f"✅ Правильно!\n\n"
    else:
        session['symbol_stats'][current_symbol] -= 1
        response = f"❌ Неправильно!\n\n"
    
    # Формируем детальную информацию о символе
    response += f"Символ: {current_symbol}\n"
    
    if quiz_info['answer_type'] == "meaning":
        response += (
            f"Значение: {symbol_data['meaning']}\n"
            f"Чтение: {symbol_data['reading']} ({symbol_data['romaji']})\n"
        )
    else:
        response += (
            f"Romaji: {symbol_data['romaji']}\n"
            f"Звук: {symbol_data['sound']}\n"
        )
    
    if not is_correct:
        if quiz_info['answer_type'] == "meaning":
            response += f"Правильный ответ: {symbol_data['meaning']}\n"
        elif quiz_info['answer_type'] == "romaji":
            response += f"Правильный ответ: {symbol_data['romaji']}\n"
        else:  # answer_type == "symbol"
            response += f"Правильный ответ: {current_symbol}\n"
        response += f"Твой ответ: {update.message.text}\n"
    
    response += f"\n📊 Твой счет: {session['score']}/{session['total_questions']}"
    
    keyboard = [
        [InlineKeyboardButton("🎯 Следующий вопрос", callback_data=f"next_{current_quiz_type}")],
        [InlineKeyboardButton("📊 Показать статистику", callback_data="show_stats")],
        [InlineKeyboardButton("🔙 Выбрать другой тип", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Редактируем сообщение с вопросом, показывая результат
    if session.get('current_question_message_id'):
        try:
            await context.bot.edit_message_text(
                chat_id=user_id,
                message_id=session['current_question_message_id'],
                text=response,
                reply_markup=reply_markup
            )
        except Exception:
            # Если не удалось отредактировать, отправляем новое
            message = await update.message.reply_text(response, reply_markup=reply_markup)
            session['current_question_message_id'] = message.message_id
            session['all_question_message_ids'].append(message.message_id)
    else:
        message = await update.message.reply_text(response, reply_markup=reply_markup)
        session['current_question_message_id'] = message.message_id
        session['all_question_message_ids'].append(message.message_id)


async def handle_button_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, selected_answer: str) -> None:
    """Обрабатывает ответ пользователя через кнопки"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    session = bot_state.get_user_session(user_id)
    
    if not session['waiting_for_answer'] or not session.get('quiz_started'):
        await query.message.reply_text("Сначала выбери тип викторины командой /start!")
        return
    
    current_symbol = session['current_symbol']
    current_quiz_type = session['current_quiz_type']
    
    if not current_symbol or not current_quiz_type:
        await query.message.reply_text("Произошла ошибка. Начни заново с /start")
        return
    
    quiz_info = QUIZ_TYPES[current_quiz_type]
    symbol_data = quiz_info['data'][current_symbol]
    
    session['total_questions'] += 1
    session['waiting_for_answer'] = False
    
    is_correct = selected_answer == current_symbol
    
    if is_correct:
        session['score'] += 1
        session['symbol_stats'][current_symbol] += 1
        response = f"✅ Правильно!\n\n"
    else:
        session['symbol_stats'][current_symbol] -= 1
        response = f"❌ Неправильно!\n\n"
    
    # Формируем детальную информацию о символе
    response += f"Символ: {current_symbol}\n"
    response += (
        f"Romaji: {symbol_data['romaji']}\n"
        f"Звук: {symbol_data['sound']}\n"
    )
    
    if not is_correct:
        response += f"Правильный ответ: {current_symbol}\n"
        response += f"Твой ответ: {selected_answer}\n"
    
    response += f"\n📊 Твой счет: {session['score']}/{session['total_questions']}"
    
    keyboard = [
        [InlineKeyboardButton("🎯 Следующий вопрос", callback_data=f"next_{current_quiz_type}")],
        [InlineKeyboardButton("📊 Показать статистику", callback_data="show_stats")],
        [InlineKeyboardButton("🔙 Выбрать другой тип", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Редактируем сообщение с вопросом, показывая результат
    try:
        await query.edit_message_text(
            text=response,
            reply_markup=reply_markup
        )
    except Exception:
        # Если не удалось отредактировать, отправляем новое
        message = await query.message.reply_text(response, reply_markup=reply_markup)
        session['current_question_message_id'] = message.message_id
        session['all_question_message_ids'].append(message.message_id)


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает статистику пользователя"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    session = bot_state.get_user_session(user_id)
    
    if session['total_questions'] == 0:
        stats_text = "📊 У тебя пока нет статистики. Начни викторину!"
    else:
        accuracy = (session['score'] / session['total_questions']) * 100
        stats_text = (
            f"📊 Твоя статистика:\n\n"
            f"✅ Правильных ответов: {session['score']}\n"
            f"❌ Неправильных ответов: {session['total_questions'] - session['score']}\n"
            f"📝 Всего вопросов: {session['total_questions']}\n"
            f"🎯 Точность: {accuracy:.1f}%"
        )
    
    # Определяем кнопку для продолжения викторины
    current_quiz_type = session.get('current_quiz_type')
    if current_quiz_type and session.get('quiz_started'):
        continue_button_text = "🎯 Продолжить викторину"
        continue_callback = f"continue_{current_quiz_type}"
    else:
        continue_button_text = "🔙 Выбрать викторину"
        continue_callback = "back_to_menu"
    
    keyboard = [[InlineKeyboardButton(continue_button_text, callback_data=continue_callback)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = await query.message.reply_text(stats_text, reply_markup=reply_markup)
    session['stats_message_id'] = message.message_id
    session['all_stats_message_ids'].append(message.message_id)


async def delete_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Удаляет сообщение пользователя, если оно есть"""
    query = update.callback_query
    user_id = query.from_user.id
    session = bot_state.get_user_session(user_id)
    
    # Удаляем сообщение пользователя, если оно было сохранено
    if session.get('user_answer_message_id'):
        try:
            await context.bot.delete_message(
                chat_id=user_id,
                message_id=session['user_answer_message_id']
            )
            session['user_answer_message_id'] = None
        except Exception:
            # Если не удалось удалить (например, сообщение уже удалено), игнорируем
            pass


async def delete_stats_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Удаляет сообщение со статистикой, если оно есть"""
    query = update.callback_query
    user_id = query.from_user.id
    session = bot_state.get_user_session(user_id)
    
    # Удаляем сообщение со статистикой, если оно было сохранено
    if session.get('stats_message_id'):
        try:
            await context.bot.delete_message(
                chat_id=user_id,
                message_id=session['stats_message_id']
            )
            session['stats_message_id'] = None
        except Exception:
            # Если не удалось удалить (например, сообщение уже удалено), игнорируем
            pass


async def delete_all_messages_and_show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """РАДИКАЛЬНОЕ РЕШЕНИЕ: Удаляет ВСЕ сообщения и создает новое главное меню"""
    query = update.callback_query
    user_id = query.from_user.id
    session = bot_state.get_user_session(user_id)
    
    # Собираем ВСЕ ID сообщений из списков
    all_message_ids = []
    all_message_ids.extend(session.get('all_main_menu_message_ids', []))
    all_message_ids.extend(session.get('all_question_message_ids', []))
    all_message_ids.extend(session.get('all_user_answer_message_ids', []))
    all_message_ids.extend(session.get('all_stats_message_ids', []))
    all_message_ids.extend(session.get('all_submenu_message_ids', []))
    
    # Также добавляем текущие ID на случай, если они не попали в списки
    current_ids = [
        session.get('main_menu_message_id'),
        session.get('current_question_message_id'),
        session.get('user_answer_message_id'),
        session.get('stats_message_id'),
        session.get('submenu_message_id')
    ]
    all_message_ids.extend([id for id in current_ids if id is not None])
    
    # Удаляем дубликаты
    unique_message_ids = list(set(all_message_ids))
    
    logger.info(f"Удаляем {len(unique_message_ids)} сообщений: {unique_message_ids}")
    
    # Удаляем все сообщения
    for message_id in unique_message_ids:
        try:
            await context.bot.delete_message(
                chat_id=user_id,
                message_id=message_id
            )
        except Exception as e:
            logger.debug(f"Не удалось удалить сообщение {message_id}: {e}")
            # Игнорируем ошибки удаления
            pass
    
    # Полностью очищаем все ID сообщений
    session['main_menu_message_id'] = None
    session['current_question_message_id'] = None
    session['user_answer_message_id'] = None
    session['stats_message_id'] = None
    session['submenu_message_id'] = None
    # Очищаем все списки ID сообщений
    session['all_question_message_ids'] = []
    session['all_user_answer_message_ids'] = []
    session['all_stats_message_ids'] = []
    session['all_main_menu_message_ids'] = []
    session['all_submenu_message_ids'] = []
    
    # Сбрасываем состояние викторины
    session['waiting_for_answer'] = False
    session['quiz_started'] = False
    
    # Создаем СОВЕРШЕННО НОВОЕ главное меню
    welcome_message = (
        f"🇯🇵 **Выбери тип викторины:**\n\n"
        "🈳 **Кандзи** - изучение иероглифов\n"
        "🈶 **Хирагана** - основная слоговая азбука\n"
        "🈯 **Катакана** - слоговая азбука для заимствованных слов\n\n"
        "Для каждой азбуки доступны два режима:\n"
        "• Символ → Romaji\n"
        "• Romaji → Символ"
    )
    
    keyboard = [
        [InlineKeyboardButton("🈳 Кандзи", callback_data="quiz_kanji")],
        [InlineKeyboardButton("🈶 Хирагана", callback_data="menu_hiragana")],
        [InlineKeyboardButton("🈯 Катакана", callback_data="menu_katakana")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # ВСЕГДА создаем новое сообщение (никаких попыток редактирования!)
    message = await context.bot.send_message(
        chat_id=user_id,
        text=welcome_message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    session['main_menu_message_id'] = message.message_id
    session['all_main_menu_message_ids'].append(message.message_id)
    
    logger.info(f"Создано новое главное меню с ID: {message.message_id}")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    
    if query.data.startswith("quiz_"):
        quiz_type = query.data.replace("quiz_", "")
        await start_quiz(update, context, quiz_type)
    elif query.data.startswith("next_"):
        quiz_type = query.data.replace("next_", "")
        # Удаляем сообщение пользователя и статистику перед следующим вопросом
        await delete_user_message(update, context)
        await delete_stats_message(update, context)
        await start_quiz(update, context, quiz_type)
    elif query.data.startswith("continue_"):
        quiz_type = query.data.replace("continue_", "")
        # Удаляем сообщение со статистикой и продолжаем викторину
        await delete_stats_message(update, context)
        await start_quiz(update, context, quiz_type)
    elif query.data.startswith("answer_"):
        selected_answer = query.data.replace("answer_", "")
        await handle_button_answer(update, context, selected_answer)
    elif query.data == "show_stats":
        await show_stats(update, context)
    elif query.data == "back_to_menu":
        await delete_all_messages_and_show_menu(update, context)
    elif query.data == "menu_hiragana":
        await show_hiragana_menu(update, context)
    elif query.data == "hiragana_basic_menu":
        await show_hiragana_basic_menu(update, context)
    elif query.data == "hiragana_dakuten_menu":
        await show_hiragana_dakuten_menu(update, context)
    elif query.data == "hiragana_full_menu":
        await show_hiragana_full_menu(update, context)
    elif query.data == "menu_katakana":
        await show_katakana_menu(update, context)


def main() -> None:
    """Запуск бота"""
    token = os.getenv('BOT_TOKEN')
    if not token:
        logger.error("BOT_TOKEN не найден в переменных окружения!")
        return
    
    bot_state.symbol_generator.generate_all_files()
    logger.info("Файлы символов сгенерированы")
    
    application = Application.builder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))
    
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
