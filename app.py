from flask import Flask, render_template_string, request, redirect, url_for, session
import datetime

app = Flask(__name__)
app.secret_key = 'ahad_topup_secret_key_secure'

# ডেমো ডাটাবেজ
users_db = {}
orders_db = []

# ডিফল্ট ওয়েবসাইট সেটিংস (যা অ্যাডমিন প্যানেল থেকে পরিবর্তন করা যাবে)
site_settings = {
    "site_title": "AHAD TOPUP",
    "banner_text": "ফ্রি ফায়ার ইনস্ট্যান্ট অটো টপ-আপ",
    "payment_number": "01727246581"
}

# অ্যাডমিন ক্রেডেনশিয়াল
ADMIN_USERNAME = "ahadadmin"
ADMIN_PASSWORD = "123"

# HTML Templates
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
    <header class="flex justify-between items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <span class="text-xl font-bold tracking-wider text-emerald-400">{{ settings.site_title }}</span>
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
                <p class="text-sm font-medium text-slate-300">{{ settings.banner_text }}</p>
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
""" + BOTTOM_NAV

ORDER_TEMPLATE = BASE_HEAD + """
    <header class="flex items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <a href="/" class="text-slate-300 mr-4 text-lg"><i class="fa-solid fa-arrow-left"></i></a>
        <h1 class="text-base font-bold uppercase tracking-wider text-slate-200">{{ title }}</h1>
    </header>

    <form action="/submit-order" method="POST" class="p-4 max-w-md mx-auto space-y-4">
        <input type="hidden" name="service" value="{{ title }}">
        
        <div class="bg-amber-500/10 border border-amber-500/40 p-3.5 rounded-xl space-y-2">
            <div class="flex items-center text-amber-400 font-bold text-xs">
                <i class="fa-solid fa-triangle-exclamation mr-1.5 text-sm"></i> গুরুত্বপূর্ণ নিয়মাবলী ও শর্তাবলি:
            </div>
            <ul class="text-[11px] text-slate-300 space-y-1 list-disc list-inside">
                <li>অবশ্যම সঠিক <strong>Player UID</strong> প্রদান করুন।</li>
                <li>ভুয়া বা ভুল UID অথবা ভুয়া TrxID প্রদান করলে আপনার অ্যাকাউন্ট <strong>চিরতরে ব্যান</strong> হতে পারে।</li>
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
                <button type="button" onclick="selectPayment(this, 'bKash', '{{ settings.payment_number }} (Personal)')" class="pay-btn bg-slate-900 border border-slate-700 p-3 rounded-xl text-center text-xs font-bold text-pink-500">bKash</button>
                <button type="button" onclick="selectPayment(this, 'Nagad', '{{ settings.payment_number }} (Personal)')" class="pay-btn bg-slate-900 border border-slate-700 p-3 rounded-xl text-center text-xs font-bold text-orange-500">Nagad</button>
                <button type="button" onclick="selectPayment(this, 'Rocket', '{{ settings.payment_number }} (Personal)')" class="pay-btn bg-slate-900 border border-slate-700 p-3 rounded-xl text-center text-xs font-bold text-purple-500">Rocket</button>
            </div>
            <input type="hidden" name="payment" id="selectedPaymentInput" required>
        </div>

        <div id="paymentBox" class="hidden bg-slate-900 p-4 rounded-xl border border-emerald-500/50 space-y-3">
            <p class="text-xs text-slate-300">Send money to this number: <strong id="merchantNum" class="text-emerald-400"></strong></p>
            <div>
                <label class="block text-xs font-semibold text-slate-400 mb-1">TRANSACTION ID (TrxID)</label>
                <input type="text" name="trxid" required placeholder="Enter TrxID" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-emerald-500">
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
            <h2 class="text-xl font-bold text-center text-emerald-400 mb-1">{{ settings.site_title }}</h2>
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

# আপডেট করা অ্যাডমিন ড্যাশবোর্ড টেমপ্লেট (যেখানে ওয়েবসাইট এডিট করার সেটিংসও থাকবে)
ADMIN_DASHBOARD_TEMPLATE = BASE_HEAD + """
    <header class="flex justify-between items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <span class="text-xl font-bold tracking-wider text-amber-400">ADMIN DASHBOARD</span>
        <a href="/admin/logout" class="bg-red-500/20 border border-red-500/40 text-red-400 px-3 py-1.5 rounded-lg text-xs font-bold">Logout</a>
    </header>

    <main class="p-4 max-w-2xl mx-auto space-y-6">
        <!-- ওয়েবসাইট সেটিংস এডিট ফর্ম -->
        <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-4 shadow-xl">
            <h2 class="text-sm font-bold text-amber-400 uppercase tracking-wider"><i class="fa-solid fa-gears mr-1.5"></i> Website Settings (কাস্টমাইজেশন)</h2>
            <form action="/admin/update-settings" method="POST" class="space-y-3">
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">Website Title</label>
                    <input type="text" name="site_title" value="{{ settings.site_title }}" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-amber-500">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">Banner Notice Text</label>
                    <input type="text" name="banner_text" value="{{ settings.banner_text }}" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-amber-500">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">Payment / Personal Number (Bkash/Nagad/Rocket)</label>
                    <input type="text" name="payment_number" value="{{ settings.payment_number }}" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-amber-500">
                </div>
                <button type="submit" class="w-full bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold py-2.5 rounded-xl text-xs transition">
                    UPDATE WEBSITE SETTINGS
                </button>
            </form>
        </div>

        <h2 class="text-sm font-bold text-slate-400 uppercase tracking-wider">All User Orders</h2>
        
        {% if orders %}
            {% for o in orders %}
            <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-3">
                <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-emerald-400">Order #{{ o.id }} - {{ o.service }}</span>
                    <span class="text-xs px-2.5 py-1 rounded-full font-bold 
                        {% if o.status == 'Pending' %} bg-amber-500/20 text-amber-400 border border-amber-500/30
                        {% elif o.status == 'Completed' %} bg-emerald-500/20 text-emerald-400 border border-emerald-500/30
                        {% else %} bg-red-500/20 text-red-400 border border-red-500/30 {% endif %}">
                        {{ o.status }}
                    </span>
                </div>
                <div class="grid grid-cols-2 gap-2 text-xs text-slate-300 bg-slate-800/50 p-2.5 rounded-lg border border-slate-800">
                    <p>User: <strong class="text-white">{{ o.username }}</strong></p>
                    <p>UID: <strong class="text-white">{{ o.uid }}</strong></p>
                    <p>Package: <strong class="text-white">{{ o.package }}</strong></p>
                    <p>TrxID: <strong class="text-amber-400">{{ o.trxid }}</strong></p>
                </div>
                
                {% if o.status == 'Pending' %}
                <div class="flex space-x-2 pt-1">
                    <a href="/admin/action/complete/{{ o.id }}" class="flex-1 bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold py-2 rounded-lg text-xs text-center transition">
                        <i class="fa-solid fa-check mr-1"></i> Complete
                    </a>
                    <a href="/admin/action/reject/{{ o.id }}" class="flex-1 bg-red-500 hover:bg-red-600 text-white font-bold py-2 rounded-lg text-xs text-center transition">
                        <i class="fa-solid fa-xmark mr-1"></i> Reject
                    </a>
                </div>
                {% endif %}
            </div>
            {% endfor %}
        {% else %}
            <div class="text-center py-10 text-slate-500">
                <i class="fa-solid fa-folder-open text-4xl mb-2"></i>
                <p class="text-sm">কোনো অর্ডার জমা হয়নি!</p>
            </div>
        {% endif %}
    </main>
"""

ADMIN_LOGIN_TEMPLATE = BASE_HEAD + """
    <div class="flex items-center justify-center min-h-screen p-4">
        <div class="bg-slate-900 border border-slate-800 w-full max-w-sm rounded-2xl p-6 shadow-2xl">
            <h2 class="text-xl font-bold text-center text-amber-400 mb-1">ADMIN LOGIN</h2>
            <p class="text-xs text-center text-slate-400 mb-6">অ্যাডমিন প্যানেলে প্রবেশ করুন</p>
            
            {% if error %}
            <div class="bg-red-500/20 border border-red-500 text-red-300 text-xs p-3 rounded-xl mb-4 text-center">{{ error }}</div>
            {% endif %}

            <form method="POST" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">ADMIN USERNAME</label>
                    <input type="text" name="username" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-amber-500">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">PASSWORD</label>
                    <input type="password" name="password" required class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-amber-500">
                </div>

                <button type="submit" class="w-full bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold py-3 rounded-xl text-sm transition">
                    LOGIN TO DASHBOARD
                </button>
            </form>
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
            users_db[uname] = {
                'name': name,
                'email': email,
                'username': uname,
                'password': pwd,
                'joined_date': datetime.datetime.now().strftime("%d %B, %Y")
            }
            session['user'] = uname
            return redirect(url_for('home'))
    return render_template_string(AUTH_TEMPLATE, is_signup=True, error=error, settings=site_settings)

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
    return render_template_string(ORDER_TEMPLATE, title=data['title'], packages=data['packages'], settings=site_settings)

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
    return redirect(url_for('my_orders'))

@app.route('/orders')
def my_orders():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_orders = [o for o in orders_db if o['username'] == session['user']]
    return render_template_string(ORDERS_TEMPLATE, orders=user_orders, settings=site_settings)

@app.route('/account')
def account():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_info = users_db.get(session['user'], {'name': 'User', 'username': session['user'], 'joined_date': 'Today'})
    return render_template_string(ACCOUNT_TEMPLATE, user=user_info, settings=site_settings)

# --- অ্যাডমিন প্যানেল রাউটসমূহ ---
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        uname = request.form.get('username').strip()
        pwd = request.form.get('password')
        if uname == ADMIN_USERNAME and pwd == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        error = 'ভুল অ্যাডমিন ইউজারনেম বা পাসওয়ার্ড!'
    return render_template_string(ADMIN_LOGIN_TEMPLATE, error=error, settings=site_settings)

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    return render_template_string(ADMIN_DASHBOARD_TEMPLATE, orders=orders_db, settings=site_settings)

@app.route('/admin/update-settings', methods=['POST'])
def update_settings():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    site_settings['site_title'] = request.form.get('site_title').strip()
    site_settings['banner_text'] = request.form.get('banner_text').strip()
    site_settings['payment_number'] = request.form.get('payment_number').strip()
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/action/<action_type>/<int:order_id>')
def admin_action(action_type, order_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    for o in orders_db:
        if o['id'] == order_id:
            if action_type == 'complete':
                o['status'] = 'Completed'
            elif action_type == 'reject':
                o['status'] = 'Rejected'
            break
            
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
