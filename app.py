import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit tràn màn hình
st.set_page_config(
    page_title="How to Catch Fish 3D",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Xóa lề mặc định của Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0rem !important;}
    body { overflow: hidden; background-color: #050b14; }
    </style>
""", unsafe_allow_html=True)

# Mã nguồn HTML5 + Three.js 3D Game
threejs_game_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>How to Catch Fish 3D</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        body, html { width: 100%; height: 100%; overflow: hidden; font-family: 'Segoe UI', Tahoma, sans-serif; background: #050b14; }
        #webgl-container { width: 100vw; height: 100vh; display: block; }
        
        /* UI OVERLAY MÀN HÌNH CHÍNH (MAIN MENU) */
        #mainMenu {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(90deg, rgba(5,11,20,0.95) 0%, rgba(5,11,20,0.6) 50%, rgba(5,11,20,0) 100%);
            display: flex; flex-direction: column; justify-content: center; padding-left: 8%;
            z-index: 100;
        }
        .game-subtitle { font-size: 13px; letter-spacing: 4px; color: #cbd5e1; margin-bottom: 5px; border-left: 3px solid #f6ad55; padding-left: 10px; }
        .game-title { font-size: 58px; font-weight: 900; line-height: 0.95; color: #f6ad55; text-transform: uppercase; margin-bottom: 30px; text-shadow: 3px 3px 10px rgba(0,0,0,0.9); }
        .menu-btn {
            width: 220px; padding: 14px 20px; margin-bottom: 12px; background: rgba(22, 38, 54, 0.85); color: #e2e8f0;
            border: 1px solid #2d4a5c; border-radius: 6px; font-weight: bold; font-size: 15px; text-align: left;
            cursor: pointer; transition: all 0.25s ease; backdrop-filter: blur(5px);
        }
        .menu-btn:hover { background: #f6ad55; color: #0b1d28; border-color: #f6ad55; transform: translateX(10px); }

        /* HUD BANNER TRONG GAME */
        #hud {
            position: absolute; top: 15px; left: 15px; right: 15px; display: none; justify-content: space-between;
            background: rgba(11, 22, 34, 0.85); padding: 12px 25px; border-radius: 12px; border: 1px solid #1e3a5f; color: white;
            font-weight: bold; z-index: 10; backdrop-filter: blur(8px);
        }
        .hud-item { display: flex; align-items: center; gap: 8px; font-size: 15px; }

        /* MÀN HÌNH MINIGAME CÂU CÁ BOSS 3D */
        #fishingUI {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: rgba(11, 22, 34, 0.92); border: 2px solid #00d2ff; padding: 25px 40px; border-radius: 20px;
            color: white; text-align: center; display: none; z-index: 50; width: 420px; box-shadow: 0 0 30px rgba(0, 210, 255, 0.3);
        }
        .bar-bg { width: 100%; height: 24px; background: #1e293b; border-radius: 12px; margin: 15px 0; overflow: hidden; position: relative; }
        .bar-fill { height: 100%; background: #22c55e; width: 0%; transition: width 0.1s; }
        .tension-indicator { position: absolute; top: 0; bottom: 0; width: 8px; background: #38bdf8; border-radius: 4px; }
        .safe-zone { position: absolute; top: 0; bottom: 0; left: 40%; width: 30%; background: rgba(34, 197, 94, 0.45); }

        /* THÔNG BÁO */
        #msgBox {
            position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%);
            background: rgba(15, 23, 42, 0.9); color: #f8fafc; padding: 12px 25px; border-radius: 25px;
            border: 1px solid #38bdf8; font-weight: bold; display: none; z-index: 20; text-align: center;
        }
    </style>
    <!-- THƯ VIỆN THREE.JS DỰNG ĐỒ HỌA 3D -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="webgl-container"></div>

    <!-- MÀN HÌNH MAIN MENU CHUẨN ĐỒ HỌA -->
    <div id="mainMenu">
        <div class="game-subtitle">A SURVIVAL FISHING ADVENTURE</div>
        <div class="game-title">HOW TO<br>CATCH<br>FISH</div>
        <button class="menu-btn" onclick="start3DGame()">▶ CONTINUE / PLAY</button>
        <button class="menu-btn" onclick="start3DGame()">★ NEW GAME</button>
        <button class="menu-btn" onclick="alert('Lái thuyền 3D bằng phím W/A/S/D. Lái sát vào Đảo và nhấn [SPACE] để săn cá Boss!')">⚙ INSTRUCTIONS</button>
    </div>

    <!-- HUD THÔNG SỐ -->
    <div id="hud">
        <div class="hud-item">💰 Vàng: <span id="goldVal">200</span></div>
        <div class="hud-item">❤️ HP: <span id="hpVal">100</span></div>
        <div class="hud-item">🚤 Thuyền 3D: <span id="boatVal">Cấp 1</span></div>
        <div class="hud-item">🔑 Chìa khóa: <span id="keyVal">1/3</span></div>
        <div class="hud-item">📍 Đảo: <span id="islandVal">Đảo Tân Thủ</span></div>
    </div>

    <!-- MINIGAME CÂU CÁ 3D -->
    <div id="fishingUI">
        <h3 id="bossTitle" style="color: #f6ad55; margin-bottom: 5px;">⚔️ CHIẾN ĐẤU BOSS</h3>
        <p style="font-size: 13px; color: #94a3b8;">Bấm [SPACE] liên tục để giữ vạch màu xanh dương ở vùng an toàn màu xanh lá!</p>
        
        <div class="bar-bg">
            <div id="progBar" class="bar-fill"></div>
        </div>
        
        <div class="bar-bg" style="height: 30px;">
            <div class="safe-zone"></div>
            <div id="tensionBar" class="tension-indicator" style="left: 50%;"></div>
        </div>

        <button style="margin-top: 10px; padding: 8px 20px; background: #ef4444; border: none; color: white; font-weight: bold; border-radius: 6px; cursor: pointer;" onclick="cancelFishing()">Rút Lui</button>
    </div>

    <div id="msgBox"></div>

<script>
// --- THREE.JS INITIALIZATION ---
let scene, camera, renderer;
let boat3D, ocean;
let islandMeshes = [];

// --- GAME LOGIC STATES ---
let inMenu = true;
let isFishing = false;
let gold = 200, hp = 100, boatLevel = 1;
let keysOwned = [1];
let currentIslandId = 1;

// --- BOAT MOVEMENT VARIABLES ---
const boatState = {
    x: 0, z: 0, angle: 0, speed: 0,
    maxSpeed: 0.6, accel: 0.02, friction: 0.96
};

const keys = {};
window.addEventListener('keydown', e => keys[e.code] = true);
window.addEventListener('keyup', e => keys[e.code] = false);

// --- DỮ LIỆU CÁC ĐẢO 3D ---
const islandData = [
    { id: 1, name: "Đảo Tân Thủ", x: -40, z: -40, radius: 25, color: 0x22c55e, boss: "🦈 Cá Trê Khổng Lồ", keyReq: null, keyReward: 2 },
    { id: 2, name: "Đảo San Hò", x: 50, z: -50, radius: 30, color: 0x06b6d4, boss: "🐊 Cá Sấu Nước Mặn", keyReq: 2, keyReward: 3 },
    { id: 3, name: "Đảo Quái Vật", x: 10, z: 60, radius: 35, color: 0xef4444, boss: "🐉 Thủy Quái Leviathan", keyReq: 3, keyReward: 4 }
];

function init3D() {
    const container = document.getElementById('webgl-container');
    
    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0b1d28);
    scene.fog = new THREE.FogExp2(0x0b1d28, 0.008);

    // Camera
    camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 30, 50);

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xffedd5, 1.2);
    sunLight.position.set(100, 150, 50);
    sunLight.castShadow = true;
    scene.add(sunLight);

    // Ocean Surface
    const waterGeo = new THREE.PlaneGeometry(500, 500, 32, 32);
    const waterMat = new THREE.MeshPhongMaterial({ color: 0x0f3854, shininess: 80, flatShading: true });
    ocean = new THREE.Mesh(waterGeo, waterMat);
    ocean.rotation.x = -Math.PI / 2;
    scene.add(ocean);

    // Create 3D Islands
    islandData.forEach(isl => {
        const islandGroup = new THREE.Group();
        islandGroup.position.set(isl.x, 0, isl.z);

        // Island Land Mesh
        const landGeo = new THREE.CylinderGeometry(isl.radius, isl.radius + 10, 8, 16);
        const landMat = new THREE.MeshLambertMaterial({ color: isl.color });
        const land = new THREE.Mesh(landGeo, landMat);
        land.position.y = 2;
        islandGroup.add(land);

        // Palm trees on island
        for(let i=0; i<5; i++) {
            const trunkGeo = new THREE.CylinderGeometry(0.5, 0.8, 8);
            const trunkMat = new THREE.MeshLambertMaterial({ color: 0x78350f });
            const trunk = new THREE.Mesh(trunkGeo, trunkMat);
            trunk.position.set((Math.random()-0.5)*isl.radius*0.8, 8, (Math.random()-0.5)*isl.radius*0.8);
            islandGroup.add(trunk);
        }

        scene.add(islandGroup);
        islandMeshes.push({ group: islandGroup, data: isl });
    });

    // Create 3D Boat
    boat3D = new THREE.Group();
    const hullGeo = new THREE.ConeGeometry(3, 10, 4);
    const hullMat = new THREE.MeshStandardMaterial({ color: 0x9a3412, roughness: 0.4 });
    const hull = new THREE.Mesh(hullGeo, hullMat);
    hull.rotation.x = Math.PI / 2;
    boat3D.add(hull);

    boat3D.position.set(0, 1.5, 0);
    scene.add(boat3D);

    window.addEventListener('resize', onWindowResize);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// --- MINIGAME FISHING LOGIC ---
let tension = 50, progress = 0;

function start3DGame() {
    document.getElementById('mainMenu').style.display = 'none';
    document.getElementById('hud').style.display = 'flex';
    inMenu = false;
    showMsg("⛵ Hãy dùng phím W/A/S/D để lái thuyền 3D đến các hòn đảo!");
}

function showMsg(txt, duration = 3000) {
    const box = document.getElementById('msgBox');
    box.innerText = txt;
    box.style.display = 'block';
    setTimeout(() => { box.style.display = 'none'; }, duration);
}

// --- ANIMATION & GAME LOOP ---
function animate() {
    requestAnimationFrame(animate);

    if (inMenu) {
        // Camera xoay vòng quanh đại dương ở màn hình Menu chính
        const time = Date.now() * 0.0003;
        camera.position.x = Math.sin(time) * 90;
        camera.position.z = Math.cos(time) * 90;
        camera.position.y = 45;
        camera.lookAt(0, 0, 0);
    } else if (!isFishing) {
        // Lái thuyền 3D
        if (keys['KeyW'] || keys['ArrowUp']) boatState.speed = Math.min(boatState.speed + boatState.accel, boatState.maxSpeed);
        else if (keys['KeyS'] || keys['ArrowDown']) boatState.speed = Math.max(boatState.speed - boatState.accel, -boatState.maxSpeed/2);
        else boatState.speed *= boatState.friction;

        if (keys['KeyA'] || keys['ArrowLeft']) boatState.angle += 0.04;
        if (keys['KeyD'] || keys['ArrowRight']) boatState.angle -= 0.04;

        boatState.x += Math.sin(boatState.angle) * boatState.speed;
        boatState.z += Math.cos(boatState.angle) * boatState.speed;

        boat3D.position.x = boatState.x;
        boat3D.position.z = boatState.z;
        boat3D.rotation.y = boatState.angle;

        // Camera đi theo sau thuyền 3D (Third person camera)
        camera.position.x = boatState.x - Math.sin(boatState.angle) * 35;
        camera.position.z = boatState.z - Math.cos(boatState.angle) * 35;
        camera.position.y = boatState.y + 20;
        camera.lookAt(boatState.x, 2, boatState.z);

        // Kiểm tra khoảng cách sát đảo
        islandData.forEach(isl => {
            const dx = boatState.x - isl.x;
            const dz = boatState.z - isl.z;
            const dist = Math.sqrt(dx*dx + dz*dz);

            if (dist < isl.radius + 8) {
                if (isl.keyReq && !keysOwned.includes(isl.keyReq)) {
                    showMsg("🔒 Đảo này chưa có chìa khóa mở cổng!");
                } else {
                    if (keys['Space']) {
                        currentIslandId = isl.id;
                        openFishingMinigame(isl);
                    } else {
                        showMsg("⚓ Bấm [SPACE] để thả cần săn Boss " + isl.boss + "!");
                    }
                }
            }
        });
    } else {
        // Cập nhật minigame câu cá
        tension -= 0.35;
        if (keys['Space']) tension += 1.2;
        tension = Math.max(0, Math.min(100, tension));

        document.getElementById('tensionBar').style.left = tension + '%';

        if (tension >= 40 && tension <= 70) progress += 0.4;
        else progress -= 0.15;
        progress = Math.max(0, Math.min(100, progress));

        document.getElementById('progBar').style.width = progress + '%';

        if (progress >= 100) {
            const currentIsl = islandData[currentIslandId - 1];
            if (!keysOwned.includes(currentIsl.keyReward)) {
                keysOwned.push(currentIsl.keyReward);
                showMsg("🎉 THẮNG LỢI! Hạ gục " + currentIsl.boss + " & nhận CHÌA KHÓA mới!", 4000);
            } else {
                gold += 200;
                showMsg("🎉 Thắng Boss +200 🪙 Vàng!", 3000);
            }
            cancelFishing();
        }
    }

    // Cập nhật HUD
    document.getElementById('goldVal').innerText = gold;
    document.getElementById('hpVal').innerText = hp;
    document.getElementById('keyVal').innerText = keysOwned.length + "/3";
    document.getElementById('islandVal').innerText = islandData[currentIslandId - 1].name;

    renderer.render(scene, camera);
}

function openFishingMinigame(isl) {
    isFishing = true;
    tension = 50; progress = 0;
    document.getElementById('bossTitle').innerText = "⚔️ SĂN BOSS: " + isl.boss;
    document.getElementById('fishingUI').style.display = 'block';
}

function cancelFishing() {
    isFishing = false;
    document.getElementById('fishingUI').style.display = 'none';
}

// Khởi chạy Three.js
init3D();
animate();
</script>
</body>
</html>
"""

# Nhúng vào ứng dụng Streamlit
components.html(threejs_game_code, height=750, scrolling=False)
