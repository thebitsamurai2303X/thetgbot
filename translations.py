"""Simple translation strings for supported languages."""
from typing import Dict

SUPPORTED_LANGS = {
    'en': 'English',
    'ru': 'Russian',
    'ar': 'Arabic',
    'es': 'Spanish',
    'az': 'Azerbaijani',
    'tr': 'Turkish',
    'fr': 'French',
    'de': 'German',
}

_STRINGS: Dict[str, Dict[str, str]] = {}


def _add(lang: str, strings: Dict[str, str]):
    _STRINGS[lang] = strings


# English
_add('en', {
    'choose_language': 'Select language',
    'welcome': '''🎨 Hi! I'm a Font Bot. Send me any text and I'll create stylish and unique fonts for you!

👨‍💻 Created by: @thebitsamurai
🤖 Other projects: @ytdlpload_bot
📢 Community: @ytdlpdeveloper''',
    'subscription_required': '❗️ Please subscribe to @ytdlpdeveloper to use this bot!\n\nClick the button below when you\'re done.',
    'check_subscription': '✅ Check Subscription',
    'subscription_confirmed': '✅ Thank you for subscribing! You can now use the bot.',
    'no_fonts': 'No fonts found. Run the downloader to populate the fonts/ folder.',
})

# Russian
_add('ru', {
    'choose_language': 'Выберите язык',
    'welcome': '''🎨 Привет! Я бот шрифтов. Пришли мне любой текст, и я отправлю тебе стильные и уникальные шрифты!

👨‍💻 Разработано: @thebitsamurai
🤖 Остальные проекты: @ytdlpload_bot
📢 ТГК: @ytdlpdeveloper''',
    'subscription_required': '❗️ Пожалуйста, подпишись на канал @ytdlpdeveloper чтобы использовать бота!\n\nНажми на кнопку ниже, когда будешь готов.',
    'check_subscription': '✅ Проверить подписку',
    'subscription_confirmed': '✅ Спасибо за подписку! Теперь ты можешь использовать бота.',
    'no_fonts': 'Шрифты не найдены. Запустите downloader чтобы заполнить папку fonts/.',
})

# Arabic
_add('ar', {
    'choose_language': 'اختر اللغة',
    'welcome': '''🎨 مرحباً! أنا بوت الخطوط. أرسل لي أي نص وسأرسل لك خطوطاً مميزة وفريدة!

👨‍💻 تم التطوير بواسطة: @thebitsamurai
🤖 المشاريع الأخرى: @ytdlpload_bot
📢 المجتمع: @ytdlpdeveloper''',
    'subscription_required': '❗️ يرجى الاشتراك في @ytdlpdeveloper لاستخدام البوت!\n\nانقر على الزر أدناه عند الانتهاء.',
    'check_subscription': '✅ تحقق من الاشتراك',
    'subscription_confirmed': '✅ شكراً لاشتراكك! يمكنك الآن استخدام البوت.',
    'no_fonts': 'لم يتم العثور على خطوط. شغّل أداة تنزيل الخطوط.',
})

# Spanish
_add('es', {
    'choose_language': 'Seleccione el idioma',
    'welcome': '''🎨 ¡Hola! Soy el Bot de Fuentes. ¡Envíame cualquier texto y te enviaré fuentes elegantes y únicas!

👨‍💻 Creado por: @thebitsamurai
🤖 Otros proyectos: @ytdlpload_bot
📢 Comunidad: @ytdlpdeveloper''',
    'subscription_required': '❗️ ¡Por favor suscríbete a @ytdlpdeveloper para usar este bot!\n\nHaz clic en el botón de abajo cuando hayas terminado.',
    'check_subscription': '✅ Verificar Suscripción',
    'subscription_confirmed': '✅ ¡Gracias por suscribirte! Ahora puedes usar el bot.',
    'no_fonts': 'No se encontraron fuentes. Ejecuta el descargador para llenar la carpeta fonts/.',
})

# Azerbaijani
_add('az', {
    'choose_language': 'Dili seçin',
    'welcome': '''🎨 Salam! Mən Şrift Botuyam. Mənə istənilən mətn göndərin və mən sizə stillı və unikal şriftlər göndərəcəm!

👨‍💻 Yaradıcı: @thebitsamurai
🤖 Digər layihələr: @ytdlpload_bot
📢 İcma: @ytdlpdeveloper''',
    'subscription_required': '❗️ Zəhmət olmasa, botu istifadə etmək üçün @ytdlpdeveloper kanalına abunə olun!\n\nHazır olduqda aşağıdakı düyməyə klikləyin.',
    'check_subscription': '✅ Abunəliyi Yoxla',
    'subscription_confirmed': '✅ Abunə olduğunuz üçün təşəkkür edirik! İndi botu istifadə edə bilərsiniz.',
    'no_fonts': 'Şriftlər tapılmadı. Fonts qovluğunu doldurmaq üçün yükləyicini işə salın.',
})

# Turkish
_add('tr', {
    'choose_language': 'Dil seçin',
    'welcome': '''🎨 Merhaba! Ben Font Botu. Bana herhangi bir metin gönder ve sana şık ve benzersiz fontlar göndereceğim!

👨‍💻 Geliştirici: @thebitsamurai
🤖 Diğer projeler: @ytdlpload_bot
📢 Topluluk: @ytdlpdeveloper''',
    'subscription_required': '❗️ Lütfen botu kullanmak için @ytdlpdeveloper kanalına abone olun!\n\nHazır olduğunuzda aşağıdaki butona tıklayın.',
    'check_subscription': '✅ Aboneliği Kontrol Et',
    'subscription_confirmed': '✅ Abone olduğunuz için teşekkürler! Artık botu kullanabilirsiniz.',
    'no_fonts': 'Yazı tipi bulunamadı. fonts/ klasörünü doldurmak için indiriciyi çalıştırın.',
})

# French
_add('fr', {
    'choose_language': 'Choisir la langue',
    'welcome': '''🎨 Salut ! Je suis le Bot de Polices. Envoyez-moi n'importe quel texte et je vous enverrai des polices élégantes et uniques !

👨‍💻 Créé par : @thebitsamurai
🤖 Autres projets : @ytdlpload_bot
📢 Communauté : @ytdlpdeveloper''',
    'subscription_required': '❗️ Veuillez vous abonner à @ytdlpdeveloper pour utiliser ce bot !\n\nCliquez sur le bouton ci-dessous une fois terminé.',
    'check_subscription': '✅ Vérifier l\'abonnement',
    'subscription_confirmed': '✅ Merci de votre abonnement ! Vous pouvez maintenant utiliser le bot.',
    'no_fonts': 'Aucune police trouvée. Lancez le téléchargeur pour remplir le dossier fonts/.',
})

# German
_add('de', {
    'choose_language': 'Sprache wählen',
    'welcome': '''🎨 Hallo! Ich bin der Schriftarten-Bot. Sende mir einen beliebigen Text und ich schicke dir stilvolle und einzigartige Schriftarten!

👨‍💻 Entwickelt von: @thebitsamurai
🤖 Andere Projekte: @ytdlpload_bot
📢 Community: @ytdlpdeveloper''',
    'subscription_required': '❗️ Bitte abonniere @ytdlpdeveloper um diesen Bot zu nutzen!\n\nKlicke unten wenn du fertig bist.',
    'check_subscription': '✅ Abonnement prüfen',
    'subscription_confirmed': '✅ Danke fürs Abonnieren! Du kannst den Bot jetzt nutzen.',
    'no_fonts': 'Keine Schriftarten gefunden. Führe den Downloader aus, um den Ordner fonts/ zu füllen.',
})


def get(lang: str, key: str) -> str:
    if lang not in _STRINGS:
        lang = 'en'
    return _STRINGS[lang].get(key, _STRINGS['en'].get(key, ''))
