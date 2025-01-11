// static/js/script.js  
  
document.addEventListener('DOMContentLoaded', function () {  
    /* Time Zone Display */  
    function updateTime() {  
        const japanTime = new Date().toLocaleString("en-US", {  
            timeZone: "Asia/Tokyo",  
            hour: '2-digit',  
            minute: '2-digit',  
            second: '2-digit',  
            hour12: false  
        });  
        const nepalTime = new Date().toLocaleString("en-US", {  
            timeZone: "Asia/Kathmandu",  
            hour: '2-digit',  
            minute: '2-digit',  
            second: '2-digit',  
            hour12: false  
        });  
  
        const japanTimeElement = document.getElementById('japan-time');  
        const nepalTimeElement = document.getElementById('nepal-time');  
  
        if (japanTimeElement) {  
            japanTimeElement.textContent = `Japan: ${japanTime}`;  
        }  
        if (nepalTimeElement) {  
            nepalTimeElement.textContent = `Nepal: ${nepalTime}`;  
        }  
    }  
  
    updateTime();  
    setInterval(updateTime, 1000); // Refresh every second  
  
    /* Theme Toggle Switch */  
    const themeCheckbox = document.getElementById('theme-checkbox');  
  
    if (themeCheckbox) {  
        themeCheckbox.addEventListener('change', function () {  
            const htmlElement = document.documentElement;  
            if (this.checked) {  
                htmlElement.setAttribute('data-theme', 'dark');  
                localStorage.setItem('theme', 'dark');  
            } else {  
                htmlElement.setAttribute('data-theme', 'light');  
                localStorage.setItem('theme', 'light');  
            }  
        });  
  
        /* Apply Saved Theme on Page Load */  
        const savedTheme = localStorage.getItem('theme') || 'light';  
        document.documentElement.setAttribute('data-theme', savedTheme);  
        if (savedTheme === 'dark') {  
            themeCheckbox.checked = true;  
        } else {  
            themeCheckbox.checked = false;  
        }  
    }  
  
    /* Language Switcher */  
    const languageSwitcher = document.getElementById('language-switcher');  
    const langElements = document.querySelectorAll('[data-lang-key]');  
  
    const translations = {  
        en: {  
            'welcome-message': 'Welcome to Sakura News Network',  
            'tagline': 'Your trusted source for the latest news and insights.',  
            'home': 'Home',  
            'about': 'About',  
            'contact': 'Contact',  
            'categories': 'Categories',  
            'politics': 'Politics',  
            'technology': 'Technology',  
            'entertainment': 'Entertainment',  
            'business': 'Business',  
            'breaking': 'Breaking',  
            'read_more': 'Read More',  
            'latest_news': 'Latest News',  
            'about-us': 'About Us',  
            'about-desc': 'Sakura News is your trusted source for the latest news and in-depth analysis from around the world.',  
            'quick-links': 'Quick Links',  
            'follow-us': 'Follow Us',  
            'rights-reserved': 'All rights reserved',  
            'send_message': 'Send Message',  
            'subscribe': 'Subscribe to Our Newsletter',  
            'newsletter-desc': 'Stay updated with the latest news and exclusive content.',  
            'subscribe-btn': 'Subscribe',  
            'site-title': 'Sakura News Network'  
        },  
        np: {  
            'welcome-message': 'साकुरा न्युज नेटवर्कमा स्वागत छ',  
            'tagline': 'अन्तर्राष्ट्रिय स्तरको समाचार र विश्लेषणको लागि तपाईंको विश्वासिलो स्रोत।',  
            'home': 'होम',  
            'about': 'हाम्रोबारे',  
            'contact': 'सम्पर्क',  
            'categories': 'वर्गहरू',  
            'politics': 'राजनीति',  
            'technology': 'प्रविधि',  
            'entertainment': 'मनोरञ्जन',  
            'business': 'व्यापार',  
            'breaking': 'ताजा',  
            'read_more': 'थप पढ्नुहोस्',  
            'latest_news': 'नवीनतम समाचार',  
            'about-us': 'हाम्रोबारे',  
            'about-desc': 'साकुरा न्युज विश्वभरिबाट नवीनतम समाचार र गहन विश्लेषणको लागि तपाईंको विश्वासिलो स्रोत हो।',  
            'quick-links': 'छिटो लिंकहरू',  
            'follow-us': 'हामीलाई पछ्याउनुहोस्',  
            'rights-reserved': 'सबै अधिकार सुरक्षित',  
            'send_message': 'सन्देश पठाउनुहोस्',  
            'subscribe': 'हाम्रो न्यूजलेटर सदस्यता लिनुहोस्',  
            'newsletter-desc': 'नवीनतम समाचार र विशेष सामग्री संग अपडेट रहनुहोस्।',  
            'subscribe-btn': 'सदस्यता लिनुहोस्',  
            'site-title': 'साकुरा न्युज नेटवर्क'  
        },  
        jp: {  
            'welcome-message': 'サクラニュースネットワークへようこそ',  
            'tagline': '世界中から最新のニュースと洞察をお届けする信頼できる情報源。',  
            'home': 'ホーム',  
            'about': '私たちについて',  
            'contact': 'お問い合わせ',  
            'categories': 'カテゴリー',  
            'politics': '政治',  
            'technology': 'テクノロジー',  
            'entertainment': 'エンターテインメント',  
            'business': 'ビジネス',  
            'breaking': '速報',  
            'read_more': '続きを読む',  
            'latest_news': '最新ニュース',  
            'about-us': '私たちについて',  
            'about-desc': 'さくらニュースは、世界中からの最新ニュースと詳細な分析をお届けする信頼できる情報源です。',  
            'quick-links': 'クイックリンク',  
            'follow-us': 'フォローする',  
            'rights-reserved': '全著作権所有',  
            'send_message': 'メッセージを送る',  
            'subscribe': 'ニュースレターを購読する',  
            'newsletter-desc': '最新のニュースと独占コンテンツをお届けします。',  
            'subscribe-btn': '購読する',  
            'site-title': 'サクラニュースネットワーク'  
        }  
    };  
  
    function changeLanguage(language) {  
        langElements.forEach(element => {  
            const key = element.getAttribute('data-lang-key');  
            if (translations[language] && translations[language][key]) {  
                element.innerHTML = translations[language][key];  
            } else {  
                element.innerHTML = translations['en'][key] || element.innerHTML;  
            }  
        });  
  
        // Save selected language to localStorage  
        localStorage.setItem('language', language);  
    }  
  
    if (languageSwitcher) {  
        languageSwitcher.addEventListener('change', function () {  
            const selectedLanguage = this.value;  
            changeLanguage(selectedLanguage);  
        });  
  
        /* Apply Saved Language on Page Load */  
        const savedLanguage = localStorage.getItem('language') || 'en';  
        languageSwitcher.value = savedLanguage;  
        changeLanguage(savedLanguage);  
    }  
  
    /* Back to Top Button */  
    const backToTopButton = document.getElementById('back-to-top');  
  
    if (backToTopButton) {  
        window.addEventListener('scroll', () => {  
            if (window.pageYOffset > 300) {  
                backToTopButton.style.display = 'block';  
            } else {  
                backToTopButton.style.display = 'none';  
            }  
        });  
  
        backToTopButton.addEventListener('click', () => {  
            window.scrollTo({  
                top: 0,  
                behavior: 'smooth'  
            });  
        });  
    }  
  
    /* Newsletter Form Submission */  
    const newsletterForm = document.getElementById('newsletter-form');  
    if (newsletterForm) {  
        newsletterForm.addEventListener('submit', function (e) {  
            e.preventDefault();  
            // Implement AJAX call or form submission logic  
            alert('Thank you for subscribing!');  
            newsletterForm.reset();  
        });  
    }  
  
    /* Breaking News Ticker */  
    const newsTicker = document.getElementById('news-ticker');  
    if (newsTicker) {  
        const tickerItems = newsTicker.innerHTML;  
        newsTicker.innerHTML += tickerItems; // Duplicate the content for seamless scrolling  
  
        let currentPosition = 0;  
        function scrollTicker() {  
            currentPosition += 1; // Adjust the speed here  
            if (currentPosition >= newsTicker.scrollWidth / 2) {  
                currentPosition = 0;  
            }  
            newsTicker.style.transform = `translateX(-${currentPosition}px)`;  
            requestAnimationFrame(scrollTicker);  
        }  
        scrollTicker();  
    }  
});  