from flask import Flask, render_template_string, request, redirect, url_for, session
import datetime

app = Flask(__name__)
app.secret_key = 'ahad_topup_secret_key_secure'

# ডেটাবেজ
users_db = {}
orders_db = []
add_money_db = []

# ওয়েবসাইট সেটিংস
site_settings = {
    "site_title": "AHAD TOPUP",
    "banner_text": "ফ্রি ফায়ার ইনস্ট্যান্ট অটো টপ-আপ",
    "banner_image": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600&auto=format&fit=crop&q=80",
    "payment_number": "01727246581",
    "telegram_link": "https://t.me/ahahackr",
    "notice_text": "⚠️ জরুরি ঘোষণা: কোনো ভুয়া TrxID বা ভুল তথ্য দিলে অ্যাকাউন্ট চিরতরে ব্যান করা হবে। লেনদেনের সময় সতর্ক থাকুন!",
    # সার্ভিস কার্ড
    "service_1_name": "FF LIKES", "service_1_icon": "fa-solid fa-thumbs-up text-red-500",
    "service_2_name": "UID TOPUP", "service_2_icon": "fa-solid fa-id-card text-emerald-400",
    "service_3_name": "UNIPIN VOUCHER", "service_3_icon": "fa-solid fa-ticket text-amber-400",
    "service_4_name": "WEEKLY MONTHLY", "service_4_icon": "fa-solid fa-box-open text-purple-400",
    "service_5_name": "LEVEL UP PASS", "service_5_icon": "fa-solid fa-shield-halved text-blue-400",
    "service_6_name": "WEEKLY LITE", "service_6_icon": "fa-solid fa-gem text-cyan-400"
}

ADMIN_USERNAME = "ahadadmin"
ADMIN_PASSWORD = "123"

# বেস টেমপ্লেট (সাথে এন্ট্রি নোটিফিকেশন পপ-আপ ও ভাসমান টেলিগ্রাম বাটন)
BASE_HEAD = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ settings.site_title }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; }
        .card-bg { background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid #334155; }
        .floating-support {
            position: fixed; bottom: 85px; right: 20px; background-color: #0088cc; color: white;
            width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center;
            justify-content: center; font-size: 24px; box-shadow: 0 4px 10px rgba(0,0,0,0.4); z-index: 50;
        }
    </style>
</head>
<body class="pb-24">

    <!-- এন্ট্রি ওয়ার্নিং নোটিফিকেশন মোডাল -->
    <div id="welcomeWarningModal" class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
        <div class="bg-slate-900 border border-amber-500/50 w-full max-w-sm rounded-2xl p-5 shadow-2xl space-y-4">
            <div class="flex items-center space-x-2 text-amber-400">
                <i class="fa-solid fa-triangle-exclamation text-xl"></i>
                <h3 class="font-bold text-base">জরूरी সতর্কতা ও নোটিশ</h3>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">{{ settings.notice_text }}</p>
            <button onclick="closeWarningModal()" class="w-full bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold py-2.5 rounded-xl text-xs transition">
                বুঝেছি (OK)
            </button>
        </div>
    </div>

    <script>
        function closeWarningModal() {
            document.getElementById('welcomeWarningModal').style.display = 'none';
        }
    </script>
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
    <!-- Floating Telegram Support Button (@ahahackr) -->
    <a href="https://t.me/ahahackr" target="_blank" class="floating-support" title="Telegram Support">
        <i class="fa-brands fa-telegram-plane"></i>
    </a>
</body>
</html>
"""

INDEX_TEMPLATE = BASE_HEAD + """
    <header class="flex justify-between items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <span class="text-xl font-bold tracking-wider text-emerald-400">{{ settings.site_title }}</span>
        <div class="flex items-center space-x-3">
            <a href="https://t.me/ahahackr" target="_blank" class="bg-sky-500/20 border border-sky-500/50 text-sky-400 px-3 py-1.5 rounded-full text-xs font-bold flex items-center">
                <i class="fa-brands fa-telegram mr-1 text-sm"></i> Telegram
            </a>
            <div class="flex items-center bg-emerald-600/20 border border-emerald-500/50 px-3 py-1.5 rounded-full">
                <i class="fa-solid fa-wallet text-emerald-400 mr-1.5"></i>
                <span class="text-sm font-semibold text-emerald-300">0 ৳</span>
            </div>
        </div>
    </header>

    <main class="p-4 max-w-md mx-auto space-y-4">
        <!-- ব্যানার -->
        <div class="w-full h-40 bg-slate-800 rounded-xl relative border border-slate-700 flex items-center justify-center overflow-hidden shadow-lg">
            {% if settings.banner_image %}
            <img src="{{ settings.banner_image }}" class="absolute inset-0 w-full h-full object-cover opacity-40">
            {% endif %}
            <div class="text-center p-4 relative z-10">
                <i class="fa-solid fa-fire text-amber-500 text-3xl mb-1"></i>
                <p class="text-sm font-bold text-white drop-shadow">{{ settings.banner_text }}</p>
            </div>
        </div>

        <h2 class="text-center font-bold tracking-wider text-slate-200 mb-2 text-lg border-b border-slate-800 pb-2">REGULAR TOPUP</h2>

        <div class="grid grid-cols-3 gap-3">
            <a href="/order/ff-likes" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <i class="{{ settings.service_1_icon }} text-xl"></i>
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_1_name }}</span>
            </a>
            <a href="/order/uid-topup" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <i class="{{ settings.service_2_icon }} text-xl"></i>
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_2_name }}</span>
            </a>
            <a href="/order/unipin" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <i class="{{ settings.service_3_icon }} text-xl"></i>
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_3_name }}</span>
            </a>
            <a href="/order/weekly-monthly" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <i class="{{ settings.service_4_icon }} text-xl"></i>
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_4_name }}</span>
            </a>
            <a href="/order/level-up" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <i class="{{ settings.service_5_icon }} text-xl"></i>
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_5_name }}</span>
            </a>
            <a href="/order/weekly-lite" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <i class="{{ settings.service_6_icon }} text-xl"></i>
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_6_name }}</span>
            </a>
        </div>
    </main>
""" + BOTTOM_NAV

ADD_MONEY_TEMPLATE = BASE_HEAD + """
    <header class="flex items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <a href="/" class="text-slate-300 mr-4 text-lg"><i class="fa-solid fa-arrow-left"></i></a>
        <h1 class="text-base font-bold uppercase tracking-wider text-slate-200">Add Money (ওয়ালেট)</h1>
    </header>

    <main class="p-4 max-w-md mx-auto space-y-4">
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-4">
            <h2 class="text-sm font-bold text-emerald-400">টাকা অ্যাড করতে অ্যামাউন্ট দিন:</h2>
            <form action="/submit-add-money" method="POST" class="space-y-3">
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">পরিমাণ (Amount in BDT)</label>
                    <input type="number" name="amount" required placeholder="উদা: 100" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-emerald-500">
                </div>
                <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold py-3 rounded-xl text-xs transition">
                    প্রসিড করুন (Next)
                </button>
            </form>
        </div>
    </main>
""" + BOTTOM_NAV

ADD_MONEY_PAY_TEMPLATE = BASE_HEAD + """
    <header class="flex items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <a href="/add-money" class="text-slate-300 mr-4 text-lg"><i class="fa-solid fa-arrow-left"></i></a>
        <h1 class="text-base font-bold uppercase tracking-wider text-slate-200">Complete Payment</h1>
    </header>

    <form action="/confirm-add-money" method="POST" class="p-4 max-w-md mx-auto space-y-4">
        <input type="hidden" name="amount" value="{{ amount }}">
        
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-2 text-center">
            <p class="text-xs text-slate-400">অ্যাড করতে চান:</p>
            <h2 class="text-2xl font-bold text-emerald-400">{{ amount }} ৳</h2>
        </div>

        <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-3">
            <p class="text-xs text-slate-300">আমাদের বিকাশ পার্সোনাল নাম্বারে টাকা পাঠান:</p>
            <div class="bg-slate-800 p-3 rounded-lg text-center border border-slate-700">
                <span class="text-lg font-bold text-amber-400 select-all">{{ settings.payment_number }}</span>
                <p class="text-[10px] text-slate-400 mt-0.5">(Send Money / Cash In)</p>
            </div>
            <div>
                <label class="block text-xs font-semibold text-slate-400 mb-1">TRANSACTION ID (TrxID)</label>
                <input type="text" name="trxid" required placeholder="বিকাশ TrxID দিন" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-emerald-500">
            </div>
        </div>

        <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold py-3.5 rounded-xl shadow-lg transition">
            SUBMIT TRXID
        </button>
    </form>
""" + BOTTOM_NAV

ORDER_TEMPLATE = BASE_HEAD + """
    <header class="flex items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <a href="/" class="text-slate-300 mr-4 text-lg"><i class="fa-solid fa-arrow-left"></i></a>
        <h1 class="text-base font-bold uppercase tracking-wider text-slate-200">{{ title }}</h1>
    </header>

    <form action="/submit-order" method="POST" class="p-4 max-w-md mx-auto space-y-4">
        <input type="hidden" name="service" value="{{ title }}">
        
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
                <button type="button" onclick="selectPayment(this, 'bKash', '{{ settings.payment_number }}')" class="pay-btn bg-slate-900 border border-slate-700 p-3 rounded-xl text-center text-xs font-bold text-pink-500">bKash</button>
                <button type="button" onclick="selectPayment(this, 'Nagad', '{{ settings.payment_number }}')" class="pay-btn bg-slate-900 border border-slate-700 p-3 rounded-xl text-center text-xs font-bold text-orange-500">Nagad</button>
                <button type="button" onclick="selectPayment(this, 'Rocket', '{{ settings.payment_number }}')" class="pay-btn bg-slate-900 border border-slate-700 p-3 rounded-xl text-center text-xs font-bold text-purple-500">Rocket</button>
            </div>
            <input type="hidden" name="payment" id="selectedPaymentInput" required>
        </div>

        <div id="paymentBox" class="hidden bg-slate-900 p-4 rounded-xl border border-emerald-500/50 space-y-3">
            <p class="text-xs text-slate-300">Send money to: <strong id="merchantNum" class="text-emerald-400"></strong></p>
            <div>
                <label class="block text-xs font-semibold text-slate-400 mb-1">TRANSACTION ID (TrxID)</label>
                <input type="text" name="trxid" required placeholder="Enter TrxID" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-emerald-500">
            </div>
        </div>

        <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold py-3.5 rounded-xl shadow-lg transition mt-2">
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
        <h1 class="text-base font-bold uppercase tracking-wider text-slate-200">My Orders & Add Money History</h1>
    </header>

    <main class="p-4 max-w-md mx-auto space-y-4">
        <h3 class="text-xs font-bold text-slate-400 uppercase">Topup Orders</h3>
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
            <p class="text-xs text-slate-500 text-center py-2">কোনো টপআপ অর্ডার নেই!</p>
        {% endif %}

        <h3 class="text-xs font-bold text-slate-400 uppercase pt-2">Add Money Requests</h3>
        {% if add_moneys %}
            {% for am in add_moneys %}
            <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-2">
                <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-sky-400">Add Money: {{ am.amount }} ৳</span>
                    <span class="text-xs px-2.5 py-1 rounded-full font-bold 
                        {% if am.status == 'Pending' %} bg-amber-500/20 text-amber-400 border border-amber-500/30
                        {% elif am.status == 'Approved' %} bg-emerald-500/20 text-emerald-400 border border-emerald-500/30
                        {% else %} bg-red-500/20 text-red-400 border border-red-500/30 {% endif %}">
                        {{ am.status }}
                    </span>
                </div>
                <p class="text-xs text-slate-300">TrxID: <strong class="text-amber-300">{{ am.trxid }}</strong></p>
            </div>
            {% endfor %}
        {% else %}
            <p class="text-xs text-slate-500 text-center py-2">কোনো অ্যাড মানি রিকোয়েস্ট নেই!</p>
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
            <a href="/logout" class="block bg-red-500/10 border border-red-500/30 text-red-400 font-bold py-2.5 rounded-xl text-xs hover:bg-red-500 hover:text-white transition">
                LOGOUT ACCOUNT
            </a>
        </div>
    </main>
""" + BOTTOM_NAV

AUTH_TEMPLATE = BASE_HEAD + """
    <div class="flex items-center justify-center min-h-screen p-4">
        <div class="bg-slate-900 border border-slate-800 w-full max-w-sm rounded-2xl p-6 shadow-2xl">
            <h2 class="text-xl font-bold text-center text-emerald-400 mb-1">{{ settings.site_title }}</h2>
            <p class="text-xs text-center text-slate-400 mb-6">আপনার অ্যাকাউন্টে লগইন বা সাইন আপ করুন</p>
            
            {% if error %}
            <div class="bg-red-500/20 border border-red-500 text-red-300 text-xs p-3 rounded-xl mb-4 text-center">{{ error }}</div>
            {% endif %}

            <form method="POST" class="space-y-4">
                {% if is_signup %}
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">FULL NAME</label>
                    <input type="text" name="name" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">EMAIL</label>
                    <input type="email" name="email" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white">
                </div>
                {% endif %}
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">MOBILE NUMBER / USERNAME</label>
                    <input type="text" name="username" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">PASSWORD</label>
                    <input type="password" name="password" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white">
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

# আলাদা সুরক্ষিত অ্যাডমিন প্যানেল টেমপ্লেট (`/admin`)
ADMIN_DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Control Panel</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>body { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; }</style>
</head>
<body class="p-4 pb-24">
    <div class="max-w-2xl mx-auto space-y-6">
        <div class="flex justify-between items-center bg-slate-900 border border-slate-800 p-4 rounded-xl">
            <span class="text-lg font-bold text-amber-400">ADMIN CONTROL PANEL</span>
            <div class="flex space-x-2">
                <a href="/" class="bg-slate-800 text-slate-200 px-3 py-1.5 rounded-lg text-xs font-bold">Home</a>
                <a href="/admin/logout" class="bg-red-500 text-white px-3 py-1.5 rounded-lg text-xs font-bold">Logout</a>
            </div>
        </div>

        <!-- Add Money Requests -->
        <h2 class="text-sm font-bold text-sky-400 uppercase tracking-wider">Pending Add Money Requests</h2>
        {% if add_moneys %}
            {% for am in add_moneys %}
                {% if am.status == 'Pending' %}
                <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-2">
                    <p class="text-xs text-slate-300">User: <strong class="text-white">{{ am.username }}</strong> | Amount: <strong class="text-emerald-400">{{ am.amount }} ৳</strong></p>
                    <p class="text-xs text-slate-300">TrxID: <strong class="text-amber-300">{{ am.trxid }}</strong></p>
                    <div class="flex space-x-2 pt-1">
                        <a href="/admin/add-money-action/approve/{{ am.id }}" class="flex-1 bg-emerald-500 text-slate-950 font-bold py-2 rounded-lg text-xs text-center">Approve</a>
                        <a href="/admin/add-money-action/reject/{{ am.id }}" class="flex-1 bg-red-500 text-white font-bold py-2 rounded-lg text-xs text-center">Reject</a>
                    </div>
                </div>
                {% endif %}
            {% endfor %}
        {% else %}
            <p class="text-xs text-slate-500">কোনো পেন্ডিং অ্যাড মানি রিকোয়েস্ট নেই।</p>
        {% endif %}

        <!-- Topup Orders -->
        <h2 class="text-sm font-bold text-amber-400 uppercase tracking-wider pt-4">Pending Topup Orders</h2>
        {% if orders %}
            {% for o in orders %}
                {% if o.status == 'Pending' %}
                <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-2">
                    <p class="text-xs text-slate-300">Order #{{ o.id }} - <strong class="text-emerald-400">{{ o.service }}</strong> (User: {{ o.username }})</p>
                    <p class="text-xs text-slate-300">UID: <strong class="text-white">{{ o.uid }}</strong> | Package: <strong class="text-white">{{ o.package }}</strong></p>
                    <p class="text-xs text-slate-300">TrxID: <strong class="text-amber-300">{{ o.trxid }}</strong></p>
                    <div class="flex space-x-2 pt-1">
                        <a href="/admin/order-action/complete/{{ o.id }}" class="flex-1 bg-emerald-500 text-slate-950 font-bold py-2 rounded-lg text-xs text-center">Complete</a>
                        <a href="/admin/order-action/reject/{{ o.id }}" class="flex-1 bg-red-500 text-white font-bold py-2 rounded-lg text-xs text-center">Reject</a>
                    </div>
                </div>
                {% endif %}
            {% endfor %}
        {% else %}
            <p class="text-xs text-slate-500">কোনো পেন্ডিং অর্ডার নেই।</p>
        {% endif %}
    </div>
</body>
</html>
"""

ADMIN_LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>body { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; }</style>
</head>
<body class="flex items-center justify-center min-h-screen p-4">
    <div class="bg-slate-900 border border-slate-800 w-full max-w-sm rounded-2xl p-6 shadow-2xl">
        <h2 class="text-xl font-bold text-center text-amber-400 mb-1">ADMIN LOGIN</h2>
        <p class="text-xs text-center text-slate-400 mb-6">গোপন অ্যাডমিন প্যানেল</p>
        
        {% if error %}
        <div class="bg-red-500/20 border border-red-500 text-red-300 text-xs p-3 rounded-xl mb-4 text-center">{{ error }}</div>
        {% endif %}

        <form method="POST" class="space-y-4">
            <div>
                <label class="block text-xs font-semibold text-slate-400 mb-1">USERNAME</label>
                <input type="text" name="username" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white">
            </div>
            <div>
                <label class="block text-xs font-semibold text-slate-400 mb-1">PASSWORD</label>
                <input type="password" name="password" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white">
            </div>
            <button type="submit" class="w-full bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold py-3 rounded-xl text-sm transition">
                LOGIN
            </button>
        </form>
    </div>
</body>
</html>
"""

# ফ্লাস্ক রাউটসমূহ
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template_string(INDEX_TEMPLATE, settings=site_settings)

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
    return render_template_string(AUTH_TEMPLATE, is_signup=False, error=error, settings=site_settings)

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
            users_db[uname] = {'name': name, 'email': email, 'username': uname, 'password': pwd}
            session['user'] = uname
            return redirect(url_for('home'))
    return render_template_string(AUTH_TEMPLATE, is_signup=True, error=error, settings=site_settings)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/add-money')
def add_money():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template_string(ADD_MONEY_TEMPLATE, settings=site_settings)

@app.route('/submit-add-money', methods=['POST'])
def submit_add_money():
    if 'user' not in session:
        return redirect(url_for('login'))
    amount = request.form.get('amount')
    return render_template_string(ADD_MONEY_PAY_TEMPLATE, amount=amount, settings=site_settings)

@app.route('/confirm-add-money', methods=['POST'])
def confirm_add_money():
    if 'user' not in session:
        return redirect(url_for('login'))
    req_id = len(add_money_db) + 1
    am_data = {
        'id': req_id,
        'username': session['user'],
        'amount': request.form.get('amount'),
        'trxid': request.form.get('trxid'),
        'status': 'Pending'
    }
    add_money_db.append(am_data)
    return redirect(url_for('my_orders'))

@app.route('/order/<service_type>')
def order_page(service_type):
    if 'user' not in session:
        return redirect(url_for('login'))
    services = {
        'ff-likes': {'title': site_settings['service_1_name'], 'packages': {'100 Likes': '30 ৳', '500 Likes': '130 ৳'}},
        'uid-topup': {'title': site_settings['service_2_name'], 'packages': {'100 Diamonds': '85 ৳', '310 Diamonds': '250 ৳'}},
        'unipin': {'title': site_settings['service_3_name'], 'packages': {'Unipin 50': '50 ৳'}},
        'weekly-monthly': {'title': site_settings['service_4_name'], 'packages': {'Weekly': '165 ৳'}},
        'level-up': {'title': site_settings['service_5_name'], 'packages': {'Level Up': '95 ৳'}},
        'weekly-lite': {'title': site_settings['service_6_name'], 'packages': {'Weekly Lite': '80 ৳'}}
    }
    data = services.get(service_type, {'title': 'Topup', 'packages': {'Pack': '100 ৳'}})
    return render_template_string(ORDER_TEMPLATE, title=data['title'], packages=data['packages'], settings=site_settings)

@app.route('/submit-order', methods=['POST'])
def submit_order():
    if 'user' not in session:
        return redirect(url_for('login'))
    order_id = len(orders_db) + 1
    order_data = {
        'id': order_id,
        'username': session['user'],
        'service': request.form.get('service'),
        'uid': request.form.get('uid'),
        'package': request.form.get('package'),
        'trxid': request.form.get('trxid'),
        'status': 'Pending'
    }
    orders_db.append(order_data)
    return redirect(url_for('my_orders'))

@app.route('/orders')
def my_orders():
    if 'user' not in session:
        return redirect(url_for('login'))
    u_orders = [o for o in orders_db if o['username'] == session['user']]
    u_am = [am for am in add_money_db if am['username'] == session['user']]
    return render_template_string(ORDERS_TEMPLATE, orders=u_orders, add_moneys=u_am, settings=site_settings)

@app.route('/codes')
def codes():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template_string(ORDERS_TEMPLATE, orders=[], add_moneys=[], settings=site_settings)

@app.route('/account')
def account():
    if 'user' not in session:
        return redirect(url_for('login'))
    u_info = users_db.get(session['user'], {'name': 'User', 'username': session['user']})
    return render_template_string(ACCOUNT_TEMPLATE, user=u_info, settings=site_settings)

# আলাদা অ্যাডমিন রাউটসমূহ (`/admin`)
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        uname = request.form.get('username').strip()
        pwd = request.form.get('password')
        if uname == ADMIN_USERNAME and pwd == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        error = 'ভুল ইউজারনেম বা পাসওয়ার্ড!'
    return render_template_string(ADMIN_LOGIN_TEMPLATE, error=error)

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    return render_template_string(ADMIN_DASHBOARD_TEMPLATE, orders=orders_db, add_moneys=add_money_db)

@app.route('/admin/order-action/<action>/<int:oid>')
def order_action(action, oid):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    for o in orders_db:
        if o['id'] == oid:
            o['status'] = 'Completed' if action == 'complete' else 'Rejected'
            break
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add-money-action/<action>/<int:aid>')
def add_money_action(action, aid):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    for am in add_money_db:
        if am['id'] == aid:
            am['status'] = 'Approved' if action == 'approve' else 'Rejected'
            break
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
