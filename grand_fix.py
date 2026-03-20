import os
import re

dir_path = r'c:\Users\jmaslowski\OneDrive - DRAGONFLY.PL Sp. z o.o\JAKUB-domowy\_git\stronka internetowaq'
files = ['index.html', 'faq.html', 'kontakt.html', 'oferta.html', 'demo.html']

for f in files:
    fp = os.path.join(dir_path, f)
    if not os.path.exists(fp): continue
    with open(fp, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 1. Fix Dark Mode Tab Switching FOUC
    content = content.replace("transition: background 0.5s, color 0.5s;", "")
    
    if "<script>if(localStorage.getItem('theme') === 'dark') document.body.classList.add('dark-mode');</script>" not in content:
        content = content.replace("<body>", "<body>\n    <script>if(localStorage.getItem('theme') === 'dark') document.body.classList.add('dark-mode');</script>")
    
    # Update toggleTheme in JS to add transition dynamically so it only animates on click, not page load
    old_toggle = """function applyTheme(theme) {
            const icon = document.querySelector('.theme-toggle i');
            if (theme === 'dark') {
                document.body.classList.add('dark-mode');
                if (icon) icon.classList.replace('fa-moon', 'fa-sun');
            } else {
                document.body.classList.remove('dark-mode');
                if (icon) icon.classList.replace('fa-sun', 'fa-moon');
            }
        }

        function toggleTheme() {
            const current = localStorage.getItem('theme') === 'dark' ? 'light' : 'dark';
            localStorage.setItem('theme', current);
            applyTheme(current);
        }"""
        
    new_toggle = """function applyTheme(theme) {
            const icon = document.querySelector('.theme-toggle i');
            if (theme === 'dark') {
                document.body.classList.add('dark-mode');
                if (icon) icon.classList.replace('fa-moon', 'fa-sun');
            } else {
                document.body.classList.remove('dark-mode');
                if (icon) icon.classList.replace('fa-sun', 'fa-moon');
            }
        }

        function toggleTheme() {
            document.body.style.transition = 'background 0.5s, color 0.5s'; 
            const current = localStorage.getItem('theme') === 'dark' ? 'light' : 'dark';
            localStorage.setItem('theme', current);
            applyTheme(current);
        }"""
    content = content.replace(old_toggle, new_toggle)
    
    # Remove the old savedTheme logic at the bottom so it doesn't run twice
    content = re.sub(r'// 1\. Sprawdź zapisany motyw przy starcie\s*const savedTheme = localStorage\.getItem\(\'theme\'\);\s*if \(savedTheme\) \{\s*applyTheme\(savedTheme\);\s*\}', '', content)

    # 2. Fix Kontakt.html Completely
    if f == 'kontakt.html':
        # Fix broken head tag if exists
        head_end = content.find('</nav>\n        </div>\n    </hea') 
        if head_end != -1:
            content = content[:head_end] + '</nav>\n        </div>\n    </header>' + content[head_end+len('</nav>\n        </div>\n    </hea'):]
        
        kontakt_main = """
<main style="flex-grow: 1; display: flex; align-items: center; padding: 40px 0;">
    <section class="contact-section">
        <div class="container">
            <div class="contact-grid">
                <div class="contact-info reveal active">
                    <p style="color: var(--primary); font-weight: 700; text-transform: uppercase; letter-spacing: 2px; font-size: 0.85rem; margin-bottom: 10px;">Masz pytania?</p>
                    <h2>Bądźmy w kontakcie</h2>
                    <p class="desc">Zastanawiasz się nad inteligentnym domem? Rozwieję Twoje wątpliwości. Napisz do mnie lub zadzwoń, a przygotuję darmową wstępną wycenę dla Twojego budynku.</p>
                    <div class="contact-method">
                        <div class="contact-icon"><i class="fa-solid fa-envelope"></i></div>
                        <div class="method-text">
                            <h4>Email</h4>
                            <a href="mailto:kontakt@massmarth.pl">kontakt@massmarth.pl</a>
                        </div>
                    </div>
                    <div class="contact-method">
                        <div class="contact-icon"><i class="fa-brands fa-linkedin"></i></div>
                        <div class="method-text">
                            <h4>LinkedIn</h4>
                            <a href="#">Profil MasSmartH</a>
                        </div>
                    </div>
                </div>
                <div class="contact-form-box reveal active">
                    <h3 style="font-size: 1.8rem; margin-bottom: 25px; color: var(--dark);">Wyślij wiadomość</h3>
                    <form onsubmit="event.preventDefault(); alert('Dziękuję za wiadomość! Odezwiemy się wkrótce.');">
                        <div class="form-group">
                            <label>Twoje Imię</label>
                            <input type="text" class="form-control" placeholder="Jan Kowalski" required>
                        </div>
                        <div class="form-group">
                            <label>Twój adres E-mail</label>
                            <input type="email" class="form-control" placeholder="jan@example.com" required>
                        </div>
                        <div class="form-group">
                            <label>Wiadomość</label>
                            <textarea class="form-control" placeholder="Opisz krótko o co chciałbyś zapytać..." required></textarea>
                        </div>
                        <button type="submit" class="btn" style="width: 100%; border-radius: 12px; margin-top: 10px;">Wyślij zapytanie <i class="fa-solid fa-paper-plane" style="margin-left: 8px;"></i></button>
                    </form>
                </div>
            </div>
        </div>
    </section>
</main>
"""
        start = content.find('</header>') + len('</header>')
        end = content.find('<footer>')
        content = content[:start] + kontakt_main + content[end:]

    # 3. Add Animations to index.html
    if f == 'index.html':
        anim_css = """
        /* Premium Animations */
        @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-15px); } 100% { transform: translateY(0px); } }
        @keyframes pulse-glow { 0% { box-shadow: 0 0 0 0 rgba(99,102,241,0.5); } 70% { box-shadow: 0 0 0 15px rgba(99,102,241,0); } 100% { box-shadow: 0 0 0 0 rgba(99,102,241,0); } }
        .hero-actions .btn:not(.btn-outline) { animation: pulse-glow 2.5s infinite; }
        .portfolio-item { animation: float 6s ease-in-out infinite; }
        .portfolio-item:nth-child(2) { animation-delay: 1s; }
        .portfolio-item:nth-child(3) { animation-delay: 2s; }
        .portfolio-item:nth-child(4) { animation-delay: 3s; }
        .hero { position: relative; overflow: hidden; }
        .hero::before { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle at 50% 50%, rgba(99,102,241,0.03) 0%, transparent 40%); animation: spin 30s linear infinite; z-index: -1; pointer-events: none;}
        @keyframes spin { 100% { transform: rotate(360deg); } }
        """
        if "Premium Animations" not in content:
            style_idx = content.rfind('</style>')
            content = content[:style_idx] + anim_css + content[style_idx:]

    # 4. FAQ Search Implementation
    if f == 'faq.html':
        faq_js = """
        // Wyszukiwarka FAQ
        const searchInput = document.querySelector('.faq-search input');
        if(searchInput) {
            searchInput.addEventListener('input', (e) => {
                const term = e.target.value.toLowerCase();
                document.querySelectorAll('.faq-item').forEach(item => {
                    const q = item.querySelector('.faq-question').innerText.toLowerCase();
                    const a = item.querySelector('.faq-answer').innerText.toLowerCase();
                    if(q.includes(term) || a.includes(term)) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            });
        }
        """
        if "Wyszukiwarka FAQ" not in content:
            script_idx = content.rfind('</script>')
            content = content[:script_idx] + faq_js + content[script_idx:]

    with open(fp, 'w', encoding='utf-8') as file:
        file.write(content)

print("success")
