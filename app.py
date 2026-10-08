from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# টেলিগ্রাম বট তথ্য
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
        payload = {
            "chat_id": TELEGRAM_CHAT_ID, 
            "text": msg, 
            "parse_mode": "Markdown",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {"text": "✅ Approve", "callback_data": f"approve_{player_id}"},
                        {"text": "❌ Reject", "callback_data": f"reject_{player_id}"}
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
        .modal-desc { font-size: 13px; color: #cbd5e1; margin-bottom: 20px; line-height: 1.6; }
        .modal-btn { background: linear-gradient(45deg, #dc2626, #ef4444); color: #fff; border: none; padding: 11px 20px; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%; font-size: 14px; box-shadow: 0 0 15px rgba(220,38,38,0.6); }

        /* Banner Slider */
        .slider-container { position: relative; width: 100%; height: 210px; overflow: hidden; background: #0f172a; border-bottom: 2px solid #1e293b; }
        .slide { position: absolute; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out; background-size: cover; background-position: center; }
        .slide.active { opacity: 1; }
        .banner-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, rgba(5,7,10,0.1), rgba(5,7,10,0.95)); display: flex; align-items: flex-end; padding: 15px; box-sizing: border-box; }
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

        .leaderboard-box { background: #0f172a; margin: 0 16px 20px; border-radius: 14px; border: 1px solid #1e293b; padding: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.4); }
        .lb-item { display: flex; justify-content: space-between; padding: 9px 0; border-bottom: 1px solid #1e293b; font-size: 13px; }

        .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: #0f172a; border-top: 2px solid #1e293b; display: flex; justify-content: space-around; padding: 9px 0; z-index: 100; box-shadow: 0 -4px 15px rgba(0,0,0,0.5); }
        .nav-item { text-decoration: none; color: #94a3b8; font-size: 11px; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 3px; }
        .nav-item.active { color: #ef4444; font-weight: bold; }
        .nav-item svg { width: 20px; height: 20px; fill: currentColor; }
    </style>
</head>
<body>

    <!-- Age Warning Modal -->
    <div class="modal-overlay" id="warningModal">
        <div class="modal-box">
            <div class="modal-title">⚠️ সতর্কবার্তা (Warning)</div>
            <div class="modal-desc">বাচ্চারা ১৮ বছরের নিচে টপ-আপ করা নিষেধ এবং এটি সম্পূর্ণ বেআইনি। আপনি কি ১৮ বছরের উর্ধ্বে?</div>
            <button class="modal-btn" onclick="closeModal()">হ্যাঁ, আমার বয়স ১৮+</button>
        </div>
    </div>

    <div class="header">
        <div class="logo"><span><b>AHAD</b></span>TOPUP</div>
        <a href="{{ telegram_support }}" class="support-btn" target="_blank">Support</a>
    </div>

    <!-- FF Character Banners with Custom Red Glow Aesthetics -->
    <div class="slider-container">
        <div class="slide active" style="background-image: linear-gradient(rgba(5,7,10,0.3), rgba(5,7,10,0.9)), url('https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600');">
            <div class="banner-overlay"><div class="banner-tag">🔥 Free Fire Red G-Lock Special</div></div>
        </div>
        <div class="slide" style="background-image: linear-gradient(rgba(5,7,10,0.3), rgba(5,7,10,0.9)), url('https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=600');">
            <div class="banner-overlay"><div class="banner-tag">⚡ Weekly & Monthly Mega Discount</div></div>
        </div>
    </div>

    <div class="section-title">⚡ প্রিমি엄 ক্যাটাগরি (Topup Categories)</div>
    
    <!-- 4 Main Free Fire Character / Category Options using the given high-end theme -->
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

    <div class="section-title">🏆 লিডারবোর্ড (Top Buyers)</div>
    <div class="leaderboard-box">
        <div class="lb-item"><span>1. Rashed (UID: ***452)</span> <span style="color: #ef4444;">Monthly</span></div>
        <div class="lb-item"><span>2. Tanvir (UID: ***891)</span> <span style="color: #ef4444;">Weekly</span></div>
        <div class="lb-item"><span>3. Fahim (UID: ***230)</span> <span style="color: #ef4444;">115 Diamonds</span></div>
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
        function closeModal() {
            document.getElementById('warningModal').style.display = 'none';
        }
        function selectCat(catName) {
            document.getElementById('selectedCategory').value = catName;
            window.scrollTo({top: 550, behavior: 'smooth'});
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
