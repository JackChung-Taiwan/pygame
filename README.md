# Pygame 遊戲程式設計教室

一個以 Python 藍、白、黃色系設計的繁體中文 Pygame 教學網站，內容包含：

- Python 與 Pygame 安裝步驟
- Pygame 常用模組與 Function 搜尋表
- 視窗、遊戲迴圈、鍵盤、繪圖、碰撞、文字及音效教學
- 網頁版鍵盤控制練習場
- 三款完整 Pygame 遊戲：貪食蛇、閃避隕石、點擊目標
- 響應式版面與手機導覽選單

## 瀏覽教學網站

直接開啟 `index.html`，或使用 VS Code 的 Live Server。

也可以在專案目錄執行：

```bash
python -m http.server 8000
```

再開啟瀏覽器前往 `http://localhost:8000`。

## 安裝 Pygame

```bash
python -m pip install -r requirements.txt
```

## 執行遊戲範例

```bash
python examples/snake.py
python examples/dodge_game.py
python examples/click_target.py
```

## 遊戲操作

### 貪食蛇

- 方向鍵或 WASD：移動
- 空白鍵：暫停／繼續
- R：重新開始

### 閃避隕石

- 左右方向鍵或 A、D：移動
- R：重新開始

### 點擊目標

- 滑鼠左鍵：點擊目標
- R：重新開始

## GitHub Pages 發布

1. 進入儲存庫的 **Settings**。
2. 開啟 **Pages**。
3. 在 **Build and deployment** 選擇 **Deploy from a branch**。
4. Branch 選擇 `main`，資料夾選擇 `/ (root)`。
5. 儲存後等待 GitHub Pages 完成部署。

## 專案結構

```text
pygame/
├── index.html
├── styles.css
├── script.js
├── examples/
│   ├── snake.py
│   ├── dodge_game.py
│   └── click_target.py
├── requirements.txt
└── README.md
```
