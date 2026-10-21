import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit full màn hình
st.set_page_config(
    page_title="How to Catch Fish 3D",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Xóa lề mặc định
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0rem !important;}
    body { overflow: hidden; background-color: #040914; margin: 0; }
    </style>
""", unsafe_allow_html=True)

# Mã nguồn HTML5 + Three.js 3D Game tích hợp trực tiếp
game_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>How to Fish 3D</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        body, html { width: 100%; height: 100%; overflow: hidden; font-family: 'Courier New', Courier, monospace; background: #040914; }
        #webgl-container { width: 100vw; height: 100vh; display: block; }
        
        /* MAIN MENU */
        #mainMenu {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(90deg, rgba(4,9,20,0.95) 0%, rgba(4,9,20,0.5) 50%, rgba(4,9,20,0) 100%);
            display: flex; flex-direction: column; justify-content: center; padding-left: 8%;
            z-index: 100;
        }
        .game-subtitle { font-size: 13px; letter-spacing: 4px; color: #94a3b8; margin-bottom: 5px; border-left: 3px solid #f6ad55; padding-left: 10px; }
        .game-title { font-size: 64px; font-weight: 900; line-height: 0.92; color: #f6ad55; text-transform: uppercase; margin-bottom: 30px; text-shadow: 4px 4px 12px rgba(0,0,0,0.9); }
        .menu-btn {
            width: 240px; padding: 14px 22px; margin-bottom: 12px; background: rgba(15, 23, 42, 0.85); color: #e2e8f0;
            border: 1px solid #334155; border-radius: 4px; font-weight: bold; font-size: 16px; text-align: left;
            cursor: pointer; transition: all 0.2s ease; backdrop-filter: blur(6px);
        }
        .menu-btn:hover { background: #f6ad55; color: #040914; border-color: #f6ad55; transform: translateX(10px); }

        /* HUD IN-GAME */
        #hud {
            position: absolute; top: 15px; left: 15px; right: 15px; display: none; justify-content: space-between;
            background: rgba(11, 19, 30, 0.85); padding: 12px 25px; border-radius: 8px; border: 1px solid #1e293b; color: white;
            font-weight: bold; z-index: 10; backdrop-filter: blur(8px);
        }
        .hud-item { display: flex; align-items: center; gap: 8px; font-size: 16px; }

        /* DIALOG / PROMPT BOX */
        #promptBox {
            position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%);
            background: rgba(15, 23, 42, 0.9); color: #38bdf8; padding: 12px 30px; border-radius: 30px;
            border: 2px solid #00d2ff; font-weight: bold; display: none; z-index: 20; text-align: center;
            box-shadow: 0 0 20px rgba(0, 210, 255, 0.4);
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="webgl-container"></div>

    <!-- MAIN MENU -->
    <div id="mainMenu">
        <div class="game-subtitle">A SURVIVAL FISHING ADVENTURE</div>
        <div class="game-title">HOW TO<br>CATCH<br>FISH</div>
        <button class="menu-btn" onclick="startGame()">▶ NEW GAME</button>
        <button class="menu-btn" onclick="startGame()">★ CONTINUE</button>
        <button class="menu-btn" onclick="alert('Phím W/A/S/D: Di chuyển\nSPACE: Nhảy\n1: Cần câu / 2: Súng\nE: Nói chuyện NPC / Lên thuyền\nChuột trái: Bắn / Quăng câu')">⚙ SETTINGS</button>
    </div>

    <!-- HUD -->
    <div id="hud">
        <div class="hud-item">💰 Vàng: <span id="goldVal">200</span></div>
        <div class="hud-item">❤️ HP: <span id="hpVal">100</span></div>
        <div class="hud-item">🗡️ Trang bị: <span id="itemVal">Cần câu (1)</span></div>
        <div class="hud-item">🔑 Chìa khóa: <span id="keyVal">1/3</span></div>
    </div>

    <div id="promptBox">Bấm [E] để tương tác</div>

<script>
let scene, camera, renderer;
let player, boat, npc;
let isBoating = false, inMenu = true;

let gold = 200, hp = 100, activeItem = "Cần câu";
const keys = {};

window.addEventListener('keydown', e => {
    keys[e.code] = true;
    if(e.code === 'Digit1') { activeItem = "Cần câu"; updateHUD(); }
    if(e.code === 'Digit2') { activeItem = "Súng săn (Shotgun)"; updateHUD(); }
});
window.addEventListener('keyup', e => keys[e.code] = false);

function init3D() {
    const container = document.getElementById('webgl-container');

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x040914);
    scene.fog = new THREE.FogExp2(0x040914, 0.005);

    camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 20, 35);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);

    // Light
    const ambLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambLight);
    const dirLight = new THREE.DirectionalLight(0xffedd5, 1.0);
    dirLight.position.set(50, 100, 50);
    scene.add(dirLight);

    // Ocean
    const oceanGeo = new THREE.PlaneGeometry(500, 500);
    const oceanMat = new THREE.MeshPhongMaterial({ color: 0x0f172a, shininess: 80 });
    const ocean = new THREE.Mesh(oceanGeo, oceanMat);
    ocean.rotation.x = -Math.PI / 2;
    scene.add(ocean);

    // Starter Island
    const islandGeo = new THREE.CylinderGeometry(30, 35, 8, 16);
    const islandMat = new THREE.MeshLambertMaterial({ color: 0x15803d });
    const island = new THREE.Mesh(islandGeo, islandMat);
    island.position.set(0, 3, 0);
    scene.add(island);

    // Player (Low-poly character)
    player = new THREE.Group();
    const bodyGeo = new THREE.CylinderGeometry(0.8, 0.8, 3);
    const bodyMat = new THREE.MeshLambertMaterial({ color: 0x1e3a8a });
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.position.y = 1.5;
    player.add(body);

    const headGeo = new THREE.SphereGeometry(0.8);
    const headMat = new THREE.MeshLambertMaterial({ color: 0xfde047 });
    const head = new THREE.Mesh(headGeo, headMat);
    head.position.y = 3.5;
    player.add(head);

    player.position.set(0, 7, 0);
    scene.add(player);

    // Boat
    boat = new THREE.Group();
    const boatGeo = new THREE.BoxGeometry(5, 2, 12);
    const boatMat = new THREE.MeshLambertMaterial({ color: 0x7c2d12 });
    const boatMesh = new THREE.Mesh(boatGeo, boatMat);
    boat.add(boatMesh);
    boat.position.set(15, 1, 15);
    scene.add(boat);

    // NPC Fisherman Joe
    npc = new THREE.Group();
    const npcBody = new THREE.Mesh(bodyGeo, new THREE.MeshLambertMaterial({ color: 0xea580c }));
    npcBody.position.y = 1.5;
    npc.add(npcBody);
    const npcHead = new THREE.Mesh(headGeo, headMat);
    npcHead.position.y = 3.5;
    npc.add(npcHead);
    npc.position.set(-8, 7, 5);
    scene.add(npc);

    window.addEventListener('resize', onWindowResize);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function startGame() {
    document.getElementById('mainMenu').style.display = 'none';
    document.getElementById('hud').style.display = 'flex';
    inMenu = false;
}

function updateHUD() {
    document.getElementById('goldVal').innerText = gold;
    document.getElementById('hpVal').innerText = hp;
    document.getElementById('itemVal').innerText = activeItem;
}

function animate() {
    requestAnimationFrame(animate);

    if (inMenu) {
        const t = Date.now() * 0.0003;
        camera.position.x = Math.sin(t) * 60;
        camera.position.z = Math.cos(t) * 60;
        camera.position.y = 30;
        camera.lookAt(0, 0, 0);
    } else {
        // Player Controls
        const speed = 0.3;
        if (keys['KeyW']) player.position.z -= speed;
        if (keys['KeyS']) player.position.z += speed;
        if (keys['KeyA']) player.position.x -= speed;
        if (keys['KeyD']) player.position.x += speed;

        // Jump physics
        if (keys['Space'] && player.position.y <= 7.1) {
            player.position.y += 1.5;
        }
        if (player.position.y > 7) player.position.y -= 0.08;

        // Camera Follows Player
        camera.position.x = player.position.x;
        camera.position.z = player.position.z + 20;
        camera.position.y = player.position.y + 12;
        camera.lookAt(player.position.x, player.position.y, player.position.z);

        // Interaction Prompt
        const prompt = document.getElementById('promptBox');
        const distToNPC = player.position.distanceTo(npc.position);
        const distToBoat = player.position.distanceTo(boat.position);

        if (distToNPC < 4) {
            prompt.style.display = 'block';
            prompt.innerText = "Bấm [E] để nói chuyện với Lão Ngư Joe";
            if (keys['KeyE']) { alert("Joe: 'Hãy cẩn thận! Ngoài khơi có quái vật biển đấy, nhớ mang theo súng!'"); keys['KeyE'] = false; }
        } else if (distToBoat < 5) {
            prompt.style.display = 'block';
            prompt.innerText = "Bấm [E] để Lên / Lái Thuyền";
        } else {
            prompt.style.display = 'none';
        }
    }

    renderer.render(scene, camera);
}

init3D();
animate();
</script>
</body>
</html>
"""

# Nhúng vào Streamlit
components.html(game_code, height=780, scrolling=False)
