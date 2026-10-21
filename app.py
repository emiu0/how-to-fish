import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit full màn hình
st.set_page_config(
    page_title="How to Catch Fish 3D - Low-Poly Remastered",
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
    body { overflow: hidden; background-color: #040914; margin: 0; }
    </style>
""", unsafe_allow_html=True)

# WebGL 3D Game Engine (Three.js)
game_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>How to Fish 3D Remastered</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        body, html { width: 100%; height: 100%; overflow: hidden; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #040914; }
        #webgl-container { width: 100vw; height: 100vh; display: block; }
        
        /* MAIN MENU GIAO DIỆN CHUẨN YOUTUBE */
        #mainMenu {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(90deg, rgba(4,9,20,0.95) 0%, rgba(4,9,20,0.4) 55%, rgba(4,9,20,0) 100%);
            display: flex; flex-direction: column; justify-content: center; padding-left: 8%;
            z-index: 100;
        }
        .game-subtitle { font-size: 13px; letter-spacing: 5px; color: #94a3b8; margin-bottom: 5px; border-left: 3px solid #f6ad55; padding-left: 10px; font-weight: bold; }
        .game-title { font-size: 64px; font-weight: 900; line-height: 0.92; color: #f6ad55; text-transform: uppercase; margin-bottom: 30px; text-shadow: 4px 4px 12px rgba(0,0,0,0.9); font-family: 'Courier New', monospace; }
        .menu-btn {
            width: 240px; padding: 14px 22px; margin-bottom: 12px; background: rgba(15, 23, 42, 0.85); color: #e2e8f0;
            border: 1px solid #334155; border-radius: 6px; font-weight: bold; font-size: 15px; text-align: left;
            cursor: pointer; transition: all 0.25s ease; backdrop-filter: blur(8px);
        }
        .menu-btn:hover { background: #f6ad55; color: #040914; border-color: #f6ad55; transform: translateX(10px); }

        /* HUD BANNER */
        #hud {
            position: absolute; top: 15px; left: 15px; right: 15px; display: none; justify-content: space-between;
            background: rgba(11, 19, 30, 0.85); padding: 12px 25px; border-radius: 10px; border: 1px solid #1e293b; color: white;
            font-weight: bold; z-index: 10; backdrop-filter: blur(8px); box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }
        .hud-item { display: flex; align-items: center; gap: 8px; font-size: 15px; }

        /* KHUNG TƯƠNG TÁC / THÔNG BÁO */
        #promptBox {
            position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%);
            background: rgba(15, 23, 42, 0.9); color: #38bdf8; padding: 12px 30px; border-radius: 30px;
            border: 2px solid #00d2ff; font-weight: bold; display: none; z-index: 20; text-align: center;
            box-shadow: 0 0 25px rgba(0, 210, 255, 0.4); backdrop-filter: blur(5px);
        }
        #dialogBox {
            position: absolute; bottom: 100px; left: 50%; transform: translateX(-50%);
            background: rgba(15, 23, 42, 0.95); color: #f8fafc; padding: 20px 35px; border-radius: 15px;
            border: 2px solid #f6ad55; font-weight: bold; display: none; z-index: 30; width: 450px; text-align: left;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        }
    </style>
    <!-- THƯ VIỆN THREE.JS 3D ENGINE -->
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
        <button class="menu-btn" onclick="alert('Phím W/A/S/D: Di chuyển đi bộ hoặc Lái thuyền\nSPACE: Nhảy\nPhím 1: Cần câu / Phím 2: Súng săn Shotgun\nPhím E: Nói chuyện NPC / Lên thuyền\nGiữ Chuột Phải: Xoay Camera 3D\nChuột Trái: Bắn súng / Quăng câu')">⚙ SETTINGS</button>
    </div>

    <!-- HUD TRONG GAME -->
    <div id="hud">
        <div class="hud-item">💰 Vàng: <span id="goldVal">250</span></div>
        <div class="hud-item">❤️ HP: <span id="hpVal">100</span></div>
        <div class="hud-item">🗡️ Trang bị: <span id="itemVal">Cần câu (Phím 1)</span></div>
        <div class="hud-item">🔑 Chìa khóa: <span id="keyVal">1/3</span></div>
        <div class="hud-item">📍 Vị trí: <span id="locVal">Đảo Tân Thủ</span></div>
    </div>

    <div id="promptBox">Bấm [E] để tương tác</div>
    <div id="dialogBox">
        <div style="color: #f6ad55; font-size: 18px; margin-bottom: 8px;" id="dialogSpeaker">👨‍🌾 Lão Ngư Joe:</div>
        <div id="dialogText" style="font-size: 14px; line-height: 1.5; color: #cbd5e1;">Chào cậu! Vùng biển này đang có nhiều quái vật xuất hiện. Hãy mang theo súng săn khi lái thuyền ra xa nhé!</div>
        <div style="font-size: 11px; color: #64748b; margin-top: 10px; text-align: right;">Bấm [E] để đóng</div>
    </div>

<script>
let scene, camera, renderer;
let player, boat, npcJoe, rodMesh, shotgunMesh;
let isBoating = false, inMenu = true;

let gold = 250, hp = 100, activeEquip = "ROD"; // ROD, SHOTGUN
let walkCycle = 0;

const keys = {};
const playerState = { x: 0, y: 7, z: 0, vx: 0, vy: 0, vz: 0, rotY: 0, isGrounded: true };
const boatState = { x: 20, z: 20, rotY: 0, speed: 0, maxSpeed: 0.6, accel: 0.02, friction: 0.95 };

window.addEventListener('keydown', e => {
    keys[e.code] = true;
    if (e.code === 'Digit1') { activeEquip = "ROD"; updateEquipVisual(); }
    if (e.code === 'Digit2') { activeEquip = "SHOTGUN"; updateEquipVisual(); }
});
window.addEventListener('keyup', e => keys[e.code] = false);

// Chuột bắn súng / quăng câu
window.addEventListener('mousedown', e => {
    if (e.button === 0 && !inMenu) {
        if (activeEquip === "SHOTGUN") {
            shootShotgun();
        } else if (activeEquip === "ROD") {
            alert("🎣 Bạn đã quăng câu xuống nước! Đang chờ cá cắn câu...");
        }
    }
});

function init3D() {
    const container = document.getElementById('webgl-container');

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x061523);
    scene.fog = new THREE.FogExp2(0x061523, 0.005);

    camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 25, 40);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    // Ánh sáng PBR
    const ambLight = new THREE.AmbientLight(0xffffff, 0.65);
    scene.add(ambLight);

    const dirLight = new THREE.DirectionalLight(0xffedd5, 1.2);
    dirLight.position.set(80, 120, 60);
    dirLight.castShadow = true;
    scene.add(dirLight);

    // Biển 3D với hiệu ứng sóng
    const oceanGeo = new THREE.PlaneGeometry(600, 600, 48, 48);
    const oceanMat = new THREE.MeshPhongMaterial({ color: 0x0f2b3d, shininess: 90, flatShading: true });
    const ocean = new THREE.Mesh(oceanGeo, oceanMat);
    ocean.rotation.x = -Math.PI / 2;
    scene.add(ocean);

    // Đảo Khởi Nguồn 3D Low-Poly
    const islandGroup = new THREE.Group();
    const landGeo = new THREE.CylinderGeometry(35, 42, 10, 20);
    const landMat = new THREE.MeshLambertMaterial({ color: 0x16a34a });
    const land = new THREE.Mesh(landGeo, landMat);
    land.position.y = 3;
    islandGroup.add(land);

    // Bãi cát
    const sandGeo = new THREE.CylinderGeometry(40, 45, 2, 20);
    const sandMat = new THREE.MeshLambertMaterial({ color: 0xfef08a });
    const sand = new THREE.Mesh(sandGeo, sandMat);
    sand.position.y = 0.5;
    islandGroup.add(sand);

    // Cây dừa low-poly trên đảo
    for (let i = 0; i < 8; i++) {
        const trunkGeo = new THREE.CylinderGeometry(0.6, 0.9, 10);
        const trunkMat = new THREE.MeshLambertMaterial({ color: 0x854d0e });
        const trunk = new THREE.Mesh(trunkGeo, trunkMat);
        const angle = (i / 8) * Math.PI * 2;
        const r = 15 + Math.random() * 12;
        trunk.position.set(Math.cos(angle)*r, 12, Math.sin(angle)*r);
        trunk.rotation.z = (Math.random() - 0.5) * 0.2;
        islandGroup.add(trunk);

        const leavesGeo = new THREE.ConeGeometry(5, 4, 6);
        const leavesMat = new THREE.MeshLambertMaterial({ color: 0x15803d });
        const leaves = new THREE.Mesh(leavesGeo, leavesMat);
        leaves.position.set(trunk.position.x, 17, trunk.position.z);
        islandGroup.add(leaves);
    }

    scene.add(islandGroup);

    // Bến tàu gỗ (Pier)
    const pierGeo = new THREE.BoxGeometry(8, 1, 22);
    const pierMat = new THREE.MeshLambertMaterial({ color: 0x78350f });
    const pier = new THREE.Mesh(pierGeo, pierMat);
    pier.position.set(0, 4.5, 30);
    scene.add(pier);

    // Mô hình Nhân vật Chính 3D (Humanoid Low-Poly Puppet)
    player = new THREE.Group();
    
    const bodyGeo = new THREE.CylinderGeometry(0.9, 0.9, 3.2, 8);
    const bodyMat = new THREE.MeshLambertMaterial({ color: 0x1d4ed8 }); // Áo lam đặc trưng
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.position.y = 2;
    player.add(body);

    const headGeo = new THREE.SphereGeometry(1.0, 8, 8);
    const headMat = new THREE.MeshLambertMaterial({ color: 0xfde047 });
    const head = new THREE.Mesh(headGeo, headMat);
    head.position.y = 4.2;
    player.add(head);

    // Cần câu 3D & Súng săn 3D trên tay
    const rodGeo = new THREE.CylinderGeometry(0.1, 0.2, 10);
    const rodMat = new THREE.MeshLambertMaterial({ color: 0xf59e0b });
    rodMesh = new THREE.Mesh(rodGeo, rodMat);
    rodMesh.rotation.x = Math.PI / 3;
    rodMesh.position.set(1.2, 3, 2);
    player.add(rodMesh);

    const gunGeo = new THREE.BoxGeometry(0.4, 0.6, 5);
    const gunMat = new THREE.MeshLambertMaterial({ color: 0x334155 });
    shotgunMesh = new THREE.Mesh(gunGeo, gunMat);
    shotgunMesh.position.set(1.2, 2.5, 1.5);
    shotgunMesh.visible = false;
    player.add(shotgunMesh);

    player.position.set(0, 8, 25);
    scene.add(player);

    // Thuyền máy 3D
    boat = new THREE.Group();
    const boatHullGeo = new THREE.BoxGeometry(6, 2.5, 14);
    const boatHullMat = new THREE.MeshLambertMaterial({ color: 0x9a3412 });
    const boatHull = new THREE.Mesh(boatHullGeo, boatHullMat);
    boatHull.position.y = 1;
    boat.add(boatHull);

    boat.position.set(12, 1, 30);
    scene.add(boat);

    // NPC Fisherman Joe
    npcJoe = new THREE.Group();
    const npcBody = new THREE.Mesh(bodyGeo, new THREE.MeshLambertMaterial({ color: 0xea580c })); // Áo cam
    npcBody.position.y = 2;
    npcJoe.add(npcBody);
    const npcHead = new THREE.Mesh(headGeo, headMat);
    npcHead.position.y = 4.2;
    npcJoe.add(npcHead);
    npcJoe.position.set(-2, 8, 28);
    scene.add(npcJoe);

    window.addEventListener('resize', onWindowResize);
}

function updateEquipVisual() {
    if (activeEquip === "ROD") {
        rodMesh.visible = true;
        shotgunMesh.visible = false;
    } else {
        rodMesh.visible = false;
        shotgunMesh.visible = true;
    }
    document.getElementById('itemVal').innerText = activeEquip === "ROD" ? "Cần câu (Phím 1)" : "Súng săn Shotgun (Phím 2)";
}

function shootShotgun() {
    // Hiệu ứng lóe sáng nổ súng
    const flash = new THREE.PointLight(0xfef08a, 5, 20);
    flash.position.set(player.position.x, player.position.y + 3, player.position.z + 3);
    scene.add(flash);
    setTimeout(() => scene.remove(flash), 100);
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

// --- GAME LOOP 3D ---
function animate() {
    requestAnimationFrame(animate);

    if (inMenu) {
        // Camera tự động xoay quanh đảo 3D ở Menu chính
        const t = Date.now() * 0.0003;
        camera.position.x = Math.sin(t) * 75;
        camera.position.z = Math.cos(t) * 75;
        camera.position.y = 35;
        camera.lookAt(0, 0, 0);
    } else {
        if (!isBoating) {
            // Điều khiển Nhân vật
            let moveX = 0, moveZ = 0;
            if (keys['KeyW']) moveZ -= 0.35;
            if (keys['KeyS']) moveZ += 0.35;
            if (keys['KeyA']) moveX -= 0.35;
            if (keys['KeyD']) moveX += 0.35;

            playerState.x += moveX;
            playerState.z += moveZ;

            if (moveX !== 0 || moveZ !== 0) {
                player.rotation.y = Math.atan2(moveX, moveZ);
            }

            // Nhảy (Jump)
            if (keys['Space'] && playerState.isGrounded) {
                playerState.vy = 0.8;
                playerState.isGrounded = false;
            }

            // Trọng lực rơi
            playerState.vy -= 0.04;
            playerState.y += playerState.vy;

            if (playerState.y <= 8) {
                playerState.y = 8;
                playerState.vy = 0;
                playerState.isGrounded = true;
            }

            player.position.set(playerState.x, playerState.y, playerState.z);

            // Camera góc nhìn thứ ba đi theo Nhân vật
            camera.position.x = playerState.x;
            camera.position.z = playerState.z + 22;
            camera.position.y = playerState.y + 12;
            camera.lookAt(playerState.x, playerState.y + 2, playerState.z);

            // Kiểm tra tương tác gần NPC hoặc Thuyền
            const prompt = document.getElementById('promptBox');
            const distNPC = player.position.distanceTo(npcJoe.position);
            const distBoat = player.position.distanceTo(boat.position);

            if (distNPC < 5) {
                prompt.style.display = 'block';
                prompt.innerText = "Bấm [E] để đối thoại với Lão Ngư Joe";
                if (keys['KeyE']) {
                    document.getElementById('dialogBox').style.display = 'block';
                    keys['KeyE'] = false;
                }
            } else if (distBoat < 6) {
                prompt.style.display = 'block';
                prompt.innerText = "Bấm [E] để Lên / Lái Thuyền";
                if (keys['KeyE']) {
                    isBoating = true;
                    player.visible = false;
                    keys['KeyE'] = false;
                }
            } else {
                prompt.style.display = 'none';
            }
        } else {
            // Điều khiển Lái Thuyền 3D
            if (keys['KeyW']) boatState.speed = Math.min(boatState.speed + boatState.accel, boatState.maxSpeed);
            else if (keys['KeyS']) boatState.speed = Math.max(boatState.speed - boatState.accel, -boatState.maxSpeed / 2);
            else boatState.speed *= boatState.friction;

            if (keys['KeyA']) boatState.rotY += 0.035;
            if (keys['KeyD']) boatState.rotY -= 0.035;

            boatState.x += Math.sin(boatState.rotY) * boatState.speed;
            boatState.z += Math.cos(boatState.rotY) * boatState.speed;

            boat.position.set(boatState.x, 1, boatState.z);
            boat.rotation.y = boatState.rotY;

            // Camera đi theo Thuyền
            camera.position.x = boatState.x - Math.sin(boatState.rotY) * 35;
            camera.position.z = boatState.z - Math.cos(boatState.rotY) * 35;
            camera.position.y = 20;
            camera.lookAt(boatState.x, 2, boatState.z);

            const prompt = document.getElementById('promptBox');
            prompt.style.display = 'block';
            prompt.innerText = "Đang lái thuyền. Bấm [E] để Rời Thuyền";

            if (keys['KeyE']) {
                isBoating = false;
                player.visible = true;
                playerState.x = boatState.x + 3;
                playerState.z = boatState.z + 3;
                keys['KeyE'] = false;
            }
        }
    }

    // Đóng hộp thoại
    if (keys['KeyE'] && document.getElementById('dialogBox').style.display === 'block') {
        document.getElementById('dialogBox').style.display = 'none';
        keys['KeyE'] = false;
    }

    renderer.render(scene, camera);
}

// Khởi chạy
init3D();
animate();
</script>
</body>
</html>
"""

# Nhúng ứng dụng game 3D vào Streamlit
components.html(game_code, height=780, scrolling=False)
