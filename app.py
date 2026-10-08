from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# তোমার টেলিগ্রাম বট ক্রেডেনশিয়ালস
TELEGRAM_BOT_TOKEN = "8970671481:AAFACF5V3b59JyLbdBNzszEH5VAlyefhLww"
TELEGRAM_ADMIN_CHAT_ID = "8662169982"

def send_telegram_notification(order_details):
    try:
        message = (
            f"🚨 **New Order Received!** 🚨\n\n"
            f"👤 **Service:** {order_details.get('service')}\n"
            f"🎮 **UID/Details:** {order_details.get('uid')}\n"
            f"📦 **Package:** {order_details.get('package')}\n"
            f"💳 **Payment:** {order_details.get('payment')}\n"
            f"💰 **Amount:** {order_details.get('amount')}"
        )
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_ADMIN_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)
    except Exception as e:
        print("Telegram Error:", e)

# সম্পূর্ণ স্টাইলিশ অ্যাপ ডিজাইন (এক ফাইলের মধ্যে)
INDEX_TEMPLATE = """
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

    <!-- Welcome Modal / Notice -->
    <div id="noticeModal" class="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-slate-700 w-full max-w-sm rounded-2xl p-5 text-center shadow-2xl">
            <div class="w-12 h-12 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto mb-3 text-xl">
                <i class="fa-solid fa-bullhorn"></i>
            </div>
            <h3 class="text-lg font-bold text-white mb-2">স্বাগতম Ahad Topup-এ!</h3>
            <p class="text-xs text-slate-300 mb-4">আমাদের অফিশিয়াল টেলিগ্রাম চ্যানেল ও সেটআপ ভিডিও দেখতে নিচের লিঙ্কে জয়েন করুন।</p>
            <a href="https://t.me/ahadtopup" target="_blank" class="block w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 rounded-xl text-sm mb-2 transition">
                <i class="fa-brands fa-telegram mr-1.5"></i> Telegram Channel
            </a>
            <button onclick="closeNotice()" class="w-full bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold py-2 rounded-xl text-xs transition">
                CLOSE & CONTINUE
            </button>
        </div>
    </div>

    <!-- Top Header -->
    <header class="flex justify-between items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <span class="text-xl font-bold tracking-wider text-emerald-400">AHAD TOPUP</span>
        <div class="flex items-center space-x-3">
            <div class="flex items-center bg-emerald-600/20 border border-emerald-500/50 px-3 py-1.5 rounded-full">
                <i class="fa-solid fa-wallet text-emerald-400 mr-1.5"></i>
                <span class="text-sm font-semibold text-emerald-300">0 ৳</span>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="p-4 max-w-md mx-auto">
        <div class="w-full h-36 bg-slate-800 rounded-xl mb-6 relative border border-slate-700 flex items-center justify-center overflow-hidden">
            <div class="text-center p-4">
                <i class="fa-solid fa-fire text-amber-500 text-3xl mb-1"></i>
                <p class="text-sm font-medium text-slate-300">ফ্রি ফায়ার ইনস্ট্যান্ট অটো টপ-আপ প্ল্যাটফর্ম</p>
            </div>
        </div>

        <h2 class="text-center font-bold tracking-wider text-slate-200 mb-4 text-lg border-b border-slate-800 pb-2">REGULAR TOPUP</h2>

        <!-- Cards matching exact categories -->
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

    <!-- Floating Circular Support Button -->
    <a href="https://t.me/ahahackr" target="_blank" class="fixed bottom-20 right-4 w-14 h-14 bg-blue-500 text-white rounded-full flex items-center justify-center shadow-xl shadow-blue-500/40 z-50 hover:bg-blue-600 transition">
        <i class="fa-brands fa-telegram text-2xl"></i>
    </a>

    <!-- Bottom Navigation Bar -->
    <nav class="fixed bottom-0 left-0 right-0 bg-slate-900 border-t border-slate-800 flex justify-around items-center h-16 z-40 max-w-md mx-auto">
        <a href="/" class="flex flex-col items-center text-emerald-400">
            <i class="fa-solid fa-house text-lg"></i>
            <span class="text-[10px] mt-1 font-medium">Home</span>
        </a>
        <a href="#" class="flex flex-col items-center text-slate-400">
            <i class="fa-solid fa-bag-shopping text-lg"></i>
            <span class="text-[10px] mt-1 font-medium">My Orders</span>
        </a>
        <a href="#" class="flex flex-col items-center -mt-5">
            <div class="w-14 h-14 bg-emerald-500 rounded-full flex items-center justify-center shadow-lg shadow-emerald-500/30 text-slate-950 border-4 border-slate-900">
                <i class="fa-solid fa-plus text-xl font-bold"></i>
            </div>
            <span class="text-[10px] mt-1 font-medium text-slate-300">Add Money</span>
        </a>
        <a href="#" class="flex flex-col items-center text-slate-400">
            <i class="fa-solid fa-code text-lg"></i>
            <span class="text-[10px] mt-1 font-medium">My Codes</span>
        </a>
        <a href="#" class="flex flex-col items-center text-slate-400">
            <i class="fa-solid fa-user text-lg"></i>
            <span class="text-[10px] mt-1 font-medium">My Account</span>
        </a>
    </nav>

    <script>
        function closeNotice() {
            document.getElementById('noticeModal').style.display = 'none';
        }
    </script>
</body>
</html>
"""

ORDER_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Ahad Topup</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; }
        .package-card { background: #1e293b; border: 2px solid #334155; }
        .package-card.selected { border-color: #10b981; background: rgba(16, 185, 129, 0.1); }
    </style>
</head>
<body class="pb-20">
    <header class="flex items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
        <a href="/" class="text-slate-300 mr-4 text-lg"><i class="fa-solid fa-arrow-left"></i></a>
        <h1 class="text-base font-bold uppercase tracking-wider text-slate-200">{{ title }}</h1>
    </header>

    <form action="/submit-order" method="POST" class="p-4 max-w-md mx-auto space-y-5">
        <input type="hidden" name="service" value="{{ title }}">
        
        <!-- UID / Input Box -->
        <div class="bg-slate-900 p-4 rounded-xl border border-slate-800">
            <label class="block text-xs font-semibold text-slate-400 mb-2">
                {% if 'Like' in title %}ENTER PLAYER UID OR PROFILE LINK{% else %}ENTER PLAYER UID{% endif %}
            </label>
            <input type="text" name="uid" required placeholder="Enter here..." class="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-emerald-500">
        </div>

        <!-- Specific Packages based on Category -->
        <div>
            <label class="block text-xs font-semibold text-slate-400 mb-2">SELECT PACKAGE</label>
            <div class="grid grid-cols-2 gap-3">
                {% for pkg, price in packages.items() %}
                <div onclick="selectPackage(this, '{{ pkg }} - {{ price }}')" class="package-card p-3 rounded-xl cursor-pointer text-center transition">
                    <p class="text-sm font-bold text-white">{{ pkg }}</p>
                    <p class="text-xs text-emerald-400 font-semibold mt-1">{{ price }}</p>
                </div>
                {% endfor %}
            </div>
            <input type="hidden" name="package" id="selectedPackageInput" required>
        </div>

        <!-- Payment Method -->
        <div>
            <label class="block text-xs font-semibold text-slate-400 mb-2">SELECT PAYMENT</label>
            <div class="grid grid-cols-3 gap-3">
                <button type="button" onclick="selectPayment(this, 'bKash')" class="pay-btn bg-slate-900 border border-slate-700 p-3 rounded-xl text-center text-xs font-bold text-pink-500 transition">bKash</button>
                <button type="button" onclick="selectPayment(this, 'Nagad')" class="pay-btn bg-slate-900 border border-slate-700 p-3 rounded-xl text-center text-xs font-bold text-orange-500 transition">Nagad</button>
                <button type="button" onclick="selectPayment(this, 'Rocket')" class="pay-btn bg-slate-900 border border-slate-700 p-3 rounded-xl text-center text-xs font-bold text-purple-500 transition">Rocket</button>
            </div>
            <input type="hidden" name="payment" id="selectedPaymentInput" required>
        </div>

        <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold py-3.5 rounded-xl shadow-lg shadow-emerald-500/25 transition mt-4">
            ORDER NOW
        </button>
    </form>

    <!-- Floating Circular Support Button -->
    <a href="https://t.me/ahahackr" target="_blank" class="fixed bottom-6 right-4 w-14 h-14 bg-blue-500 text-white rounded-full flex items-center justify-center shadow-xl shadow-blue-500/40 z-50 hover:bg-blue-600 transition">
        <i class="fa-brands fa-telegram text-2xl"></i>
    </a>

    <script>
        function selectPackage(element, pkgName) {
            document.querySelectorAll('.package-card').forEach(card => card.classList.remove('selected'));
            element.classList.add('selected');
            document.getElementById('selectedPackageInput').value = pkgName;
        }

        function selectPayment(element, method) {
            document.querySelectorAll('.pay-btn').forEach(btn => btn.style.borderColor = '#334155');
            element.style.borderColor = '#10b981';
            document.getElementById('selectedPaymentInput').value = method;
        }
    </script>
</body>
</html>
"""

SUCCESS_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order Success</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style> body { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; } </style>
</head>
<body class="flex items-center justify-center min-h-screen p-4">
    <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl text-center max-w-sm w-full shadow-2xl">
        <div class="w-16 h-16 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto mb-4 text-3xl">
            <i class="fa-solid fa-check"></i>
        </div>
        <h2 class="text-xl font-bold text-white mb-2">অর্ডার সফল হয়েছে!</h2>
        <p class="text-xs text-slate-300 mb-6">আপনার অর্ডারটি রিসিভ করা হয়েছে এবং টেলিগ্রাম বটে নোটিফিকেশন পাঠানো হয়েছে। খুব শীঘ্রই প্রসেস করা হবে।</p>
        <a href="/" class="block w-full bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold py-3 rounded-xl text-sm transition">
            BACK TO HOME
        </a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(INDEX_TEMPLATE)

@app.route('/order/<service_type>')
def order_page(service_type):
    # নির্দিষ্ট সার্ভিস অনুযায়ী আলাদা আলাদা প্যাকেজ লিস্ট
    services = {
        'ff-likes': {
            'title': 'FF Likes',
            'packages': {'100 Likes': '30 ৳', '500 Likes': '130 ৳', '1000 Likes': '250 ৳', '2000 Likes': '480 ৳'}
        },
        'uid-topup': {
            'title': 'UID Topup',
            'packages': {'100 Diamonds': '85 ৳', '310 Diamonds': '250 ৳', '520 Diamonds': '410 ৳', '1060 Diamonds': '820 ৳'}
        },
        'unipin': {
            'title': 'Unipin Voucher',
            'packages': {'Unipin 50 BDT': '50 ৳', 'Unipin 100 BDT': '100 ৳', 'Unipin 500 BDT': '490 ৳'}
        },
        'weekly-monthly': {
            'title': 'Weekly Monthly',
            'packages': {'Weekly Membership': '165 ৳', 'Monthly Membership': '520 ৳', 'Weekly + Monthly': '680 ৳'}
        },
        'level-up': {
            'title': 'Level Up Pass',
            'packages': {'Level Up Pass': '95 ৳'}
        },
        'weekly-lite': {
            'title': 'Weekly Lite',
            'packages': {'Weekly Lite Pass': '80 ৳'}
        }
    }
    
    data = services.get(service_type, {'title': 'Topup Service', 'packages': {'Standard Pack': '100 ৳'}})
    return render_template_string(ORDER_TEMPLATE, title=data['title'], packages=data['packages'])

@app.route('/submit-order', methods=['POST'])
def submit_order():
    service = request.form.get('service')
    uid = request.form.get('uid')
    package = request.form.get('package')
    payment = request.form.get('payment')
    
    order_data = {
        'service': service,
        'uid': uid,
        'package': package,
        'payment': payment,
        'amount': package.split(' - ')[-1] if ' - ' in package else 'N/A'
    }
    
    # টেলিগ্রাম বটে নোটিফিকেশন পাঠানো
    send_telegram_notification(order_data)
    
    return render_template_string(SUCCESS_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
