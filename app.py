from flask import Flask, render_template_string, request, redirect, url_for, session
import random
import datetime

app = Flask(__name__)
app.secret_key = 'ahad_topup_secret_key_secure'

# ডাটাবেস সিমুলেশন
users_db = {}
orders_db = []
add_money_db = []

promo_codes = {
    "AHAD50": 50,
    "FREE20": 20
}

banners_db = [
    {"id": 1, "image_url": "https://lh3.googleusercontent.com/d/1TFlAfznm-h_XvxBWm3nLCqouvCb1hVS6", "caption": "ফ্রি ফায়ার ইনস্ট্যান্ট অটো টপ-আপ"},
    {"id": 2, "image_url": "https://lh3.googleusercontent.com/d/1KSmxyifb-7fMI2CM__GYkEHwGiaoGslr", "caption": "১০০% ট্রাস্টেড ও দ্রুত সার্ভিস"}
]

site_settings = {
    "site_title": "AHAD TOPUP",
    "payment_number": "01727246581",
    "telegram_link": "https://t.me/ahahackr",
    "notice_text": "⚠️ সাবধান! কেউ কোনো ভুয়া TrxID বা ভুল তথ্য দিয়ে ট্রাই করলে সাথে সাথে একাউন্ট ব্যান করা হবে! 🤬🛑\n\nকোনো সমস্যা হলে টেলিগ্রামে যোগাযোগ করুন: @ahahackr\n— আহাদ 😎✊",
    "is_app_off": False,  # অ্যাডমিন থেকে অ্যাপ অফ রাখার সুইচ (True / False)
    
    "service_1_name": "FF LIKES",
    "service_1_icon": "https://lh3.googleusercontent.com/d/1Epgm0nOw4e3yY6ExS_aTooGYOPU9C49p",
    "service_1_pkgs": "100 Likes - 30 ৳, 500 Likes - 130 ৳, 1000 Likes - 250 ৳",
    "service_1_warning": "সঠিক ইউজারনেম বা আইডি দিন।",

    "service_2_name": "UID TOPUP",
    "service_2_icon": "https://lh3.googleusercontent.com/d/1jbB56j3MXlpC4ERjQN233O5vb3_0wcxg",
    "service_2_pkgs": "100 Diamonds - 85 ৳, 310 Diamonds - 250 ৳, 520 Diamonds - 410 ৳",
    "service_2_warning": "সঠিক Player UID প্রদান করুন।",

    "service_3_name": "UNIPIN VOUCHER",
    "service_3_icon": "https://lh3.googleusercontent.com/d/1pNofYB4QRXAsprIlDjKYUVooB9MSPGSL",
    "service_3_pkgs": "Unipin 50 BDT - 50 ৳, Unipin 100 BDT - 100 ৳",
    "service_3_warning": "ভাউচার কোড সফলভাবে পেমেন্ট হওয়ার পর My Codes-এ পেয়ে যাবেন।",

    "service_4_name": "WEEKLY MONTHLY",
    "service_4_icon": "https://lh3.googleusercontent.com/d/1FGhbD63WLtCGWg66yxXKdqmAaMOxlD-u",
    "service_4_pkgs": "Weekly Membership - 165 ৳, Monthly Membership - 520 ৳",
    "service_4_warning": "ইন-গেম রুলস মেনে অর্ডার করুন।",

    "service_5_name": "LEVEL UP PASS",
    "service_5_icon": "https://lh3.googleusercontent.com/d/1MBjQL62p6XDsYfzZDo-onhdH95-HjOVS",
    "service_5_pkgs": "Level Up Pass - 95 ৳",
    "service_5_warning": "আইডিতে লেভেল আপ পাস আগে কেনা থাকলে অর্ডার করবেন না।",

    "service_6_name": "WEEKLY LITE",
    "service_6_icon": "https://lh3.googleusercontent.com/d/1z6mxPGvtlJH6KjdrKzArryHz0nIGIA1L",
    "service_6_pkgs": "Weekly Lite Pass - 80 ৳",
    "service_6_warning": "সঠিক তথ্য দিয়ে পেমেন্ট কনফার্ম করুন।"
}

ADMIN_USERNAME = "ahadadmin"
ADMIN_PASSWORD = "123"

# 🕌 ৫ ওয়াক্ত নামাজের অটো-অফ টাইম ফিল্টার
def check_prayer_or_maintenance():
    # অ্যাডমিন যদি নিজে অ্যাপ অফ করে রাখে
    if site_settings.get("is_app_off"):
        return True, "🛠️ অ্যাপটির আপডেট কাজ চলছে, অনুগ্রহ করে অপেক্ষা করুন..."
    
    # বর্তমান লোকাল সময় চেক (HH:MM ফরম্যাটে)
    now_time = datetime.datetime.now().strftime("%H:%M")
    
    # ৫ ওয়াক্ত নামাজের নির্ধারিত অফ টাইম রেঞ্জ
    prayer_times = [
        ("04:45", "05:45", "ফজর"),
        ("13:00", "13:30", "জোহর"),
        ("16:15", "17:00", "আসর"),
        ("17:45", "18:30", "মাগরিব"),
        ("19:45", "20:30", "এশা")
    ]
    
    for start, end, name in prayer_times:
        if start <= now_time <= end:
            return True, f"🕌 পবিত্র {name} নামাজের জন্য অ্যাপ সাময়িকভাবে বন্ধ রয়েছে। নামাজের ওয়াক্ত শেষে আবার চালু হবে।"
            
    return False, ""

# 🔒 মিডলওয়্যার: সব রিকোয়েস্ট চেক করার জন্য
@app.before_request
def check_app_status():
    # অ্যাডমিন প্যানেল এবং স্ট্যাটিক রুট ছাড়া বাকি সব পেজে অফ স্ক্রিন দেখাবে
    if request.endpoint and not request.endpoint.startswith('admin') and request.endpoint not in ['static', 'app_closed']:
        is_closed, reason_msg = check_prayer_or_maintenance()
        if is_closed:
            return render_template_string(CLOSED_TEMPLATE, reason=reason_msg)

CLOSED_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App Closed</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-950 text-white min-h-screen flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-800 p-8 rounded-3xl max-w-sm text-center space-y-5 shadow-2xl">
        <div class="w-20 h-20 bg-amber-500/10 border-2 border-amber-500/40 rounded-full flex items-center justify-center mx-auto text-3xl animate-bounce">
            ⏰
        </div>
        <h2 class="text-lg font-bold text-amber-400 uppercase tracking-wider">অ্যাপ বর্তমানে বন্ধ আছে</h2>
        <div class="bg-slate-800/80 p-4 rounded-2xl border border-slate-700">
            <p class="text-xs text-slate-200 leading-relaxed font-medium">{{ reason }}</p>
        </div>
        <p class="text-[10px] text-slate-500">আমাদের অ্যাপটি ২৪ ঘণ্টা চালু থাকে, তবে নামাজের সময় ও আপডেট চলায় সাময়িক বিরতি দেওয়া হয়। ধন্যবাদ।</p>
    </div>
</body>
</html>
"""

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
        body.light-mode { background-color: #f1f5f9 !important; color: #0f172a !important; }
        body.light-mode .bg-slate-900 { background-color: #ffffff !important; border-color: #e2e8f0 !important; color: #0f172a !important; }
        body.light-mode .card-bg { background: linear-gradient(135deg, #ffffff, #f8fafc) !important; border-color: #cbd5e1 !important; }
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
        window.addEventListener('DOMContentLoaded', () => {
            const savedTheme = localStorage.getItem('site_theme');
            if(savedTheme === 'light') { document.body.classList.add('light-mode'); }
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
        <a href="/spin" class="flex flex-col items-center text-amber-400 hover:text-amber-300">
            <i class="fa-solid fa-dharmachakra text-lg"></i>
            <span class="text-[10px] mt-1 font-medium">Spin & Win</span>
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
        <div class="flex items-center space-x-2">
            <div class="flex items-center bg-amber-500/20 border border-amber-500/40 px-2.5 py-1 rounded-full text-amber-300 font-bold text-xs">
                🪙 <span class="ml-1">{{ tokens }}</span>
            </div>
            <div class="flex items-center bg-emerald-600/20 border border-emerald-500/50 px-2.5 py-1 rounded-full text-emerald-300 font-bold text-xs">
                ৳ <span class="ml-1">{{ wallet_balance }}</span>
            </div>
        </div>
    </header>

    <main class="p-4 max-w-md mx-auto space-y-4">
        <!-- ২৪ ঘণ্টা সার্ভিস ব্যাজ -->
        <div class="bg-emerald-500/10 border border-emerald-500/30 p-2.5 rounded-xl flex items-center justify-center space-x-2 text-emerald-400">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
            <span class="text-[11px] font-bold">২৪ ঘণ্টা আমাদের সার্ভিস ও অটো টপ-আপ ওপেন থাকে!</span>
        </div>

        <!-- স্লাইডার ব্যানার -->
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

        <!-- স্পিন অ্যান্ড ফ্রি ডায়মন্ড কুইক লিংক -->
        <div class="grid grid-cols-2 gap-3">
            <a href="/spin" class="bg-gradient-to-r from-amber-500 to-orange-600 p-3 rounded-2xl shadow-lg text-slate-950 flex flex-col justify-between">
                <div class="text-xl">🎰</div>
                <div>
                    <h3 class="font-black text-xs uppercase">Daily Spin</h3>
                    <p class="text-[9px] font-bold opacity-90">টোকেন জিতুন ফ্রিতে!</p>
                </div>
            </a>
            <a href="/free-diamond" class="bg-gradient-to-r from-sky-500 to-blue-600 p-3 rounded-2xl shadow-lg text-white flex flex-col justify-between">
                <div class="text-xl">💎</div>
                <div>
                    <h3 class="font-black text-xs uppercase">Free Diamond</h3>
                    <p class="text-[9px] font-bold opacity-90">টোকেন দিয়ে ডায়মন্ড নিন!</p>
                </div>
            </a>
        </div>

        <!-- সার্চ বার -->
        <div class="relative">
            <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-3.5 text-slate-400 text-xs"></i>
            <input type="text" id="serviceSearchInput" onkeyup="filterServices()" placeholder="সার্ভিস খুঁজুন (যেমন: UID, Likes)..." class="w-full bg-slate-900 border border-slate-800 rounded-xl py-2.5 pl-10 pr-4 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500">
        </div>

        <h2 class="text-center font-bold tracking-wider text-slate-200 mb-2 text-lg border-b border-slate-800 pb-2">REGULAR TOPUP</h2>

        <div class="grid grid-cols-3 gap-3" id="servicesGrid">
            <a href="/order/1" class="service-card card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <img src="{{ settings.service_1_icon }}" class="w-full h-full object-cover">
                </div>
                <span class="service-title text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_1_name }}</span>
            </a>
            <a href="/order/2" class="service-card card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <img src="{{ settings.service_2_icon }}" class="w-full h-full object-cover">
                </div>
                <span class="service-title text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_2_name }}</span>
            </a>
            <a href="/order/3" class="service-card card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <img src="{{ settings.service_3_icon }}" class="w-full h-full object-cover">
                </div>
                <span class="service-title text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_3_name }}</span>
            </a>
            <a href="/order/4" class="service-card card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <img src="{{ settings.service_4_icon }}" class="w-full h-full object-cover">
                </div>
                <span class="service-title text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_4_name }}</span>
            </a>
            <a href="/order/5" class="service-card card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <img src="{{ settings.service_5_icon }}" class="w-full h-full object-cover">
                </div>
                <span class="service-title text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_5_name }}</span>
            </a>
            <a href="/order/6" class="service-card card-bg p-2.5 rounded-xl text-center flex flex-col items-center hover:border-emerald-500 transition">
                <div class="w-16 h-16 bg-slate-800 rounded-lg mb-2 flex items-center justify-center border border-slate-700 overflow-hidden">
                    <img src="{{ settings.service_6_icon }}" class="w-full h-full object-cover">
                </div>
                <span class="service-title text-[11px] font-bold text-slate-200 leading-tight">{{ settings.service_6_name }}</span>
            </a>
        </div>
    </main>

    <script>
        function filterServices() {
            let input = document.getElementById('serviceSearchInput').value.toLowerCase();
            let cards = document.getElementsByClassName('service-card');
            for (let card of cards) {
                let title = card.querySelector('.service-title').innerText.toLowerCase();
                if (title.includes(input)) {
                    card.style.display = "flex";
                } else {
                    card.style.display = "none";
                }
            }
        }
    </script>
""" + BOTTOM_NAV

SPIN_TEMPLATE = BASE_HEAD + """
    <header class="flex items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <a href="/" class="text-slate-300 mr-4 text-lg"><i class="fa-solid fa-arrow-left"></i></a>
        <h1 class="text-base font-bold uppercase tracking-wider text-slate-200"><i class="fa-solid fa-dharmachakra mr-1 text-amber-400"></i> Daily Free Spin Token</h1>
    </header>

    <main class="p-4 max-w-md mx-auto space-y-5 text-center">
        <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-4 shadow-xl">
            <h2 class="text-sm font-bold text-amber-400">প্রতিদিন ২৪ ঘণ্টায় ১ বার স্পিন করুন!</h2>
            <p class="text-xs text-slate-300">আপনার বর্তমান টোকেন: <strong class="text-amber-400 font-mono text-sm">🪙 {{ tokens }}</strong></p>
            
            {% if message %}
            <div class="bg-amber-500/20 border border-amber-500 text-amber-300 text-xs p-3 rounded-xl font-bold">
                {{ message }}
            </div>
            {% endif %}

            <div class="w-32 h-32 bg-amber-500/10 border-4 border-amber-500 rounded-full mx-auto flex items-center justify-center text-4xl shadow-2xl animate-pulse">
                🎰
            </div>

            <form action="/play-spin" method="POST">
                <button type="submit" class="w-full bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-slate-950 font-black py-3.5 rounded-xl text-sm shadow-lg transition transform active:scale-95">
                    SPIN FOR TOKEN NOW
                </button>
            </form>
            <p class="text-[10px] text-slate-400">স্পিন করে টোকেন জমিয়ে ফ্রিতে উইকলি ও মান্থলি রিডিম করুন!</p>
        </div>
    </main>
""" + BOTTOM_NAV

FREE_DIAMOND_TEMPLATE = BASE_HEAD + """
    <header class="flex items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <a href="/" class="text-slate-300 mr-4 text-lg"><i class="fa-solid fa-arrow-left"></i></a>
        <h1 class="text-base font-bold uppercase tracking-wider text-sky-400"><i class="fa-solid fa-gem mr-1"></i> FREE DIAMOND STORE</h1>
    </header>

    <main class="p-4 max-w-md mx-auto space-y-4">
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl flex justify-between items-center">
            <span class="text-xs text-slate-300">আপনার মোট টোকেন:</span>
            <span class="text-sm font-bold text-amber-400 font-mono">🪙 {{ tokens }} Token</span>
        </div>

        {% if msg %}
        <div class="bg-emerald-500/20 border border-emerald-500 text-emerald-300 text-xs p-3 rounded-xl font-bold text-center">
            {{ msg }}
        </div>
        {% endif %}

        <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl space-y-3">
            <div class="flex justify-between items-center">
                <h3 class="text-sm font-bold text-white">Weekly Membership (Free)</h3>
                <span class="bg-amber-500/20 text-amber-300 border border-amber-500/40 text-[10px] font-bold px-2.5 py-1 rounded-full">১,০০,০০০ Token</span>
            </div>
            <p class="text-[11px] text-slate-400">১ লাখ টোকেন জমিয়ে ফ্রিতে নিন উইকলি মেম্বারশিপ!</p>
            <form action="/redeem-diamond" method="POST" class="space-y-2">
                <input type="hidden" name="type" value="weekly">
                <input type="text" name="uid" required placeholder="Enter Player UID" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-xs text-white">
                <button type="submit" class="w-full bg-sky-500 hover:bg-sky-600 text-slate-950 font-bold py-2.5 rounded-xl text-xs transition">
                    ১ লাখ টোকেন দিয়ে রিডিম করুন
                </button>
            </form>
        </div>

        <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl space-y-3">
            <div class="flex justify-between items-center">
                <h3 class="text-sm font-bold text-white">Monthly Membership (Free)</h3>
                <span class="bg-amber-500/20 text-amber-300 border border-amber-500/40 text-[10px] font-bold px-2.5 py-1 rounded-full">৫,০০,০০০ Token</span>
            </div>
            <p class="text-[11px] text-slate-400">৫ লাখ টোকেন জমিয়ে ফ্রিতে কিনুন মান্থলি মেম্বারশিপ!</p>
            <form action="/redeem-diamond" method="POST" class="space-y-2">
                <input type="hidden" name="type" value="monthly">
                <input type="text" name="uid" required placeholder="Enter Player UID" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-xs text-white">
                <button type="submit" class="w-full bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold py-2.5 rounded-xl text-xs transition">
                    ৫ লাখ টোকেন দিয়ে রিডিম করুন
                </button>
            </form>
        </div>
    </main>
""" + BOTTOM_NAV

SETTINGS_TEMPLATE = BASE_HEAD + """
    <header class="flex items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <a href="/" class="text-slate-300 mr-4 text-lg"><i class="fa-solid fa-arrow-left"></i></a>
        <h1 class="text-base font-bold uppercase tracking-wider text-slate-200"><i class="fa-solid fa-gear mr-1 text-emerald-400"></i> Settings & Profile</h1>
    </header>

    <main class="p-4 max-w-md mx-auto space-y-4">
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl text-center space-y-2">
            <div class="w-16 h-16 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto text-2xl font-bold border border-emerald-500/30">
                {{ user.name[0].upper() }}
            </div>
            <h2 class="text-base font-bold text-white">{{ user.name }}</h2>
            <p class="text-xs text-slate-400">Username: {{ user.username }}</p>
            <div class="inline-block bg-amber-500/20 border border-amber-500/40 text-amber-300 px-3 py-1 rounded-full text-xs font-mono font-bold">
                USER UID: {{ user.user_uid }}
            </div>
            <div class="grid grid-cols-2 gap-2 mt-2">
                <div class="bg-slate-800 p-2.5 rounded-xl border border-slate-700">
                    <p class="text-[10px] text-slate-400">Wallet Balance</p>
                    <p class="text-sm font-bold text-emerald-400">{{ user.wallet }} ৳</p>
                </div>
                <div class="bg-slate-800 p-2.5 rounded-xl border border-slate-700">
                    <p class="text-[10px] text-slate-400">Total Tokens</p>
                    <p class="text-sm font-bold text-amber-400 font-mono">🪙 {{ user.tokens }}</p>
                </div>
            </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-3">
            <h3 class="text-xs font-bold text-amber-400 uppercase tracking-wider"><i class="fa-solid fa-share-nodes mr-1"></i> Referral Program</h3>
            <p class="text-[11px] text-slate-400">বন্ধুকে রেফার করুন এবং বোনাস পান:</p>
            <div class="bg-slate-800 p-2.5 rounded-xl border border-slate-700 flex justify-between items-center">
                <span class="text-xs font-mono text-emerald-400 select-all">https://ahadtopup.com/ref/{{ user.user_uid }}</span>
                <button onclick="navigator.clipboard.writeText('https://ahadtopup.com/ref/{{ user.user_uid }}'); alert('Referral link copied!');" class="bg-emerald-500 text-slate-950 font-bold px-3 py-1 rounded-lg text-xs">Copy</button>
            </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-3">
            <h3 class="text-xs font-bold text-amber-400 uppercase tracking-wider"><i class="fa-solid fa-palette mr-1"></i> Theme Settings</h3>
            <div class="grid grid-cols-2 gap-3 pt-1">
                <button onclick="changeTheme('light')" class="bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold py-2.5 rounded-xl text-xs flex items-center justify-center shadow">
                    <i class="fa-solid fa-sun mr-1.5 text-base"></i> Sun (Light)
                </button>
                <button onclick="changeTheme('dark')" class="bg-slate-800 hover:bg-slate-700 text-white font-bold py-2.5 rounded-xl text-xs flex items-center justify-center border border-slate-700">
                    <i class="fa-solid fa-moon mr-1.5 text-base"></i> Night (Dark)
                </button>
            </div>
        </div>

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

        <div class="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-2">
            <label class="block text-xs font-semibold text-slate-400">PROMO / COUPON CODE (Optional)</label>
            <input type="text" name="promo" placeholder="Enter Promo Code (e.g. AHAD50)" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-xs text-amber-400 uppercase font-bold">
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

ORDERS_TEMPLATE = BASE_HEAD + """
    <header class="flex items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <a href="/" class="text-slate-300 mr-4 text-lg"><i class="fa-solid fa-arrow-left"></i></a>
        <h1 class="text-base font-bold uppercase tracking-wider text-slate-200">My Orders & Invoice</h1>
    </header>

    <main class="p-4 max-w-md mx-auto space-y-4">
        <h3 class="text-xs font-bold text-slate-400 uppercase">Topup Orders</h3>
        {% if orders %}
            {% for o in orders %}
            <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-2 relative">
                <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-emerald-400">#ORD-{{ o.id }} - {{ o.service }}</span>
                    <span class="text-[10px] px-2.5 py-1 rounded-full font-bold 
                        {% if o.status == 'Pending' %} bg-amber-500/20 text-amber-400 border border-amber-500/30
                        {% elif o.status == 'Completed' %} bg-emerald-500/20 text-emerald-400 border border-emerald-500/30
                        {% else %} bg-red-500/20 text-red-400 border border-red-500/30 {% endif %}">
                        {{ o.status }}
                    </span>
                </div>
                <p class="text-xs text-slate-300">UID: <strong>{{ o.uid }}</strong></p>
                <p class="text-xs text-slate-300">Package: <strong>{{ o.package }}</strong></p>
                <p class="text-xs text-slate-300">Payment: <strong class="text-amber-300">{{ o.payment }} {% if o.trxid %} (TrxID: {{ o.trxid }}) {% endif %}</strong></p>
                <p class="text-[10px] text-slate-500 text-right">{{ o.time }}</p>
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
    <div class="max-w-3xl mx-auto space-y-6">
        <div class="flex justify-between items-center bg-slate-900 border border-slate-800 p-4 rounded-xl">
            <span class="text-lg font-bold text-amber-400">ADMIN CONTROL PANEL</span>
            <div class="flex space-x-2">
                <a href="/" class="bg-slate-800 text-slate-200 px-3 py-1.5 rounded-lg text-xs font-bold">Home</a>
                <a href="/admin/logout" class="bg-red-500 text-white px-3 py-1.5 rounded-lg text-xs font-bold">Logout</a>
            </div>
        </div>

        <!-- 🔴 অ্যাপ ম্যানুয়াল অফ / আপডেট মোড সুইচ -->
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl flex justify-between items-center shadow-xl">
            <div>
                <h3 class="text-sm font-bold text-white flex items-center">
                    <i class="fa-solid fa-power-off mr-2 text-red-500"></i> App Maintenance Mode
                </h3>
                <p class="text-[11px] text-slate-400 mt-0.5">অ্যাপটি বন্ধ করে দিলে ইউজারের স্ক্রিনে আপডেট নোটিশ দেখাবে।</p>
            </div>
            <a href="/admin/toggle-app-status" class="px-5 py-2.5 rounded-xl font-bold text-xs transition {% if settings.is_app_off %} bg-emerald-500 text-slate-950 {% else %} bg-red-500 text-white {% endif %}">
                {{ 'ENABLE APP (ON)' if settings.is_app_off else 'DISABLE APP (OFF)' }}
            </a>
        </div>

        <div class="grid grid-cols-3 gap-3">
            <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl text-center">
                <p class="text-[10px] text-slate-400 font-bold uppercase">Total Users</p>
                <h3 class="text-xl font-black text-sky-400 mt-1">{{ total_users }}</h3>
            </div>
            <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl text-center">
                <p class="text-[10px] text-slate-400 font-bold uppercase">Total Orders</p>
                <h3 class="text-xl font-black text-emerald-400 mt-1">{{ total_orders }}</h3>
            </div>
            <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl text-center">
                <p class="text-[10px] text-slate-400 font-bold uppercase">Pending</p>
                <h3 class="text-xl font-black text-amber-400 mt-1">{{ pending_orders }}</h3>
            </div>
        </div>

        <!-- ১. রেজিস্টার্ড ইউজারের UID ডাটাবেস সেকশন -->
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-4 shadow-xl">
            <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                <h2 class="text-sm font-bold text-sky-400 uppercase tracking-wider"><i class="fa-solid fa-users-gear mr-1.5"></i> Registered Users UID Interface</h2>
                <span class="text-xs bg-sky-500/20 text-sky-300 font-bold px-2.5 py-1 rounded-full">Total: {{ total_users }} Users</span>
            </div>

            <!-- ইউজার সার্চ বার -->
            <form action="/admin/search-user" method="POST" class="flex space-x-2">
                <input type="text" name="search_term" placeholder="Search by User UID or Username..." required class="flex-1 bg-slate-800 border border-slate-700 rounded-xl p-2.5 text-xs text-white uppercase">
                <button type="submit" class="bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold px-4 py-2.5 rounded-xl text-xs">Search UID</button>
            </form>

            {% if searched_user %}
            <div class="bg-slate-800 p-4 rounded-xl border border-amber-500/50 space-y-2">
                <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-emerald-400">{{ searched_user.name }}</span>
                    <span class="text-[10px] px-2 py-0.5 rounded-full font-bold {% if searched_user.is_banned %} bg-red-500/20 text-red-400 border border-red-500/30 {% else %} bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 {% endif %}">
                        {{ 'BANNED' if searched_user.is_banned else 'ACTIVE' }}
                    </span>
                </div>
                <p class="text-xs text-slate-300">Username: <strong>{{ searched_user.username }}</strong></p>
                <p class="text-xs text-slate-300">User UID: <strong class="text-amber-300">{{ searched_user.user_uid }}</strong></p>
                <p class="text-xs text-slate-300">Wallet Balance: <strong class="text-emerald-400">{{ searched_user.wallet }} ৳</strong> | Spin Tokens: <strong class="text-amber-400 font-mono">🪙 {{ searched_user.tokens }}</strong></p>
                <div class="pt-2">
                    <a href="/admin/toggle-ban/{{ searched_user.username }}" class="block w-full text-center font-bold py-2 rounded-lg text-xs {% if searched_user.is_banned %} bg-emerald-500 text-slate-950 {% else %} bg-red-500 text-white {% endif %}">
                        {{ 'UNBAN THIS USER' if searched_user.is_banned else 'BAN THIS USER' }}
                    </a>
                </div>
            </div>
            {% elif search_error %}
            <p class="text-xs text-red-400 text-center py-1 font-bold">{{ search_error }}</p>
            {% endif %}

            <!-- সব রেজিস্টার্ড ইউজারের UID লিস্ট -->
            <div class="space-y-2 max-h-56 overflow-y-auto pr-1">
                {% for u in all_users %}
                <div class="bg-slate-800 p-3 rounded-xl border border-slate-700 flex justify-between items-center text-xs">
                    <div>
                        <p class="font-bold text-white">{{ u.name }} <span class="text-amber-300 font-mono">({{ u.user_uid }})</span></p>
                        <p class="text-[10px] text-slate-400">Mobile: {{ u.username }} | Wallet: {{ u.wallet }}৳ | Tokens: 🪙{{ u.tokens }}</p>
                    </div>
                    <a href="/admin/toggle-ban/{{ u.username }}" class="px-3 py-1.5 rounded-lg text-[10px] font-bold {% if u.is_banned %} bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 {% else %} bg-red-500/20 text-red-400 border border-red-500/30 {% endif %}">
                        {{ 'Unban' if u.is_banned else 'Ban' }}
                    </a>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- ২. ক্যাটাগরি ওয়াইজ অর্ডার ম্যানেজমেন্ট -->
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-4 shadow-xl">
            <h2 class="text-sm font-bold text-amber-400 uppercase tracking-wider border-b border-slate-800 pb-2"><i class="fa-solid fa-list-check mr-1.5"></i> Order Management (Category Wise)</h2>

            <!-- ক্যাটাগরি ১: ফ্রি ডায়মন্ড উইথড্র অপশন -->
            <div class="space-y-3 pt-1">
                <div class="flex items-center space-x-2 text-sky-400 font-bold text-xs uppercase">
                    <i class="fa-solid fa-gem text-sm"></i>
                    <h3>1. Free Diamond Store Withdrawals (Token Redeem)</h3>
                </div>
                {% set free_orders = orders | selectattr('service', 'equalto', 'FREE DIAMOND STORE') | list %}
                {% if free_orders %}
                    {% for o in free_orders %}
                    <div class="bg-slate-800/80 p-3.5 rounded-xl border border-sky-500/30 space-y-2">
                        <div class="flex justify-between items-center">
                            <span class="text-xs font-bold text-sky-300">#ORD-{{ o.id }} ({{ o.package }})</span>
                            <span class="text-[10px] px-2.5 py-0.5 rounded-full font-bold {% if o.status == 'Pending' %} bg-amber-500/20 text-amber-400 {% elif o.status == 'Completed' %} bg-emerald-500/20 text-emerald-400 {% else %} bg-red-500/20 text-red-400 {% endif %}">
                                {{ o.status }}
                            </span>
                        </div>
                        <p class="text-xs text-slate-300">User: <strong class="text-white">{{ o.username }}</strong> | Game UID: <strong class="text-amber-300">{{ o.uid }}</strong></p>
                        <p class="text-xs text-slate-300">Deducted Tokens: <strong class="text-amber-400 font-mono">🪙 {{ o.trxid }}</strong></p>
                        {% if o.status == 'Pending' %}
                        <div class="flex space-x-2 pt-1">
                            <a href="/admin/order-action/complete/{{ o.id }}" class="flex-1 bg-emerald-500 text-slate-950 font-bold py-1.5 rounded-lg text-xs text-center">Approve & Send</a>
                            <a href="/admin/order-action/reject/{{ o.id }}" class="flex-1 bg-red-500 text-white font-bold py-1.5 rounded-lg text-xs text-center">Reject</a>
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}
                {% else %}
                    <p class="text-[11px] text-slate-500 italic bg-slate-800/40 p-2.5 rounded-xl">কোনো ফ্রি ডায়মন্ড রিডিম রিকোয়েস্ট নেই।</p>
                {% endif %}
            </div>

            <hr class="border-slate-800">

            <!-- ক্যাটাগরি ২: সরাসরি পেমেন্ট অর্ডার -->
            <div class="space-y-3">
                <div class="flex items-center space-x-2 text-emerald-400 font-bold text-xs uppercase">
                    <i class="fa-solid fa-money-bill-wave text-sm"></i>
                    <h3>2. Direct Payment Orders (bKash / Nagad / Rocket TrxID)</h3>
                </div>
                {% set direct_orders = orders | rejectattr('service', 'equalto', 'FREE DIAMOND STORE') | selectattr('payment', 'ne', 'Wallet') | list %}
                {% if direct_orders %}
                    {% for o in direct_orders %}
                    <div class="bg-slate-800/80 p-3.5 rounded-xl border border-emerald-500/30 space-y-2">
                        <div class="flex justify-between items-center">
                            <span class="text-xs font-bold text-emerald-300">#ORD-{{ o.id }} - {{ o.service }}</span>
                            <span class="text-[10px] px-2.5 py-0.5 rounded-full font-bold {% if o.status == 'Pending' %} bg-amber-500/20 text-amber-400 {% elif o.status == 'Completed' %} bg-emerald-500/20 text-emerald-400 {% else %} bg-red-500/20 text-red-400 {% endif %}">
                                {{ o.status }}
                            </span>
                        </div>
                        <p class="text-xs text-slate-300">User: <strong class="text-white">{{ o.username }}</strong> | Game UID: <strong class="text-white">{{ o.uid }}</strong></p>
                        <p class="text-xs text-slate-300">Package: <strong class="text-white">{{ o.package }}</strong></p>
                        <p class="text-xs text-slate-300">Payment Method: <strong class="text-amber-300">{{ o.payment }} (TrxID: {{ o.trxid }})</strong></p>
                        {% if o.status == 'Pending' %}
                        <div class="flex space-x-2 pt-1">
                            <a href="/admin/order-action/complete/{{ o.id }}" class="flex-1 bg-emerald-500 text-slate-950 font-bold py-1.5 rounded-lg text-xs text-center">Complete</a>
                            <a href="/admin/order-action/reject/{{ o.id }}" class="flex-1 bg-red-500 text-white font-bold py-1.5 rounded-lg text-xs text-center">Reject</a>
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}
                {% else %}
                    <p class="text-[11px] text-slate-500 italic bg-slate-800/40 p-2.5 rounded-xl">কোনো সরাসরি পেমেন্টের অর্ডার নেই।</p>
                {% endif %}
            </div>

            <hr class="border-slate-800">

            <!-- ক্যাটাগরি ৩: ওয়ালেট অর্ডার -->
            <div class="space-y-3">
                <div class="flex items-center space-x-2 text-amber-400 font-bold text-xs uppercase">
                    <i class="fa-solid fa-wallet text-sm"></i>
                    <h3>3. Wallet Balance Paid Orders</h3>
                </div>
                {% set wallet_orders = orders | selectattr('payment', 'equalto', 'Wallet') | list %}
                {% if wallet_orders %}
                    {% for o in wallet_orders %}
                    <div class="bg-slate-800/80 p-3.5 rounded-xl border border-amber-500/30 space-y-2">
                        <div class="flex justify-between items-center">
                            <span class="text-xs font-bold text-amber-300">#ORD-{{ o.id }} - {{ o.service }}</span>
                            <span class="text-[10px] px-2.5 py-0.5 rounded-full font-bold {% if o.status == 'Pending' %} bg-amber-500/20 text-amber-400 {% elif o.status == 'Completed' %} bg-emerald-500/20 text-emerald-400 {% else %} bg-red-500/20 text-red-400 {% endif %}">
                                {{ o.status }}
                            </span>
                        </div>
                        <p class="text-xs text-slate-300">User: <strong class="text-white">{{ o.username }}</strong> | Game UID: <strong class="text-white">{{ o.uid }}</strong></p>
                        <p class="text-xs text-slate-300">Package: <strong class="text-white">{{ o.package }}</strong></p>
                        <p class="text-xs text-slate-300">Paid Status: <strong class="text-emerald-400">Wallet Balance Deducted</strong></p>
                        {% if o.status == 'Pending' %}
                        <div class="flex space-x-2 pt-1">
                            <a href="/admin/order-action/complete/{{ o.id }}" class="flex-1 bg-emerald-500 text-slate-950 font-bold py-1.5 rounded-lg text-xs text-center">Complete</a>
                            <a href="/admin/order-action/reject/{{ o.id }}" class="flex-1 bg-red-500 text-white font-bold py-1.5 rounded-lg text-xs text-center">Reject</a>
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}
                {% else %}
                    <p class="text-[11px] text-slate-500 italic bg-slate-800/40 p-2.5 rounded-xl">কোনো ওয়ালেট ব্যালেন্সের অর্ডার নেই।</p>
                {% endif %}
            </div>
        </div>

        <!-- ৩. ওয়েবসাইট কাস্টমাইজেশন সেকশন -->
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

        <!-- ৪. স্লাইডার ব্যানার সেকশন -->
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-3">
            <h2 class="text-sm font-bold text-sky-400 uppercase tracking-wider"><i class="fa-solid fa-images mr-1"></i> স্লাইডার ব্যানার ম্যানেজার</h2>
            <form action="/admin/add-banner" method="POST" class="space-y-2">
                <input type="text" name="image_url" placeholder="ছবির লিংক (Google Drive / Direct URL)" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-xs text-white">
                <input type="text" name="caption" placeholder="ক্যাপশন (যেমন: ৫০% ডিসকাউন্ট)" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2 text-xs text-white">
                <button type="submit" class="w-full bg-sky-500 text-slate-950 font-bold py-2 rounded-lg text-xs">+ নতুন ব্যানার অ্যাড করুন</button>
            </form>
            <div class="space-y-2 pt-2">
                {% for b in banners %}
                <div class="bg-slate-800 p-2 rounded-xl border border-slate-700 flex justify-between items-center text-xs">
                    <span class="truncate max-w-[200px] text-slate-300">{{ b.caption }}</span>
                    <a href="/admin/delete-banner/{{ b.id }}" class="text-red-400 font-bold hover:underline">Delete</a>
                </div>
                {% endfor %}
            </div>
        </div>

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
        return redirect(url_for('logout'))
    user = users_db[uname]
    if user.get('is_banned'):
        session.pop('user', None)
        return "আপনার অ্যাকাউন্টটি ব্যান করা হয়েছে!"
    return render_template_string(INDEX_TEMPLATE, settings=site_settings, banners=banners_db, wallet_balance=user.get('wallet', 0.0), tokens=user.get('tokens', 0))

@app.route('/spin')
def spin_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    uname = session['user']
    user = users_db.get(uname, {})
    return render_template_string(SPIN_TEMPLATE, message=None, settings=site_settings, tokens=user.get('tokens', 0))

@app.route('/play-spin', methods=['POST'])
def play_spin():
    if 'user' not in session:
        return redirect(url_for('login'))
    uname = session['user']
    user = users_db[uname]
    
    now = datetime.datetime.now()
    last_spin = user.get('last_spin')
    
    if last_spin:
        time_diff = now - last_spin
        if time_diff.total_seconds() < 86400:
            hours_left = int((86400 - time_diff.total_seconds()) // 3600)
            mins_left = int(((86400 - time_diff.total_seconds()) % 3600) // 60)
            msg = f"আজকের স্পিন শেষ! আবার {hours_left} ঘণ্টা {mins_left} মিনিট পর ট্রাই করুন।"
            return render_template_string(SPIN_TEMPLATE, message=msg, settings=site_settings, tokens=user.get('tokens', 0))
            
    win_token = random.choice([50, 100, 200, 500, 1000, 2000])
    user['tokens'] = user.get('tokens', 0) + win_token
    user['last_spin'] = now
    
    msg = f"অভিনন্দন! আপনি চাকা ঘুরে পেয়েছেন 🪙 {win_token} টোকেন বোনাস!"
    return render_template_string(SPIN_TEMPLATE, message=msg, settings=site_settings, tokens=user.get('tokens', 0))

@app.route('/free-diamond')
def free_diamond_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    uname = session['user']
    user = users_db.get(uname, {})
    return render_template_string(FREE_DIAMOND_TEMPLATE, settings=site_settings, tokens=user.get('tokens', 0), msg=None)

@app.route('/redeem-diamond', methods=['POST'])
def redeem_diamond():
    if 'user' not in session:
        return redirect(url_for('login'))
    uname = session['user']
    user = users_db[uname]
    
    rtype = request.form.get('type')
    uid = request.form.get('uid')
    
    needed_tokens = 100000 if rtype == 'weekly' else 500000
    pkg_name = "FREE Weekly Membership" if rtype == 'weekly' else "FREE Monthly Membership"
    
    if user.get('tokens', 0) < needed_tokens:
        msg = f"আপনার পর্যাপ্ত টোকেন নেই! প্রয়োজন {needed_tokens} টোকেন।"
        return render_template_string(FREE_DIAMOND_TEMPLATE, settings=site_settings, tokens=user.get('tokens', 0), msg=msg)
        
    user['tokens'] -= needed_tokens
    
    order_id = len(orders_db) + 1
    now_str = datetime.datetime.now().strftime("%I:%M %p, %d %b")
    order_data = {
        'id': order_id,
        'username': uname,
        'service': 'FREE DIAMOND STORE',
        'uid': uid,
        'package': pkg_name,
        'payment': 'Redeemed Token',
        'trxid': f'{needed_tokens}',
        'status': 'Pending',
        'time': now_str
    }
    orders_db.append(order_data)
    
    msg = f"সফলভাবে {pkg_name} এর জন্য রিডিম রিকোয়েস্ট পাঠানো হয়েছে!"
    return render_template_string(FREE_DIAMOND_TEMPLATE, settings=site_settings, tokens=user.get('tokens', 0), msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        uname = request.form.get('username').strip()
        pwd = request.form.get('password')
        if uname in users_db and users_db[uname].get('password') == pwd:
            if users_db[uname].get('is_banned'):
                error = 'আপনার অ্যাকাউন্টটি ব্যান করা হয়েছে!'
            else:
                session['user'] = uname
                return redirect(url_for('home'))
        else:
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
            generated_uid = f"UID-{random.randint(100000, 999999)}"
            users_db[uname] = {
                'name': name,
                'email': email,
                'username': uname,
                'password': pwd,
                'user_uid': generated_uid,
                'wallet': 0.0,
                'tokens': 0,
                'last_spin': None,
                'is_banned': False
            }
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
        return redirect(url_for('logout'))
    user = users_db[uname]
    
    package_str = request.form.get('package')
    payment_method = request.form.get('payment')
    trxid = request.form.get('trxid', 'N/A')
    promo = request.form.get('promo', '').strip().upper()
    
    discount = 0
    if promo in promo_codes:
        discount = promo_codes[promo]

    if payment_method == 'Wallet':
        try:
            price = float(package_str.split('-')[-1].replace('৳', '').strip())
        except:
            price = 0.0
            
        final_price = max(0, price - discount)
            
        if user.get('wallet', 0.0) < final_price:
            return f"ওয়ালেটে পর্যাপ্ত ব্যালেন্স নেই! প্রয়োজন: {final_price} ৳"
        user['wallet'] -= final_price
        trxid = 'Wallet Paid'

    order_id = len(orders_db) + 1
    now_str = datetime.datetime.now().strftime("%I:%M %p, %d %b")
    order_data = {
        'id': order_id,
        'username': uname,
        'service': request.form.get('service'),
        'uid': request.form.get('uid'),
        'package': package_str,
        'payment': payment_method,
        'trxid': trxid,
        'status': 'Pending',
        'time': now_str
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

@app.route('/settings')
def settings_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    uname = session['user']
    if uname not in users_db:
        return redirect(url_for('logout'))
    u_info = users_db[uname]
    return render_template_string(SETTINGS_TEMPLATE, user=u_info, settings=site_settings)

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
    
    tot_users = len(users_db)
    tot_orders = len(orders_db)
    pend_orders = len([o for o in orders_db if o['status'] == 'Pending'])
    
    return render_template_string(
        ADMIN_DASHBOARD_TEMPLATE, 
        orders=orders_db, 
        add_moneys=add_money_db, 
        banners=banners_db, 
        settings=site_settings,
        promos=promo_codes,
        total_users=tot_users,
        total_orders=tot_orders,
        pending_orders=pend_orders,
        all_users=list(users_db.values()),
        searched_user=None,
        search_error=None
    )

@app.route('/admin/toggle-app-status')
def toggle_app_status():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    site_settings['is_app_off'] = not site_settings.get('is_app_off', False)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/search-user', methods=['POST'])
def search_user():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    s_term = request.form.get('search_term').strip().upper()
    found_u = None
    for u in users_db.values():
        if u.get('user_uid', '').upper() == s_term or u.get('username', '').upper() == s_term:
            found_u = u
            break
            
    tot_users = len(users_db)
    tot_orders = len(orders_db)
    pend_orders = len([o for o in orders_db if o['status'] == 'Pending'])

    return render_template_string(
        ADMIN_DASHBOARD_TEMPLATE, 
        orders=orders_db, 
        add_moneys=add_money_db, 
        banners=banners_db, 
        settings=site_settings,
        promos=promo_codes,
        total_users=tot_users,
        total_orders=tot_orders,
        pending_orders=pend_orders,
        all_users=list(users_db.values()),
        searched_user=found_u,
        search_error=None if found_u else "কোনো ইউজার পাওয়া যায়নি!"
    )

@app.route('/admin/toggle-ban/<uname>')
def toggle_ban(uname):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    if uname in users_db:
        users_db[uname]['is_banned'] = not users_db[uname].get('is_banned', False)
    return redirect(url_for('admin_dashboard'))

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

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
