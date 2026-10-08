from flask import Flask, render_template_string, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "ahad_topup_secret_key_super_secure"

# টেলিগ্রাম বট তথ্য
TELEGRAM_BOT_TOKEN = "8970671481:AAFAC5V3b59JyLbdBlizsEh5VA"
TELEGRAM_CHAT_ID = "8662160082"
TELEGRAM_SUPPORT = "https://t.me/ahadtopup"
TELEGRAM_CHANNEL = "https://t.me/ahadtopup"
TUTORIAL_VIDEO_LINK = "https://t.me/ahadtopup"  # এখানে তোমার ভিডিও বা চ্যানেলের লিংক থাকবে
BKASH_NUMBER = "01727246581"

# মেমোরি ডাটাবেজ (অর্ডার হিস্টরি সংরক্ষণের জন্য)
orders_db = []
order_counter = 1001

def send_telegram_order(order_id, player_id, category, package, txid):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        msg = (
            f"🔥 *AHAD TOPUP - NEW ORDER* 🔥\n\n"
            f"🆔 *Order ID:* #{order_id}\n"
            f"📂 *Category:* {category}\n"
            f"📦 *Package:* {package}\n"
            f"🎮 *Player UID:* `{player_id}`\n"
            f"💸 *TrxID:* `{txid}`\n"
            f"📱 *bKash No:* {BKASH_NUMBER}\n\n"
            f"⚠️ স্ট্যাটাস: পেন্ডিং (Pending)"
        )
        payload = {
            "chat_id": TELEGRAM_CHAT_ID, 
            "text": msg, 
            "parse_mode": "Markdown",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {"text": "✅ Approve & Send Diamond", "callback_data": f"approve_{order_id}"},
                        {"text": "❌ Reject", "callback_data": f"reject_{order_id}"}
                    ]
                ]
            }
        }
        res = requests.post(url, json=payload, timeout=5)
        print("Telegram Response:", res.text)
    except Exception as e:
        print("Telegram Error:", e)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ahad Topup - Premium Free Fire Shop</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #05070a; margin: 0; padding-bottom: 90px; color: #fff; }
        .header { background: linear-gradient(135deg, #0f172a, #1e1b4b); padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #dc2626; position: sticky; top: 0; z-index: 100; box-shadow: 0 4px 20px rgba(220, 38, 38, 0.3); }
        .logo { font-size: 20px; font-weight: bold; color: #fff; display: flex; align-items: center; gap: 8px; }
        .logo span { color: #dc2626; text-shadow: 0 0 10px rgba(220,38,38,0.8); }
        .support-btn { background: linear-gradient(45deg, #dc2626, #ef4444); color: #fff; padding: 6px 14px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 13px; box-shadow: 0 0 10px rgba(220,38,38,0.5); }
        
        /* Modal Popup Styling */
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); display: flex; justify-content: center; align-items: center; z-index: 9999; }
        .modal-box { background: #0f172a; border: 2px solid #dc2626; width: 85%; max-width: 350px; padding: 22px; border-radius: 14px; text-align: center; box-shadow: 0 0 30px rgba(220,38,38,0.5); }
        .modal-title { color: #ef4444; font-size: 18px; font-weight: bold; margin-bottom: 10px; text-transform: uppercase; }
        .modal-desc { font-size: 13px; color: #cbd5e1; margin-bottom: 15px; line-height: 1.6; }
        .tutorial-link { display: inline-block; color: #00ff88; font-weight: bold; font-size: 13px; margin-bottom: 15px; text-decoration: underline; }
        .modal-btn { background: linear-gradient(45deg, #dc2626, #ef4444); color: #fff; border: none; padding: 11px 20px; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%; font-size: 14px; box-shadow: 0 0 15px rgba(220,38,38,0.6); }

        /* Banner Slider */
        .slider-container { position: relative; width: 100%; height: 210px; overflow: hidden; background: #0f172a; border-bottom: 2px solid #1e293b; }
        .slide { position: absolute; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out; background-size: cover; background-position: center; }
        .slide.active { opacity: 1; }
        .banner-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, rgba(5,7,10,0.3), rgba(5,7,10,0.95)); display: flex; align-items: flex-end; padding: 15px; box-sizing: border-box; }
        .banner-tag { background: #dc2626; color: #fff; padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; text-transform: uppercase; box-shadow: 0 0 10px rgba(220,38,38,0.8); }

        .section-title { font-size: 15px; font-weight: bold; color: #ef4444; margin: 18px 16px 10px; text-transform: uppercase; letter-spacing: 1px; display: flex; align-items: center; gap: 6px; }
        
        /* Category Grid */
        .cat-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; padding: 0 16px; margin-bottom: 15px; }
        .cat-card { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 14px; text-align: center; cursor: pointer; transition: 0.3s; text-decoration: none; color: #fff; display: flex; flex-direction: column; align-items: center; gap: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.4); }
        .cat-card:hover { border-color: #dc2626; background: #162032; transform: translateY(-2px); box-shadow: 0 0 15px rgba(220,38,38,0.3); }
        .cat-card img { width: 55px; height: 55px; object-fit: cover; border-radius: 50%; border: 2px solid #dc2626; box-shadow: 0 0 10px rgba(220,38,38,0.5); }
        .cat-name { font-size: 13px; font-weight: bold; color: #f3f4f6; }

        /* Form Box */
        .form-box { background: #0f172a; margin: 0 16px 20px; padding: 20px; border-radius: 14px; border: 1px solid #1e293b; box-shadow: 0 6px 20px rgba(0,0,0,0.6); }
        .form-box label { font-size: 13px; font-weight: bold; display: block; margin-bottom: 6px; color: #ef4444; }
        .form-box input, .form-box select { width: 100%; padding: 12px; background: #05070a; border: 1px solid #334155; color: #fff; border-radius: 8px; font-size: 14px; box-sizing: border-box; margin-bottom: 14px; }
        .form-box input:focus, .form-box select:focus { border-color: #dc2626; outline: none; box-shadow: 0 0 8px rgba(220,38,38,0.4); }
        .check-btn { background: linear-gradient(45deg, #dc2626, #ef4444); color: #fff; width: 100%; padding: 13px; border: none; border-radius: 8px; font-weight: bold; font-size: 15px; cursor: pointer; text-transform: uppercase; box-shadow: 0 0 15px rgba(220,38,38,0.5); transition: 0.2s; }
        .check-btn:hover { opacity: 0.9; }

        /* History Section */
        .history-box { background: #0f172a; margin: 0 16px 20px; border-radius: 14px; border: 1px solid #1e293b; padding: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.4); }
        .history-item { background: #05070a; border: 1px solid #1e293b; padding: 12px; border-radius: 8px; margin-bottom: 10px; font-size: 13px; }
        .status-pending { color: #facc15; font-weight: bold; }
        .status-success { color: #22c55e; font-weight: bold; }

        .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: #0f172a; border-top: 2px solid #1e293b; display: flex; justify-content: space-around; padding: 9px 0; z-index: 100; box-shadow: 0 -4px 15px rgba(0,0,0,0.5); }
        .nav-item { text-decoration: none; color: #94a3b8; font-size: 11px; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 3px; cursor: pointer; }
        .nav-item.active { color: #ef4444; font-weight: bold; }
        .nav-item svg { width: 20px; height: 20px; fill: currentColor; }
    </style>
</head>
<body>

    <!-- Age Warning & Tutorial Modal -->
    <div class="modal-overlay" id="warningModal">
        <div class="modal-box">
            <div class="modal-title">⚠️ সতর্কবার্তা (Warning)</div>
            <div class="modal-desc">বাচ্চারা ১৮ বছরের নিচে টপ-আপ করা নিষেধ এবং এটি সম্পূর্ণ বেআইনি। আপনি কি ১৮ বছরের উর্ধ্বে?</div>
            <a href="{{ tutorial_link }}" target="_blank" class="tutorial-link">📺 কিভাবে টপআপ করবেন? ভিডিও দেখতে এখানে ক্লিক করুন</a>
            <button class="modal-btn" onclick="closeModal()">হ্যাঁ, আমার বয়স ১৮+</button>
        </div>
    </div>

    <div class="header">
        <div class="logo"><span><b>AHAD</b></span>TOPUP</div>
        <a href="{{ telegram_support }}" class="support-btn" target="_blank">Support</a>
    </div>

    <!-- FF Character Banners -->
    <div class="slider-container">
        <div class="slide active" style="background-image: linear-gradient(rgba(5,7,10,0.3), rgba(5,7,10,0.9)), url('https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600');">
            <div class="banner-overlay"><div class="banner-tag">🔥 Free Fire Red G-Lock Special</div></div>
        </div>
        <div class="slide" style="background-image: linear-gradient(rgba(5,7,10,0.3), rgba(5,7,10,0.9)), url('https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=600');">
            <div class="banner-overlay"><div class="banner-tag">⚡ Weekly & Monthly Mega Discount</div></div>
        </div>
    </div>

    <div id="homeSection">
        <div class="section-title">⚡ প্রিমি엄 ক্যাটাগরি (Topup Categories)</div>
        
        <div class="cat-grid">
            <div class="cat-card" onclick="selectCat('Weekly Offer')">
                <img src="https://images.unsplash.com/photo-1542751371-adc38448a05e?w=150" alt="Weekly">
                <div class="cat-name">উইকলি অফার (Weekly)</div>
            </div>
            <div class="cat-card" onclick="selectCat('Monthly Offer')">
                <img src="https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=150" alt="Monthly">
                <div class="cat-name">মান্থলি অফার (Monthly)</div>
            </div>
            <div class="cat-card" onclick="selectCat('UID Topup')">
                <img src="https://images.unsplash.com/photo-1511512578047-dfb367046420?w=150" alt="UID">
                <div class="cat-name">প্লেয়ার ইউআইডি (UID Topup)</div>
            </div>
            <div class="cat-card" onclick="selectCat('Level Up Pass')">
                <img src="https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=150" alt="Level Up">
                <div class="cat-name">লেভেল আপ পাস (Level Up)</div>
            </div>
        </div>

        <div class="form-box">
            <label>💎 টপ-আপ অর্ডার ও পেমেন্ট ফর্ম</label>
            {% if success_msg %}
                <p style="color: #22c55e; font-weight: bold; font-size: 13px; background: rgba(34,197,94,0.1); padding: 10px; border-radius: 6px; border: 1px solid #22c55e; margin-bottom: 14px;">{{ success_msg }}</p>
            {% endif %}
            <form method="POST">
                <label>সিলেক্টেড ক্যাটাগরি:</label>
                <input type="text" id="selectedCategory" name="category" value="Weekly Offer" readonly style="color: #ef4444; font-weight: bold;">
                
                <label>প্যাকেজ নির্বাচন করুন:</label>
                <select name="package" required>
                    <option value="Weekly Membership - ৳160">Weekly Membership - ৳160</option>
                    <option value="Monthly Membership - ৳750">Monthly Membership - ৳750</option>
                    <option value="115 Diamonds - ৳85">115 Diamonds - ৳85</option>
                    <option value="Level Up Pass - ৳80">Level Up Pass - ৳80</option>
                </select>

                <label>ফ্রি ফায়ার প্লেয়ার ইউআইডি (Player UID):</label>
                <input type="text" name="player_id" placeholder="যেমন: 1234567890" required>

                <div style="font-size: 13px; color: #cbd5e1; margin-bottom: 10px; background: #05070a; padding: 10px; border-radius: 8px; border: 1px dashed #334155;">
                    বিকাশ পার্সোনাল সেন্ড মানি করুন: <b style="color: #ef4444;">{{ bkash }}</b>
                </div>

                <label>বিকাশ ট্রানজেকশন আইডি (TrxID):</label>
                <input type="text" name="txid" placeholder="টাকা পাঠিয়ে TrxID এখানে দিন" required>

                <button type="submit" class="check-btn">অর্ডার কনফার্ম করুন</button>
            </form>
        </div>
    </div>

    <!-- Order History Section -->
    <div id="historySection" style="display: none;">
        <div class="section-title">📦 আমার অর্ডার হিস্টরি (Order History)</div>
        <div class="history-box">
            {% if orders %}
                {% for o in orders %}
                <div class="history-item">
                    <div><b>Order ID:</b> #{{ o.id }}</div>
                    <div><b>Category:</b> {{ o.category }}</div>
                    <div><b>Package:</b> {{ o.package }}</div>
                    <div><b>UID:</b> {{ o.player_id }}</div>
                    <div><b>TrxID:</b> {{ o.txid }}</div>
                    <div><b>স্ট্যাটাস:</b> 
                        {% if o.status == 'Pending' %}
                            <span class="status-pending">⏳ পেন্ডিং (Pending - যাচাই চলছে)</span>
                        {% else %}
                            <span class="status-success">✅ সফলভাবে ডায়মন্ড পাঠানো হয়েছে!</span>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <p style="text-align: center; color: #94a3b8; font-size: 13px;">কোনো অর্ডার হিস্টরি পাওয়া যায়নি!</p>
            {% endif %}
        </div>
    </div>

    <div class="nav-bar">
        <a onclick="showTab('home')" class="nav-item active" id="navHome">
            <svg viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>Home
        </a>
        <a onclick="showTab('history')" class="nav-item" id="navHistory">
            <svg viewBox="0 0 24 24"><path d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z"/></svg>History
        </a>
        <a href="{{ telegram_channel }}" class="nav-item" target="_blank">
            <svg viewBox="0 0 24 24"><path d="M18 3H6c-1.66 0-3 1.34-3 3v12c0 1.66 1.34 3 3 3h12c1.66 0 3-1.34 3-3V6c0-1.66-1.34-3-3-3zm-9 13.5v-9l7 4.5-7 4.5z"/></svg>Channel
        </a>
    </div>

    <script>
        function closeModal() {
            document.getElementById('warningModal').style.display = 'none';
        }
        function selectCat(catName) {
            document.getElementById('selectedCategory').value = catName;
            window.scrollTo({top: 550, behavior: 'smooth'});
        }
        function showTab(tab) {
            if(tab == 'home') {
                document.getElementById('homeSection').style.display = 'block';
                document.getElementById('historySection').style.display = 'none';
                document.getElementById('navHome').classList.add('active');
                document.getElementById('navHistory').classList.remove('active');
            } else {
                document.getElementById('homeSection').style.display = 'none';
                document.getElementById('historySection').style.display = 'block';
                document.getElementById('navHistory').classList.add('active');
                document.getElementById('navHome').classList.remove('active');
            }
        }
        let slides = document.querySelectorAll('.slide');
        let currentSlide = 0;
        setInterval(() => {
            slides[currentSlide].classList.remove('active');
            currentSlide = (currentSlide + 1) % slides.length;
            slides[currentSlide].classList.add('active');
        }, 3500);
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    global order_counter
    success_msg = None
    if request.method == 'POST':
        category = request.form.get('category')
        package = request.form.get('package')
        player_id = request.form.get('player_id')
        txid = request.form.get('txid')
        
        if player_id and package and txid:
            current_order_id = order_counter
            order_counter += 1
            
            # ডাটাবেজে নতুন অর্ডার যোগ করা (পেন্ডিং স্ট্যাটাসসহ)
            new_order = {
                "id": current_order_id,
                "category": category,
                "package": package,
                "player_id": player_id,
                "txid": txid,
                "status": "Pending"
            }
            orders_db.insert(0, new_order)
            
            # টেলিগ্রাম বটে অর্ডার পাঠানো
            send_telegram_order(current_order_id, player_id, category, package, txid)
            success_msg = f"অর্ডার সফলভাবে সাবমিট হয়েছে! অর্ডার আইডি: #{current_order_id}. হিস্টরি থেকে স্ট্যাটাস চেক করুন।"

    return render_template_string(
        HTML_TEMPLATE, 
        telegram_support=TELEGRAM_SUPPORT, 
        telegram_channel=TELEGRAM_CHANNEL, 
        tutorial_link=TUTORIAL_VIDEO_LINK,
        bkash=BKASH_NUMBER, 
        success_msg=success_msg,
        orders=orders_db
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
