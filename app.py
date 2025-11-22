# app.py - ConnectoMedia Full Website with WhatsApp + Email
from flask import Flask, render_template_string, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.parse
import webbrowser
import threading
import time

app = Flask(__name__)

# UPDATE THESE 2 LINES ONLY
EMAIL_ADDRESS = "officialconnectomedia@gmail.com"
EMAIL_PASSWORD = "your-16-digit-app-password"  # Get from: https://myaccount.google.com/apppasswords

# Your WhatsApp Number (India format)
WHATSAPP_NUMBER = "917909092283"  # Your number without +

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ConnectoMedia – Digital Media Agency</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Satoshi:wght@700;900&display=swap" rel="stylesheet">
  <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
  <style>
    :root { --primary: #0A3D62; --accent: #00D4FF; --light: #f8fafc; --dark: #0f172a; }
    * { margin:0; padding:0; box-sizing:border-box; }
    body { font-family:'Inter',sans-serif; background:var(--light); color:var(--dark); line-height:1.6; }
    h1,h2,h3 { font-family:'Satoshi',sans-serif; font-weight:700; }

    header {
      position:fixed; top:0; left:0; right:0; padding:20px 5%; background:rgba(10,61,98,0.95);
      backdrop-filter:blur(12px); z-index:1000; display:flex; justify-content:space-between; align-items:center;
      transition:all 0.4s;
    }
    header.scrolled { padding:15px 5%; box-shadow:0 10px 30px rgba(0,0,0,0.15); }
    .logo { color:white; font-size:1.8rem; font-weight:900; display:flex; align-items:center; gap:12px; }
    .logo img { height:50px; border-radius:12px; }
    nav { display:flex; gap:35px; }
    nav a { color:white; font-weight:500; position:relative; }
    nav a::after { content:''; position:absolute; width:0; height:2px; bottom:-8px; left:50%; background:var(--accent); transition:0.4s; }
    nav a:hover::after { width:100%; left:0; }
    .hamburger { display:none; cursor:pointer; }
    .hamburger span { width:25px; height:3px; background:white; margin:4px 0; }

    .hero {
      min-height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center;
      text-align:center; background:linear-gradient(135deg,#0A3D62,#1e4d72,#2563eb); color:white; padding:0 5%;
    }
    .hero h1 { font-size:4.2rem; background:linear-gradient(90deg,#fff,var(--accent)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
    .hero p { font-size:1.4rem; max-width:700px; opacity:0.9; margin:30px 0; }
    .cta { padding:16px 40px; background:white; color:var(--primary); border-radius:50px; font-weight:700; box-shadow:0 10px 30px rgba(0,0,0,0.2); transition:0.4s; }
    .cta:hover { transform:translateY(-5px); background:var(--accent); color:white; }

    section { padding:120px 5%; }
    h2 { font-size:3rem; text-align:center; margin-bottom:70px; color:var(--primary); }
    .services-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:30px; max-width:1200px; margin:0 auto; }
    .service-card { background:white; padding:40px; border-radius:20px; text-align:center; box-shadow:0 10px 40px rgba(0,0,0,0.08); transition:0.4s; }
    .service-card:hover { transform:translateY(-15px); box-shadow:0 25px 60px rgba(10,61,98,0.15); }

    .about { background:linear-gradient(135deg,#f1f5f9,#e2e8f0); }
    .about p { max-width:800px; margin:0 auto; font-size:1.2rem; text-align:center; color:#64748b; }

    .contact form { max-width:600px; margin:50px auto 0; display:grid; gap:20px; }
    .contact input, .contact textarea {
      padding:161px 16px; border:none; border-radius:12px; background:white; box-shadow:0 5px 20px rgba(0,0,0,0.08); font-size:1rem;
    }
    .contact button {
      padding:16px 40px; background:var(--primary); color:white; border:none; border-radius:50px;
      font-weight:600; cursor:pointer; transition:0.4s; justify-self:center;
    }
    .contact button:hover { background:#1e4d72; transform:translateY(-3px); }
    .contact button:disabled { background:#999; cursor:not-allowed; }

    .message { padding:15px; border-radius:8px; margin-top:15px; text-align:center; font-weight:500; }
    .success { background:#d4edda; color:#155724; border:1px solid #c3e6cb; }
    .error { background:#f8d7da; color:#721c24; border:1px solid #f5c6cb; }

    footer { background:var(--dark); color:white; text-align:center; padding:50px 20px; }

    @media (max-width:768px) {
      .hamburger { display:flex; flex-direction:column; }
      nav { display:none; position:fixed; top:80px; left:0; right:0; background:var(--primary); flex-direction:column; padding:20px; }
      nav.active { display:flex; }
      .hero h1 { font-size:2.8rem; }
    }
  </style>
</head>
<body>

  <header id="header">
    <div class="logo">
      <img src="https://via.placeholder.com/60x60/0A3D62/ffffff?text=CM" alt="Logo">
      ConnectoMedia
    </div>
    <nav id="nav">
      <a href="#services">Services</a>
      <a href="#about">About</a>
      <a href="#contact">Contact</a>
    </nav>
    <div class="hamburger" onclick="document.getElementById('nav').classList.toggle('active')">
      <span></span><span></span><span></span>
    </div>
  </header>

  <section class="hero">
    <h1 data-aos="fade-up">Connecting Creators<br>With Brands, Authentically</h1>
    <p data-aos="fade-up" data-aos-delay="200">We help brands scale through strategy, content creation & marketing execution.</p>
    <a href="#contact" class="cta" data-aos="fade-up" data-aos-delay="400">Get In Touch</a>
  </section>

  <section id="services">
    <h2 data-aos="fade-up">Our Services</h2>
    <div class="services-grid">
      <div class="service-card" data-aos="fade-up" data-aos-delay="100"><h3>Media Strategy</h3><p>Data-driven audience targeting & scaling.</p></div>
      <div class="service-card" data-aos="fade-up" data-aos-delay="200"><h3>Content Creation</h3><p>Reels, ads, videos & visuals that convert.</p></div>
      <div class="service-card" data-aos="fade-up" data-aos-delay="300"><h3>Brand Marketing</h3><p>Performance campaigns across platforms.</p></div>
    </div>
  </section>

  <section id="about" class="about">
    <h2 data-aos="fade-up">About ConnectoMedia</h2>
    <p data-aos="fade-up" data-aos-delay="200">
      Modern digital media agency helping brands grow through strategy, content & performance marketing.
    </p>
  </section>

  <section id="contact" class="contact">
    <h2 data-aos="fade-up">Let's Work Together</h2>
    <p>Email: <strong>officialconnectomedia@gmail.com</strong> | WhatsApp: <strong>+91 7909092283</strong></p>

    <form id="contactForm" data-aos="fade-up" data-aos-delay="200">
      <input type="text" name="name" placeholder="Your Name" required />
      <input type="email" name="email" placeholder="Your Email" required />
      <textarea name="message" rows="5" placeholder="Your Message" required></textarea>
      <button type="submit">Send Message</button>
      <div id="formMessage"></div>
    </form>
  </section>

  <footer>© 2025 ConnectoMedia. All Rights Reserved.</footer>

  <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
  <script>
    AOS.init({ duration: 1000, once: true });
    window.addEventListener('scroll', () => {
      document.getElementById('header').classList.toggle('scrolled', window.scrollY > 50);
    });

    document.getElementById('contactForm').addEventListener('submit', async function(e) {
      e.preventDefault();
      const button = this.querySelector('button');
      const msgDiv = document.getElementById('formMessage');
      const formData = new FormData(this);

      button.disabled = true;
      button.textContent = 'Sending...';
      msgDiv.innerHTML = '';

      try {
        const res = await fetch('/submit', { method: 'POST', body: formData });
        const data = await res.json();

        if (data.success) {
          msgDiv.innerHTML = '<div class="message success">Sent! Check your WhatsApp</div>';
          this.reset();
        } else {
          msgDiv.innerHTML = '<div class="message error">' + data.message + '</div>';
        }
      } catch (err) {
        msgDiv.innerHTML = '<div class="message error">No internet connection</div>';
      } finally {
        button.disabled = false;
        button.textContent = 'Send Message';
      }
    });
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        message = request.form['message'].strip()

        # Send Email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = f"New Lead: {name}"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        server.quit()

        # Auto Open WhatsApp Web with pre-filled message
        whatsapp_text = urllib.parse.quote(f"New Lead!\nName: {name}\nEmail: {email}\nMessage: {message}")
        whatsapp_url = f"https://web.whatsapp.com/send?phone={WHATSAPP_NUMBER}&text={whatsapp_text}"
        
        def open_whatsapp():
            time.sleep(2)
            webbrowser.open(whatsapp_url)
        
        threading.Thread(target=open_whatsapp, daemon=True).start()

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    print("\n CONNECTOMEDIA WEBSITE IS LIVE! \n")
    print("   Website → http://127.0.0.1:5000")
    print("   When someone submits → You get Email + WhatsApp opens automatically!\n")
    app.run(debug=True, port=5000)
