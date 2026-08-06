import os
import logging
from fastapi import FastAPI, Request, Response
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Fetch environment variables or fallbacks
BOT_TOKEN = os.getenv("BOT_TOKEN", "8985024640:AAE4A-iUtgoZXVqUGR02lznKd1A9J2g54fk")
GOOGLE_DRIVE_LINK = os.getenv("GOOGLE_DRIVE_LINK", "https://drive.google.com/drive/folders/1OT0q-0mxRZNTgafyuHJfd7TGlFqQvoQp")
GOOGLE_FORM_LINK = os.getenv("GOOGLE_FORM_LINK", "https://docs.google.com/forms/d/e/1FAIpQLSciV5HEHKgOIQ_O1nxj836ThG3i807eM5htfp5jdKK7CYrVdQ/viewform?usp=dialog")

# --- 1. MAIN MENU KEYBOARD ---
def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🏢 About Company (SAIL)", callback_data="cat_company")],
        [InlineKeyboardButton("💰 Pay and Allowance", callback_data="cat_pay")],
        [InlineKeyboardButton("📜 Leave Rules & Regulations", callback_data="cat_leave")],
        [InlineKeyboardButton("🏥 Medical Benefits", callback_data="cat_medical")],
        [InlineKeyboardButton("📚 Library & Recreation", callback_data="cat_lib")],
        [InlineKeyboardButton("📂 Downloadable Forms & Documents", callback_data="cat_forms")],
        [InlineKeyboardButton("🎓 Central Induction & Schedule", callback_data="cat_induction")],
        [InlineKeyboardButton("📞 Contact Details & Key Numbers", callback_data="cat_contact")],
        [InlineKeyboardButton("💬 Submit Feedback / Queries (Google Form)", url=GOOGLE_FORM_LINK)]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- 2. SUB-MENU KEYBOARDS & TEXTS ---
def get_category_view(cat_id):
    if cat_id == "cat_company":
        text = "🏢 *About Company (SAIL)*\n\nSelect an official plant portal to visit:"
        keyboard = [
            [InlineKeyboardButton("🌐 SAIL Main Official Portal", url="https://www.sail.co.in")],
            [InlineKeyboardButton("🏬 Bhilai Steel Plant (BSP)", url="https://www.sail.co.in/en/plants/about-bhilai-steel-plant")],
            [InlineKeyboardButton("🏬 Bokaro Steel Plant (BSL)", url="https://www.sail.co.in/en/page/sail-plants")],
            [InlineKeyboardButton("🏬 Durgapur Steel Plant (DSP)", url="https://www.sail.co.in/en/page/sail-plants")],
            [InlineKeyboardButton("🏬 Rourkela Steel Plant (RSP)", url="https://www.sail.co.in/en/page/sail-plants")],
            [InlineKeyboardButton("🏬 IISCO Steel Plant (ISP)", url="https://www.sail.co.in/en/page/sail-plants")],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
    elif cat_id == "cat_pay":
        text = "💰 *Pay and Allowances*\n\nSelect an option below to view specific entitlement details or access the full PDF:"
        keyboard = [
            [InlineKeyboardButton("📊 Executive Pay Scales & Allowances", callback_data="detail_pay_scales")],
            [InlineKeyboardButton("✈️ Travelling & Lodging Entitlements", callback_data="detail_pay_ta")],
            [InlineKeyboardButton("📱 Mobile, Furniture & Briefcase Allowances", callback_data="detail_pay_allowances")],
            [InlineKeyboardButton("📄 Full Ready Reckoner PDF (Google Drive)", url=GOOGLE_DRIVE_LINK)],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
    elif cat_id == "cat_leave":
        text = "📜 *Leave Rules & Regulations*\n\nSelect a leave category to view specific guidelines and eligibility:"
        keyboard = [
            [InlineKeyboardButton("1️⃣ Earned Leave (EL)", callback_data="detail_el_rules")],
            [InlineKeyboardButton("2️⃣ Half Pay (HPL) & Commuted Leave", callback_data="detail_hpl_rules")],
            [InlineKeyboardButton("3️⃣ Maternity & Child Care Leave (CCL)", callback_data="detail_ccl_rules")],
            [InlineKeyboardButton("4️⃣ Special Casual Leave", callback_data="detail_scl_rules")],
            [InlineKeyboardButton("5️⃣ Extraordinary Leave & Leave Not Due", callback_data="detail_eol_rules")],
            [InlineKeyboardButton("6️⃣ Study Leave & Sabbatical Leave", callback_data="detail_study_sabbatical")],
            [InlineKeyboardButton("7️⃣ Important General Rules", callback_data="detail_general_rules")],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
    elif cat_id == "cat_medical":
        text = "🏥 *Medical Benefits*\n\nChoose an option below to view medical details or download the board form:"
        keyboard = [
            [InlineKeyboardButton("ℹ️ Medical Facilities Overview", callback_data="detail_med_facilities")],
            [InlineKeyboardButton("📋 Executive Medical Examination Board Form", callback_data="detail_med_form_info")],
            [InlineKeyboardButton("📄 Download Medical Form PDF (Google Drive)", url=GOOGLE_DRIVE_LINK)],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
    elif cat_id == "cat_lib":
        text = "📚 *Library and Recreation Facilities*\n\nSelect a topic to view details:"
        keyboard = [
            [InlineKeyboardButton("📖 Central & Public Library Rules", callback_data="detail_lib_info")],
            [InlineKeyboardButton("⚽ Sports & Recreation Facilities", callback_data="detail_sports_info")],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
    elif cat_id == "cat_forms":
        text = "📂 *Downloadable Forms & Documents*\n\nAll official documents, medical forms, and ready reckoners are hosted in our public Google Drive folder."
        keyboard = [
            [InlineKeyboardButton("📄 Open Google Drive Forms Folder", url=GOOGLE_DRIVE_LINK)],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
    elif cat_id == "cat_induction":
        text = "🎓 *Central Induction & Schedule*\n\nInformation regarding inaugural programs, plant orientation, dress codes, and video links:"
        keyboard = [
            [InlineKeyboardButton("🏛️ Inaugural Program & Schedule", callback_data="detail_ind_schedule")],
            [InlineKeyboardButton("👔 Suggested Dress Code", callback_data="detail_ind_dresscode")],
            [InlineKeyboardButton("🎥 Informative Video Links (Google Drive)", url=GOOGLE_DRIVE_LINK)],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
    elif cat_id == "cat_contact":
        text = "📞 *Contact Details & Key Numbers*\n\nAccess direct contacts for HR-L&D officials and hostel administration:"
        keyboard = [
            [InlineKeyboardButton("☎️ HR-L&D Officials & Hostel Warden Directory", callback_data="detail_contacts_list")],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
    else:
        text = "Welcome to SAIL-BSP Information Assistant!"
        keyboard = [[InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]]

    return text, InlineKeyboardMarkup(keyboard)

# --- 3. DETAIL VIEWS & BACK BUTTONS ---
def get_detail_view(detail_id):
    parent_cat = "main_menu"
    
    if detail_id == "detail_pay_scales":
        parent_cat = "cat_pay"
        text = (
            "📊 *BSP Executive Pay Scales (w.e.f. 01/01/2017)*\n\n"
            "• **E0:** ₹30,000 – 3% – ₹1,20,000\n"
            "• **E1 (MTs):** ₹50,000 – ₹1,60,000 (Placed in ₹60,000 – ₹1,80,000 after 1 yr/training)\n"
            "• **E2:** ₹70,000 – ₹2,00,000 | **E3:** ₹80,000 – ₹2,20,000\n"
            "• **E4:** ₹90,000 – ₹2,40,000 | **E5:** ₹1,00,000 – ₹2,60,000\n"
            "• **E6:** ₹1,20,000 – ₹2,80,000 | **E7/E8:** ₹1,20,000 – ₹2,80,000\n"
            "• **E9:** ₹1,50,000 – ₹3,00,000 | **Director/CEO:** ₹1,80,000 – ₹3,40,000\n\n"
            "🏥 *Non-Practicing Allowance for Doctors:* MBBS (16%), Diploma (18%), PG (20%)"
        )
    elif detail_id == "detail_pay_ta":
        parent_cat = "cat_pay"
        text = (
            "✈️ *Travelling & Lodging Entitlements*\n\n"
            "• **E0 – E3:** Travel 2AC/CC | Lodging: 3-Star / Actuals up to ₹2,500 | DA: ₹600 (Own: ₹900)\n"
            "• **E4 – E6:** Travel 1AC/CC or Air Economy | Lodging: 4-Star / Actuals up to ₹3,500 | DA: ₹750 (Own: ₹1,100)\n"
            "• **E7 – E8:** Travel 1AC/CC or Air Economy | Lodging: 4-Star / Actuals up to ₹4,500 | DA: ₹900 (Own: ₹1,300)\n"
            "• **E9 / Directors:** Air Executive / Premium Economy | Lodging: Actuals | DA: ₹1,000 – ₹1,100"
        )
    elif detail_id == "detail_pay_allowances":
        parent_cat = "cat_pay"
        text = (
            "📱 *Mobile, Furniture & Briefcase Allowances*\n\n"
            "• **Mobile Hardware Purchase (Once in 3 Yrs):**\n"
            "  - E0–E4: ₹10,000 | E5–E6: ₹15,000 | E7: ₹19,000 | E8: ₹25,000 | E9: ₹30,000\n"
            "• **Monthly Mobile Reimbursement:** E0 (₹200) to E8 (₹1,100) / E9 (Actuals)\n"
            "• **Furniture Allowance:** E1 (₹15,000), E2–E3 (₹25,000), E4–E5 (₹50,000), E6 (₹1,00,000), E7 (₹1,50,000), E8 (₹2,50,000), E9 (₹4,00,000)\n"
            "• **Briefcase Allowance (Once in 4 Yrs):** E0–E3 (₹2,150), E4–E6 (₹2,300), E7+ (₹2,600)"
        )
    elif detail_id == "detail_el_rules":
        parent_cat = "cat_leave"
        text = (
            "📋 *Earned Leave (EL) Rules*\n\n"
            "• **Credit:** Earned at 1 day for every 11 days of service.\n"
            "• **Accumulation Limit:** Maximum accumulation allowed is 300 days.\n"
            "• **Encashment:** Permitted as per company guidelines during service/retirement."
        )
    elif detail_id == "detail_hpl_rules":
        parent_cat = "cat_leave"
        text = (
            "📋 *Half Pay Leave (HPL) & Commuted Leave*\n\n"
            "• **Credit:** 20 days for each completed year of service.\n"
            "• **Commuted Leave:** Granted on medical grounds against twice the amount of HPL."
        )
    elif detail_id == "detail_ccl_rules":
        parent_cat = "cat_leave"
        text = (
            "📋 *Maternity & Child Care Leave (CCL)*\n\n"
            "• **Maternity Leave:** Up to 180 days for female employees.\n"
            "• **Child Care Leave (CCL):** Available for raising children up to 18 years of age."
        )
    elif detail_id == "detail_scl_rules":
        parent_cat = "cat_leave"
        text = (
            "📋 *Special Casual Leave*\n\n"
            "• Granted for family planning, sports events, union activities, and voluntary blood donation."
        )
    elif detail_id == "detail_eol_rules":
        parent_cat = "cat_leave"
        text = (
            "📋 *Extraordinary Leave & Leave Not Due*\n\n"
            "• **Extraordinary Leave (EOL):** Granted when no other leave is admissible.\n"
            "• **Leave Not Due:** Advanced leave granted on medical certificate."
        )
    elif detail_id == "detail_study_sabbatical":
        parent_cat = "cat_leave"
        text = (
            "📋 *Study Leave & Sabbatical Leave*\n\n"
            "• **Study Leave:** Granted for pursuing higher technical or management qualifications.\n"
            "• **Sabbatical:** Permitted for approved professional development or personal growth."
        )
    elif detail_id == "detail_general_rules":
        parent_cat = "cat_leave"
        text = (
            "📋 *Important General Leave Rules*\n\n"
            "• Leave cannot be claimed as a matter of right.\n"
            "• Prior approval from sanctioning authority is required before proceeding on leave."
        )
    elif detail_id == "detail_med_facilities":
        parent_cat = "cat_medical"
        text = (
            "🏥 *Medical Facilities Overview*\n\n"
            "• **Hostel Hospital:** Dispensary near Sector-1 Hostel.\n"
            "• **Main Hospital:** Jawaharlal Nehru Hospital & Research Centre in Hospital Sector (860 beds).\n"
            "• **Access:** Avail medical services using the Medical Card issued during training."
        )
    elif detail_id == "detail_med_form_info":
        parent_cat = "cat_medical"
        text = (
            "📋 *Executive Medical Examination Board Form*\n\n"
            "• Required prior to appointment for Executive posts under SAIL.\n"
            "• Includes Candidate's Declaration (medical history, family history) and Medical Board Physical Examination report (vision, chest, vitals).\n"
            "• **Note:** Download the full printable form from the Google Drive link below."
        )
    elif detail_id == "detail_lib_info":
        parent_cat = "cat_lib"
        text = (
            "📖 *Library Facilities*\n\n"
            "• **Central Library (HRDC):** Open 09:00 AM to 05:30 PM. Borrow 2 books for 30 days.\n"
            "• **Public Library:** New Civic Centre (Annual membership applies)."
        )
    elif detail_id == "detail_sports_info":
        parent_cat = "cat_lib"
        text = (
            "⚽ *Sports & Recreation*\n\n"
            "• Indoor/outdoor games and Gym available at the Hostel.\n"
            "• Multiple stadia and playgrounds located near the Hostel."
        )
    elif detail_id == "detail_ind_schedule":
        parent_cat = "cat_induction"
        text = (
            "🎓 *Central Induction & Schedule*\n\n"
            "• Details regarding orientation schedules, inaugural sessions, and plant visits are available in the Google Drive folder."
        )
    elif detail_id == "detail_ind_dresscode":
        parent_cat = "cat_induction"
        text = (
            "👔 *Suggested Dress Code During Central Induction Programme*\n\n"
            "To ensure uniformity and comfort during various induction activities, trainees are advised to follow the dress code given below:\n\n"
            "1️⃣ **Medical Examination**\n"
            "• **Boys:** Half-sleeve T-shirt, Lower/track pants, Comfortable sports shoes\n"
            "• **Girls:** Half-sleeve T-shirt with lower/track pants OR Loose-fitting Salwar-Kurta, Comfortable sports shoes or sandals\n\n"
            "2️⃣ **Document Verification**\n"
            "• Casual, decent, light-coloured attire is recommended.\n"
            "• *Examples:* T-shirt/Shirt with trousers/jeans, Comfortable shoes or sandals\n\n"
            "3️⃣ **Central Induction Programme & Classroom Sessions**\n"
            "• **Boys:** Plain, light-coloured formal shirt, Dark-coloured formal trousers, Formal shoes\n"
            "• **Girls:** Plain, light-coloured formal attire (Formal shirt & trousers / Salwar Suit / Saree), Formal footwear\n\n"
            "4️⃣ **Footwear Guidelines**\n"
            "All trainees are advised to bring:\n"
            "• One pair of sports shoes (for medical examination and other activities)\n"
            "• One pair of formal shoes (for induction sessions and classroom training)"
        )
    elif detail_id == "detail_contacts_list":
        parent_cat = "cat_contact"
        text = (
            "📞 *Useful Telephone Numbers & Official Contacts*\n\n"
            "• *STD Code for Bhilai:* 0788\n"
            "• *Note:* For dialing auto exchange numbers from outside Bhilai or P&T, dial 0788-28xxxxx\n\n"
            "1️⃣ **Sanjeev Shrivastava**\n"
            "• **Designation:** GM I/c (HR-L and D)\n"
            "• **Office Ext:** 54900 | **Mobile:** 9407982131\n"
            "• **E-mail:** skshrivastava@sail.in\n\n"
            "2️⃣ **Yashvant Singh Jowhari**\n"
            "• **Designation:** DGM (HR-L and D)\n"
            "• **Office Ext:** 54925 | **Mobile:** 9407981115\n"
            "• **E-mail:** ysjowhari@sail.in\n\n"
            "3️⃣ **Neeraja Sharma**\n"
            "• **Designation:** DGM (HR-L and D)\n"
            "• **Office Ext:** 54913 | **Mobile:** 9407981854\n"
            "• **E-mail:** Neeraja.sharma@sail.in\n\n"
            "4️⃣ **Sushmita Patla**\n"
            "• **Designation:** Dy.Mgr (HR-L and D)\n"
            "• **Office Ext:** 54904 | **Mobile:** 9407982137\n"
            "• **E-mail:** sushmitapatla@sail.in\n\n"
            "5️⃣ **Sanjay Singh**\n"
            "• **Designation:** Hostel Warden\n"
            "• **Office Ext:** 58973 | **Mobile:** 9479277645\n"
            "• **E-mail:** Sanjaysingh1025@gmail.com"
        )

    keyboard = [
        [InlineKeyboardButton("◀️ Back to Category Menu", callback_data=parent_cat)],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ]
    return text, InlineKeyboardMarkup(keyboard)

# --- 4. TELEGRAM HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ *Welcome to SAIL-BSP Information Assistant!*\n\n"
        "Please choose a category below to view information:",
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard()
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        await query.edit_message_text(
            "ℹ️ *Welcome to SAIL-BSP Information Assistant!*\n\n"
            "Please choose a category below to view information:",
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )
    elif data.startswith("cat_"):
        text, markup = get_category_view(data)
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=markup
        )
    elif data.startswith("detail_"):
        text, markup = get_detail_view(data)
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=markup
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Thank you for your message! Please send /start or use the menu buttons to navigate.")

# --- 5. INITIALIZE FASTAPI & PTB ---
app = FastAPI()
ptb_app = Application.builder().token(BOT_TOKEN).build()

ptb_app.add_handler(CommandHandler("start", start))
ptb_app.add_handler(CallbackQueryHandler(button_click))
ptb_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

ptb_initialized = False

@app.get("/")
async def root():
    return {"status": "SAIL-BSP Bot Serverless Endpoint Running"}

@app.api_route("/api/index", methods=["GET", "POST"])
async def webhook_handler(request: Request):
    if request.method == "GET":
        return {"status": "SAIL-BSP Bot Serverless Webhook Endpoint Active"}

    global ptb_initialized
    if not ptb_initialized:
        await ptb_app.initialize()
        await ptb_app.start()
        ptb_initialized = True

    try:
        data = await request.json()
        update = Update.de_json(data, ptb_app.bot)
        await ptb_app.process_update(update)
        return Response(status_code=200)
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return Response(status_code=500)