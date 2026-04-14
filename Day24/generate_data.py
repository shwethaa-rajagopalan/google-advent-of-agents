import csv
import argparse 

# Predefined dataset (250 examples generated with Gemini 2.5 Pro)

PREDEFINED_EXAMPLES = [
    ["Hello, how are you today?", "English"],
    ["Hola, ¿cómo estás?", "Spanish"],
    ["Bonjour, comment ça va ?", "French"],
    ["Hallo, wie geht es dir?", "German"],
    ["Ciao, come stai?", "Italian"],
    ["Olá, como você está?", "Portuguese"],
    ["Привет, как дела?", "Russian"],
    ["你好，你今天怎么样？", "Chinese (Simplified)"],
    ["こんにちは、お元気ですか？", "Japanese"],
    ["안녕하세요, 오늘 어떠세요?", "Korean"],
    ["Merhaba, bugün nasılsın?", "Turkish"],
    ["Hej, hur mår du?", "Swedish"],
    ["Hei, hvordan har du det?", "Norwegian"],
    ["Hallo, hoe gaat het met je?", "Dutch"],
    ["Cześć, jak się masz?", "Polish"],
    ["Ahoj, jak se máš?", "Czech"],
    ["Szia, hogy vagy?", "Hungarian"],
    ["Γεια σου, τι κάνεις;", "Greek"],
    ["שלום, מה שלומך?", "Hebrew"],
    ["مرحبا، كيف حالك اليوم؟", "Arabic"],
    ["नमस्ते, आज आप कैसे हैं?", "Hindi"],
    [" خوبی؟ سلام", "Persian (Farsi)"],
    ["Apa kabar hari ini?", "Indonesian"],
    ["Kamusta ka ngayon?", "Tagalog (Filipino)"],
    ["สบายดีไหมวันนี้", "Thai"],
    ["Hôm nay bạn thế nào?", "Vietnamese"],
    ["What's up? 😄", "English"],
    ["¿Qué tal? Todo bien por aquí.", "Spanish"],
    ["Ça roule ? Super et toi ?", "French"],
    ["Alles klar bei dir? 👍", "German"],
    ["Tutto bene, grazie! E tu?", "Italian"],
    ["BRB, need to grab a coffee ☕", "English"],
    ["LOL, that's hilarious 😂", "English"],
    ["No problem!", "English"],
    ["Gracias por tu ayuda.", "Spanish"],
    ["Merci beaucoup!", "French"],
    ["Vielen Dank!", "German"],
    ["Grazie mille!", "Italian"],
    ["Muito obrigado!", "Portuguese"],
    ["Большое спасибо!", "Russian"],
    ["非常感谢！", "Chinese (Simplified)"],
    ["本当にありがとう！", "Japanese"],
    ["정말 고맙습니다!", "Korean"],
    ["Çok teşekkür ederim!", "Turkish"],
    ["Tack så mycket!", "Swedish"],
    ["Tusen takk!", "Norwegian"],
    ["Hartelijk bedankt!", "Dutch"],
    ["Dziękuję bardzo!", "Polish"],
    ["Děkuji mnohokrát!", "Czech"],
    ["Nagyon köszönöm!", "Hungarian"],
    ["Ευχαριστώ πολύ!", "Greek"],
    ["תודה רבה!", "Hebrew"],
    ["شكرا جزيلا!", "Arabic"],
    ["बहुत धन्यवाद!", "Hindi"],
    ["خیلی ممنون!", "Persian (Farsi)"],
    ["Terima kasih banyak!", "Indonesian"],
    ["Maraming salamat!", "Tagalog (Filipino)"],
    ["ขอบคุณมากครับ/ค่ะ", "Thai"],
    ["Cảm ơn bạn rất nhiều!", "Vietnamese"],
    ["I'm running a bit late, sorry!", "English"],
    ["Llego un poco tarde, lo siento.", "Spanish"],
    ["Je suis un peu en retard, désolé !", "French"],
    ["Ich bin etwas spät dran, tut mir leid!", "German"],
    ["Sono un po' in ritardo, mi dispiace!", "Italian"],
    ["Estou um pouco atrasado, desculpe!", "Portuguese"],
    ["Я немного опаздываю, извините!", "Russian"],
    ["我有点迟到了，抱歉！", "Chinese (Simplified)"],
    ["少し遅れます、すみません！", "Japanese"],
    ["조금 늦을 것 같아요, 죄송합니다!", "Korean"],
    ["Biraz geç kaldım, özür dilerim!", "Turkish"],
    ["Jag är lite sen, förlåt!", "Swedish"],
    ["Jeg er litt forsinket, beklager!", "Norwegian"],
    ["Ik ben een beetje laat, sorry!", "Dutch"],
    ["Jestem trochę spóźniony, przepraszam!", "Polish"],
    ["Mám trochu zpoždění, omlouvám se!", "Czech"],
    ["Kicsit kések, bocsánat!", "Hungarian"],
    ["Έχω αργήσει λίγο, συγγνώμη!", "Greek"],
    ["אני קצת מאחר, סליחה!", "Hebrew"],
    ["أنا متأخر قليلاً، آسف!", "Arabic"],
    ["मुझे थोड़ी देर हो गई है, माफ़ करना!", "Hindi"],
    ["من کمی دیر کردم، ببخشید!", "Persian (Farsi)"],
    ["Saya agak terlambat, maaf!", "Indonesian"],
    ["Medyo huli na ako, paumanhin!", "Tagalog (Filipino)"],
    ["ฉันมาสายไปหน่อย ขอโทษด้วยนะ", "Thai"],
    ["Tôi đến hơi muộn, xin lỗi!", "Vietnamese"],
    ["Can you send me the file?", "English"],
    ["¿Puedes enviarme el archivo?", "Spanish"],
    ["Peux-tu m'envoyer le fichier ?", "French"],
    ["Kannst du mir die Datei schicken?", "German"],
    ["Puoi inviarmi il file?", "Italian"],
    ["Você pode me enviar o arquivo?", "Portuguese"],
    ["Можешь отправить мне файл?", "Russian"],
    ["你能把文件发给我吗？", "Chinese (Simplified)"],
    ["ファイルを送ってもらえますか？", "Japanese"],
    ["파일 좀 보내줄 수 있어요?", "Korean"],
    ["Dosyayı bana gönderebilir misin?", "Turkish"],
    ["Kan du skicka filen till mig?", "Swedish"],
    ["Kan du sende meg filen?", "Norwegian"],
    ["Kun je me het bestand sturen?", "Dutch"],
    ["Czy możesz wysłać mi plik?", "Polish"],
    ["Můžeš mi poslat ten soubor?", "Czech"],
    ["El tudnád küldeni a fájlt?", "Hungarian"],
    ["Μπορείς να μου στείλεις το αρχείο;", "Greek"],
    ["אתה יכול לשלוח לי את הקובץ?", "Hebrew"],
    ["هل يمكنك إرسال الملف لي؟", "Arabic"],
    ["क्या आप मुझे फ़ाइल भेज सकते हैं?", "Hindi"],
    ["می توانید فایل را برای من ارسال کنید؟", "Persian (Farsi)"],
    ["Bisakah Anda mengirimkan saya filenya?", "Indonesian"],
    ["Maaari mo bang ipadala sa akin ang file?", "Tagalog (Filipino)"],
    ["คุณช่วยส่งไฟล์มาให้ฉันได้ไหม", "Thai"],
    ["Bạn có thể gửi cho tôi tập tin được không?", "Vietnamese"],
    ["That's awesome! 🚀", "English"],
    ["¡Qué genial! 🎉", "Spanish"],
    ["C'est génial ! 🎊", "French"],
    ["Das ist fantastisch! 🌟", "German"],
    ["È fantastico! ✨", "Italian"],
    ["Is this the correct `config.json`?", "English"],
    ["Warte mal, ich check das kurz.", "German"],
    ["Un momento, por favor.", "Spanish"],
    ["Just a sec, I'll check.", "English"],
    ["Мы должны встретиться в 3 часа дня.", "Russian"],
    ["このバグを修正する必要があります。", "Japanese"],
    ["이 버그를 수정해야 합니다.", "Korean"],
    ["Bu hatayı düzeltmemiz gerekiyor.", "Turkish"],
    ["Vi måste fixa den här buggen.", "Swedish"],
    ["Vi må fikse denne feilen.", "Norwegian"],
    ["We moeten deze bug repareren.", "Dutch"],
    ["Musimy naprawić ten błąd.", "Polish"],
    ["Musíme opravit tuto chybu.", "Czech"],
    ["Ki kell javítanunk ezt a hibát.", "Hungarian"],
    ["Πρέπει να διορθώσουμε αυτό το σφάλμα.", "Greek"],
    ["אנחנו צריכים לתקן את הבאג הזה.", "Hebrew"],
    ["يجب علينا إصلاح هذا الخطأ.", "Arabic"],
    ["हमें इस बग को ठीक करना होगा।", "Hindi"],
    ["ما باید این اشکال را برطرف کنیم.", "Persian (Farsi)"],
    ["Kita harus memperbaiki bug ini.", "Indonesian"],
    ["Kailangan nating ayusin ang bug na ito.", "Tagalog (Filipino)"],
    ["เราต้องแก้ไขข้อบกพร่องนี้", "Thai"],
    ["Chúng ta cần sửa lỗi này.", "Vietnamese"],
    ["See you later! 👋", "English"],
    ["¡Hasta luego! 👋", "Spanish"],
    ["À plus tard ! 👋", "French"],
    ["Bis später! 👋", "German"],
    ["A dopo! 👋", "Italian"],
    ["Até logo! 👋", "Portuguese"],
    ["Увидимся! 👋", "Russian"],
    ["再见！👋", "Chinese (Simplified)"],
    ["またね！👋", "Japanese"],
    ["나중에 봐요! 👋", "Korean"],
    ["Görüşürüz! 👋", "Turkish"],
    ["Okay, sounds good.", "English"],
    ["Vale, me parece bien.", "Spanish"],
    ["D'accord, ça me va.", "French"],
    ["Okay, das klingt gut.", "German"],
    ["Va bene, mi sembra buono.", "Italian"],
    ["Ok, parece bom.", "Portuguese"],
    ["Хорошо, звучит неплохо.", "Russian"],
    ["好的，听起来不错。", "Chinese (Simplified)"],
    ["わかった、良さそうだね。", "Japanese"],
    ["알겠어요, 좋은 것 같아요.", "Korean"],
    ["Tamam, kulağa hoş geliyor.", "Turkish"],
    ["Okej, det låter bra.", "Swedish"],
    ["Ok, det høres bra ut.", "Norwegian"],
    ["Oké, dat klinkt goed.", "Dutch"],
    ["Okej, brzmi dobrze.", "Polish"],
    ["Dobře, to zní dobře.", "Czech"],
    ["Rendben, jól hangzik.", "Hungarian"],
    ["Εντάξει, ακούγεται καλό.", "Greek"],
    ["בסדר, נשמע טוב.", "Hebrew"],
    ["حسنًا، هذا يبدو جيدًا.", "Arabic"],
    ["ठीक है, सुनने में अच्छा लग रहा है।", "Hindi"],
    ["باشه، خوب به نظر میرسه.", "Persian (Farsi)"],
    ["Oke, kedengarannya bagus.", "Indonesian"],
    ["Sige, mukhang maganda iyan.", "Tagalog (Filipino)"],
    ["โอเค ฟังดูดีนะ", "Thai"],
    ["Được rồi, nghe có vẻ ổn.", "Vietnamese"],
    ["What time is the meeting? 🕒", "English"],
    ["¿A qué hora es la reunión? 🕒", "Spanish"],
    ["À quelle heure est la réunion ? 🕒", "French"],
    ["Um wie viel Uhr ist das Treffen? 🕒", "German"],
    ["A che ora è la riunione? 🕒", "Italian"],
    ["A que horas é a reunião? 🕒", "Portuguese"],
    ["Во сколько встреча? 🕒", "Russian"],
    ["会议几点开始？🕒", "Chinese (Simplified)"],
    ["会議は何時ですか？🕒", "Japanese"],
    ["회의는 몇 시예요? 🕒", "Korean"],
    ["Toplantı saat kaçta? 🕒", "Turkish"],
    ["När är mötet? 🕒", "Swedish"],
    ["Når er møtet? 🕒", "Norwegian"],
    ["Hoe laat is de vergadering? 🕒", "Dutch"],
    ["O której godzinie jest spotkanie? 🕒", "Polish"],
    ["V kolik hodin je schůzka? 🕒", "Czech"],
    ["Mikor van a találkozó? 🕒", "Hungarian"],
    ["Τι ώρα είναι η συνάντηση; 🕒", "Greek"],
    ["באיזו שעה הפגישה? 🕒", "Hebrew"],
    ["في أي وقت الاجتماع؟ 🕒", "Arabic"],
    ["मीटिंग कितने बजे है? 🕒", "Hindi"],
    ["جلسه ساعت چند است؟ 🕒", "Persian (Farsi)"],
    ["Jam berapa pertemuannya? 🕒", "Indonesian"],
    ["Anong oras ang pulong? 🕒", "Tagalog (Filipino)"],
    ["ประชุมกี่โมง 🕒", "Thai"],
    ["Mấy giờ họp vậy? 🕒", "Vietnamese"],
    ["Let's start the project. 💪", "English"],
    ["Empecemos el proyecto. 💪", "Spanish"],
    ["Commençons le projet. 💪", "French"],
    ["Fangen wir mit dem Projekt an. 💪", "German"],
    ["Iniziamo il progetto. 💪", "Italian"],
    ["Давай начнем проект. 💪", "Russian"],
    ["プロジェクトを始めましょう。💪", "Japanese"],
    ["프로젝트를 시작합시다. 💪", "Korean"],
    ["Haydi projeye başlayalım. 💪", "Turkish"],
    ["My favorite color is blue. What's yours?", "English"],
    ["Mi color favorito es el azul. ¿Cuál es el tuyo?", "Spanish"],
    ["Ma couleur préférée est le bleu. Et la tienne ?", "French"],
    ["Meine Lieblingsfarbe ist Blau. Was ist deine?", "German"],
    ["Il mio colore preferito è il blu. Qual è il tuo?", "Italian"],
    ["Minha cor favorita é azul. Qual é a sua?", "Portuguese"],
    ["Мой любимый цвет - синий. А твой?", "Russian"],
    ["我最喜欢的颜色是蓝色。你的是什么？", "Chinese (Simplified)"],
    ["私の好きな色は青です。あなたのは何色ですか？", "Japanese"],
    ["제가 가장 좋아하는 색은 파란색입니다. 당신은요?", "Korean"],
    ["En sevdiğim renk mavi. Seninki ne?", "Turkish"],
    ["Min favoritfärg är blå. Vilken är din?", "Swedish"],
    ["Min favorittfarge er blå. Hva er din?", "Norwegian"],
    ["Mijn lievelingskleur is blauw. Wat is die van jou?", "Dutch"],
    ["Mój ulubiony kolor to niebieski. A jaki jest twój?", "Polish"],
    ["Moje oblíbená barva je modrá. Jaká je tvoje?", "Czech"],
    ["A kedvenc színem a kék. És a tiéd?", "Hungarian"],
    ["Το αγαπημένο μου χρώμα είναι το μπλε. Ποιο είναι το δικό σου;", "Greek"],
    ["הצבע האהוב עליי הוא כחול. מה שלך?", "Hebrew"],
    ["لوني المفضل هو الأزرق. ما هو لونك المفضل؟", "Arabic"],
    ["मेरा पसंदीदा रंग नीला है। आपका क्या है?", "Hindi"],
    ["رنگ مورد علاقه من آبی است. مال شما چیست؟", "Persian (Farsi)"],
    ["Warna favorit saya adalah biru. Apa warna favoritmu?", "Indonesian"],
    ["Ang paborito kong kulay ay asul. Ano ang sa iyo?", "Tagalog (Filipino)"],
    ["สีที่ฉันชอบคือสีน้ำเงิน คุณล่ะชอบสีอะไร", "Thai"],
    ["Màu yêu thích của tôi là màu xanh dương. Còn bạn thì sao?", "Vietnamese"],
    ["I need help with this code: `print('Hello World')`", "English"],
    ["Este es un mensaje en español con algunos términos en inglés como 'debug' o 'commit'.", "Spanish"],
    ["C'est un message en français avec des mots anglais : 'weekend', 'cool'.", "French"],
    ["Das ist eine deutsche Nachricht, aber ich sage manchmal 'OK'.", "German"],
    ["Questo è un messaggio in italiano, ma a volte uso 'meeting'.", "Italian"],
    ["Это русское сообщение, но я использую слово 'online'.", "Russian"],
    ["这是一个中文信息，但我们也会说 'bye bye'。", "Chinese (Simplified)"],
    ["これは日本語のメッセージですが、「OK」と言うこともあります。", "Japanese"],
    ["이것은 한국어 메시지이지만 'OK'라고 말하기도 합니다.", "Korean"],
    ["Bu Türkçe bir mesaj ama bazen 'check-in' diyoruz.", "Turkish"],
    ["Could you please review my PR?", "English"],
    ["The API returned a 404 error.", "English"],
    ["Let's sync up later today. 🤝", "English"]
]

NUM_PREDEFINED = len(PREDEFINED_EXAMPLES)

def generate_csv_data(num_examples_to_generate):
    """
    Generates the data for the CSV file.
    Args:
        num_examples_to_generate (int): The total number of examples to generate.
    Returns:
        list: A list of lists, where each inner list is a row for the CSV.
    """
    data_to_write = []
    if num_examples_to_generate <= 0:
        return data_to_write # Return empty list if 0 or negative examples requested

    for i in range(num_examples_to_generate):
        current_id = i + 1 # IDs are 1-based
        
        # Select an example from the predefined list
        # Use modulo operator to loop through PREDEFINED_EXAMPLES if num_examples_to_generate > NUM_PREDEFINED
        example_index = i % NUM_PREDEFINED
        
        chat_message = PREDEFINED_EXAMPLES[example_index][0]
        language = PREDEFINED_EXAMPLES[example_index][1]
        
        data_to_write.append([current_id, chat_message, language])
        
    return data_to_write

def main():
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(
        description="Generate a CSV dataset of chat messages for language detection.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter 
    )
    parser.add_argument(
        "--num_examples",
        "-n",
        type=int,
        default=NUM_PREDEFINED, 
        help="Total number of chat message examples to generate in the CSV."
    )
    parser.add_argument(
        "--output_file",
        "-o",
        type=str,
        default="chat_dataset.csv",
        help="Name of the CSV file to be created."
    )
    args = parser.parse_args()

    num_to_generate = args.num_examples
    output_filename = args.output_file

    if num_to_generate <= 0:
        print("Number of examples must be a positive integer. Exiting.")
        return

    # --- Generate Data ---
    print(f"Generating {num_to_generate} chat message examples...")
    generated_data = generate_csv_data(num_to_generate)

    # --- Write to CSV ---
    header = ['id', 'chat_message', 'language']
    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(header) 
            csvwriter.writerows(generated_data) 
        print(f"Successfully created '{output_filename}' with {len(generated_data)} records.")
    except IOError:
        print(f"Error: Could not write to file '{output_filename}'. Check permissions or path.")
    except Exception as e:
        print(f"An unexpected error occurred during CSV writing: {e}")

if __name__ == "__main__":
    if len(PREDEFINED_EXAMPLES) != 250:
        print(f"Warning: The PREDEFINED_EXAMPLES list currently has {len(PREDEFINED_EXAMPLES)} entries.")
        print("For the intended looping behavior and diversity, it should contain 250 unique examples.")
        print("The script will still work, but looping will occur over the available examples.")
    NUM_PREDEFINED = len(PREDEFINED_EXAMPLES) # Update NUM_PREDEFINED based on actual list length for safety

    main()