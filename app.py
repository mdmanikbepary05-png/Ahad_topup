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
from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

TELEGRAM_SUPPORT = "https://t.me/ahadtopup"
TELEGRAM_CHANNEL = "https://t.me/ahadtopup"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ahad Topup - Premium Free Fire Shop</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f7f6; margin: 0; padding-bottom: 70px; color: #333; }
        .header { background: #fff; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; position: sticky; top: 0; z-index: 100; }
        .logo { font-size: 20px; font-weight: bold; color: #1a1a73; display: flex; align-items: center; gap: 6px; }
        .logo span { color: #00b862; }
        .login-btn { background: #00b862; color: #fff; padding: 6px 16px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px; }
        
        /* Banner Slider Styling */
        .slider-container { position: relative; width: 100%; height: 160px; overflow: hidden; margin-bottom: 15px; background: #0f172a; }
        .slide { position: absolute; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out; background-size: cover; background-position: center; }
        .slide.active { opacity: 1; }
        .banner-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, rgba(0,0,0,0.4), rgba(0,0,0,0.1)); display: flex; justify-content: space-between; padding: 10px 15px; box-sizing: border-box; }
        .banner-brand-name { color: #fff; font-weight: bold; font-size: 15px; background: rgba(0, 184, 98, 0.85); padding: 3px 10px; border-radius: 4px; height: fit-content; text-transform: uppercase; letter-spacing: 1px; }

        .section-title { font-size: 18px; font-weight: bold; color: #0f172a; margin: 15px 16px 10px; text-transform: uppercase; }
        
        .grid-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; padding: 0 16px; margin-bottom: 15px; }
        .card { background: #fff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
        .card-title { font-size: 13px; font-weight: bold; color: #1e293b; margin-bottom: 4px; }
        .card-price { font-size: 12px; color: #00b862; font-weight: bold; }

        .form-box { background: #fff; margin: 0 16px 15px; padding: 16px; border-radius: 10px; border: 1px solid #e2e8f0; }
        .form-box label { font-size: 14px; font-weight: bold; display: block; margin-bottom: 8px; }
        .form-box input { width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 14px; box-sizing: border-box; margin-bottom: 10px; }
        .check-btn { background: #00b862; color: #fff; width: 100%; padding: 10px; border: none; border-radius: 6px; font-weight: bold; font-size: 14px; cursor: pointer; }

        .orders-box { background: #fff; margin: 0 16px; border-radius: 10px; border: 1px solid #e2e8f0; padding: 12px; }
        .order-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-weight: bold; font-size: 15px; }
        .order-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #f1f5f9; font-size: 13px; }
        .badge-done { background: #dcfce7; color: #15803d; padding: 3px 8px; border-radius: 20px; font-size: 11px; font-weight: bold; }

        .nav-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: #fff; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-around; padding: 8px 0; z-index: 1000; }
        .nav-item { text-decoration: none; color: #64748b; font-size: 11px; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 3px; }
        .nav-item.active { color: #00b862; font-weight: bold; }
        .nav-item svg { width: 20px; height: 20px; fill: currentColor; }
    </style>
</head>
<body>

    <div class="header">
        <div class="logo"><span><b>AHAD</b></span>TOPUP</div>
        <a href="{{ telegram_support }}" class="login-btn" target="_blank">Support</a>
    </div>

    <!-- Auto Slider with Ahad Tag -->
    <div class="slider-container">
        <div class="slide active" style="background-image: url('https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600');">
            <div class="banner-overlay">
                <div class="banner-brand-name">Ahad Topup</div>
            </div>
        </div>
        <div class="slide" style="background-image: url('https://images.unsplash.com/photo-1511512578047-dfb367046420?w=600');">
            <div class="banner-overlay">
                <div class="banner-brand-name">Giveaway Offer</div>
            </div>
        </div>
        <div class="slide" style="background-image: url('https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=600');">
            <div class="banner-overlay">
                <div class="banner-brand-name">Trusted Shop</div>
            </div>
        </div>
    </div>

    <div class="section-title">Regular Topup</div>
    <div class="grid-container">
        <div class="card">
            <div class="card-title">200 FF LIKE</div>
            <div class="card-price">BDT 30</div>
        </div>
        <div class="card">
            <div class="card-title">UID TOPUP</div>
            <div class="card-price">Instant</div>
        </div>
        <div class="card">
            <div class="card-title">WEEKLY / MONTHLY</div>
            <div class="card-price">BDT 155+</div>
        </div>
        <div class="card">
            <div class="card-title">LEVEL UP PASS</div>
            <div class="card-price">BDT 75</div>
        </div>
    </div>

    <div class="form-box">
        <label>2. Account Info</label>
        <input type="text" placeholder="এখানে প্লেয়ার আইডি বসান">
        <button class="check-btn">আপনার গেম আইডির নাম চেক করুন</button>
    </div>

    <div class="orders-box">
        <div class="order-header">
            <span>Recent Orders</span>
            <span style="color: #00b862; font-size: 12px;">● Live</span>
        </div>
        <div class="order-item">
            <span><b>Emon Khan</b><br><small>Level Up Package</small></span>
            <span class="badge-done">Done</span>
        </div>
        <div class="order-item">
            <span><b>Ariful Islam</b><br><small>115 Diamond - ৳78</small></span>
            <span class="badge-done">Done</span>
        </div>
        <div class="order-item">
            <span><b>Siam</b><br><small>50 Diamond - ৳35</small></span>
            <span class="badge-done">Done</span>
        </div>
    </div>

    <div class="nav-bar">
        <a href="#" class="nav-item active">
            <svg viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
            Home
        </a>
        <a href="{{ telegram_channel }}" class="nav-item" target="_blank">
            <svg viewBox="0 0 24 24"><path d="M18 3H6c-1.66 0-3 1.34-3 3v12c0 1.66 1.34 3 3 3h12c1.66 0 3-1.34 3-3V6c0-1.66-1.34-3-3-3zm-9 13.5v-9l7 4.5-7 4.5z"/></svg>
            Tutorial
        </a>
        <a href="#" class="nav-item">
            <svg viewBox="0 0 24 24"><path d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0-2-.9-2-2V4c0-1.1-.9-2-2-2zm0 14H8V4h12v12z"/></svg>
            TopUp
        </a>
        <a href="{{ telegram_support }}" class="nav-item" target="_blank">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H7c0-2.76 2.24-5 5-5s5 2.24 5 5c0 1.03-.42 1.98-1.03 2.75z"/></svg>
            Contact Us
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

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, telegram_support=TELEGRAM_SUPPORT, telegram_channel=TELEGRAM_CHANNEL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
