from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# তোমার টেলিগ্রাম বট তথ্য
TELEGRAM_BOT_TOKEN = "8970671481:AAFAC5V3b59JyLbdBlizsEh5VA"
TELEGRAM_CHAT_ID = "8662160082"
TELEGRAM_SUPPORT = "https://t.me/ahadtopup"
TELEGRAM_CHANNEL = "https://t.me/ahadtopup"
BKASH_NUMBER = "01727246581"

def send_telegram_order(player_id, category, package, txid):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        msg = (
            f"🔥 *AHAD TOPUP - NEW ORDER* 🔥\n\n"
            f"📂 *Category:* {category}\n"
            f"📦 *Package:* {package}\n"
            f"🆔 *Player UID:* `{player_id}`\n"
            f"💸 *TrxID:* `{txid}`\n"
            f"📱 *bKash No:* {BKASH_NUMBER}"
        )
        keyboard = {
            "inline_keyboard": [
                [{"text": "✅ Approve (Yes)", "callback_data": f"approve_{player_id}"},
                 {"text": "❌ Reject (No)", "callback_data": f"reject_{player_id}"}]
            ]
        }
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown", "reply_markup": keyboard}
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("Error:", e)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ahad Topup - Premium Free Fire Shop</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #07090e; margin: 0; padding-bottom: 80px; color: #fff; }
        .header { background: #0f172a; padding: 14px 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; position: sticky; top: 0; z-index: 100; }
        .logo { font-size: 20px; font-weight: bold; color: #fff; display: flex; align-items: center; gap: 6px; }
        .logo span { color: #00ff88; }
        .support-btn { background: #00ff88; color: #000; padding: 6px 14px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 13px; }
        
        /* Modal Popup Styling */
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); display: flex; justify-content: center; align-items: center; z-index: 9999; }
        .modal-box { background: #111827; border: 2px solid #00ff88; width: 85%; max-width: 350px; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 0 20px rgba(0,255,136,0.3); }
        .modal-title { color: #ff4d4d; font-size: 18px; font-weight: bold; margin-bottom: 10px; }
        .modal-desc { font-size: 13px; color: #d1d5db; margin-bottom: 20px; line-height: 1.5; }
        .modal-btn { background: #00ff88; color: #000; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; width: 100%; font-size: 14px; }

        /* Banner Slider */
        .slider-container { position: relative; width: 100%; height: 180px; overflow: hidden; background: #0f172a; }
        .slide { position: absolute; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out; background-size: cover; background-position: center; }
        .slide.active { opacity: 1; }
        .banner-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(7,9,14,0.9)); display: flex; align-items: flex-end; padding: 12px; box-sizing: border-box; }
        .banner-tag { background: #00ff88; color: #000; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; text-transform: uppercase; }

        .section-title { font-size: 15px; font-weight: bold; color: #00ff88; margin: 18px 16px 10px; text-transform: uppercase; letter-spacing: 1px; display: flex; align-items: center; gap: 5px; }
        
        /* Category Grid */
        .cat-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; padding: 0 16px; margin-bottom: 15px; }
        .cat-card { background: #111827; border: 1px solid #1f2937; border-radius: 10px; padding: 14px; text-align: center; cursor: pointer; transition: 0.2s; text-decoration: none; color: #fff; display: flex; flex-direction: column; align-items: center; gap: 6px; }
        .cat-card:hover { border-color: #00ff88; background: #1f2937; }
        .cat-card img { width: 45px; height: 45px; object-fit: contain; }
        .cat-name { font-size: 13px; font-weight: bold; color: #f3f4f6; }

        /* Form Box */
        .form-box { background: #111827; margin: 0 16px 20px; padding: 18px; border-radius: 12px; border: 1px solid #1f2937; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        .form-box label { font-size: 13px; font-weight: bold; display: block; margin-bottom: 6px; color: #00ff88; }
        .form-box input, .form-box select { width: 100%; padding: 11px; background: #07090e; border: 1px solid #374151; color: #fff; border-radius: 8px; font-size: 14px; box-sizing: border-box; margin-bottom: 12px; }
        .check-btn { background: linear-gradient(45deg, #00ff88, #00b862); color: #000; width: 100%; padding: 12px; border: none; border-radius: 8px; font-weight: bold; font-size: 15px; cursor: pointer; text-transform: uppercase; }

        .leaderboard-box { background: #111827; margin: 0 16px 20px; border-radius: 12px; border: 1px solid #1f2937; padding: 14px; }
        .lb-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #1f2937; font-size: 13px; }

        .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: #0f172a; border-top: 1px solid #1e293b; display: flex; justify-content: space-around; padding: 8px 0; z-index: 100; }
        .nav-item { text-decoration: none; color: #94a3b8; font-size: 11px; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 3px; }
        .nav-item.active { color: #00ff88; font-weight: bold; }
        .nav-item svg { width: 20px; height: 20px; fill: currentColor; }
    </style>
</head>
<body>

    <!-- Age Warning Modal -->
    <div class="modal-overlay" id="warningModal">
        <div class="modal-box">
            <div class="modal-title">⚠️ সতর্কবার্তা (Warning)</div>
            <div class="modal-desc">১৮ বছরের নিচে কারো জন্য টপ-আপ করা নিষেধ এবং এটি সম্পূর্ণ বেআইনি। আপনি কি ১৮ বছরের উর্ধ্বে?</div>
            <button class="modal-btn" onclick="closeModal()">হ্যাঁ, আমার বয়স ১৮+</button>
        </div>
    </div>

    <div class="header">
        <div class="logo"><span><b>AHAD</b></span>TOPUP</div>
        <a href="{{ telegram_support }}" class="support-btn" target="_blank">Support</a>
    </div>

    <!-- FF Character Banners -->
    <div class="slider-container">
        <div class="slide active" style="background-image: url('https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600');">
            <div class="banner-overlay"><div class="banner-tag">Alok & Chrono Special Offer</div></div>
        </div>
        <div class="slide" style="background-image: url('https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=600');">
            <div class="banner-overlay"><div class="banner-tag">Weekly & Monthly Mega Discount</div></div>
        </div>
        <div class="slide" style="background-image: url('https://images.unsplash.com/photo-1511512578047-dfb367046420?w=600');">
            <div class="banner-overlay"><div class="banner-tag">Level Up Pass & UID Topup</div></div>
        </div>
    </div>

    <div class="section-title">⚡ 프리미엄 ক্যাটাগরি (Topup Categories)</div>
    
    <!-- 4 Main Free Fire Character / Category Options -->
    <div class="cat-grid">
        <div class="cat-card" onclick="selectCat('Weekly Offer')">
            <img src="https://cdn-icons-png.flaticon.com/512/3112/3112946.png" alt="Weekly">
            <div class="cat-name">উইকলি অফার (Weekly)</div>
        </div>
        <div class="cat-card" onclick="selectCat('Monthly Offer')">
            <img src="https://cdn-icons-png.flaticon.com/512/3112/3112948.png" alt="Monthly">
            <div class="cat-name">মান্থলি অফার (Monthly)</div>
        </div>
        <div class="cat-card" onclick="selectCat('UID Diamond')">
            <img src="https://cdn-icons-png.flaticon.com/512/1164/1164951.png" alt="UID">
            <div class="cat-name">প্লেয়ার ইউআইডি (UID Topup)</div>
        </div>
        <div class="cat-card" onclick="selectCat('Level Up Pass')">
            <img src="https://cdn-icons-png.flaticon.com/512/3112/3112935.png" alt="Level Up">
            <div class="cat-name">লেভেল আপ পাস (Level Up)</div>
        </div>
    </div>

    <div class="form-box">
        <label>💎 টপ-আপ অর্ডার ও পেমেন্ট ফর্ম</label>
        {% if success_msg %}
            <p style="color: #00ff88; font-weight: bold; font-size: 13px; background: rgba(0,255,136,0.1); padding: 10px; border-radius: 6px; border: 1px solid #00ff88; margin-bottom: 12px;">{{ success_msg }}</p>
        {% endif %}
        <form method="POST">
            <label>সিলেক্টেড ক্যাটাগরি:</label>
            <input type="text" id="selectedCategory" name="category" value="Weekly Offer" readonly style="color: #00ff88; font-weight: bold;">
            
            <label>প্যাকেজ নির্বাচন করুন:</label>
            <select name="package" required>
                <option value="Weekly Membership - ৳160">Weekly Membership - ৳160</option>
                <option value="Monthly Membership - ৳750">Monthly Membership - ৳750</option>
                <option value="115 Diamonds - ৳85">115 Diamonds - ৳85</option>
                <option value="Level Up Pass - ৳80">Level Up Pass - ৳80</option>
            </select>

            <label>ফ্রি ফায়ার প্লেয়ার ইউআইডি (Player UID):</label>
            <input type="text" name="player_id" placeholder="যেমন: 1234567890" required>

            <div style="font-size: 13px; color: #94a3b8; margin-bottom: 8px; background: #07090e; padding: 8px; border-radius: 6px; border: 1px dashed #374151;">
                বিকাশ পার্সোনাল সেন্ড মানি করুন: <b style="color: #00ff88;">{{ bkash }}</b>
            </div>

            <label>বিকাশ ট্রানজেকশন আইডি (TrxID):</label>
            <input type="text" name="txid" placeholder="টাকা পাঠিয়ে TrxID এখানে দিন" required>

            <button type="submit" class="check-btn">ভেরিফাই ও অর্ডার কনফার্ম করুন</button>
        </form>
    </div>

    <div class="section-title">🏆 লিডারবোর্ড (Top Buyers)</div>
    <div class="leaderboard-box">
        <div class="lb-item"><span>1. Rashed (UID: ***452)</span> <span style="color: #00ff88;">Monthly</span></div>
        <div class="lb-item"><span>2. Tanvir (UID: ***891)</span> <span style="color: #00ff88;">Weekly</span></div>
        <div class="lb-item"><span>3. Fahim (UID: ***230)</span> <span style="color: #00ff88;">115 Diamonds</span></div>
    </div>

    <div class="nav-bar">
        <a href="#" class="nav-item active">
            <svg viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>Home
        </a>
        <a href="{{ telegram_channel }}" class="nav-item" target="_blank">
            <svg viewBox="0 0 24 24"><path d="M18 3H6c-1.66 0-3 1.34-3 3v12c0 1.66 1.34 3 3 3h12c1.66 0 3-1.34 3-3V6c0-1.66-1.34-3-3-3zm-9 13.5v-9l7 4.5-7 4.5z"/></svg>Channel
        </a>
        <a href="{{ telegram_support }}" class="nav-item" target="_blank">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H7c0-2.76 2.24-5 5-5s5 2.24 5 5c0 1.03-.42 1.98-1.03 2.75z"/></svg>Support
        </a>
    </div>

    <script>
        // Modal Control
        function closeModal() {
            document.getElementById('warningModal').style.display = 'none';
        }

        // Category Selection
        function selectCat(catName) {
            document.getElementById('selectedCategory').value = catName;
            window.scrollTo({top: 550, behavior: 'smooth'});
        }

        // Banner Slider
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
    success_msg = None
    if request.method == 'POST':
        category = request.form.get('category')
        package = request.form.get('package')
        player_id = request.form.get('player_id')
        txid = request.form.get('txid')
        if player_id and package and txid:
            send_telegram_order(player_id, category, package, txid)
            success_msg = "অর্ডার সফলভাবে সাবমিট হয়েছে! ট্রানজেকশন যাচাই করে দ্রুত ডায়মন্ড পাঠিয়ে দেওয়া হবে।"
    return render_template_string(HTML_TEMPLATE, telegram_support=TELEGRAM_SUPPORT, telegram_channel=TELEGRAM_CHANNEL, bkash=BKASH_NUMBER, success_msg=success_msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
