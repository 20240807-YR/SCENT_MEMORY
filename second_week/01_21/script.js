window.onload = function() {
    // 1. 스크롤 위치 초기화 (새로고침 시 깨짐 방지)
    const container = document.querySelector('.scroll-container');
    if (container) {
        container.scrollTo(0, 0);
    }

    // 2. [핵심] 비디오 강제 재생 스크립트
    const videos = document.querySelectorAll('video');
    
    videos.forEach(video => {
        // 브라우저 정책상 소리 끈 상태(muted)여야 자동 재생 가능
        video.muted = true;
        video.playsInline = true; // iOS 대응
        
        // 재생 시도
        const playPromise = video.play();

        if (playPromise !== undefined) {
            playPromise.then(_ => {
                // 재생 성공!
                console.log("Video playing successfully");
            })
            .catch(error => {
                // 재생 실패 시 로그 출력
                console.log("Autoplay blocked. Trying to force mute.", error);
                video.muted = true;
                video.play();
            });
        }
    });
};

// Intersection Observer (섹션 감지 시 클래스 추가 - 필요 시 확장 가능)
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active');
            // 화면에 들어온 비디오 다시 재생 확인
            const video = entry.target.querySelector('video');
            if(video) video.play(); 
        } else {
            // 화면에서 나가면 멈춤 (성능 최적화)
            const video = entry.target.querySelector('video');
            if(video) video.pause();
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('.section').forEach(section => {
    observer.observe(section);
});