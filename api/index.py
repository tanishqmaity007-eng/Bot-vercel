import os
import json
import logging
import httpx
from fastapi import FastAPI, Request, Response
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import firebase_admin
from firebase_admin import credentials, firestore

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_DRIVE_LINK = os.getenv("GOOGLE_DRIVE_LINK")
GOOGLE_FORM_LINK = os.getenv("GOOGLE_FORM_LINK")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
FIREBASE_CLIENT_EMAIL = os.getenv("FIREBASE_CLIENT_EMAIL")
FIREBASE_PRIVATE_KEY = os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n")

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate({
            "type": "service_account",
            "project_id": FIREBASE_PROJECT_ID,
            "private_key": FIREBASE_PRIVATE_KEY,
            "client_email": FIREBASE_CLIENT_EMAIL,
        })
        firebase_admin.initialize_app(cred)
        logger.info("Firebase initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing Firebase: {e}")

db = firestore.client() if firebase_admin._apps else None

# Initialize FastAPI app
app = FastAPI()

# Initialize Telegram Bot Application
ptb_app = Application.builder().token(BOT_TOKEN).build()

# --- Telegram Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"Hello, {user.first_name}!\n\n"
        "Welcome to the SAIL-BSP Bot. Choose an option below to get started:"
    )
    
    keyboard = [
        [InlineKeyboardButton("📁 Access Study Drive", url=GOOGLE_DRIVE_LINK)],
        [InlineKeyboardButton("📝 Submit Feedback Form", url=GOOGLE_FORM_LINK)],
        [InlineKeyboardButton("ℹ️ Help / Info", callback_data="help_info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Store user log in Firestore
    if db:
        try:
            db.collection("users").document(str(user.id)).set({
                "first_name": user.first_name,
                "username": user.username,
                "last_active": firestore.SERVER_TIMESTAMP
            }, merge=True)
        except Exception as e:
            logger.error(f"Failed to log user to Firebase: {e}")

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "help_info":
        info_text = (
            "📌 *Bot Assistance*\n\n"
            "Use the provided buttons to access resources directly.\n"
            "If you run into issues, contact your administrator."
        )
        await query.message.reply_text(info_text, parse_mode="Markdown")

# Register Handlers
ptb_app.add_handler(CommandHandler("start", start_command))
ptb_app.add_handler(CallbackQueryHandler(button_callback))

# Initialization flag for PTB
ptb_initialized = False

# --- FastAPI Routes ---

@app.get("/")
async def root():
    return {"status": "SAIL-BSP Bot Serverless Endpoint Running"}

@app.post("/api/index")
async def webhook_handler(request: Request):
    global ptb_initialized
    if not ptb_initialized:
        await ptb_app.initialize()
        ptb_initialized = True

    try:
        data = await request.json()
        update = Update.de_json(data, ptb_app.bot)
        await ptb_app.process_update(update)
        return Response(status_code=200)
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return Response(status_code=500)