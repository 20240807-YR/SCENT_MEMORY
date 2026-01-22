// SCENT_DATA에 색상 정보(color) 추가
const SCENT_DATA = {
    top: { 
        video: "../01_21/assets/video/top/top.mp4", 
        title: "TOP NOTE", 
        desc: "Fresh Pear & Lily of the Valley",
        color: "#e8f5e9" // 연한 초록색 (Pear)
    },
    middle: { 
        video: "../01_21/assets/video/middle/middle.mp4", 
        title: "MIDDLE NOTE", 
        desc: "Iris & Rose, Floral Powdery",
        color: "#f8bbd0" // 분홍색 (Rose)
    },
    base: { 
        video: "../01_21/assets/video/base/base.mp4", 
        title: "BASE NOTE", 
        desc: "White Musk & Patchouli Skin Scent",
        color: "#efebe9" // 베이지색 (Musk)
    },
    overall: { 
        video: "../01_21/assets/video/hero/hero.mp4", 
        title: "OVERALL IMPRESSION", 
        desc: "Maison Margiela Lazy Sunday Morning",
        color: "#ffffff" // 흰색 (Clean Linen)
    }
};

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. 섹션 스크롤 감지 (기존 유지)
    const sections = document.querySelectorAll('.section');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, { threshold: 0.3 });

    sections.forEach(sec => observer.observe(sec));


    // 2. 비디오 오버레이 및 파티클 로직
    const navButtons = document.querySelectorAll('.nav-btn');
    const overlay = document.getElementById('visual-overlay');
    const closeBtn = document.getElementById('close-overlay-btn');
    const videoElement = document.getElementById('evidence-video');
    const overlayTitle = document.getElementById('overlay-title');
    const overlayDesc = document.getElementById('overlay-desc');
    const petalContainer = document.getElementById('petal-container'); // 파티클 컨테이너

    // 꽃잎 생성 함수
    function createPetals(color) {
        petalContainer.innerHTML = ''; // 기존 꽃잎 초기화
        const petalCount = 30; // 꽃잎 개수

        for (let i = 0; i < petalCount; i++) {
            const petal = document.createElement('div');
            petal.classList.add('petal');
            petal.style.setProperty('--petal-color', color); // 색상 설정
            
            // 랜덤 위치 및 애니메이션 설정
            petal.style.left = `${Math.random() * 100}%`;
            petal.style.animationDuration = `${Math.random() * 3 + 3}s`; // 3~6초
            petal.style.animationDelay = `${Math.random() * 2}s`;
            
            petalContainer.appendChild(petal);
        }
    }

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.getAttribute('data-target');
            const data = SCENT_DATA[target];
            if(data) {
                videoElement.src = data.video;
                overlayTitle.textContent = data.title;
                overlayDesc.textContent = data.desc;
                
                overlay.classList.remove('hidden');
                void overlay.offsetWidth; 
                overlay.classList.add('visible');
                
                videoElement.play().catch(e => console.log("Video Play Error:", e));

                // 파티클 효과 실행
                createPetals(data.color);
            }
        });
    });

    closeBtn.addEventListener('click', () => {
        overlay.classList.remove('visible');
        setTimeout(() => {
            overlay.classList.add('hidden');
            videoElement.pause();
            videoElement.src = "";
            petalContainer.innerHTML = ''; // 오버레이 닫으면 꽃잎 제거
        }, 500);
    });


    // 3. 채팅 인터페이스 로직 (기존 유지)
    const chatHistory = document.getElementById('chat-history');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // 초기 Aura Muse 인사 메시지를 대화 히스토리로 처리
    appendMessage(
        "반갑습니다. Aura Muse입니다.<br>당신의 기억 속 일요일 아침은 어떤 풍경인가요?<br>지금 머무르고 있는 공간의 분위기나 기분을 들려주세요.",
        "agent-msg"
    );

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        appendMessage(text, 'user-msg');
        userInput.value = '';

        const loadingId = appendMessage("…", 'agent-msg');

        try {
            const response = await fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            if (!response.ok) throw new Error('Server Error');

            const data = await response.json();
            
            const loadingMsg = document.getElementById(loadingId);
            if(loadingMsg) loadingMsg.remove();
            
            appendMessage(data.reply, 'agent-msg');

        } catch (error) {
            console.error('Connection Error:', error);
            const loadingMsg = document.getElementById(loadingId);
            if (loadingMsg) {
                loadingMsg.innerText = "잠시 응답이 지연되고 있습니다. 다시 한 번 말을 걸어주세요.";
            }
        }
    }

    function appendMessage(text, className) {
        const div = document.createElement('div');
        div.className = `message ${className}`;
        div.innerHTML = text.replace(/\n/g, '<br>');
        div.id = 'msg-' + Date.now();
        chatHistory.appendChild(div);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        return div.id;
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});