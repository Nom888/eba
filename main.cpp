#include <iostream>
#include <App.h>
#include <unistd.h>

#define US_LISTEN_REUSE_PORT 1

int main() {
    const int port = 9001;

    for (int i = 0; i < 3; ++i) {
        if (!fork()) {
            break;
        }
    }

    const char* content = R"(
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KNEW Project | The Future of Blockman Go</title>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&family=Tajawal:wght@400;700&display=swap" rel="stylesheet">

    <style>
        :root {
            --primary-color: #0D0D2B;
            --secondary-color: #1A1A3D;
            --accent-color: #3D5AFE;
            --telegram-color: #24A1DE;
            --text-color: #FFFFFF;
            --glow-color: rgba(61, 90, 254, 0.7);
        }

        html[lang="ar"] {
            direction: rtl;
            font-family: 'Tajawal', sans-serif;
        }

        body {
            font-family: 'Montserrat', sans-serif;
            background-color: var(--primary-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
            line-height: 1.6;
            overflow-x: hidden;
        }

        #particles-js {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1;
            background-color: var(--primary-color);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 2;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
        }

        .logo {
            font-size: 2.5em;
            font-weight: 900;
            color: var(--text-color);
            text-shadow: 0 0 10px var(--glow-color);
        }

        .lang-switcher button {
            background: none;
            border: 1px solid var(--accent-color);
            color: var(--text-color);
            padding: 8px 15px;
            margin-left: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
        }
        
        html[lang="ar"] .lang-switcher button {
            margin-left: 0;
            margin-right: 10px;
        }

        .lang-switcher button:hover,
        .lang-switcher button.active {
            background-color: var(--accent-color);
            box-shadow: 0 0 15px var(--glow-color);
        }

        .hero {
            text-align: center;
            padding: 100px 0;
        }

        .hero .coming-soon {
            display: inline-block;
            background-color: var(--accent-color);
            color: white;
            padding: 5px 20px;
            border-radius: 20px;
            font-weight: bold;
            margin-bottom: 20px;
            box-shadow: 0 0 15px var(--glow-color);
        }

        .hero h1 {
            font-size: 4em;
            font-weight: 900;
            margin-bottom: 20px;
            line-height: 1.2;
            text-shadow: 0 0 20px var(--glow-color);
        }

        .hero p {
            font-size: 1.5em;
            max-width: 700px;
            margin: 0 auto 40px;
            opacity: 0.8;
        }

        .cta-buttons a {
            background-color: var(--telegram-color);
            color: var(--text-color);
            padding: 15px 35px;
            text-decoration: none;
            border-radius: 5px;
            margin: 0 10px;
            font-size: 1.1em;
            font-weight: bold;
            transition: all 0.3s ease;
            display: inline-block;
        }

        .cta-buttons a:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2), 0 0 20px var(--telegram-color);
        }
        
        .cta-buttons .secondary-btn {
            background-color: transparent;
            border: 2px solid var(--telegram-color);
        }

        .features {
            padding: 80px 0;
            text-align: center;
        }

        .features h2 {
            font-size: 3em;
            margin-bottom: 60px;
            text-shadow: 0 0 15px var(--glow-color);
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 40px;
        }

        .feature-card {
            background-color: var(--secondary-color);
            padding: 40px 20px;
            border-radius: 10px;
            border: 1px solid var(--accent-color);
            box-shadow: 0 0 20px rgba(61, 90, 254, 0.2);
            transition: all 0.3s ease;
        }
        
        html[lang="ar"] .feature-card {
            text-align: right;
        }

        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 0 30px var(--glow-color);
        }

        .feature-card i {
            font-size: 3em;
            color: var(--accent-color);
            margin-bottom: 20px;
        }

        .feature-card h3 {
            font-size: 1.5em;
            margin-bottom: 10px;
        }

        .join-us {
            background: linear-gradient(45deg, var(--accent-color), #24A1DE);
            padding: 80px 20px;
            text-align: center;
            border-radius: 15px;
            margin: 50px 0;
        }
        
        .join-us h2 {
            font-size: 2.8em;
            margin-bottom: 20px;
        }

        .join-us p {
            font-size: 1.2em;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
            margin-bottom: 30px;
        }

        .join-us .telegram-btn {
            background-color: var(--text-color);
            color: var(--telegram-color);
            font-size: 1.2em;
        }
        
        .join-us .telegram-btn i {
            margin-right: 10px;
        }
        
        html[lang="ar"] .join-us .telegram-btn i {
            margin-right: 0;
            margin-left: 10px;
        }

        footer {
            text-align: center;
            padding: 40px 0;
            border-top: 1px solid var(--secondary-color);
        }

        @media (max-width: 768px) {
            .hero h1 { font-size: 2.8em; }
            .hero p { font-size: 1.2em; }
            .features h2, .join-us h2 { font-size: 2.2em; }
            .cta-buttons a { margin-bottom: 15px; width: 80%; }
        }
    </style>
</head>
<body>

    <div id="particles-js"></div>

    <div class="container">
        <header>
            <div class="logo">KNEW</div>
            <nav class="lang-switcher">
                <button data-lang="en">EN</button>
                <button data-lang="ru">RU</button>
                <button data-lang="ar">AR</button>
            </nav>
        </header>

        <main>
            <section class="hero">
                <div class="coming-soon" data-translate="coming_soon">COMING SOON</div>
                <h1 data-translate="hero_title">A New Era of Blockman Go</h1>
                <p data-translate="hero_subtitle">Get ready for a fresh take on your favorite game. A rebalanced experience, community events, and a vibrant player base are on the horizon.</p>
                <div class="cta-buttons">
                    <a href="https://t.me/kn_ew" target="_blank" data-translate="btn_join_channel"><i class="fab fa-telegram-plane"></i> Follow News</a>
                    <a href="https://t.me/+Ex5ukUDa1RRkMmIy" target="_blank" class="secondary-btn" data-translate="btn_join_group">Join Community</a>
                </div>
            </section>

            <section class="features">
                <h2 data-translate="features_title">What to Expect?</h2>
                <div class="features-grid">
                    <div class="feature-card">
                        <i class="fas fa-balance-scale"></i>
                        <h3 data-translate="feature1_title">Generous Economy</h3>
                        <p data-translate="feature1_desc">Experience a balanced economy where your efforts are truly rewarded. Get easier access to items without the harsh grind.</p>
                    </div>
                    <div class="feature-card">
                        <i class="fas fa-users"></i>
                        <h3 data-translate="feature2_title">Community Events</h3>
                        <p data-translate="feature2_desc">Become part of a server where players matter. We plan to host regular events, contests, and activities shaped by community feedback.</p>
                    </div>
                    <div class="feature-card">
                        <i class="fas fa-rocket"></i>
                        <h3 data-translate="feature3_title">Optimized Gameplay</h3>
                        <p data-translate="feature3_desc">Enjoy a smoother, more stable gaming experience. We are focused on technical excellence to ensure less lag and more fun.</p>
                    </div>
                </div>
            </section>

            <section class="join-us">
                <h2 data-translate="join_title">Be the First to Know!</h2>
                <p data-translate="join_subtitle">The revolution is in the works! Join our Telegram for development updates, sneak peeks, and the official launch announcement. We will also be announcing our Discord server soon!</p>
                <a href="https://t.me/kn_ew" target="_blank" class="cta-buttons telegram-btn" data-translate="btn_join_now"><i class="fab fa-telegram-plane"></i> Follow the Project</a>
            </section>
        </main>

        <footer>
            <p data-translate="footer_text">&copy; 2024 KNEW Project. All rights reserved. This is an unofficial private server for Blockman Go.</p>
        </footer>
    </div>

    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS("particles-js", {
            "particles": {
                "number": {"value": 80, "density": {"enable": true, "value_area": 800}},
                "color": {"value": "#3D5AFE"},
                "shape": {"type": "circle", "stroke": {"width": 0, "color": "#000000"}, "polygon": {"nb_sides": 5}},
                "opacity": {"value": 0.5, "random": false, "anim": {"enable": false, "speed": 1, "opacity_min": 0.1, "sync": false}},
                "size": {"value": 3, "random": true, "anim": {"enable": false, "speed": 40, "size_min": 0.1, "sync": false}},
                "line_linked": {"enable": true, "distance": 150, "color": "#ffffff", "opacity": 0.2, "width": 1},
                "move": {"enable": true, "speed": 2, "direction": "none", "random": false, "straight": false, "out_mode": "out", "bounce": false, "attract": {"enable": false, "rotateX": 600, "rotateY": 1200}}
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {"onhover": {"enable": true, "mode": "repulse"}, "onclick": {"enable": true, "mode": "push"}, "resize": true},
                "modes": {"grab": {"distance": 400, "line_linked": {"opacity": 1}}, "bubble": {"distance": 400, "size": 40, "duration": 2, "opacity": 8, "speed": 3}, "repulse": {"distance": 200, "duration": 0.4}, "push": {"particles_nb": 4}, "remove": {"particles_nb": 2}}
            },
            "retina_detect": true
        });
    </script>
    
    <script>
        const translations = {
            'en': {
                'page_title': 'KNEW Project | The Future of Blockman Go',
                'coming_soon': 'COMING SOON',
                'hero_title': 'A New Era of Blockman Go',
                'hero_subtitle': 'Get ready for a fresh take on your favorite game. A rebalanced experience, community events, and a vibrant player base are on the horizon.',
                'btn_join_channel': '<i class="fab fa-telegram-plane"></i> Follow News',
                'btn_join_group': 'Join Community',
                'features_title': 'What to Expect?',
                'feature1_title': 'Generous Economy',
                'feature1_desc': 'Experience a balanced economy where your efforts are truly rewarded. Get easier access to items without the harsh grind.',
                'feature2_title': 'Community Events',
                'feature2_desc': 'Become part of a server where players matter. We plan to host regular events, contests, and activities shaped by community feedback.',
                'feature3_title': 'Optimized Gameplay',
                'feature3_desc': 'Enjoy a smoother, more stable gaming experience. We are focused on technical excellence to ensure less lag and more fun.',
                'join_title': 'Be the First to Know!',
                'join_subtitle': 'The revolution is in the works! Join our Telegram for development updates, sneak peeks, and the official launch announcement. We will also be announcing our Discord server soon!',
                'btn_join_now': '<i class="fab fa-telegram-plane"></i> Follow the Project',
                'footer_text': '&copy; 2024 KNEW Project. All rights reserved. This is an unofficial private server for Blockman Go.'
            },
            'ru': {
                'page_title': 'Проект KNEW | Будущее Blockman Go',
                'coming_soon': 'СКОРО',
                'hero_title': 'Новая Эра Blockman Go',
                'hero_subtitle': 'Приготовьтесь к свежему взгляду на любимую игру. Вас ждёт переработанный баланс, события от сообщества и активная база игроков.',
                'btn_join_channel': '<i class="fab fa-telegram-plane"></i> Следить за Новостями',
                'btn_join_group': 'Вступить в Сообщество',
                'features_title': 'Что вас ожидает?',
                'feature1_title': 'Щедрая Экономика',
                'feature1_desc': 'Оцените сбалансированную экономику, где ваши старания вознаграждаются. Получайте предметы легче и без изнурительного гринда.',
                'feature2_title': 'События от Сообщества',
                'feature2_desc': 'Станьте частью сервера, где игроки имеют значение. Мы планируем проводить регулярные ивенты и конкурсы с учётом ваших пожеланий.',
                'feature3_title': 'Оптимизированный Геймплей',
                'feature3_desc': 'Наслаждайтесь более плавным и стабильным игровым процессом. Мы сосредоточены на техническом качестве, чтобы обеспечить меньше лагов и больше удовольствия.',
                'join_title': 'Узнайте первыми!',
                'join_subtitle': 'Революция в разработке! Присоединяйтесь к нашему Telegram, чтобы следить за новостями, видеть эксклюзивные материалы и не пропустить анонс даты запуска. Скоро мы также анонсируем наш Discord сервер!',
                'btn_join_now': '<i class="fab fa-telegram-plane"></i> Следить за проектом',
                'footer_text': '&copy; 2024 Проект KNEW. Все права защищены. Это неофициальный приватный сервер Blockman Go.'
            },
            'ar': {
                'page_title': 'مشروع KNEW | مستقبل Blockman Go',
                'coming_soon': 'قريبًا',
                'hero_title': 'عصر جديد من Blockman Go',
                'hero_subtitle': 'استعد لنظرة جديدة على لعبتك المفضلة. تجربة متوازنة، فعاليات مجتمعية، وقاعدة لاعبين نابضة بالحياة في الأفق.',
                'btn_join_channel': '<i class="fab fa-telegram-plane"></i> تابع الأخبار',
                'btn_join_group': 'انضم للمجتمع',
                'features_title': 'ماذا تتوقع؟',
                'feature1_title': 'اقتصاد سخي',
                'feature1_desc': 'جرّب اقتصادًا متوازنًا حيث تُكافأ جهودك حقًا. احصل على العناصر بسهولة أكبر دون الحاجة إلى اللعب الممل والمتكرر.',
                'feature2_title': 'فعاليات مجتمعية',
                'feature2_desc': 'كن جزءًا من سيرفر يهتم باللاعبين. نخطط لاستضافة فعاليات ومسابقات وأنشطة منتظمة يتم تشكيلها بناءً على آراء المجتمع.',
                'feature3_title': 'لعب مُحسَّن',
                'feature3_desc': 'استمتع بتجربة لعب أكثر سلاسة واستقرارًا. نحن نركز على التميز التقني لضمان تقليل التأخير وزيادة المتعة.',
                'join_title': 'كن أول من يعلم!',
                'join_subtitle': 'الثورة قيد الإعداد! انضم إلى قناتنا على تيليجرام لمتابعة تحديثات التطوير، والحصول على لمحات حصرية، وعدم تفويت إعلان الإطلاق الرسمي. سنعلن أيضًا عن سيرفر ديسكورد الخاص بنا قريبًا!',
                'btn_join_now': '<i class="fab fa-telegram-plane"></i> تابع المشروع',
                'footer_text': '&copy; 2024 مشروع KNEW. جميع الحقوق محفوظة. هذا سيرفر خاص غير رسمي للعبة Blockman Go.'
            }
        };

        const langSwitcher = document.querySelector('.lang-switcher');
        const langButtons = document.querySelectorAll('[data-lang]');
        const translatableElements = document.querySelectorAll('[data-translate]');

        const setLanguage = (lang) => {
            document.documentElement.lang = lang;
            document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';

            document.title = translations[lang]['page_title'];

            translatableElements.forEach(el => {
                const key = el.dataset.translate;
                if (translations[lang][key]) {
                    el.innerHTML = translations[lang][key];
                }
            });

            langButtons.forEach(btn => {
                btn.classList.remove('active');
                if (btn.dataset.lang === lang) {
                    btn.classList.add('active');
                }
            });

            localStorage.setItem('knew_lang', lang);
        };

        langSwitcher.addEventListener('click', (event) => {
            if (event.target.tagName === 'BUTTON') {
                const lang = event.target.dataset.lang;
                if (lang) {
                    setLanguage(lang);
                }
            }
        });

        document.addEventListener('DOMContentLoaded', () => {
            const savedLang = localStorage.getItem('knew_lang');
            if (savedLang && translations[savedLang]) {
                setLanguage(savedLang);
            } else {
                const browserLang = navigator.language.split('-')[0];
                const defaultLang = translations[browserLang] ? browserLang : 'en';
                setLanguage(defaultLang);
            }
        });
    </script>
</body>
</html>
)";

    uWS::App{}.get("/*", [content](auto *res, auto *req) {
        res->writeStatus("200 OK")
           ->writeHeader("Content-Type", "text/html")
           ->end(content);
    }).listen(port, US_LISTEN_REUSE_PORT, [port](auto *listen_socket) {
        if (listen_socket) {
            std::cout << "Процесс " << getpid() << " слушает порт " << port << std::endl;
        } else {
            std::cout << "Процесс " << getpid() << " НЕ СМОГ занять порт " << port << std::endl;
        }
    }).run();
}
