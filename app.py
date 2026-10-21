import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang web Streamlit full màn hình
st.set_page_config(
    page_title="How to Catch Fish - 2D Interactive Game",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ẩn header và footer mặc định của Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0rem !important;}
    </style>
""", unsafe_allow_html=True)

# Code HTML5 Canvas & JavaScript nguyên khối cho Game Đồ Họa 2D
game_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>How to Catch Fish 2D</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        body, html { width: 100%; height: 100%; overflow: hidden; background: #08121e; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        #gameCanvas { display: block; width: 100vw; height: 100vh; background: #0b1d28; }
        
        /* Overlay UI Buttons */
        .ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
        .interactive { pointer-events: auto; }
        
        /* Menu Overlay */
        #mainMenu {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(135deg, rgba(11,29,40,0.95) 0%, rgba(19,34,45,0.85) 100%);
            display: flex; flex-direction: column; justify-content: center; padding-left: 8%;
            z-index: 100;
        }
        .game-subtitle { font-size: 14px; letter-spacing: 4px; color: #cbd5e1; margin-bottom: 5px; border-left: 3px solid #f6ad55; padding-left: 10px; }
        .game-title { font-size: 64px; font-weight: 900; line-height: 0.9; color: #f6ad55; text-transform: uppercase; margin-bottom: 30px; text-shadow: 4px 4px 10px rgba(0,0,0,0.8); }
        .menu-btn {
            width: 220px; padding: 14px 20px; margin-bottom: 12px; background: #1a2e3b; color: #e2e8f0;
            border: 1px solid #2d4a5c; border-radius: 6px; font-weight: bold; font-size: 16px; text-align: left;
            cursor: pointer; transition: all 0.2s ease;
        }
        .menu-btn:hover { background: #f6ad55; color: #0b1d28; border-color: #f6ad55; transform: translateX(10px); }
        
        /* HUD Bar */
        #hud {
            position: absolute; top: 15px; left: 15px; right: 15px; display: none; justify-content: space-between;
            background: rgba(15, 23, 42, 0.85); padding: 12px 20px; border-radius: 10px; border: 1px solid #334155; color: white;
            font-weight: bold; z-index: 10;
        }
        .hud-item { display: flex; align-items: center; gap: 8px; font-size: 16px; }
        
        /* Dialog Box */
        #msgBox {
            position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%);
            background: rgba(15, 23, 42, 0.9); color: #f8fafc; padding: 15px 30px; border-radius: 30px;
            border: 2px solid #38bdf8; font-weight: bold; display: none; z-index: 20; text-align: center;
        }
    </style>
</head>
<body>

    <canvas id="gameCanvas"></canvas>

    <!-- MAIN MENU OVERLAY -->
    <div id="mainMenu" class="interactive">
        <div class="game-subtitle">A SURVIVAL FISHING ADVENTURE</div>
        <div class="game-title">HOW TO<br>CATCH<br>FISH</div>
        <button class="menu-btn" onclick="startGame()">▶ CONTINUED / PLAY</button>
        <button class="menu-btn" onclick="startGame()">★ NEW GAME</button>
        <button class="menu-btn" onclick="alert('Game 2D How To Fish - Dùng phím Mũi Tên/WASD để lái thuyền, bấm SPACE để quăng câu!')">⚙ INSTRUCTIONS</button>
    </div>

    <!-- HUD IN-GAME -->
    <div id="hud">
        <div class="hud-item">🪙 Vàng: <span id="goldVal">200</span></div>
        <div class="hud-item">❤️ HP: <span id="hpVal">100</span></div>
        <div class="hud-item">🚤 Cấp Thuyền: <span id="boatVal">1</span></div>
        <div class="hud-item">🔑 Chìa khóa: <span id="keyVal">1/3</span></div>
        <div class="hud-item">📍 Đảo: <span id="islandVal">Đảo Tân Thủ</span></div>
    </div>

    <div id="msgBox"></div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// --- GAME STATES ---
let gameState = 'MENU'; // MENU, SAILING, FISHING
let gold = 200;
let hp = 100;
let boatLevel = 1;
let keysOwned = [1];
let currentIsland = 1;

// --- BOAT OBJECT ---
const boat = {
    x: window.innerWidth / 2,
    y: window.innerHeight / 2,
    angle: 0,
    speed: 0,
    maxSpeed: 3.5,
    accel: 0.15,
    friction: 0.96,
    radius: 18
};

// --- KEYS LOGIC ---
const keys = {};
window.addEventListener('keydown', e => keys[e.code] = true);
window.addEventListener('keyup', e => keys[e.code] = false);

// --- ISLANDS DATA (2D POSITION) ---
const islands = [
    { id: 1, name: "Đảo Tân Thủ", x: window.innerWidth * 0.25, y: window.innerHeight * 0.35, radius: 80, color: "#22c55e", keyReq: null, keyReward: 2, boss: "🦈 Cá Trê Khổng Lồ" },
    { id: 2, name: "Đảo San Hò", x: window.innerWidth * 0.75, y: window.innerHeight * 0.3, radius: 95, color: "#06b6d4", keyReq: 2, keyReward: 3, boss: "🐊 Cá Sấu Nước Mặn" },
    { id: 3, name: "Đảo Quái Vật", x: window.innerWidth * 0.5, y: window.innerHeight * 0.75, radius: 110, color: "#ef4444", keyReq: 3, keyReward: 4, boss: "🐉 Thủy Quái Leviathan" }
];

// --- FISHING MINIGAME VARIABLES ---
let fishingState = 'CAST'; // CAST, WAIT, REEL
let tension = 50;
let fishPos = 50;
let targetPos = 50;
let fishProgress = 0;
let currentBoss = "";

function showMsg(txt, duration = 2500) {
    const box = document.getElementById('msgBox');
    box.innerText = txt;
    box.style.display = 'block';
    setTimeout(() => { box.style.display = 'none'; }, duration);
}

function startGame() {
    document.getElementById('mainMenu').style.display = 'none';
    document.getElementById('hud').style.display = 'flex';
    gameState = 'SAILING';
    showMsg("⛵ Hãy dùng phím W/A/S/D hoặc Mũi Tên để lái thuyền đến khu vực có Đảo!");
}

function updateHUD() {
    document.getElementById('goldVal').innerText = gold;
    document.getElementById('hpVal').innerText = hp;
    document.getElementById('boatVal').innerText = boatLevel;
    document.getElementById('keyVal').innerText = keysOwned.length + "/3";
    document.getElementById('islandVal').innerText = islands[currentIsland - 1].name;
}

// ================= GAME LOOP =================
function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    if (gameState === 'MENU') {
        drawOceanBackground();
        drawIslands();
    } 
    else if (gameState === 'SAILING') {
        updateSailing();
        drawOceanBackground();
        drawIslands();
        drawBoat();
        checkProximity();
    } 
    else if (gameState === 'FISHING') {
        drawOceanBackground();
        drawFishingMinigame();
    }
    
    updateHUD();
    requestAnimationFrame(gameLoop);
}

// --- DRAW OCEAN & WAVES ---
function drawOceanBackground() {
    ctx.fillStyle = '#0f2735';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Wave lines
    ctx.strokeStyle = '#183c50';
    ctx.lineWidth = 2;
    for (let i = 0; i < canvas.height; i += 40) {
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(canvas.width, i);
        ctx.stroke();
    }
}

// --- DRAW ISLANDS ---
function drawIslands() {
    islands.forEach(isl => {
        // Safe Zone / Island Circle
        ctx.fillStyle = isl.color;
        ctx.beginPath();
        ctx.arc(isl.x, isl.y, isl.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.lineWidth = 4;
        ctx.strokeStyle = '#fef08a';
        ctx.stroke();

        // Label
        ctx.fillStyle = 'white';
        ctx.font = 'bold 14px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(isl.name, isl.x, isl.y - isl.radius - 10);

        // Lock / Unlock status
        if (isl.keyReq && !keysOwned.includes(isl.keyReq)) {
            ctx.fillStyle = '#f87171';
            ctx.fillText("🔒 Khóa (Cần Chìa)", isl.x, isl.y + 5);
        } else {
            ctx.fillStyle = '#4ade80';
            ctx.fillText("⚓ Vùng Cập Bến", isl.x, isl.y + 5);
        }
    });
}

// --- UPDATE SAILING PHYSICS ---
function updateSailing() {
    if (keys['KeyW'] || keys['ArrowUp']) {
        boat.speed = Math.min(boat.speed + boat.accel, boat.maxSpeed);
    } else if (keys['KeyS'] || keys['ArrowDown']) {
        boat.speed = Math.max(boat.speed - boat.accel, -boat.maxSpeed / 2);
    } else {
        boat.speed *= boat.friction;
    }

    if (keys['KeyA'] || keys['ArrowLeft']) boat.angle -= 0.05;
    if (keys['KeyD'] || keys['ArrowRight']) boat.angle += 0.05;

    boat.x += Math.cos(boat.angle) * boat.speed;
    boat.y += Math.sin(boat.angle) * boat.speed;

    // Screen bounds
    boat.x = Math.max(30, Math.min(canvas.width - 30, boat.x));
    boat.y = Math.max(30, Math.min(canvas.height - 30, boat.y));
}

// --- DRAW BOAT ---
function drawBoat() {
    ctx.save();
    ctx.translate(boat.x, boat.y);
    ctx.rotate(boat.angle);

    // Boat body
    ctx.fillStyle = '#b45309';
    ctx.beginPath();
    ctx.moveTo(20, 0);
    ctx.lineTo(-15, -10);
    ctx.lineTo(-15, 10);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.restore();
}

// --- CHECK PROXIMITY TO ISLANDS ---
function checkProximity() {
    islands.forEach(isl => {
        const dx = boat.x - isl.x;
        const dy = boat.y - isl.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < isl.radius + boat.radius) {
            if (isl.keyReq && !keysOwned.includes(isl.keyReq)) {
                showMsg("🔒 Đảo này đã bị khóa! Hãy đánh bại Boss ở đảo trước để lấy Chìa Khóa!");
            } else {
                if (keys['Space']) {
                    currentIsland = isl.id;
                    currentBoss = isl.boss;
                    startFishingMinigame();
                } else {
                    showMsg("⚓ Bấm [SPACE] để thả cần câu & Săn Boss cá lớn ở " + isl.name + "!");
                }
            }
        }
    });
}

// --- MINIGAME CÂU CÁ 2D ---
function startFishingMinigame() {
    gameState = 'FISHING';
    fishingState = 'REEL';
    tension = 50;
    fishPos = 50;
    fishProgress = 0;
}

function drawFishingMinigame() {
    ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#f6ad55';
    ctx.font = 'bold 28px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText("⚔️ ĐANG CHIẾN ĐẤU VỚI BOSS: " + currentBoss, canvas.width / 2, 80);

    ctx.fillStyle = '#cbd5e1';
    ctx.font = '16px sans-serif';
    ctx.fillText("Nhấn [SPACE] liên tục để giữ thanh kéo trong vùng an toàn (40 - 70)!", canvas.width / 2, 115);

    // Progress Bar
    ctx.fillStyle = '#334155';
    ctx.fillRect(canvas.width / 2 - 150, 150, 300, 20);
    ctx.fillStyle = '#22c55e';
    ctx.fillRect(canvas.width / 2 - 150, 150, fishProgress * 3, 20);

    // Tension Bar Graphic
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(canvas.width / 2 - 150, 200, 300, 40);
    
    // Target Safe Zone
    ctx.fillStyle = 'rgba(34, 197, 94, 0.4)';
    ctx.fillRect(canvas.width / 2 - 150 + 120, 200, 90, 40);

    // Player Indicator
    ctx.fillStyle = '#38bdf8';
    ctx.fillRect(canvas.width / 2 - 150 + (tension * 3) - 5, 195, 10, 50);

    // Minigame Logic
    tension -= 0.4; // Decay
    if (keys['Space']) tension += 1.2;
    tension = Math.max(0, Math.min(100, tension));

    if (tension >= 40 && tension <= 70) {
        fishProgress += 0.3;
    } else {
        fishProgress -= 0.1;
    }
    fishProgress = Math.max(0, Math.min(100, fishProgress));

    // Win condition
    if (fishProgress >= 100) {
        const isl = islands[currentIsland - 1];
        if (!keysOwned.includes(isl.keyReward)) {
            keysOwned.push(isl.keyReward);
            showMsg("🎉 THẮNG LỢI! Bạn đã thu phục " + currentBoss + " & nhặt được CHÌA KHÓA mới!", 4000);
        } else {
            gold += 200;
            showMsg("🎉 Bạn đã hạ gục " + currentBoss + " & thưởng +200 🪙!", 3000);
        }
        gameState = 'SAILING';
    }

    // Exit Button
    ctx.fillStyle = '#ef4444';
    ctx.fillRect(canvas.width / 2 - 60, 300, 120, 40);
    ctx.fillStyle = 'white';
    ctx.font = 'bold 16px sans-serif';
    ctx.fillText("Rút Lui", canvas.width / 2, 325);
}

// Click to Quit Minigame
window.addEventListener('click', e => {
    if (gameState === 'FISHING') {
        if (e.clientX >= canvas.width / 2 - 60 && e.clientX <= canvas.width / 2 + 60 &&
            e.clientY >= 300 && e.clientY <= 340) {
            gameState = 'SAILING';
        }
    }
});

// Run Game
gameLoop();
</script>
</body>
</html>
"""

# Nhúng Game vào trang Streamlit bằng HTML/Iframe
components.html(game_code, height=750, scrolling=False)
