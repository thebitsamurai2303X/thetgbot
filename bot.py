"""Simple Telegram bot that renders received text into an image using random fonts."""
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from renderer import pick_font, render_text_image, list_fonts
from text_transforms import available_styles, transform, generate_variants
from translations import SUPPORTED_LANGS, get as tr_get
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
import uuid


# Session store for /text pagination: session_id -> {variants, page, per_page, user_id}
SESSIONS: dict[str, dict] = {}


# Simple in-memory user language store: user_id -> lang_code
USER_LANG: dict[int, str] = {}


load_dotenv()


TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')


async def check_subscription(user_id: int, bot) -> bool:
    """Check if user is subscribed to the required channel."""
    try:
        member = await bot.get_chat_member('@ytdlpdeveloper', user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Show a bilingual prompt and inline keyboard to choose language
    choose_text = 'Выберите язык / Select language'
    # build keyboard rows (2 columns)
    buttons = []
    row = []
    for code, name in SUPPORTED_LANGS.items():
        row.append(InlineKeyboardButton(name, callback_data=f'setlang:{code}'))
        if len(row) >= 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(choose_text, reply_markup=keyboard)





async def styles_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    styles = available_styles()
    await update.message.reply_text('Доступные стили:\n' + ', '.join(styles))


async def style_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # /style <style> <text>
    args = context.args
    if not args or len(args) < 2:
        await update.message.reply_text('Использование: /style <style> <текст>')
        return
    style = args[0]
    text = ' '.join(args[1:])
    try:
        t = transform(text, style)
    except KeyError:
        user_id = update.effective_user.id
        lang = USER_LANG.get(user_id, 'en')
        await update.message.reply_text('Неизвестный стиль. Используйте /styles чтобы увидеть список')
        return
    font = pick_font(size=72)
    img = render_text_image(t, font, size=64)
    await update.message.reply_photo(img)


async def callback_set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data or ''
    if not data.startswith('setlang:'):
        return
    
    code = data.split(':', 1)[1]
    if code not in SUPPORTED_LANGS:
        await query.edit_message_text('Unsupported language')
        return
    
    user_id = update.effective_user.id
    USER_LANG[user_id] = code
    
    # Check subscription status
    is_subscribed = await check_subscription(user_id, context.bot)
    if not is_subscribed:
        # Show subscription requirement message
        buttons = [[InlineKeyboardButton(tr_get(code, 'check_subscription'), 
                                       callback_data=f'check_sub:{code}')]]
        keyboard = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            tr_get(code, 'subscription_required'),
            reply_markup=keyboard
        )
        return
    
    # If subscribed, show welcome message
    welcome = tr_get(code, 'welcome')
    await query.edit_message_text(welcome)


async def callback_session_nav(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data or ''
    if ':' not in data:
        return
    session_id, action = data.split(':', 1)
    sess = SESSIONS.get(session_id)
    if not sess:
        await query.edit_message_text('Session expired or not found')
        return
    if update.effective_user.id != sess.get('user_id'):
        await query.answer('This session is not yours', show_alert=True)
        return
    per = sess.get('per_page', 5)
    total = len(sess['variants'])
    pages = (total + per - 1) // per
    if action == 'next':
        sess['page'] = (sess.get('page', 0) + 1) % pages
    elif action == 'prev':
        sess['page'] = (sess.get('page', 0) - 1) % pages
    page = sess.get('page', 0)
    start = page * per
    end = min(start + per, total)
    chunk = sess['variants'][start:end]

    # Just show page number in text, variants will be clickable buttons
    text = f"Page {page+1}/{pages}"

    # Build keyboard with clickable variant buttons
    kb = []
    for v in chunk:
        # Use the variant text itself as the button label
        # Limit the visible text to keep buttons reasonable
        visible = v[:30]  # Show first 30 chars in button
        kb.append([InlineKeyboardButton(visible, switch_inline_query_current_chat=v)])
    left = '⬅️'
    right = '➡️'
    kb.append([InlineKeyboardButton(left, callback_data=f'{session_id}:prev'), InlineKeyboardButton(right, callback_data=f'{session_id}:next')])
    keyboard = InlineKeyboardMarkup(kb)
    await query.edit_message_text(text, reply_markup=keyboard)


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or '').strip()
    if not text:
        return
    
    # Check subscription first
    user_id = update.effective_user.id
    is_subscribed = await check_subscription(user_id, context.bot)
    if not is_subscribed:
        code = USER_LANG.get(user_id, 'en')
        buttons = [[InlineKeyboardButton(tr_get(code, 'check_subscription'), 
                                       callback_data=f'check_sub:{code}')]]
        keyboard = InlineKeyboardMarkup(buttons)
        await update.message.reply_text(
            tr_get(code, 'subscription_required'),
            reply_markup=keyboard
        )
        return
        
    # Always produce 50 textual variants (10 pages × 5 variants per page)
    variants = generate_variants(text, max_variants=50)
    if not variants:
        await update.message.reply_text('No variants generated')
        return
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {'variants': variants, 'page': 0, 'per_page': 5, 'user_id': update.effective_user.id}
    # show first page
    per = 5
    total = len(variants)
    pages = (total + per - 1) // per
    chunk = variants[0:per]
    # Instead of a message with a preview + copy button, we'll just show the variants as buttons
    text_msg = f"Page 1/{pages}"
    kb = []
    for v in chunk:
        # Use the variant text itself as the button label
        # Limit the visible text to keep buttons reasonable
        visible = v[:30]  # Show first 30 chars in button
        kb.append([InlineKeyboardButton(visible, switch_inline_query_current_chat=v)])
    left = '⬅️'
    right = '➡️'
    kb.append([InlineKeyboardButton(left, callback_data=f'{session_id}:prev'), InlineKeyboardButton(right, callback_data=f'{session_id}:next')])
    keyboard = InlineKeyboardMarkup(kb)
    await update.message.reply_text(text_msg, reply_markup=keyboard)


async def text_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text('Использование: /text <текст>')
        return
    text = ' '.join(args)
    variants = generate_variants(text, max_variants=50)
    if not variants:
        await update.message.reply_text('No variants generated')
        return
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {'variants': variants, 'index': 0, 'user_id': update.effective_user.id}
    left = '⬅️'
    right = '➡️'
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(left, callback_data=f'{session_id}:prev'), InlineKeyboardButton(right, callback_data=f'{session_id}:next')]])
    await update.message.reply_text(f"1/{len(variants)}\n{variants[0]}", reply_markup=keyboard)


async def callback_check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data or ''
    if not data.startswith('check_sub:'):
        return
    
    code = data.split(':', 1)[1]
    user_id = update.effective_user.id
    
    is_subscribed = await check_subscription(user_id, context.bot)
    if is_subscribed:
        # Show welcome message if now subscribed
        welcome = tr_get(code, 'welcome')
        await query.edit_message_text(welcome)
    else:
        # Show subscription requirement message again
        buttons = [[InlineKeyboardButton(tr_get(code, 'check_subscription'), 
                                       callback_data=f'check_sub:{code}')]]
        keyboard = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            tr_get(code, 'subscription_required'),
            reply_markup=keyboard
        )

def main():
    token = TELEGRAM_TOKEN
    if not token:
        raise RuntimeError('Set TELEGRAM_TOKEN in .env')
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('styles', styles_cmd))
    app.add_handler(CommandHandler('style', style_cmd))
    app.add_handler(CommandHandler('text', text_cmd))
    # callback for language selection (setlang:code)
    app.add_handler(CallbackQueryHandler(callback_set_language, pattern=r'^setlang:'))
    # callback for subscription check
    app.add_handler(CallbackQueryHandler(callback_check_subscription, pattern=r'^check_sub:'))
    # callback for session navigation (sessionid:prev|next)
    app.add_handler(CallbackQueryHandler(callback_session_nav, pattern=r'^[0-9a-fA-F\-]+:(prev|next)$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    print('Bot started')
    app.run_polling()


if __name__ == '__main__':
    main()
