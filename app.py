from flask import Flask, render_template_string

app = Flask(__name__)

# সম্পূর্ণ হোমপেজ ও অর্ডার পেজের এইচটিএমএল ডিজাইন একসাথে
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
    <!-- Top Header -->
    <header class="flex justify-between items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-50">
        <div class="flex items-center space-x-2">
            <span class="text-xl font-bold tracking-wider text-emerald-400">AHAD TOPUP</span>
        </div>
        <div class="flex items-center space-x-3">
            <div class="flex items-center bg-emerald-600/20 border border-emerald-500/50 px-3 py-1.5 rounded-full">
                <i class="fa-solid fa-wallet text-emerald-400 mr-1.5"></i>
                <span class="text-sm font-semibold text-emerald-300">0 ৳</span>
            </div>
            <div class="w-9 h-9 bg-slate-800 border border-slate-700 rounded-full flex items-center justify-center text-slate-300">
                <i class="fa-solid fa-user text-sm"></i>
            </div>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="p-4 max-w-md mx-auto">
        <div class="w-full h-36 bg-slate-800 rounded-xl mb-6 overflow-hidden relative border border-slate-700 flex items-center justify-center">
            <div class="text-center">
                <i class="fa-solid fa-fire text-amber-500 text-3xl mb-1"></i>
                <p class="text-sm font-medium text-slate-300">স্পেশাল অফার ও ডিসকাউন্ট!</p>
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

    <!-- Bottom Navigation Bar -->
    <nav class="fixed bottom-0 left-0 right-0 bg-slate-900 border-t border-slate-800 flex justify-around items-center h-16 z-50 max-w-md mx-auto">
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
</body>
</html>
"""

ORDER_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order - Ahad Topup</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: sans-serif; }
        .package-card { background: #1e293b; border: 2px solid #334155; }
        .package-card.selected { border-color: #10b981; background: rgba(16, 185, 129, 0.1); }
    </style>
</head>
<body class="pb-20">
    <header class="flex items-center p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-50">
        <a href="/" class="text-slate-300 mr-4 text-lg"><i class="fa-solid fa-arrow-left"></i></a>
        <h1 class="text-base font-bold uppercase tracking-wider text-slate-200">{{ title }}</h1>
    </header>

    <div class="p-4 max-w-md mx-auto space-y-5">
        <div class="bg-slate-900 p-4 rounded-xl border border-slate-800">
            <label class="block text-xs font-semibold text-slate-400 mb-2">ENTER PLAYER UID</label>
            <input type="text" placeholder="Enter your Free Fire UID" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-emerald-500">
        </div>

        <div>
            <label class="block text-xs font-semibold text-slate-400 mb-2">SELECT PACKAGE</label>
            <div class="grid grid-cols-2 gap-3">
                <div onclick="selectPackage(this)" class="package-card p-3 rounded-xl cursor-pointer text-center transition">
                    <p class="text-sm font-bold text-white">100 Diamonds</p>
                    <p class="text-xs text-emerald-400 font-semibold mt-1">85 ৳</p>
                </div>
                <div onclick="selectPackage(this)" class="package-card p-3 rounded-xl cursor-pointer text-center transition">
                    <p class="text-sm font-bold text-white">310 Diamonds</p>
                    <p class="text-xs text-emerald-400 font-semibold mt-1">250 ৳</p>
                </div>
                <div onclick="selectPackage(this)" class="package-card p-3 rounded-xl cursor-pointer text-center transition">
                    <p class="text-sm font-bold text-white">520 Diamonds</p>
                    <p class="text-xs text-emerald-400 font-semibold mt-1">410 ৳</p>
                </div>
                <div onclick="selectPackage(this)" class="package-card p-3 rounded-xl cursor-pointer text-center transition">
                    <p class="text-sm font-bold text-white">Weekly Membership</p>
                    <p class="text-xs text-emerald-400 font-semibold mt-1">165 ৳</p>
                </div>
            </div>
        </div>

        <div>
            <label class="block text-xs font-semibold text-slate-400 mb-2">SELECT PAYMENT</label>
            <div class="grid grid-cols-3 gap-3">
                <button class="bg-slate-900 border border-slate-700 p-3 rounded-xl text-center text-xs font-bold text-pink-500 hover:border-pink-500 transition">bKash</button>
                <button class="bg-slate-900 border border-slate-700 p-3 rounded-xl text-center text-xs font-bold text-orange-500 hover:border-orange-500 transition">Nagad</button>
                <button class="bg-slate-900 border border-slate-700 p-3 rounded-xl text-center text-xs font-bold text-purple-500 hover:border-purple-500 transition">Rocket</button>
            </div>
        </div>

        <button class="w-full bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold py-3.5 rounded-xl shadow-lg shadow-emerald-500/20 transition mt-4">
            ORDER NOW
        </button>
    </div>

    <script>
        function selectPackage(element) {
            document.querySelectorAll('.package-card').forEach(card => card.classList.remove('selected'));
            element.classList.add('selected');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(INDEX_TEMPLATE)

@app.route('/order/<service_type>')
def order_page(service_type):
    titles = {
        'ff-likes': 'FF Likes Order',
        'uid-topup': 'UID Topup',
        'unipin': 'Unipin Voucher',
        'weekly-monthly': 'Weekly & Monthly Offer',
        'level-up': 'Level Up Pass',
        'weekly-lite': 'Weekly Lite'
    }
    title = titles.get(service_type, 'Topup Service')
    return render_template_string(ORDER_TEMPLATE, title=title)

if __name__ == '__main__':
    app.run(debug=True)
