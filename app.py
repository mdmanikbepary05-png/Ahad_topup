from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

BKASH_NUMBER = "01727246581"
TELEGRAM_BOT_TOKEN = "8970671481:AAFACF5V3b59JyLbdBNzszEH5VAlyefhLww"
TELEGRAM_CHAT_ID = "8662169982"
TELEGRAM_SUPPORT = "https://t.me/ahadtopup"
TELEGRAM_CHANNEL = "https://t.me/ahadtopup"

def send_telegram_notification(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("Error:", e)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ahad TopUp - Premium Free Fire Shop</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #07090e, #0f172a); color: #fff; margin: 0; padding: 10px; }
        .container { max-width: 480px; margin: 15px auto; background: rgba(30, 41, 59, 0.95); padding: 20px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); border: 1px solid #334155; backdrop-filter: blur(10px); }
        
        .brand-header { text-align: center; margin-bottom: 15px; }
        .brand-header h1 { margin: 0; color: #f59e0b; font-size: 26px; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 2px 10px rgba(245,158,11,0.4); }
        .brand-header p { color: #38bdf8; font-size: 13px; margin: 5px 0 0 0; font-weight: bold; }

        .slider-container { position: relative; width: 100%; height: 160px; border-radius: 12px; overflow: hidden; margin-bottom: 15px; border: 2px solid #475569; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        .slide { position: absolute; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out; background-size: cover; background-position: center; display: flex; align-items: flex-end; }
        .slide.active { opacity: 1; }
        .slide-text { background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); width: 100%; padding: 10px; text-align: center; font-weight: bold; color: #facc15; font-size: 14px; text-shadow: 0 1px 3px rgba(0,0,0,0.9); }

        .support-float { display: flex; justify-content: space-between; margin-bottom: 15px; gap: 10px; }
        .support-btn { flex: 1; background: #2563eb; color: #fff; text-decoration: none; padding: 10px; border-radius: 8px; text-align: center; font-size: 13px; font-weight: bold; box-shadow: 0 4px 10px rgba(37,99,235,0.4); transition: 0.3s; }
        .support-btn:hover { background: #1d4ed8; }
        .channel-btn { background: #0ea5e9; }
        .channel-btn:hover { background: #0284c7; }

        .section-title { color: #38bdf8; font-size: 15px; font-weight: bold; margin: 15px 0 8px 0; border-left: 3px solid #f59e0b; padding-left: 8px; text-align: left; }
        input, select { width: 100%; padding: 12px; margin: 6px 0; border-radius: 10px; border: 1px solid #475569; background: #0f172a; color: #fff; box-sizing: border-box; font-size: 14px; outline: none; transition: 0.3s; }
        input:focus, select:focus { border-color: #f59e0b; box-shadow: 0 0 8px rgba(245,158,11,0.4); }
        
        .bkash-box { background: linear-gradient(135deg, #db2777, #be185d); color: white; padding: 12px; border-radius: 10px; margin: 12px 0; font-weight: bold; text-align: center; box-shadow: 0 4px 12px rgba(219,39,119,0.3); }
        
        button { background: linear-gradient(135deg, #f59e0b, #d97706); color: #000; font-weight: bold; padding: 14px; width: 100%; border: none; border-radius: 10px; cursor: pointer; margin-top: 15px; font-size: 16px; text-transform: uppercase; transition: 0.3s; box-shadow: 0 4px 15px rgba(245,158,11,0.4); }
        button:hover { background: linear-gradient(135deg, #d97706, #b45309); transform: translateY(-2px); }
    </style>
</head>
<body>
    <div class="container">
        <div class="brand-header">
            <h1>🔥 Ahad TopUp 🔥</h1>
            <p>বাংলাদেশের সেরা কম দামে ডায়মন্ড টপআপ ওয়েবসাইট</p>
        </div>

        <div class="support-float">
            <a href="{{ support_link }}" target="_blank" class="support-btn">💬 টেলিগ্রাম সাপোর্ট</a>
            <a href="{{ channel_link }}" target="_blank" class="support-btn channel-btn">🎁 গিভওয়ে চ্যানেল</a>
        </div>

        <div class="slider-container">
            <div class="slide active" style="background-image: url('https://images.unsplash.com/photo-1542751371-adc38448a05e?w=500');">
                <div class="slide-text">⚡ সুপার ফাস্ট উইকলি ও মান্থলি অফার!</div>
            </div>
            <div class="slide" style="background-image: url('https://images.unsplash.com/photo-1511512578047-dfb367046420?w=500');">
                <div class="slide-text">🎁 বিশেষ গিভওয়ে ও মেগা ডিসকাউন্ট!</div>
            </div>
            <div class="slide" style="background-image: url('https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=500');">
                <div class="slide-text">🛡️ ১০০% ট্রাস্টেড ও নিরাপদ টপআপ সার্ভিস!</div>
            </div>
        </div>

        {% if not success %}
        <form method="POST">
            <div class="section-title">১. জিমেইল ও গেম একাউন্ট ইনফো</div>
            <input type="email" name="email" list="gmail-suggestions" required placeholder="আপনার জিমেইল আইডি (ট্যাপ করলে জিমেইল শো হবে)">
            <datalist id="gmail-suggestions">
                <option value="@gmail.com">
            </datalist>

            <input type="text" name="uid" required placeholder="আপনার ফ্রি ফায়ার UID দিন">

            <div class="section-title">২. সেরা অফার প্যাকেজ সিলেক্ট করুন</div>
            <select name="package" required>
                <option value="25 Dias - 25 BDT">২৫ ডায়মন্ড - ২৫ টাকা</option>
                <option value="115 Dias - 85 BDT">১১৫ ডায়মন্ড (লেভেল আপ) - ৮৫ টাকা</option>
                <option value="Weekly Membership - 160 BDT">সাপ্তাহিক মেম্বারশিপ - ১৬০ টাকা</option>
                <option value="Monthly Membership - 450 BDT">মাসিক মেম্বারশিপ - ৪৫০ টাকা</option>
                <option value="Giveaway Special Pack">গিভওয়ে স্পেশাল প্যাক</option>
            </select>

            <div class="bkash-box">
                বিকাশ পার্সোনাল নম্বর:<br><span style="font-size: 18px; letter-spacing: 1px;">{{ bkash }}</span><br>
                <small style="font-size: 11px; font-weight: normal;">প্রথমে এই নম্বরে ক্যাশ আউট বা সেন্ড মানি করুন</small>
            </div>

            <div class="section-title">৩. পেমেন্ট ভেরিফিকেশন</div>
            <input type="text" name="sender" required placeholder="যে বিকাশ নম্বর থেকে টাকা পাঠিয়েছেন">
            <input type="text" name="trx" required placeholder="ট্রানজাকশন আইডি (TrxID দিন)">

            <button type="submit">অর্ডার কনফার্ম করুন</button>
        </form>
        {% else %}
            <div style="text-align: center; padding: 30px 10px;">
                <h3 style="color: #4ade80; font-size: 22px;">🎉 অর্ডার সফলভাবে জমা হয়েছে!</h3>
                <p style="color: #94a3b8; font-size: 14px;">আপনার পেমেন্ট ও জিমেইল ভেরিফাই করে খুব দ্রুত আপনার আইডিতে ডায়মন্ড বা অফার পৌঁছে দেওয়া হবে।</p>
                <a href="/"><button style="background:#334155; color:#fff; margin-top:20px;">আরেকটি অর্ডার করুন</button></a>
            </div>
        {% endif %}
    </div>

    <script>
        let slides = document.querySelectorAll('.slide');
        let currentSlide = 0;
        function nextSlide() {
            slides[currentSlide].classList.remove('active');
            currentSlide = (currentSlide + 1) % slides.length;
            slides[currentSlide].classList.add('active');
        }
        setInterval(nextSlide, 3500);
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    success = False
    if request.method == 'POST':
        email = request.form.get('email')
        uid = request.form.get('uid')
        package = request.form.get('package')
        sender = request.form.get('sender')
        trx = request.form.get('trx')
        
        msg = f"🚨 *নতুন অর্ডার এসেছে!* 🚨\n\n📧 *Gmail:* `{email}`\n🎮 *UID:* `{uid}`\n📦 *Package:* `{package}`\n📱 *Sender:* `{sender}`\n🔑 *TrxID:* `{trx}`"
        send_telegram_notification(msg)
        success = True
        
    return render_template_string(HTML_TEMPLATE, bkash=BKASH_NUMBER, support_link=TELEGRAM_SUPPORT, channel_link=TELEGRAM_CHANNEL, success=success)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
