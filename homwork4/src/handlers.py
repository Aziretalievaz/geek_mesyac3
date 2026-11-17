from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from src.state import Quiz
from src.keyboards import reply_buttons, inline_buttons, replay_buttons
from db.users import get_user, create_user, update_user, delete_user
from db.results import save_result
from db.stats import get_history, get_top, get_hardest
from db.questions import get_all_questions

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username or "Аноним"
    )
    await message.answer(
        f"Privet, {message.from_user.username}!\n"
        f"Ty uspeshno zaregan.\n\n"
        f"Tvoi profil:\n"
        f"ID: {user['id']}\n"
        f"Telegram ID: {user['telegram_id']}\n"
        f"Imya: {user['username']}",
        reply_markup=reply_buttons
    )
    print(f"Пользователь {message.from_user.full_name} написал команду /start!")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Dostupnie komandi:\n\n"
        "/start - команда для запуска\n"
        "/help - список команд\n"
        "/profile - prosmotr profilya\n"
        "/change_name <novoe_imya> - izmenit imya\n"
        "/delete_me - udalit profil\n"
        "/history - istoriya otvetov\n"
        "/top - top igrokov\n"
        "/hardest - samiy slojniy vopros",
        reply_markup=inline_buttons
    )


@router.message(Command("profile"))
async def cmd_profile(message: Message):
    user = get_user(message.from_user.id)

    if user:
        await message.answer(
            f"Tvoi profile:\n"
            f"ID: {user['id']}\n"
            f"Telegram ID: {user['telegram_id']}\n"
            f"Imya: {user['username']}"
        )
    else:
        await message.answer("Ty ne zaregan. Napishi /start")


@router.message(Command("change_name"))
async def cmd_change_name(message: Message):
    new_name = message.text.split(maxsplit=1)

    if len(new_name) < 2:
        await message.answer("Чтобы поменять имя напиши: /change_name Новое Имя")
        return

    user = get_user(message.from_user.id)

    if not user:
        await message.answer(
            "Ti eshe ne zaregan. Napishi /start"
        )
        return

    update_user(
        telegram_id=message.from_user.id,
        username=new_name[1]
    )

    await message.answer(
        f"Imya uspeshno izmeneno na {new_name[1]}!"
    )


    

@router.message(Command("delete_me"))
async def cmd_delete_me(message: Message):
    user = get_user(message.from_user.id)

    if not user:
        await message.answer(
            "Ty eshe ne zaregistrirovan, Udalyat ne4ego"
        )
        return

    delete_user(telegram_id=message.from_user.id)

    await message.answer(
        "Tvoi profil uspeshno udalen iz bazi dannix."
    ) 

@router.message(Command("history"))
async def cmd_history(message: Message):
    history = get_history(telegram_id=message.from_user.id)

    if not history:
        await message.answer("Ответов нет в базе!")
        return

    text = "Последние ответы:\n\n"

    for i, row in enumerate(history, 1):
        mark = "Верно" if row["is_correct"] else "Неверно"
        text += f"{i}. {mark} - {row['question_text']}\n"

    await message.answer(text)


@router.message(Command("top"))
async def cmd_top(message: Message):
    players = get_top()

    if not players:
        await message.answer("Otvetov net v baze")
        return

    text = "Top igrokov:\n\n"

    for i, player in enumerate(players, 1):
        text += (
            f"{i}. {player['username']} - "
            f"{player['correct']}/{player['total']}\n"
        )

    await message.answer(text)


@router.message(Command("hardest"))
async def cmd_hardest(message: Message):
    question = get_hardest()

    if not question:
        await message.answer("Voprosov net v baze")
        return

    await message.answer(
        f"Samuy slojniy vopros:\n"
        f"{question['question_text']}\n"
        f"Pravilnye otvety: {question['success_rate']}%"
    )


@router.message(F.text == "Корзина")
async def cmd_group(message: Message):
    await message.answer("Твоя корзина пуста(")


@router.callback_query(F.data == "quiz_start")
async def quiz_start(callback: CallbackQuery, state: FSMContext):

    questions = get_all_questions()

    if not questions:
        await callback.answer()
        await callback.message.answer("Voprosov net v baze")
        return

    await callback.answer("Начинаем игру!", show_alert=True)

    await state.update_data(
        questions=questions,
        index=0,
        score=0
    )

    await state.set_state(Quiz.waiting_answer)

    await callback.message.answer(
        f"Вопрос 1: {questions[0]['question_text']}"
    )


@router.message(Quiz.waiting_answer)
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    score = data["score"]
    questions = data["questions"]
    user = get_user(telegram_id=message.from_user.id)
    q = questions[index] 

    is_correct = message.text.lower() == q['correct_answer'].lower()
    save_result(
        user_id=user["id"],
        question_id=q["id"],
        is_correct=is_correct
    )

    if is_correct:
        score += 1
        await message.answer("Правильно! +1")

    else:
        await message.answer(f"Неверно. Правильный ответ: {q['correct_answer']}")

    index += 1
    if index >= len(questions):
        await message.answer(
            f"Конец! Счет: {score}/{len(questions)}",
            reply_markup=replay_buttons
        )
        await state.clear()
    else:
        await state.update_data(index=index, score=score)
        await message.answer(f"Вопрос {index + 1}: {questions[index]['question_text']}")


# @dp.message(F.from_user.id == 1288365917)
# async def cmd_group(message: Message):
#     await message.answer("Привет мой создатель!!!")


@router.message()
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")