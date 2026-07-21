const menuButton = document.querySelector('.menu-button');
const navLinks = document.querySelector('.nav-links');

menuButton?.addEventListener('click', () => {
  const isOpen = navLinks.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(isOpen));
  document.body.classList.toggle('menu-open', isOpen);
});

document.querySelectorAll('.nav-links a').forEach((link) => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    menuButton?.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('menu-open');
  });
});

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.08 });

document.querySelectorAll('.reveal').forEach((element) => revealObserver.observe(element));

document.querySelectorAll('.copy-button').forEach((button) => {
  button.addEventListener('click', async () => {
    const original = button.textContent;
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      button.textContent = '已複製';
    } catch {
      button.textContent = '請手動複製';
    }
    window.setTimeout(() => { button.textContent = original; }, 1300);
  });
});

const functionSearch = document.querySelector('#function-search');
const functionCards = [...document.querySelectorAll('.function-card')];
const noResults = document.querySelector('#no-results');

functionSearch?.addEventListener('input', () => {
  const keyword = functionSearch.value.trim().toLowerCase();
  let visibleCount = 0;

  functionCards.forEach((card) => {
    const searchable = `${card.dataset.search} ${card.textContent}`.toLowerCase();
    const visible = searchable.includes(keyword);
    card.classList.toggle('hidden', !visible);
    if (visible) visibleCount += 1;
  });

  noResults.hidden = visibleCount !== 0;
});

const lessonTabs = document.querySelectorAll('.lesson-tab');
const lessonPanels = document.querySelectorAll('.lesson-panel');

lessonTabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    lessonTabs.forEach((item) => {
      item.classList.remove('active');
      item.setAttribute('aria-selected', 'false');
    });
    lessonPanels.forEach((panel) => panel.classList.remove('active'));

    tab.classList.add('active');
    tab.setAttribute('aria-selected', 'true');
    document.querySelector(`#lesson-${tab.dataset.lesson}`)?.classList.add('active');
  });
});

document.querySelectorAll('.code-toggle').forEach((button) => {
  button.addEventListener('click', () => {
    const code = document.querySelector(`#${button.dataset.target}`);
    const open = code.classList.toggle('open');
    button.textContent = open ? '收合重點' : '查看重點';
  });
});

document.querySelector('#current-year').textContent = new Date().getFullYear();

// Browser practice game: mirrors the main concepts used in a Pygame loop.
const canvas = document.querySelector('#game-canvas');
const context = canvas?.getContext('2d');
const scoreElement = document.querySelector('#demo-score');
const messageElement = document.querySelector('#demo-message');
const resetButton = document.querySelector('#reset-demo');

if (canvas && context) {
  const keys = new Set();
  const player = { x: 50, y: 150, width: 34, height: 34, speed: 230 };
  const coin = { x: 470, y: 130, radius: 13 };
  let score = 0;
  let focused = false;
  let previousTime = performance.now();

  function resetDemo() {
    player.x = 50;
    player.y = 150;
    score = 0;
    scoreElement.textContent = '0';
    moveCoin();
    messageElement.textContent = '點擊畫面後開始操作';
    canvas.focus();
  }

  function moveCoin() {
    coin.x = 30 + Math.random() * (canvas.width - 60);
    coin.y = 30 + Math.random() * (canvas.height - 60);
  }

  function update(deltaTime) {
    if (!focused) return;
    let dx = 0;
    let dy = 0;
    if (keys.has('arrowleft') || keys.has('a')) dx -= 1;
    if (keys.has('arrowright') || keys.has('d')) dx += 1;
    if (keys.has('arrowup') || keys.has('w')) dy -= 1;
    if (keys.has('arrowdown') || keys.has('s')) dy += 1;

    if (dx && dy) {
      const normalizer = Math.SQRT1_2;
      dx *= normalizer;
      dy *= normalizer;
    }

    player.x += dx * player.speed * deltaTime;
    player.y += dy * player.speed * deltaTime;
    player.x = Math.max(0, Math.min(canvas.width - player.width, player.x));
    player.y = Math.max(0, Math.min(canvas.height - player.height, player.y));

    const closestX = Math.max(player.x, Math.min(coin.x, player.x + player.width));
    const closestY = Math.max(player.y, Math.min(coin.y, player.y + player.height));
    const distanceX = coin.x - closestX;
    const distanceY = coin.y - closestY;

    if ((distanceX * distanceX) + (distanceY * distanceY) < coin.radius * coin.radius) {
      score += 1;
      scoreElement.textContent = String(score);
      messageElement.textContent = `成功收集第 ${score} 枚金幣！`;
      moveCoin();
    }
  }

  function drawGrid() {
    context.strokeStyle = 'rgba(255,255,255,0.08)';
    context.lineWidth = 1;
    for (let x = 0; x <= canvas.width; x += 32) {
      context.beginPath(); context.moveTo(x, 0); context.lineTo(x, canvas.height); context.stroke();
    }
    for (let y = 0; y <= canvas.height; y += 32) {
      context.beginPath(); context.moveTo(0, y); context.lineTo(canvas.width, y); context.stroke();
    }
  }

  function draw() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    const gradient = context.createLinearGradient(0, 0, canvas.width, canvas.height);
    gradient.addColorStop(0, '#153a5f');
    gradient.addColorStop(1, '#2d6594');
    context.fillStyle = gradient;
    context.fillRect(0, 0, canvas.width, canvas.height);
    drawGrid();

    context.beginPath();
    context.arc(coin.x, coin.y, coin.radius, 0, Math.PI * 2);
    context.fillStyle = '#ffd343';
    context.shadowColor = 'rgba(255, 211, 67, .65)';
    context.shadowBlur = 16;
    context.fill();
    context.shadowBlur = 0;
    context.beginPath();
    context.arc(coin.x - 4, coin.y - 4, 3, 0, Math.PI * 2);
    context.fillStyle = '#fff2a8';
    context.fill();

    context.fillStyle = '#eef7ff';
    context.fillRect(player.x, player.y, player.width, player.height);
    context.fillStyle = '#3776ab';
    context.fillRect(player.x + 6, player.y + 7, 7, 7);
    context.fillRect(player.x + 21, player.y + 7, 7, 7);
    context.fillStyle = '#ffd343';
    context.fillRect(player.x + 10, player.y + 23, 14, 5);
  }

  function frame(time) {
    const deltaTime = Math.min((time - previousTime) / 1000, 0.033);
    previousTime = time;
    update(deltaTime);
    draw();
    requestAnimationFrame(frame);
  }

  canvas.addEventListener('focus', () => {
    focused = true;
    messageElement.textContent = '使用方向鍵或 WASD 收集金幣';
  });
  canvas.addEventListener('blur', () => { focused = false; keys.clear(); });
  canvas.addEventListener('click', () => canvas.focus());
  window.addEventListener('keydown', (event) => {
    const key = event.key.toLowerCase();
    if (focused && ['arrowup', 'arrowdown', 'arrowleft', 'arrowright', 'w', 'a', 's', 'd'].includes(key)) {
      event.preventDefault();
      keys.add(key);
    }
  });
  window.addEventListener('keyup', (event) => keys.delete(event.key.toLowerCase()));
  resetButton?.addEventListener('click', resetDemo);

  moveCoin();
  requestAnimationFrame(frame);
}
