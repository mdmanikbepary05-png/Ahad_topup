from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# তোমার টেলিগ্রাম বট তথ্য
TELEGRAM_BOT_TOKEN = "8970671481:AAFAC5V3b59JyLbdBlizsEh5VA"
TELEGRAM_CHAT_ID = "8662160082"
TELEGRAM_SUPPORT = "https://t.me/ahadtopup"
TELEGRAM_CHANNEL = "https://t.me/ahadtopup"
BKASH_NUMBER = "01727246581"

def send_telegram_order(player_id, package, txid):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        msg = (
            f"🚨 *New Topup Order!* 🚨\n\n"
            f"🆔 *Player ID:* `{player_id}`\n"
            f"📦 *Package:* {package}\n"
            f"💸 *TrxID:* `{txid}`\n"
            f"📱 *bKash No:* {BKASH_NUMBER}"
        )
        # টেলিগ্রামে Yes/No বাটন পাঠানোর ব্যবস্থা
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
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0b0f19; margin: 0; padding-bottom: 80px; color: #fff; }
        .header { background: #111827; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1f2937; position: sticky; top: 0; z-index: 100; }
        .logo { font-size: 20px; font-weight: bold; color: #fff; display: flex; align-items: center; gap: 6px; }
        .logo span { color: #00b862; }
        .support-btn { background: #00b862; color: #fff; padding: 6px 14px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 13px; }
        
        /* Banner Slider */
        .slider-container { position: relative; width: 100%; height: 180px; overflow: hidden; background: #111827; }
        .slide { position: absolute; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out; background-size: cover; background-position: center; }
        .slide.active { opacity: 1; }
        .banner-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(11,15,25,0.8)); display: flex; align-items: flex-end; padding: 12px; box-sizing: border-box; }
        .banner-tag { background: #00b862; color: #fff; padding: 4px 10px; border-radius: 4px; font-size: 13px; font-weight: bold; text-transform: uppercase; }

        .section-title { font-size: 16px; font-weight: bold; color: #9ca3af; margin: 15px 16px 8px; text-transform: uppercase; letter-spacing: 1px; }
        
        .grid-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; padding: 0 16px; margin-bottom: 15px; }
        .card { background: #1f2937; border: 1px solid #374151; border-radius: 10px; padding: 12px; text-align: center; cursor: pointer; transition: 0.2s; }
        .card:hover { border-color: #00b862; }
        .card-title { font-size: 13px; font-weight: bold; color: #f3f4f6; margin-bottom: 4px; }
        .card-price { font-size: 13px; color: #00b862; font-weight: bold; }

        .form-box { background: #1f2937; margin: 0 16px 15px; padding: 16px; border-radius: 10px; border: 1px solid #374151; }
        .form-box label { font-size: 13px; font-weight: bold; display: block; margin-bottom: 6px; color: #d1d5db; }
        .form-box input, .form-box select { width: 100%; padding: 10px; background: #111827; border: 1px solid #374151; color: #fff; border-radius: 6px; font-size: 14px; box-sizing: border-box; margin-bottom: 10px; }
        .check-btn { background: #00b862; color: #fff; width: 100%; padding: 10px; border: none; border-radius: 6px; font-weight: bold; font-size: 14px; cursor: pointer; }

        .leaderboard-box { background: #1f2937; margin: 0 16px 15px; border-radius: 10px; border: 1px solid #374151; padding: 12px; }
        .lb-item { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #374151; font-size: 13px; }

        .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: #111827; border-top: 1px solid #1f2937; display: flex; justify-content: space-around; padding: 8px 0; z-index: 1000; }
        .nav-item { text-decoration: none; color: #9ca3af; font-size: 11px; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 3px; }
        .nav-item.active { color: #00b862; font-weight: bold; }
        .nav-item svg { width: 20px; height: 20px; fill: currentColor; }
    </style>
</head>
<body>

    <div class="header">
        <div class="logo"><span><b>AHAD</b></span>TOPUP</div>
        <a href="{{ telegram_support }}" class="support-btn" target="_blank">Support</a>
    </div>

    <!-- FF Character Banners -->
<div class="slider-container">
    <div class="slide active" style="background-image: url('https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600');">
        <div class="banner-overlay"><div class="banner-tag">Ahad Topup Exclusive</div></div>
    </div>
    <div class="slide" style="background-image: url('https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=600');">
        <div class="banner-overlay"><div class="banner-tag">Weekly & Monthly Member</div></div>
    </div>
    <div class="slide" style="background-image: url('https://images.unsplash.com/photo-1511512578047-dfb367046420?w=600');">
        <div class="banner-overlay"><div class="banner-tag">Level Up Pass Offer</div></div>
    </div>
</div>

    <div class="section-title">Select Package</div>
    <div class="grid-container">
        <div class="card">
            <div class="card-title">Weekly Membership</div>
            <div class="card-price">৳ 160</div>
        </div>
        <div class="card">
            <div class="card-title">Monthly Membership</div>
            <div class="card-price">৳ 750</div>
        </div>
        <div class="card">
            <div class="card-title">115 Diamonds</div>
            <div class="card-price">৳ 85</div>
        </div>
        <div class="card">
            <div class="card-title">Level Up Pass</div>
            <div class="card-price">৳ 80</div>
        </div>
    </div>

    <div class="form-box">
        <label>পেমেন্ট ও অর্ডার ফর্ম</label>
        {% if success_msg %}
            <p style="color: #00b862; font-weight: bold; font-size: 13px; background: rgba(0,184,98,0.1); padding: 8px; border-radius: 5px;">{{ success_msg }}</p>
        {% endif %}
        <form method="POST">
            <input type="text" name="player_id" placeholder="Free Fire Player UID দিন" required>
            <select name="package" required>
                <option value="">প্যাকেজ সিলেক্ট করুন</option>
                <option value="Weekly Membership - ৳160">Weekly Membership - ৳160</option>
                <option value="Monthly Membership - ৳750">Monthly Membership - ৳750</option>
                <option value="115 Diamonds - ৳85">115 Diamonds - ৳85</option>
                <option value="Level Up Pass - ৳80">Level Up Pass - ৳80</option>
            </select>
            <div style="font-size: 12px; color: #9ca3af; margin-bottom: 8px;">বিকাশ সেন্ড মানি করুন: <b style="color: #00b862;">{{ bkash }}</b></div>
            <input type="text" name="txid" placeholder="বিকাশ ট্রানজেকশন আইডি (TrxID) দিন" required>
            <button type="submit" class="check-btn">ভেরিফাই করুন (Verify Order)</button>
        </form>
    </div>

    <div class="section-title">Top Buyers (Leaderboard)</div>
    <div class="leaderboard-box">
        <div class="lb-item"><span>1. Rashed (UID: ***452)</span> <span style="color: #00b862;">Monthly</span></div>
        <div class="lb-item"><span>2. Tanvir (UID: ***891)</span> <span style="color: #00b862;">Weekly</span></div>
        <div class="lb-item"><span>3. Fahim (UID: ***230)</span> <span style="color: #00b862;">115 Diamonds</span></div>
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
        player_id = request.form.get('player_id')
        package = request.form.get('package')
        txid = request.form.get('txid')
        if player_id and package and txid:
            send_telegram_order(player_id, package, txid)
            success_msg = "অর্ডার সফলভাবে সাবমিট হয়েছে! একটু অপেক্ষা করুন, যাচাই করে ডায়মন্ড পাঠিয়ে দেওয়া হবে।"
    return render_template_string(HTML_TEMPLATE, telegram_support=TELEGRAM_SUPPORT, telegram_channel=TELEGRAM_CHANNEL, bkash=BKASH_NUMBER, success_msg=success_msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
