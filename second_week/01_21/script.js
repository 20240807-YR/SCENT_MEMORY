window.onload = function() {
    const container = document.querySelector('.scroll-container');
    if (container) container.scrollTo(0, 0);
    
    forceVideoPlay(); 
    // initAgent(); // [삭제] 팅커벨 초기화 제거
    startParticleSystem(); 
    initInteractions(); 
    initSectionObserver(); 
    initChatSystem(); // [추가] 채팅 시스템 초기화
};

/* =========================================
   1. [삭제됨] AI AGENT 관련 코드 전체 제거
========================================= */
// let agentX = 0, agentY = 0; ... (모두 삭제)
// function initAgent() { ... } (모두 삭제)
// function summonAgent(x, y) { ... } (모두 삭제)
// function animateAgent() { ... } (모두 삭제)


/* =========================================
   2. INTERACTION (Clicks & Chat Toggle)
========================================= */
function initInteractions() {
    const sections = document.querySelectorAll('.section');

    sections.forEach(section => {
        section.addEventListener('click', (e) => {
            // 카드, 버튼, 채팅창, 채팅 열기 버튼 클릭은 무시
            if (e.target.closest('.glass-card') || 
                e.target.closest('button') || 
                e.target.closest('#chat-window') ||
                e.target.closest('#open-chat-btn')) return;

            // 더블 클릭 로직 제거 -> 단일 클릭으로 정보창 토글만 유지
            toggleSectionInfo(section, true);
        });
    });

    // 정보창 닫기 버튼
    document.querySelectorAll('.btn-close.card-close').forEach(btn => { // 클래스 구분 필요
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const section = btn.closest('.section');
            toggleSectionInfo(section, false);
        });
    });
}

function toggleSectionInfo(section, show) {
    if (section.classList.contains('hero-section')) return;
    const clickArea = section.querySelector('.click-area');
    if (clickArea) {
        if (show) {
            clickArea.classList.add('show-info');
            section.classList.add('dim-video');
        } else {
            clickArea.classList.remove('show-info');
            section.classList.remove('dim-video');
        }
    }
}


/* =========================================
   3. PARTICLE COLOR SYSTEM (유지)
========================================= */
const PARTICLE_COLORS = {
    'hero': '255, 255, 255',
    'top': '220, 255, 220',
    'middle': '255, 200, 230',
    'base': '255, 245, 220'
};

function initSectionObserver() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const video = entry.target.querySelector('video');
                if(video) { video.currentTime = 0; video.play(); }

                const id = entry.target.id.split('-')[0];
                const colorRGB = PARTICLE_COLORS[id] || '255, 255, 255';
                document.documentElement.style.setProperty('--particle-color', `rgba(${colorRGB}, 0.8)`);
            } else {
                const video = entry.target.querySelector('video');
                if(video) video.pause();
            }
        });
    }, { threshold: 0.5 });
    document.querySelectorAll('.section').forEach(section => observer.observe(section));
}

function startParticleSystem() {
    const container = document.getElementById('particle-container');
    setInterval(() => {
        const petal = document.createElement('div');
        petal.classList.add('petal');
        petal.style.left = Math.random() * 100 + 'vw';
        const size = Math.random() * 8 + 5; 
        petal.style.width = size + 'px';
        petal.style.height = size + 'px';
        petal.style.animationDuration = (Math.random() * 5 + 8) + 's';
        container.appendChild(petal);
        setTimeout(() => petal.remove(), 12000);
    }, 300);
}


/* =========================================
   4. CHAT SYSTEM (Updated for Black Theme)
========================================= */
const chatWindow = document.getElementById('chat-window');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const chatMessages = document.getElementById('chat-messages');
const openChatBtn = document.getElementById('open-chat-btn');
const closeChatBtn = document.getElementById('close-chat-btn');

function initChatSystem() {
    // 채팅창 열기 버튼 클릭
    openChatBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        chatWindow.classList.add('open');
        openChatBtn.style.display = 'none'; // 열리면 버튼 숨김
        setTimeout(() => chatInput.focus(), 400); // 포커스 이동
    });

    // 채팅창 닫기 버튼 클릭
    closeChatBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        chatWindow.classList.remove('open');
        openChatBtn.style.display = 'flex'; // 닫히면 버튼 다시 표시
    });

    // 메시지 전송 이벤트
    sendBtn.addEventListener('click', handleUserMessage);
    chatInput.addEventListener('keypress', (e) => { if(e.key === 'Enter') handleUserMessage(); });
}

function handleUserMessage() {
    const text = chatInput.value.trim();
    if(!text) return;
    
    addMessage(text, 'user');
    chatInput.value = '';

    // [로레알 마케터 시뮬레이션]
    setTimeout(() => {
        let reply = "";
        // (기존 로직 유지)
        if(text.includes("추천") || text.includes("향수")) {
            reply = `고객님, 편안하면서도 세련된 무드를 찾으시는군요.<br>
            그렇다면 로레알의 베스트셀러, <strong>Lazy Sunday Morning</strong>은 어떠세요? 
            일요일 아침의 깨끗한 리넨 같은 향이라 고객님 취향에 딱 맞을 거예요.`;
        } else if (text.includes("안녕")) {
            reply = "안녕하세요! 로레알 뷰티 어드바이저입니다. 오늘 기분이나 스타일은 어떠신가요? 딱 맞는 향을 찾아드릴게요.";
        } else if (text.includes("가격") || text.includes("얼마")) {
            reply = `가치는 숫자로 매길 수 없지만... 합리적인 선택이 되실 거예요. 
            매장에서 시향해 보시면 <strong>White Musk</strong> 잔향에 반해서 바로 구매하게 되실걸요?`;
        } else {
            reply = `아, 그런 느낌이시군요! 아주 감각적이세요.<br>
            그런 날엔 <strong>Lazy Sunday Morning</strong>의 부드러운 <strong>Iris</strong> 노트가 
            고객님의 분위기를 한층 더 우아하게 만들어 줄 수 있답니다.`;
        }
        addMessage(reply, 'bot');
    }, 1000);
}

// 메시지 추가 함수 (구조 변경에 맞춰 수정)
function addMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    // 프로필 사진 제거 (헤더에 있으므로 불필요)

    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'bubble';
    bubbleDiv.innerHTML = text;
    
    messageDiv.appendChild(bubbleDiv);
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function forceVideoPlay() {
    document.querySelectorAll('video').forEach(v => {
        v.muted = true; v.play().catch(()=>{});
    });
}