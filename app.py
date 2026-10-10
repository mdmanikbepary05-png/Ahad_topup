from flask import Flask, render_template_string, request, redirect, url_for, session
import datetime

app = Flask(__name__)
app.secret_key = 'ahad_topup_secret_key_secure'

users_db = {}
orders_db = []
add_money_db = []

# ড্রাইভ লিংক দিয়ে স্থায়ী স্লাইডার ব্যানার
banners_db = [
    {"id": 1, "image_url": "https://lh3.googleusercontent.com/d/1TFlAfznm-h_XvxBWm3nLCqouvCb1hVS6", "caption": "ফ্রি ফায়ার ইনস্ট্যান্ট অটো টপ-আপ"},
    {"id": 2, "image_url": "https://lh3.googleusercontent.com/d/1KSmxyifb-7fMI2CM__GYkEHwGiaoGslr", "caption": "১০০% ট্রাস্টেড ও দ্রুত সার্ভিস"}
]

# ড্রাইভ লিংক দিয়ে ৬টি সার্ভিস আইকন ও কাস্টম সেটিংস
site_settings = {
    "site_title": "AHAD TOPUP",
    "payment_number": "01727246581",
    "telegram_link": "https://t.me/ahahackr",
    "notice_text": "⚠️ সাবধান! কেউ কোনো ভুয়া TrxID বা ভুল তথ্য দিয়ে বাটপারি বা ফাজলামো করার চেষ্টা করলে সাথে সাথে অ্যাকাউন্ট এবং ডিভাইস চিরতরে ব্যান করা হবে! 😡🔥 ভুল ইউজারনেম, ভুল UID বা ভুয়া ট্রানজেকশন দিলে অর্ডার তো রিজেক্ট হবেই, সাথে একাউন্টও লক করে দেওয়া হবে। নিজে ভালো হয়ে যাও, না হলে সিস্টেম থেকে পাকাপাকিভাবে আউট করে দেওয়া হবে! 🤬🛑\n\nকোনো প্রকার সমস্যায় পড়লে সরাসরি যোগাযোগ করো: যোগাযোগ@ahahackr (টেলিগ্রাম সাপোর্ট আইডি)।\n— আহাদ 😎✊",
    
    "service_1_name": "FF LIKES",
    "service_1_icon": "https://lh3.googleusercontent.com/d/1Epgm0nOw4e3yY6ExS_aTooGYOPU9C49p",
    "service_1_pkgs": "100 Likes - 30 ৳, 500 Likes - 130 ৳, 1000 Likes - 250 ৳",
    "service_1_warning": "সঠিক ইউজারনেম বা আইডি দিন। লাইক ডেলিভারিতে ২৪ ঘণ্টা পর্যন্ত সময় লাগতে পারে।",

    "service_2_name": "UID TOPUP",
    "service_2_icon": "https://lh3.googleusercontent.com/d/1jbB56j3MXlpC4ERjQN233O5vb3_0wcxg",
    "service_2_pkgs": "100 Diamonds - 85 ৳, 310 Diamonds - 250 ৳, 520 Diamonds - 410 ৳",
    "service_2_warning": "সঠিক Player UID প্রদান করুন। ভুল UID-তে ডায়মন্ড গেলে কর্তৃপক্ষ দায়ী নয়।",

    "service_3_name": "UNIPIN VOUCHER",
    "service_3_icon": "https://lh3.googleusercontent.com/d/1pNofYB4QRXAsprIlDjKYUVooB9MSPGSL",
    "service_3_pkgs": "Unipin 50 BDT - 50 ৳, Unipin 100 BDT - 100 ৳",
    "service_3_warning": "ইউনপিন ভাউচার কোড সফলভাবে পেমেন্ট হওয়ার পর My Codes অপশনে পেয়ে যাবেন।",

    "service_4_name": "WEEKLY MONTHLY",
    "service_4_icon": "https://lh3.googleusercontent.com/d/1FGhbD63WLtCGWg66yxXKdqmAaMOxlD-u",
    "service_4_pkgs": "Weekly Membership - 165 ৳, Monthly Membership - 520 ৳",
    "service_4_warning": "উইকলি বা মান্থলি নেওয়ার আগে গেমের ইন-গেম রুলস ও লিমিট চেক করে নিন।",

    "service_5_name": "LEVEL UP PASS",
    "service_5_icon": "https://lh3.googleusercontent.com/d/1MBjQL62p6XDsYfzZDo-onhdH95-HjOVS",
    "service_5_pkgs": "Level Up Pass - 95 ৳",
    "service_5_warning": "আইডিতে লেভেল আপ পাস আগে কেনা থাকলে পুনরায় অর্ডার করবেন না।",

    "service_6_name": "WEEKLY LITE",
    "service_6_icon": "https://lh3.googleusercontent.com/d/1z6mxPGvtlJH6KjdrKzArryHz0nIGIA1L",
    "service_6_pkgs": "Weekly Lite Pass - 80 ৳",
    "service_6_warning": "সঠিক তথ্য দিয়ে পেমেন্ট কনফার্ম করুন। কোনো সমস্যা হলে টেলিগ্রামে যোগাযোগ করুন।"
}

ADMIN_USERNAME = "ahadadmin"
ADMIN_PASSWORD = "123"

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
        body { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; transition: background-color 0.3s, color 0.3s; }
        .card-bg { background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid #334155; }
        .floating-support {
            position: fixed; bottom: 85px; right: 20px; background-color: #0088cc; color: white;
            width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center;
            justify-content: center; font-size: 24px; box-shadow: 0 4px 10px rgba(0,0,0,0.4); z-index: 50;
        }

        /* Sun / Light Mode Style */
        body.light-mode {
            background-color: #f1f5f9 !important;
            color: #0f172a !important;
        }
        body.light-mode .bg-slate-900 {
            background-color: #ffffff !important;
            border-color: #e2e8f0 !important;
            color: #0f172a !important;
        }
        body.light-mode .card-bg {
            background: linear-gradient(135deg, #ffffff, #f8fafc) !important;
            border-color: #cbd5e1 !important;
        }
        body.light-mode text-slate-200, 
        body.light-mode text-slate-300, 
        body.light-mode text-white {
            color: #0f172a !important;
        }
    </style>
</head>
<body class="pb-24">

    <div id="welcomeWarningModal" class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
        <div class="bg-slate-900 border border-amber-500/50 w-full max-w-sm rounded-2xl p-5 shadow-2xl space-y-4">
            <div class="flex items-center space-x-2 text-amber-400">
                <i class="fa-solid fa-triangle-exclamation text-xl"></i>
                <h3 class="font-bold text-base">জরুরী সতর্কতা ও নোটিশ</h3>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed whitespace-pre-line">{{ settings.notice_text }}</p>
            <button onclick="closeWarningModal()" class="w-full bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold py-2.5 rounded-xl text-xs transition">
                বুঝেছি (OK)
            </button>
        </div>
    </div>
    <script>
        function closeWarningModal() { document.getElementById('welcomeWarningModal').style.display = 'none'; }
        
        // সেভ করা থিম রান করানো
        window.addEventListener('DOMContentLoaded', () => {
            const savedTheme = localStorage.getItem('site_theme');
            if(savedTheme === 'light') {
                document.body.classList.add('light-mode');
            }
        });
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
        <a href="/settings" class="flex flex-col items-center text-slate-400 hover:text-slate-200">
            <i class="fa-solid fa-gear text-lg"></i>
            <span class="text-[10px] mt-1 font-medium">Settings</span>
        </a>
    </nav>
    <a href="{{ settings.telegram_link }}" target="_blank" class="floating-support" title="Telegram Support">
        <i class="fa-brands fa-telegram-plane"></i>
    </a>
</body>
</html>
"""

INDEX_TEMPLATE = BASE_HEAD + """
    <header class="flex justify-between items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <span class="text-xl font-bold tracking-wider text-emerald-400">{{ settings.site_title }}</span>
        <div class="flex items-center space-x-3">
            <a href="{{ settings.telegram_link }}" target="_blank" class="bg-sky-500/20 border border-sky-500/50 text-sky-400 px-3 py-1.5 rounded-full text-xs font-bold flex items-center">
                <i class="fa-brands fa-telegram mr-1 text-sm"></i> Telegram
            </a>
            <div class="flex items-center bg-emerald-600/20 border border-emerald-500/50 px-3 py-1.5 rounded-full">
                <i class="fa-solid fa-wallet text-emerald-400 mr-1.5"></i>
                <span class="text-sm font-semibold text-emerald-300">{{ wallet_balance }} ৳</span>
            </div>
        </div>
    </header>

    <main class="p-4 max-w-md mx-auto space-y-4">
        <div class="w-full h-40 bg-slate-800 rounded-xl relative border border-slate-700 overflow-hidden shadow-lg">
            <div id="sliderContainer" class="w-full h-full relative">
                {% for b in banners %}
                <div class="slide absolute inset-0 w-full h-full transition-opacity duration-1000 {% if loop.index0 != 0 %}opacity-0{% else %}opacity-100{% endif %}">
                    <img src="{{ b.image_url }}" class="w-full h-full object-cover">
                    <div class="absolute inset-0 flex items-end justify-center p-3">
                        <p class="text-xs font-bold text-white drop-shadow bg-black/50 px-3 py-1 rounded-full">{{ b.caption }}</p>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <script>
            let currentSlide = 0;
            const slides = document.querySelectorAll('.slide');
            if(slides.length > 1) {
                setInterval(() => {
                    slides[currentSlide].style.opacity = 0;
                    currentSlide = (currentSlide + 1) % slides.length;
                    slides[currentSlide].style.opacity = 1;
                }, 3500);
            }
        </script>

        <h2 class="text-center font-bold tracking-wider text-slate-200 mb-2 text-lg border-b border-slate-800 pb-2">REGULAR TOPUP</h2>

        <div class="grid grid-cols-3 gap-3">
            <a href="/order/1" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <img src="{{ settings.service_1_icon }}" class="w-full h-full object-cover">
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_1_name }}</span>
            </a>
            <a href="/order/2" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <img src="{{ settings.service_2_icon }}" class="w-full h-full object-cover">
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_2_name }}</span>
            </a>
            <a href="/order/3" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <img src="{{ settings.service_3_icon }}" class="w-full h-full object-cover">
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_3_name }}</span>
            </a>
            <a href="/order/4" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <img src="{{ settings.service_4_icon }}" class="w-full h-full object-cover">
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_4_name }}</span>
            </a>
            <a href="/order/5" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <img src="{{ settings.service_5_icon }}" class="w-full h-full object-cover">
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_5_name }}</span>
            </a>
            <a href="/order/6" class="card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <img src="{{ settings.service_6_icon }}" class="w-full h-full object-cover">
                </div>
                <span class="text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_6_name }}</span>
            </a>
        </div>
    </main>
""" + BOTTOM_NAV

SETTINGS_TEMPLATE = BASE_HEAD + """
    <header class="flex items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <a href="/" class="text-slate-300 mr-4 text-lg"><i class="fa-solid fa-arrow-left"></i></a>
        <h1 class="text-base font-bold uppercase tracking-wider text-slate-200"><i class="fa-solid fa-gear mr-1 text-emerald-400"></i> Settings & Profile</h1>
    </header>

    <main class="p-4 max-w-md mx-auto space-y-4">
        <!-- ইউজার প্রোফাইল বিবরণ -->
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl text-center space-y-2">
            <div class="w-16 h-16 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto text-2xl font-bold border border-emerald-500/30">
                {{ user.name[0].upper() }}
            </div>
            <h2 class="text-base font-bold text-white">{{ user.name }}</h2>
            <p class="text-xs text-slate-400">{{ user.username }}</p>
            <div class="bg-slate-800 p-3 rounded-xl border border-slate-700 flex justify-between items-center">
                <span class="text-xs text-slate-300">Wallet Balance:</span>
                <span class="text-sm font-bold text-emerald-400">{{ user.wallet }} ৳</span>
            </div>
        </div>

        <!-- থিম ও ডিসপ্লে সেটিংস (Sun / Night Option) -->
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-3">
            <h3 class="text-xs font-bold text-amber-400 uppercase tracking-wider"><i class="fa-solid fa-palette mr-1"></i> Theme Settings</h3>
            <p class="text-[11px] text-slate-400">ইন্টারফেসের আলো বা কালার মোড পরিবর্তন করুন:</p>
            
            <div class="grid grid-cols-2 gap-3 pt-1">
                <button onclick="changeTheme('light')" class="bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold py-2.5 rounded-xl text-xs flex items-center justify-center shadow">
                    <i class="fa-solid fa-sun mr-1.5 text-base"></i> Sun (Light)
                </button>
                <button onclick="changeTheme('dark')" class="bg-slate-800 hover:bg-slate-700 text-white font-bold py-2.5 rounded-xl text-xs flex items-center justify-center border border-slate-700">
                    <i class="fa-solid fa-moon mr-1.5 text-base"></i> Night (Dark)
                </button>
            </div>
        </div>

        <!-- অর্ডার ও লেনদেন পরিসংখ্যান -->
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-3">
            <h3 class="text-xs font-bold text-sky-400 uppercase tracking-wider"><i class="fa-solid fa-chart-pie mr-1"></i> Activity Summary</h3>
            <div class="grid grid-cols-2 gap-3">
                <div class="bg-slate-800/60 p-3 rounded-xl border border-slate-700 text-center">
                    <p class="text-[10px] text-slate-400 uppercase">Total Orders</p>
                    <p class="text-lg font-bold text-emerald-400">{{ total_orders }}</p>
                </div>
                <div class="bg-slate-800/60 p-3 rounded-xl border border-slate-700 text-center">
                    <p class="text-[10px] text-slate-400 uppercase">Add Money Requests</p>
                    <p class="text-lg font-bold text-sky-400">{{ total_add_money }}</p>
                </div>
            </div>
        </div>

        <!-- লগআউট অপশন -->
        <a href="/logout" class="block w-full bg-red-500/10 border border-red-500/30 text-red-400 font-bold py-3 rounded-xl text-xs text-center hover:bg-red-500 hover:text-white transition">
            <i class="fa-solid fa-right-from-bracket mr-1"></i> LOGOUT ACCOUNT
        </a>
    </main>

    <script>
        function changeTheme(theme) {
            if(theme === 'light') {
                document.body.classList.add('light-mode');
                localStorage.setItem('site_theme', 'light');
            } else {
                document.body.classList.remove('light-mode');
                localStorage.setItem('site_theme', 'dark');
            }
        }
    </script>
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
                    <input type="number" name="amount" required placeholder="উদা: 100" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-sm text-white">
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
            </div>
            <div>
                <label class="block text-xs font-semibold text-slate-400 mb-1">TRANSACTION ID (TrxID)</label>
                <input type="text" name="trxid" required placeholder="বিকাশ TrxID দিন" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-sm text-white">
            </div>
        </div>
        <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold py-3.5 rounded-xl transition">
            SUBMIT TRXID
        </button>
    </form>
""" + BOTTOM_NAV

ORDER_TEMPLATE = BASE_HEAD + """
    <header class="flex items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <a href="/" class="text-slate-300 mr-4 text-lg"><i class="fa-solid fa-arrow-left"></i></a>
        <h1 class="text-base font-bold uppercase tracking-wider text-slate-200">{{ service_name }}</h1>
    </header>

    <form action="/submit-order" method="POST" class="p-4 max-w-md mx-auto space-y-4">
        <input type="hidden" name="service" value="{{ service_name }}">
        
        {% if service_warning %}
        <div class="bg-amber-500/10 border border-amber-500/40 p-3.5 rounded-xl space-y-1">
            <div class="flex items-center text-amber-400 font-bold text-xs">
                <i class="fa-solid fa-triangle-exclamation mr-1.5 text-sm"></i> বিশেষ সতর্কতা:
            </div>
            <p class="text-[11px] text-slate-300 leading-relaxed">{{ service_warning }}</p>
        </div>
        {% endif %}

        <div class="bg-slate-900 p-4 rounded-xl border border-slate-800">
            <label class="block text-xs font-semibold text-slate-400 mb-2">ENTER PLAYER UID</label>
            <input type="text" name="uid" required placeholder="Enter UID here..." class="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-sm text-white">
        </div>

        <div>
            <label class="block text-xs font-semibold text-slate-400 mb-2">SELECT PACKAGE</label>
            <div class="grid grid-cols-2 gap-3">
                {% for pkg in packages %}
                <div onclick="selectPackage(this, '{{ pkg }}')" class="package-card p-3 rounded-xl cursor-pointer text-center transition bg-slate-900 border border-slate-800">
                    <p class="text-sm font-bold text-white">{{ pkg }}</p>
                </div>
                {% endfor %}
            </div>
            <input type="hidden" name="package" id="selectedPackageInput" required>
        </div>

        <div>
            <label class="block text-xs font-semibold text-slate-400 mb-2">SELECT PAYMENT</label>
            <div class="grid grid-cols-4 gap-2">
                <button type="button" onclick="selectPayment(this, 'bKash')" class="pay-btn bg-slate-900 border border-slate-700 p-2.5 rounded-xl text-center text-[11px] font-bold text-pink-500">bKash</button>
                <button type="button" onclick="selectPayment(this, 'Nagad')" class="pay-btn bg-slate-900 border border-slate-700 p-2.5 rounded-xl text-center text-[11px] font-bold text-orange-500">Nagad</button>
                <button type="button" onclick="selectPayment(this, 'Rocket')" class="pay-btn bg-slate-900 border border-slate-700 p-2.5 rounded-xl text-center text-[11px] font-bold text-purple-500">Rocket</button>
                <button type="button" onclick="selectPayment(this, 'Wallet')" class="pay-btn bg-slate-900 border border-slate-700 p-2.5 rounded-xl text-center text-[11px] font-bold text-emerald-400">Wallet</button>
            </div>
            <input type="hidden" name="payment" id="selectedPaymentInput" required>
        </div>

        <div id="paymentBox" class="hidden bg-slate-900 p-4 rounded-xl border border-emerald-500/50 space-y-3">
            <p class="text-xs text-slate-300">Send money to: <strong class="text-emerald-400">{{ settings.payment_number }}</strong></p>
            <div>
                <label class="block text-xs font-semibold text-slate-400 mb-1">TRANSACTION ID (TrxID)</label>
                <input type="text" name="trxid" id="trxidInput" placeholder="Enter TrxID" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white">
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
        function selectPayment(element, method) {
            document.querySelectorAll('.pay-btn').forEach(btn => btn.style.borderColor = '#334155');
            element.style.borderColor = '#10b981';
            document.getElementById('selectedPaymentInput').value = method;
            
            const payBox = document.getElementById('paymentBox');
            const trxInput = document.getElementById('trxidInput');
            if(method === 'Wallet') {
                payBox.classList.add('hidden');
                trxInput.required = false;
            } else {
                payBox.classList.remove('hidden');
                trxInput.required = true;
            }
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
                <p class="text-xs text-slate-300">Payment: <strong class="text-amber-300">{{ o.payment }} {% if o.trxid %} (TrxID: {{ o.trxid }}) {% endif %}</strong></p>
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

AUTH_TEMPLATE = BASE_HEAD + """
    <div class="flex items-center justify-center min-h-screen p-4">
        <div class="bg-slate-900 border border-slate-800 w-full max-w-sm rounded-2xl p-6 shadow-2xl">
            <h2 class="text-xl font-bold text-center text-emerald-400 mb-1">{{ settings.site_title }}</h2>
            <p class="text-xs text-center text-slate-400 mb-6">আপনার অ্যাকাউন্টে লগইন করুন</p>
            
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
                    <label class="block text-xs font-semibold text-slate-400 mb-1">MOBILE / USERNAME</label>
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

        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-4 shadow-xl">
            <h2 class="text-sm font-bold text-amber-400 uppercase tracking-wider"><i class="fa-solid fa-sliders mr-1.5"></i> ওয়েবসাইট ও সার্ভিস কাস্টমাইজ করুন</h2>
            <form action="/admin/update-settings" method="POST" class="space-y-3">
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">Website Title</label>
                    <input type="text" name="site_title" value="{{ settings.site_title }}" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">Telegram Support Link</label>
                    <input type="text" name="telegram_link" value="{{ settings.telegram_link }}" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">Payment Number (bKash/Nagad/Rocket)</label>
                    <input type="text" name="payment_number" value="{{ settings.payment_number }}" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">Popup Notice / Warning Text</label>
                    <textarea name="notice_text" rows="4" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white">{{ settings.notice_text }}</textarea>
                </div>

                <hr class="border-slate-800 my-2">
                <h3 class="text-xs font-bold text-emerald-400 uppercase">৬টি সার্ভিস কার্ড, প্যাকেজ ও ওয়ার্নিং কাস্টমাইজার</h3>
                
                <div class="space-y-3">
                    {% for i in range(1, 7) %}
                    <div class="bg-slate-800/50 p-3 rounded-xl border border-slate-800 space-y-2">
                        <p class="text-xs font-bold text-amber-300">Service {{ i }}</p>
                        <div class="grid grid-cols-2 gap-2">
                            <input type="text" name="service_{{ i }}_name" value="{{ settings['service_' ~ i ~ '_name'] }}" class="bg-slate-800 border border-slate-700 rounded p-2 text-xs text-white" placeholder="নাম">
                            <input type="text" name="service_{{ i }}_icon" value="{{ settings['service_' ~ i ~ '_icon'] }}" class="bg-slate-800 border border-slate-700 rounded p-2 text-xs text-white" placeholder="ছবির লিংক">
                        </div>
                        <input type="text" name="service_{{ i }}_pkgs" value="{{ settings['service_' ~ i ~ '_pkgs'] }}" class="w-full bg-slate-800 border border-slate-700 rounded p-2 text-xs text-white" placeholder="প্যাকেজসমূহ">
                        <input type="text" name="service_{{ i }}_warning" value="{{ settings['service_' ~ i ~ '_warning'] }}" class="w-full bg-slate-800 border border-slate-700 rounded p-2 text-xs text-amber-200" placeholder="এই সার্ভিসের জন্য বিশেষ ওয়ার্নিং...">
                    </div>
                    {% endfor %}
                </div>

                <button type="submit" class="w-full bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold py-3 rounded-xl text-xs transition shadow-lg mt-4">
                    SAVE & UPDATE WEBSITE
                </button>
            </form>
        </div>

        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-4 shadow-xl">
            <h2 class="text-sm font-bold text-amber-400 uppercase tracking-wider"><i class="fa-solid fa-images mr-1.5"></i> স্লাইডার ব্যানার ম্যানেজ করুন</h2>
            <form action="/admin/add-banner" method="POST" class="space-y-3">
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">Banner Image URL</label>
                    <input type="text" name="image_url" required placeholder="https://..." class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">Banner Caption / Text</label>
                    <input type="text" name="caption" required placeholder="ব্যানারের টেক্সট..." class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white">
                </div>
                <button type="submit" class="w-full bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold py-2.5 rounded-xl text-xs transition">
                    + ব্যানার যুক্ত করুন
                </button>
            </form>
            
            <div class="space-y-2 pt-2">
                <p class="text-xs text-slate-400 font-semibold">সক্রিয় ব্যানারসমূহ:</p>
                {% for b in banners %}
                <div class="flex justify-between items-center bg-slate-800 p-2.5 rounded-lg border border-slate-700">
                    <span class="text-xs text-white truncate max-w-[250px]">{{ b.caption }}</span>
                    <a href="/admin/delete-banner/{{ b.id }}" class="bg-red-500/20 text-red-400 px-2.5 py-1 rounded text-xs font-bold">Delete</a>
                </div>
                {% endfor %}
            </div>
        </div>

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

        <h2 class="text-sm font-bold text-amber-400 uppercase tracking-wider pt-4">Pending Topup Orders</h2>
        {% if orders %}
            {% for o in orders %}
                {% if o.status == 'Pending' %}
                <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-2">
                    <p class="text-xs text-slate-300">Order #{{ o.id }} - <strong class="text-emerald-400">{{ o.service }}</strong> (User: {{ o.username }})</p>
                    <p class="text-xs text-slate-300">UID: <strong class="text-white">{{ o.uid }}</strong> | Package: <strong class="text-white">{{ o.package }}</strong></p>
                    <p class="text-xs text-slate-300">Payment: <strong class="text-amber-300">{{ o.payment }} {% if o.trxid %} (TrxID: {{ o.trxid }}) {% endif %}</strong></p>
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
        <form method="POST" class="space-y-4 mt-4">
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

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    uname = session['user']
    if uname not in users_db:
        users_db[uname] = {'name': uname, 'username': uname, 'wallet': 0.0}
    user = users_db[uname]
    if 'wallet' not in user:
        user['wallet'] = 0.0
    return render_template_string(INDEX_TEMPLATE, settings=site_settings, banners=banners_db, wallet_balance=user['wallet'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        uname = request.form.get('username').strip()
        pwd = request.form.get('password')
        if uname in users_db and users_db[uname].get('password') == pwd:
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
            users_db[uname] = {'name': name, 'email': email, 'username': uname, 'password': pwd, 'wallet': 0.0}
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
        'amount': float(request.form.get('amount')),
        'trxid': request.form.get('trxid'),
        'status': 'Pending'
    }
    add_money_db.append(am_data)
    return redirect(url_for('my_orders'))

@app.route('/order/<sid>')
def order_page(sid):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    services_map = {
        '1': {'name': site_settings['service_1_name'], 'pkgs': site_settings['service_1_pkgs'], 'warning': site_settings['service_1_warning']},
        '2': {'name': site_settings['service_2_name'], 'pkgs': site_settings['service_2_pkgs'], 'warning': site_settings['service_2_warning']},
        '3': {'name': site_settings['service_3_name'], 'pkgs': site_settings['service_3_pkgs'], 'warning': site_settings['service_3_warning']},
        '4': {'name': site_settings['service_4_name'], 'pkgs': site_settings['service_4_pkgs'], 'warning': site_settings['service_4_warning']},
        '5': {'name': site_settings['service_5_name'], 'pkgs': site_settings['service_5_pkgs'], 'warning': site_settings['service_5_warning']},
        '6': {'name': site_settings['service_6_name'], 'pkgs': site_settings['service_6_pkgs'], 'warning': site_settings['service_6_warning']}
    }
    
    srv = services_map.get(sid)
    if not srv:
        return redirect(url_for('home'))
        
    pkgs_list = [p.strip() for p in srv['pkgs'].split(',') if p.strip()]
    return render_template_string(ORDER_TEMPLATE, service_name=srv['name'], packages=pkgs_list, service_warning=srv['warning'], settings=site_settings)

@app.route('/submit-order', methods=['POST'])
def submit_order():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    uname = session['user']
    if uname not in users_db:
        users_db[uname] = {'name': uname, 'username': uname, 'wallet': 0.0}
    user = users_db[uname]
    
    package_str = request.form.get('package')
    payment_method = request.form.get('payment')
    trxid = request.form.get('trxid', 'N/A')
    
    if payment_method == 'Wallet':
        try:
            price = float(package_str.split('-')[-1].replace('৳', '').strip())
        except:
            price = 0.0
            
        if user.get('wallet', 0.0) < price:
            return "ওয়ালেটে পর্যাপ্ত ব্যালেন্স নেই! আগে Add Money করুন।"
        user['wallet'] -= price
        trxid = 'Wallet Paid'

    order_id = len(orders_db) + 1
    order_data = {
        'id': order_id,
        'username': uname,
        'service': request.form.get('service'),
        'uid': request.form.get('uid'),
        'package': package_str,
        'payment': payment_method,
        'trxid': trxid,
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

@app.route('/settings')
def settings_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    uname = session['user']
    if uname not in users_db:
        users_db[uname] = {'name': uname, 'username': uname, 'wallet': 0.0}
    u_info = users_db[uname]
    
    tot_orders = len([o for o in orders_db if o['username'] == uname])
    tot_am = len([am for am in add_money_db if am['username'] == uname])
    
    return render_template_string(SETTINGS_TEMPLATE, user=u_info, total_orders=tot_orders, total_add_money=tot_am, settings=site_settings)

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        uname = request.form.get('username').strip()
        pwd = request.form.get('password')
        if uname == ADMIN_USERNAME and pwd == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
    return render_template_string(ADMIN_LOGIN_TEMPLATE)

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    return render_template_string(ADMIN_DASHBOARD_TEMPLATE, orders=orders_db, add_moneys=add_money_db, banners=banners_db, settings=site_settings)

@app.route('/admin/update-settings', methods=['POST'])
def update_settings():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    site_settings['site_title'] = request.form.get('site_title').strip()
    site_settings['telegram_link'] = request.form.get('telegram_link').strip()
    site_settings['payment_number'] = request.form.get('payment_number').strip()
    site_settings['notice_text'] = request.form.get('notice_text').strip()
    
    for i in range(1, 7):
        site_settings[f'service_{i}_name'] = request.form.get(f'service_{i}_name').strip()
        
        icon_url = request.form.get(f'service_{i}_icon').strip()
        if 'drive.google.com' in icon_url:
            try:
                fid = icon_url.split('/d/')[1].split('/')[0]
                icon_url = f"https://lh3.googleusercontent.com/d/{fid}"
            except:
                pass
        site_settings[f'service_{i}_icon'] = icon_url
        
        site_settings[f'service_{i}_pkgs'] = request.form.get(f'service_{i}_pkgs').strip()
        site_settings[f'service_{i}_warning'] = request.form.get(f'service_{i}_warning').strip()
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add-banner', methods=['POST'])
def add_banner():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    raw_url = request.form.get('image_url').strip()
    if 'drive.google.com' in raw_url:
        try:
            file_id = raw_url.split('/d/')[1].split('/')[0]
            raw_url = f"https://lh3.googleusercontent.com/d/{file_id}"
        except:
            pass

    new_b = {
        'id': len(banners_db) + 1,
        'image_url': raw_url,
        'caption': request.form.get('caption').strip()
    }
    banners_db.append(new_b)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-banner/<int:bid>')
def delete_banner(bid):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    global banners_db
    banners_db = [b for b in banners_db if b['id'] != bid]
    return redirect(url_for('admin_dashboard'))

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
            if action == 'approve' and am['status'] == 'Pending':
                am['status'] = 'Approved'
                uname = am['username']
                if uname not in users_db:
                    users_db[uname] = {'name': uname, 'username': uname, 'wallet': 0.0}
                if 'wallet' not in users_db[uname]:
                    users_db[uname]['wallet'] = 0.0
                users_db[uname]['wallet'] += am['amount']
            elif action == 'reject':
                am['status'] = 'Rejected'
            break
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
