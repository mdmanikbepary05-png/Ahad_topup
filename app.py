from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
import requests
import datetime
import threading
import time

app = Flask(__name__)
app.secret_key = 'ahad_topup_secret_key_secure'

# টেলিগ্রাম ক্রেডেনশিয়ালস
TELEGRAM_BOT_TOKEN = "8970671481:AAFACF5V3b59JyLbdBNzszEH5VAlyefhLww"
TELEGRAM_ADMIN_CHAT_ID = "8662169982"

# ডেমো ডাটাবেজ
users_db = {}
orders_db = []

def send_telegram_order(order_id, order_details):
    try:
        message = (
            f"🚨 *New Order #{order_id}* 🚨\n\n"
            f"👤 *Service:* {order_details['service']}\n"
            f"🎮 *UID:* {order_details['uid']}\n"
            f"📦 *Package:* {order_details['package']}\n"
            f"💳 *Payment:* {order_details['payment']}\n"
            f"🔤 *TrxID:* `{order_details['trxid']}`\n"
            f"💰 *Amount:* {order_details['amount']}\n"
            f"👤 *User:* {order_details['username']}"
        )
        
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "✅ Complete", "callback_data": f"complete_{order_id}"},
                    {"text": "❌ Reject", "callback_data": f"reject_{order_id}"}
                ]
            ]
        }
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_ADMIN_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
            "reply_markup": keyboard
        }
        requests.post(url, json=payload)
    except Exception as e:
        print("Telegram Error:", e)

# টেলিগ্রাম বাটন কাজ করার জন্য ব্যাকগ্রাউন্ড পোলিং সিস্টেম (লোডিং বা আটকে যাওয়ার সমস্যা চিরতরে সমাধান)
def telegram_polling_worker():
    offset = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={offset}&timeout=30"
            response = requests.get(url, timeout=35)
            if response.status_code == 200:
                data = response.json()
                for result in data.get('result', []):
                    offset = result['update_id'] + 1
                    if 'callback_query' in result:
                        callback = result['callback_query']
                        callback_data = callback['data']
                        chat_id = callback['message']['chat']['id']
                        message_id = callback['message']['message_id']
                        query_id = callback['id']
                        
                        try:
                            action, order_id_str = callback_data.split('_')
                            order_id = int(order_id_str)
                            
                            for o in orders_db:
                                if o['id'] == order_id:
                                    if action == 'complete':
                                        o['status'] = 'Completed'
                                        new_text = callback['message']['text'] + "\n\n✅ *Status: COMPLETED*"
                                    else:
                                        o['status'] = 'Rejected'
                                        new_text = callback['message']['text'] + "\n\n❌ *Status: REJECTED*"
                                    
                                    # টেলিগ্রাম মেসেজ আপডেট করা
                                    edit_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageText"
                                    requests.post(edit_url, json={
                                        "chat_id": chat_id,
                                        "message_id": message_id,
                                        "text": new_text,
                                        "parse_mode": "Markdown"
                                    })
                                    
                                    # লোডিং বন্ধ করার জন্য অ্যানসার কল ব্যাক
                                    answer_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery"
                                    requests.post(answer_url, json={"callback_query_id": query_id, "text": f"Order {o['status']}!"})
                                    break
                        except Exception as inner_e:
                            print("Callback Parsing Error:", inner_e)
        except Exception as e:
            print("Polling Error:", e)
        time.sleep(2)

# ব্যাকগ্রাউন্ডে পোলিং থ্রেড স্টার্ট করা হলো
threading.Thread(target=telegram_polling_worker, daemon=True).start()

# HTML Templates
BASE_HEAD = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ahad Topup</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; }
        .card-bg { background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid #334155; }
    </style>
</head>
<body class="pb-24">
"""

BOTTOM_NAV = """
    <nav class="fixed bottom-0 left-0 right-0 bg-slate-900 border-t border-slate-800 flex justify-around items-center h-16 z-40 max-w-md mx-auto">
        <a href="/" class="flex flex-col items-center text-emerald-400">
            <i class="fa-solid fa-house text-lg"></i>
            <span class="text-[10px] mt-1 font-medium">Home</span>
        </a>
        <a href="/orders" class="flex flex-col items-center text-slate-400 hover:text-slate-200">
            <i class="fa-solid fa-bag-shopping text-lg"></i>
            <span class="text-[10px] mt-1 font-medium">My Orders</span>
        </a>
        <a href="/add-money" class="flex flex-col items-center -mt-5">
            <div class="w-14 h-14 bg-emerald-500 rounded-full flex items-center justify-center shadow-lg shadow-emerald-500/30 text-slate-950 border-4 border-slate-900">
                <i class="fa-solid fa-plus text-xl font-bold"></i>
            </div>
            <span class="text-[10px] mt-1 font-medium text-slate-300">Add Money</span>
        </a>
        <a href="/codes" class="flex flex-col items-center text-slate-400 hover:text-slate-200">
            <i class="fa-solid fa-code text-lg"></i>
            <span class="text-[10px] mt-1 font-medium">My Codes</span>
        </a>
        <a href="/account" class="flex flex-col items-center text-slate-400 hover:text-slate-200">
            <i class="fa-solid fa-user text-lg"></i>
            <span class="text-[10px] mt-1 font-medium">My Account</span>
        </a>
    </nav>
</body>
</html>
"""

INDEX_TEMPLATE = BASE_HEAD + """
    <div id="noticeModal" class="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-slate-700 w-full max-w-sm rounded-2xl p-5 text-center shadow-2xl">
            <div class="w-12 h-12 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto mb-3 text-xl">
                <i class="fa-solid fa-bullhorn"></i>
            </div>
            <h3 class="text-lg font-bold text-white mb-2">স্বাগতম Ahad Topup-এ!</h3>
            <p class="text-xs text-slate-300 mb-4">অফিশিয়াল টেলিগ্রাম চ্যানেল ও আপডেট পেতে জয়েন করুন।</p>
            <a href="https://t.me/ahadtopup" target="_blank" class="block w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 rounded-xl text-sm mb-2 transition">
                <i class="fa-brands fa-telegram mr-1.5"></i> Telegram Channel
            </a>
            <button onclick="closeNotice()" class="w-full bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold py-2 rounded-xl text-xs transition">
                CLOSE & CONTINUE
            </button>
        </div>
    </div>

    <header class="flex justify-between items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <span class="text-xl font-bold tracking-wider text-emerald-400">AHAD TOPUP</span>
        <div class="flex items-center space-x-3">
            <div class="flex items-center bg-emerald-600/20 border border-emerald-500/50 px-3 py-1.5 rounded-full">
                <i class="fa-solid fa-wallet text-emerald-400 mr-1.5"></i>
                <span class="text-sm font-semibold text-emerald-300">0 ৳</span>
            </div>
        </div>
    </header>

    <main class="p-4 max-w-md mx-auto">
        <div class="w-full h-36 bg-slate-800 rounded-xl mb-6 relative border border-slate-700 flex items-center justify-center overflow-hidden">
            <div class="text-center p-4">
                <i class="fa-solid fa-fire text-amber-500 text-3xl mb-1"></i>
                <p class="text-sm font-medium text-slate-300">ফ্রি ফায়ার ইনস্ট্যান্ট অটো টপ-আপ</p>
            </div>
        </div>

        <h2 class="text-center font-bold tracking-wider text-slate-200 mb-4 text-lg border-b border-slate-800 pb-2">REGULAR TOPUP</h2>

        <div class="grid grid-cols-3 gap-3">
            <a href="/order/ff-likes" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700">
                    <i class="fa-solid fa-thumbs-up text-red-500 text-xl"></i>
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">FF LIKES</span>
            </a>
            <a href="/order/uid-topup" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700">
                    <i class="fa-solid fa-id-card text-emerald-400 text-xl"></i>
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">UID TOPUP</span>
            </a>
            <a href="/order/unipin" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700">
                    <i class="fa-solid fa-ticket text-amber-400 text-xl"></i>
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">UNIPIN VOUCHER</span>
            </a>
            <a href="/order/weekly-monthly" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700">
                    <i class="fa-solid fa-box-open text-purple-400 text-xl"></i>
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">WEEKLY MONTHLY</span>
            </a>
            <a href="/order/level-up" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700">
                    <i class="fa-solid fa-shield-halved text-blue-400 text-xl"></i>
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">LEVEL UP PASS</span>
            </a>
            <a href="/order/weekly-lite" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700">
                    <i class="fa-solid fa-gem text-cyan-400 text-xl"></i>
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">WEEKLY LITE</span>
            </a>
        </div>
    </main>

    <a href="https://t.me/ahahackr" target="_blank" class="fixed bottom-20 right-4 w-14 h-14 bg-blue-500 text-white rounded-full flex items-center justify-center shadow-xl shadow-blue-500/40 z-50 hover:bg-blue-600 transition">
        <i class="fa-brands fa-telegram text-2xl"></i>
    </a>

    <script>
        function closeNotice() { document.getElementById('noticeModal').style.display = 'none'; }
    </script>
""" + BOTTOM_NAV

ORDER_TEMPLATE = BASE_HEAD + """
    <header class="flex items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <a href="/" class="text-slate-300 mr-4 text-lg"><i class="fa-solid fa-arrow-left"></i></a>
        <h1 class="text-base font-bold uppercase tracking-wider text-slate-200">{{ title }}</h1>
    </header>

    <form action="/submit-order" method="POST" class="p-4 max-w-md mx-auto space-y-4">
        <input type="hidden" name="service" value="{{ title }}">
        
        <!-- রুলস ও সতর্কবার্তা বক্স -->
        <div class="bg-amber-500/10 border border-amber-500/40 p-3.5 rounded-xl space-y-2">
            <div class="flex items-center text-amber-400 font-bold text-xs">
                <i class="fa-solid fa-triangle-exclamation mr-1.5 text-sm"></i> গুরুত্বপূর্ণ নিয়মাবলী ও শর্তাবলি:
            </div>
            <ul class="text-[11px] text-slate-300 space-y-1 list-disc list-inside">
                <li>অবশ্যම সঠিক <strong>Player UID</strong> প্রদান করুন।</li>
                <li>ভুয়া বা ভুল UID অথবা ভুয়া TrxID প্রদান করলে আপনার অ্যাকাউন্ট <strong>চিরতরে ব্যান</strong> হতে পারে।</li>
                <li>অর্ডার কমপ্লিট হওয়ার আগে গেম আইডি থেকে লগআউট বা নাম পরিবর্তন করবেন না।</li>
            </ul>
        </div>

        <div class="bg-slate-900 p-4 rounded-xl border border-slate-800">
            <label class="block text-xs font-semibold text-slate-400 mb-2">ENTER PLAYER UID</label>
            <input type="text" name="uid" required placeholder="Enter UID here..." class="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-emerald-500">
        </div>

        <div>
            <label class="block text-xs font-semibold text-slate-400 mb-2">SELECT PACKAGE</label>
            <div class="grid grid-cols-2 gap-3">
                {% for pkg, price in packages.items() %}
                <div onclick="selectPackage(this, '{{ pkg }} - {{ price }}')" class="package-card p-3 rounded-xl cursor-pointer text-center transition bg-slate-900 border border-slate-800">
                    <p class="text-sm font-bold text-white">{{ pkg }}</p>
                    <p class="text-xs text-emerald-400 font-semibold mt-1">{{ price }}</p>
                </div>
                {% endfor %}
            </div>
            <input type="hidden" name="package" id="selectedPackageInput" required>
        </div>

        <div>
            <label class="block text-xs font-semibold text-slate-400 mb-2">SELECT PAYMENT</label>
            <div class="grid grid-cols-3 gap-3">
                <button type="button" onclick="selectPayment(this, 'bKash', '01727246581 (Personal)')" class="pay-btn bg-slate-900 border border-slate-700 p-3 rounded-xl text-center text-xs font-bold text-pink-500">bKash</button>
                <button type="button" onclick="selectPayment(this, 'Nagad', '01727246581 (Personal)')" class="pay-btn bg-slate-900 border border-slate-700 p-3 rounded-xl text-center text-xs font-bold text-orange-500">Nagad</button>
                <button type="button" onclick="selectPayment(this, 'Rocket', '01727246581 (Personal)')" class="pay-btn bg-slate-900 border border-slate-700 p-3 rounded-xl text-center text-xs font-bold text-purple-500">Rocket</button>
            </div>
            <input type="hidden" name="payment" id="selectedPaymentInput" required>
        </div>

        <div id="paymentBox" class="hidden bg-slate-900 p-4 rounded-xl border border-emerald-500/50 space-y-3">
            <p class="text-xs text-slate-300">Send money to this number: <strong id="merchantNum" class="text-emerald-400"></strong></p>
            <div>
                <label class="block text-xs font-semibold text-slate-400 mb-1">TRANSACTION ID (TrxID)</label>
                <input type="text" name="trxid" placeholder="Enter TrxID" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-emerald-500">
            </div>
        </div>

        <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold py-3.5 rounded-xl shadow-lg shadow-emerald-500/25 transition mt-2">
            SUBMIT ORDER
        </button>
    </form>

    <script>
        function selectPackage(element, pkgName) {
            document.querySelectorAll('.package-card').forEach(card => card.style.borderColor = '#334155');
            element.style.borderColor = '#10b981';
            document.getElementById('selectedPackageInput').value = pkgName;
        }

        function selectPayment(element, method, number) {
            document.querySelectorAll('.pay-btn').forEach(btn => btn.style.borderColor = '#334155');
            element.style.borderColor = '#10b981';
            document.getElementById('selectedPaymentInput').value = method;
            document.getElementById('merchantNum').innerText = number;
            document.getElementById('paymentBox').classList.remove('hidden');
        }
    </script>
""" + BOTTOM_NAV

ORDERS_TEMPLATE = BASE_HEAD + """
    <header class="flex items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <a href="/" class="text-slate-300 mr-4 text-lg"><i class="fa-solid fa-arrow-left"></i></a>
        <h1 class="text-base font-bold uppercase tracking-wider text-slate-200">My Orders</h1>
    </header>

    <main class="p-4 max-w-md mx-auto space-y-3">
        {% if orders %}
            {% for o in orders %}
            <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-2">
                <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-emerald-400">{{ o.service }}</span>
                    <span class="text-xs px-2.5 py-1 rounded-full font-bold 
                        {% if o.status == 'Pending' %} bg-amber-500/20 text-amber-400 border border-amber-500/30
                        {% elif o.status == 'Completed' %} bg-emerald-500/20 text-emerald-400 border border-emerald-500/30
                        {% else %} bg-red-500/20 text-red-400 border border-red-500/30 {% endif %}">
                        {{ o.status }}
                    </span>
                </div>
                <p class="text-xs text-slate-300">UID: <strong>{{ o.uid }}</strong></p>
                <p class="text-xs text-slate-300">Package: <strong>{{ o.package }}</strong></p>
                <p class="text-xs text-slate-300">TrxID: <strong class="text-amber-300">{{ o.trxid }}</strong></p>
            </div>
            {% endfor %}
        {% else %}
            <div class="text-center py-20 text-slate-500">
                <i class="fa-solid fa-box-open text-4xl mb-2"></i>
                <p class="text-sm">কোনো অর্ডার পাওয়া যায়নি!</p>
            </div>
        {% endif %}
    </main>
""" + BOTTOM_NAV

ACCOUNT_TEMPLATE = BASE_HEAD + """
    <header class="flex items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <a href="/" class="text-slate-300 mr-4 text-lg"><i class="fa-solid fa-arrow-left"></i></a>
        <h1 class="text-base font-bold uppercase tracking-wider text-slate-200">My Account</h1>
    </header>

    <main class="p-4 max-w-md mx-auto space-y-4">
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl text-center">
            <div class="w-16 h-16 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto mb-3 text-2xl font-bold">
                {{ user.name[0].upper() }}
            </div>
            <h2 class="text-base font-bold text-white">{{ user.name }}</h2>
            <p class="text-xs text-slate-400 mb-4">{{ user.username }}</p>
            <div class="bg-slate-800 p-3 rounded-xl border border-slate-700 text-left space-y-1">
                <p class="text-xs text-slate-300"><i class="fa-solid fa-calendar-days text-emerald-400 mr-2"></i> Account Created: <strong>{{ user.joined_date }}</strong></p>
                <p class="text-xs text-slate-300"><i class="fa-solid fa-shield-halved text-blue-400 mr-2"></i> Status: <strong class="text-emerald-400">Active</strong></p>
            </div>
            <a href="/logout" class="block mt-4 bg-red-500/10 border border-red-500/30 text-red-400 font-bold py-2.5 rounded-xl text-xs hover:bg-red-500 hover:text-white transition">
                LOGOUT ACCOUNT
            </a>
        </div>
    </main>
""" + BOTTOM_NAV

AUTH_TEMPLATE = BASE_HEAD + """
    <div class="flex items-center justify-center min-h-screen p-4">
        <div class="bg-slate-900 border border-slate-800 w-full max-w-sm rounded-2xl p-6 shadow-2xl">
            <h2 class="text-xl font-bold text-center text-emerald-400 mb-1">AHAD TOPUP</h2>
            <p class="text-xs text-center text-slate-400 mb-6">আপনার অ্যাকাউন্টে লগইন বা সাইন আপ করুন</p>
            
            {% if error %}
            <div class="bg-red-500/20 border border-red-500 text-red-300 text-xs p-3 rounded-xl mb-4 text-center">{{ error }}</div>
            {% endif %}

            <form method="POST" class="space-y-4">
                {% if is_signup %}
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">FULL NAME</label>
                    <input type="text" name="name" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-emerald-500">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">EMAIL ADDRESS</label>
                    <input type="email" name="email" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-emerald-500">
                </div>
                {% endif %}
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">MOBILE NUMBER / USERNAME</label>
                    <input type="text" name="username" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-emerald-500">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">PASSWORD</label>
                    <input type="password" name="password" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-emerald-500">
                </div>

                <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold py-3 rounded-xl text-sm transition">
                    {{ 'CREATE ACCOUNT' if is_signup else 'LOGIN' }}
                </button>
            </form>

            <div class="text-center mt-4">
                {% if is_signup %}
                <p class="text-xs text-slate-400">Already have an account? <a href="/login" class="text-emerald-400 font-bold">Login</a></p>
                {% else %}
                <p class="text-xs text-slate-400">Don't have an account? <a href="/signup" class="text-emerald-400 font-bold">Create Account</a></p>
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>
"""

# ফ্লাস্ক রাউটসমূহ
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template_string(INDEX_TEMPLATE)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        uname = request.form.get('username').strip()
        pwd = request.form.get('password')
        if uname in users_db and users_db[uname]['password'] == pwd:
            session['user'] = uname
            return redirect(url_for('home'))
        error = 'ভুল ইউজারনেম বা পাসওয়ার্ড!'
    return render_template_string(AUTH_TEMPLATE, is_signup=False, error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        name = request.form.get('name').strip()
        email = request.form.get('email').strip()
        uname = request.form.get('username').strip()
        pwd = request.form.get('password')
        
        if uname in users_db:
            error = 'এই অ্যাকাউন্টটি আগেই রেজিস্টার্ড!'
        else:
            users_db[uname] = {
                'name': name,
                'email': email,
                'username': uname,
                'password': pwd,
                'joined_date': datetime.datetime.now().strftime("%d %B, %Y")
            }
            session['user'] = uname
            return redirect(url_for('home'))
    return render_template_string(AUTH_TEMPLATE, is_signup=True, error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/order/<service_type>')
def order_page(service_type):
    if 'user' not in session:
        return redirect(url_for('login'))
        
    services = {
        'ff-likes': {'title': 'FF Likes', 'packages': {'100 Likes': '30 ৳', '500 Likes': '130 ৳', '1000 Likes': '250 ৳'}},
        'uid-topup': {'title': 'UID Topup', 'packages': {'100 Diamonds': '85 ৳', '310 Diamonds': '250 ৳', '520 Diamonds': '410 ৳'}},
        'unipin': {'title': 'Unipin Voucher', 'packages': {'Unipin 50 BDT': '50 ৳', 'Unipin 100 BDT': '100 ৳'}},
        'weekly-monthly': {'title': 'Weekly Monthly', 'packages': {'Weekly Membership': '165 ৳', 'Monthly Membership': '520 ৳'}},
        'level-up': {'title': 'Level Up Pass', 'packages': {'Level Up Pass': '95 ৳'}},
        'weekly-lite': {'title': 'Weekly Lite', 'packages': {'Weekly Lite Pass': '80 ৳'}}
    }
    data = services.get(service_type, {'title': 'Topup Service', 'packages': {'Pack': '100 ৳'}})
    return render_template_string(ORDER_TEMPLATE, title=data['title'], packages=data['packages'])

@app.route('/submit-order', methods=['POST'])
def submit_order():
    if 'user' not in session:
        return redirect(url_for('login'))
        
    order_id = len(orders_db) + 1
    trxid = request.form.get('trxid')
    order_data = {
        'id': order_id,
        'username': session['user'],
        'service': request.form.get('service'),
        'uid': request.form.get('uid'),
        'package': request.form.get('package'),
        'payment': request.form.get('payment'),
        'trxid': trxid if trxid else 'N/A',
        'amount': request.form.get('package').split(' - ')[-1] if ' - ' in request.form.get('package') else 'N/A',
        'status': 'Pending'
    }
    
    orders_db.append(order_data)
    send_telegram_order(order_id, order_data)
    return redirect(url_for('my_orders'))

@app.route('/orders')
def my_orders():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_orders = [o for o in orders_db if o['username'] == session['user']]
    return render_template_string(ORDERS_TEMPLATE, orders=user_orders)

@app.route('/account')
def account():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_info = users_db.get(session['user'], {'name': 'User', 'username': session['user'], 'joined_date': 'Today'})
    return render_template_string(ACCOUNT_TEMPLATE, user=user_info)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
