from flask import Flask, send_from_directory
import os

app = Flask(__name__)


# --- SERWOWANIE PLIKÓW (np. tlo.png) Z FOLDERU GŁÓWNEGO ---
@app.route('/tlo.png')
def serve_image():
    # Upewnij się, że plik tlo.png jest w tym samym folderze co skrypt
    return send_from_directory('.', 'tlo.png')


PAGE_CONTENT = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Moja Biblioteka</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Kalam:wght@300;400;700&family=Patrick+Hand&display=swap" rel="stylesheet">

    <style>
        /* =========================================
           1. ZMIENNE
           ========================================= */
        :root {
            --wood-dark: #2d1b0e;
            --wood-medium: #5d4037;
            --gold: #c5a059;      
            --gold-bright: #ffd700; 
            --leather-dark: #1e130c; 
            --leather-light: #2c1e16;
            --text-on-dark: #e0d0b8;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            background-color: #0f0a06;
            font-family: 'Cinzel', serif;
            height: 100vh;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: flex-end;
        }

        /* =========================================
           2. BIBLIOTEKA
           ========================================= */
        .library-scene {
            width: 100vw; height: 100vh;
            background: radial-gradient(circle at 50% 40%, #3e2723 0%, #000 90%);
            display: flex;
            justify-content: center;
            align-items: flex-end;
            transition: filter 0.5s;
        }

        .bookshelf {
            width: 950px; height: 90vh;
            background: var(--wood-medium);
            border: 40px solid var(--wood-dark);
            border-bottom: 0;
            border-radius: 20px 20px 0 0;
            display: flex;
            flex-direction: column;
            box-shadow: 0 0 100px #000;
            position: relative;
        }

        .bookshelf::before {
            content: '';
            position: absolute;
            top: -60px; left: 20px; right: 20px; height: 60px;
            background: var(--wood-dark);
            border-radius: 100px 100px 0 0;
            box-shadow: inset 0 -10px 20px rgba(0,0,0,0.5);
        }

        .shelf-row {
            flex: 1;
            border-bottom: 25px solid var(--wood-dark);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            display: flex;
            align-items: flex-end;
            padding: 0 15px;
            gap: 8px;
            perspective: 800px;
        }

        /* =========================================
           3. KSIĄŻKI
           ========================================= */
        .book-spine {
            width: 55px; height: 85%;
            border-radius: 4px;
            position: relative;
            cursor: pointer;
            transition: transform 0.2s, margin 0.2s;
            box-shadow: inset 5px 0 10px rgba(0,0,0,0.3), 2px 2px 5px rgba(0,0,0,0.4);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1;
        }

        .book-spine:hover {
            transform: translateZ(20px) scale(1.05) translateY(-5px);
            z-index: 10;
            margin: 0 5px;
        }

        .spine-label {
            writing-mode: vertical-rl;
            text-orientation: mixed;
            font-family: 'Patrick Hand', cursive;
            font-size: 14px;
            color: rgba(255,255,255,0.85);
            letter-spacing: 1px;
            text-shadow: 0 1px 2px rgba(0,0,0,0.8);
            max-height: 90%;
            overflow: hidden;
            pointer-events: none;
        }

        .book-spine::after, .book-spine::before {
            content: ''; position: absolute; left: 0; right: 0; height: 3px;
            border-top: 1px solid rgba(255,255,255,0.3);
            border-bottom: 1px solid rgba(255,255,255,0.3);
        }
        .book-spine::after { top: 15px; }
        .book-spine::before { bottom: 15px; }

        /* =========================================
           4. INTERFEJS EDYTORA
           ========================================= */
        .overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.9);
            backdrop-filter: blur(5px);
            display: flex; justify-content: center; align-items: center;
            opacity: 0; pointer-events: none;
            transition: opacity 0.4s;
            z-index: 100;
        }
        .overlay.active { opacity: 1; pointer-events: all; }

        .big-book {
            width: 90vw; height: 90vh; max-width: 1400px;
            background: #fff;
            border-radius: 8px;
            display: flex;
            position: relative;
            box-shadow: 0 30px 100px rgba(0,0,0,1);
            overflow: hidden;
            border: 5px solid var(--leather-dark);
        }

        .page-left {
            width: 320px;
            background: linear-gradient(135deg, var(--leather-dark), var(--leather-light));
            border-right: 2px solid #000;
            padding: 40px 30px;
            display: flex;
            flex-direction: column;
            gap: 25px;
            color: var(--text-on-dark);
            box-shadow: inset -10px 0 30px rgba(0,0,0,0.5);
        }

        .page-left h4 {
            color: var(--gold);
            text-transform: uppercase;
            font-size: 13px;
            margin-bottom: 15px;
            letter-spacing: 2px;
            border-bottom: 1px solid rgba(197, 160, 89, 0.3);
            padding-bottom: 5px;
        }

        .title-input {
            width: 100%;
            padding: 10px 5px;
            font-family: 'Patrick Hand', cursive;
            font-size: 26px;
            border: none;
            border-bottom: 2px solid var(--gold);
            background: transparent;
            color: #fff;
            font-weight: bold;
            transition: 0.3s;
        }

        .title-input:focus {
            outline: none;
            border-bottom-color: var(--gold-bright);
            background: rgba(255,255,255,0.05);
        }

        .title-input::placeholder { color: rgba(255,255,255,0.2); }

        .style-options {
            display: grid; grid-template-columns: 1fr; gap: 10px;
        }

        .style-btn {
            padding: 12px 15px;
            border: 1px solid rgba(255,255,255,0.1);
            cursor: pointer;
            background: rgba(0,0,0,0.2);
            font-size: 14px;
            border-radius: 4px;
            color: #ccc;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.2s;
            font-family: 'Cinzel', serif;
        }

        .style-btn:hover {
            background: rgba(255,255,255,0.05);
            color: #fff;
            border-color: rgba(255,255,255,0.3);
        }

        .style-btn.active {
            background: var(--gold);
            color: #1a120b;
            border-color: var(--gold);
            font-weight: bold;
            box-shadow: 0 0 15px rgba(197, 160, 89, 0.4);
        }

        /* Usunięto klasę .info-footer, ponieważ sekcja została usunięta z HTML */

        .page-right {
            flex: 1;
            position: relative;
            display: flex;
            flex-direction: column;
            background: #111;
        }

        #editor-area {
            flex: 1; width: 100%;
            border: none; resize: none; outline: none;
            font-family: 'Kalam', cursive;
            font-size: 22px;
            line-height: 36px;
            padding: 40px 60px;
            transition: background 0.3s, color 0.3s;
        }

        /* --- STYLE PAPIERU --- */
        .paper-vintage {
            background-color: #d1b48c;
            background-image: url('/tlo.png');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            color: #1a0f05;
            font-weight: bold;
            text-shadow: 1px 1px 0px rgba(255, 255, 255, 0.4);
            box-shadow: inset 0 0 50px rgba(0,0,0,0.3);
        }

        .paper-lined-light {
            background-color: #fffdf7;
            background-image: linear-gradient(#bbb 2px, transparent 2px);
            background-size: 100% 36px; background-attachment: local;
            color: #2c3e50;
        }

        .paper-grid-light {
            background-color: #fff;
            background-image: 
                linear-gradient(#ccc 2px, transparent 2px),
                linear-gradient(90deg, #ccc 2px, transparent 2px);
            background-size: 36px 36px;
            background-attachment: local;
            color: #2c3e50;
        }

        .paper-lined-dark {
            background-color: #262626;
            background-image: linear-gradient(#444 1px, transparent 1px);
            background-size: 100% 36px; background-attachment: local;
            color: #dcdde1;
        }

        .paper-grid-dark {
            background-color: #262626;
            background-image: 
                linear-gradient(#383838 1px, transparent 1px),
                linear-gradient(90deg, #383838 1px, transparent 1px);
            background-size: 36px 36px; background-attachment: local;
            color: #dcdde1;
        }

        /* --- NAWIGACJA --- */
        .nav-bar {
            padding: 15px 40px;
            border-top: 1px solid rgba(255,255,255,0.05);
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(255,255,255,0.02);
            font-size: 16px;
            color: var(--gold); 
            font-family: 'Cinzel', serif;
            letter-spacing: 1px;
        }

        .nav-btn {
            background: none;
            border: 2px solid var(--gold);
            color: var(--gold);
            padding: 8px 15px;
            border-radius: 30px;
            cursor: pointer;
            opacity: 0.8;
            transition: all 0.3s ease;
            font-family: inherit;
            font-size: 24px;
            line-height: 1;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        .nav-btn:hover {
            opacity: 1;
            background: var(--gold);
            color: #1a120b;
            transform: scale(1.1);
            box-shadow: 0 4px 8px rgba(197, 160, 89, 0.4);
        }

        .close-icon {
            position: absolute; top: 15px; right: 20px;
            font-size: 28px; cursor: pointer; color: #888;
            transition: 0.2s; z-index: 20;
        }
        .close-icon:hover { color: #c0392b; transform: scale(1.1); }

        #editor-area::-webkit-scrollbar { width: 8px; }
        #editor-area::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.2); border-radius: 4px; }

    </style>
</head>
<body>

    <div class="library-scene" id="scene">
        <div class="bookshelf" id="bookshelf"></div>
    </div>

    <div class="overlay" id="overlay">
        <div class="big-book">
            <div class="close-icon" onclick="closeBook()">✕</div>

            <div class="page-left">
                <div>
                    <h4>Tytuł Księgi</h4>
                    <input type="text" id="book-title" class="title-input" placeholder="Wpisz tytuł..." maxlength="15" oninput="updateBookTitle()">
                </div>

                <div style="margin-top: 20px;">
                    <h4>Wygląd Stron</h4>
                    <div class="style-options">
                        <div class="style-btn" id="btn-vintage" onclick="setPaper('vintage')">📜 Stary Pergamin</div>
                        <div class="style-btn" id="btn-lined-light" onclick="setPaper('lined-light')">📝 Linie Jasne</div>
                        <div class="style-btn" id="btn-grid-light" onclick="setPaper('grid-light')">▦ Kratka Jasna</div>
                        <div class="style-btn" id="btn-lined-dark" onclick="setPaper('lined-dark')">🌑 Linie Ciemne</div>
                        <div class="style-btn" id="btn-grid-dark" onclick="setPaper('grid-dark')">⬛ Kratka Ciemna</div>
                    </div>
                </div>

                </div>

            <div class="page-right">
                <textarea id="editor-area" placeholder="Zacznij pisać tutaj..."></textarea>

                <div class="nav-bar" id="nav-bar">
                    <button class="nav-btn" onclick="changePage(-1)">←</button>
                    <span>STRONA <span id="page-num" style="font-weight: bold; margin-left:5px;">1</span></span>
                    <button class="nav-btn" onclick="changePage(1)">→</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const totalShelves = 3;
        const booksPerShelf = 12;
        const colors = ['#5d4037', '#4e342e', '#3e2723', '#263238', '#1b5e20', '#b71c1c', '#f57f17', '#0d47a1'];

        // Używamy wersji v4.2
        let libraryData = JSON.parse(localStorage.getItem('my_library_pro_v4')) || {};
        let currentBookId = null;
        let currentPage = 1;

        const shelfContainer = document.getElementById('bookshelf');

        function initLibrary() {
            shelfContainer.innerHTML = '';
            for(let i=0; i<totalShelves; i++) {
                let row = document.createElement('div');
                row.className = 'shelf-row';
                for(let j=0; j<booksPerShelf; j++) {
                    const bookId = `book-${i}-${j}`;
                    const bookData = libraryData[bookId] || { title: "", style: "vintage" };
                    const color = colors[(i+j) % colors.length];

                    let book = document.createElement('div');
                    book.className = 'book-spine';
                    book.id = `spine-${bookId}`;
                    book.style.backgroundColor = color;
                    book.style.height = (80 + Math.random() * 15) + '%';
                    book.onclick = () => openBook(bookId);

                    let label = document.createElement('span');
                    label.className = 'spine-label';
                    label.innerText = bookData.title;
                    book.appendChild(label);
                    row.appendChild(book);
                }
                shelfContainer.appendChild(row);
            }
        }

        function openBook(id) {
            currentBookId = id;
            currentPage = 1;

            if (!libraryData[id]) libraryData[id] = { title: "", style: "vintage", pages: {} };
            const data = libraryData[id];

            // Usunięto odniesienie do elementu 'current-book-id', bo został skasowany z HTML
            document.getElementById('book-title').value = data.title;

            setPaper(data.style, false);
            loadPageContent();

            document.getElementById('overlay').classList.add('active');
        }

        function closeBook() {
            saveCurrentPage();
            document.getElementById('overlay').classList.remove('active');
            initLibrary(); 
        }

        function updateBookTitle() {
            const newTitle = document.getElementById('book-title').value;
            libraryData[currentBookId].title = newTitle;
            saveData();
            const spineLabel = document.querySelector(`#spine-${currentBookId} .spine-label`);
            if(spineLabel) spineLabel.innerText = newTitle;
        }

        function setPaper(styleName, save=true) {
            const editor = document.getElementById('editor-area');

            editor.className = '';
            editor.classList.add('paper-' + styleName);

            document.querySelectorAll('.style-btn').forEach(btn => btn.classList.remove('active'));
            const activeBtn = document.getElementById('btn-' + styleName);
            if(activeBtn) activeBtn.classList.add('active');

            if(save && currentBookId) {
                libraryData[currentBookId].style = styleName;
                saveData();
            }
        }

        function loadPageContent() {
            const editor = document.getElementById('editor-area');
            const pages = libraryData[currentBookId].pages || {};
            editor.value = pages[currentPage] || "";
            document.getElementById('page-num').innerText = currentPage;
        }

        function saveCurrentPage() {
            if(!currentBookId) return;
            const content = document.getElementById('editor-area').value;
            if(!libraryData[currentBookId].pages) libraryData[currentBookId].pages = {};
            libraryData[currentBookId].pages[currentPage] = content;
            saveData();
        }

        function changePage(dir) {
            saveCurrentPage();
            const newPage = currentPage + dir;
            if(newPage < 1) return;
            currentPage = newPage;
            loadPageContent();
        }

        function saveData() {
            localStorage.setItem('my_library_pro_v4', JSON.stringify(libraryData));
        }

        document.getElementById('editor-area').addEventListener('input', () => {
            saveCurrentPage();
        });

        initLibrary();
    </script>
</body>
</html>
"""


@app.route('/')
def home():
    return PAGE_CONTENT


if __name__ == '__main__':
    app.run(debug=True)
