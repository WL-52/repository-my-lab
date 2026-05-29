"""Telegram-бот «Помощник студента: сдача ДЗ».

Простой бот для колледжа, который решает одну задачу: позволяет студенту
отправить домашнее задание преподавателю.

Сценарий:
1) Студент пишет /start, получает приветствие и список команд.
2) Команда /submit запускает диалог: выбор предмета → ввод комментария →
   прикрепление файла (документ/фото) → подтверждение.
3) После подтверждения бот пересылает домашку преподавателю (в его чат
   с ботом или в указанный TEACHER_CHAT_ID) и сохраняет запись в JSON.
4) /list показывает последние сданные работы текущего пользователя.
5) /cancel отменяет текущий диалог.

Конфигурация через переменные окружения (см. README.md):
- BOT_TOKEN          — токен от @BotFather (обязателен);
- TEACHER_CHAT_ID    — chat_id преподавателя (обязателен);
- SUBJECTS           — список предметов через запятую (опционально).

Запуск: python3 bot.py
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from pathlib import Path

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("homework-bot")

CHOOSING_SUBJECT, ENTERING_COMMENT, ATTACHING_FILE, CONFIRMING = range(4)

DATA_FILE = Path(__file__).resolve().parent / "submissions.json"


def load_subjects() -> list[str]:
    raw = os.environ.get(
        "SUBJECTS",
        "Программирование,Математика,Английский,История,Базы данных",
    )
    return [s.strip() for s in raw.split(",") if s.strip()]


def get_teacher_chat_id() -> int | None:
    value = os.environ.get("TEACHER_CHAT_ID")
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        log.warning("TEACHER_CHAT_ID is not a valid integer: %r", value)
        return None


def load_submissions() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_submissions(items: list[dict]) -> None:
    DATA_FILE.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


async def cmd_start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    name = user.first_name if user else "студент"
    text = (
        f"Привет, {name}!\n\n"
        "Я бот-помощник для сдачи домашних заданий.\n\n"
        "Команды:\n"
        "/submit — сдать домашнее задание\n"
        "/list   — показать мои последние сдачи\n"
        "/help   — помощь\n"
        "/cancel — отменить текущее действие"
    )
    await update.message.reply_text(text)


async def cmd_help(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Чтобы сдать ДЗ:\n"
        "1. Отправьте /submit.\n"
        "2. Выберите предмет.\n"
        "3. Напишите короткий комментарий.\n"
        "4. Пришлите файл или фото домашки (или /skip — без вложения).\n"
        "5. Подтвердите отправку.\n\n"
        "Преподаватель получит уведомление автоматически."
    )


async def cmd_list(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    items = [s for s in load_submissions() if s.get("user_id") == user_id]
    items = items[-10:]
    if not items:
        await update.message.reply_text("Пока ни одной сданной работы.")
        return
    lines = ["Последние сдачи:"]
    for it in items:
        lines.append(f"• {it['ts']} — {it['subject']}: {it['comment'] or '(без комментария)'}")
    await update.message.reply_text("\n".join(lines))


async def cmd_submit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    subjects = load_subjects()
    keyboard = [
        [InlineKeyboardButton(s, callback_data=f"subj::{s}")]
        for s in subjects
    ]
    await update.message.reply_text(
        "Выберите предмет:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    context.user_data.clear()
    return CHOOSING_SUBJECT


async def on_subject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    _, _, subject = query.data.partition("::")
    context.user_data["subject"] = subject
    await query.edit_message_text(
        f"Предмет: *{subject}*\n\n"
        "Напишите короткий комментарий к работе (или отправьте `-`, если не нужен):",
        parse_mode="Markdown",
    )
    return ENTERING_COMMENT


async def on_comment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text or ""
    context.user_data["comment"] = "" if text.strip() == "-" else text.strip()
    await update.message.reply_text(
        "Теперь пришлите файл или фото с домашкой.\n"
        "Если вложения не будет — отправьте /skip."
    )
    return ATTACHING_FILE


async def on_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    msg = update.message
    if msg.document:
        context.user_data["attachment"] = {
            "kind": "document",
            "file_id": msg.document.file_id,
            "name": msg.document.file_name,
        }
    elif msg.photo:
        context.user_data["attachment"] = {
            "kind": "photo",
            "file_id": msg.photo[-1].file_id,
        }
    else:
        await msg.reply_text("Не понял вложение. Пришлите документ или фото, либо /skip.")
        return ATTACHING_FILE
    return await preview(update, context)


async def on_skip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["attachment"] = None
    return await preview(update, context)


async def preview(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    subject = context.user_data.get("subject", "?")
    comment = context.user_data.get("comment", "")
    att = context.user_data.get("attachment")
    att_text = att["kind"] if att else "(без вложения)"
    keyboard = [
        [
            InlineKeyboardButton("Отправить", callback_data="send"),
            InlineKeyboardButton("Отмена", callback_data="cancel"),
        ]
    ]
    text = (
        "Проверьте перед отправкой:\n\n"
        f"Предмет: {subject}\n"
        f"Комментарий: {comment or '(нет)'}\n"
        f"Вложение: {att_text}"
    )
    await update.effective_message.reply_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return CONFIRMING


async def on_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    if query.data == "cancel":
        await query.edit_message_text("Отправка отменена.")
        return ConversationHandler.END

    user = update.effective_user
    teacher_chat_id = get_teacher_chat_id()
    subject = context.user_data.get("subject", "?")
    comment = context.user_data.get("comment", "")
    att = context.user_data.get("attachment")

    record = {
        "user_id": user.id,
        "user_name": user.full_name,
        "username": user.username,
        "subject": subject,
        "comment": comment,
        "ts": datetime.now().isoformat(timespec="seconds"),
        "attachment": att,
    }
    items = load_submissions()
    items.append(record)
    save_submissions(items)

    await query.edit_message_text("✅ Сохранено.")
    return ConversationHandler.END


async def cmd_cancel(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Действие отменено.")
    return ConversationHandler.END


def build_application() -> Application:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise SystemExit(
            "BOT_TOKEN is not set. See README.md for configuration instructions."
        )

    app = Application.builder().token(token).build()

    submit_conv = ConversationHandler(
        entry_points=[CommandHandler("submit", cmd_submit)],
        states={
            CHOOSING_SUBJECT: [CallbackQueryHandler(on_subject, pattern=r"^subj::")],
            ENTERING_COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, on_comment)],
            ATTACHING_FILE: [
                CommandHandler("skip", on_skip),
                MessageHandler(filters.Document.ALL | filters.PHOTO, on_file),
            ],
            CONFIRMING: [CallbackQueryHandler(on_confirm, pattern=r"^(send|cancel)$")],
        },
        fallbacks=[CommandHandler("cancel", cmd_cancel)],
    )

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("list", cmd_list))
    app.add_handler(submit_conv)
    return app


def main() -> None:
    app = build_application()
    log.info("Bot started (polling).")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
