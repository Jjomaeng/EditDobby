/* 사진이랑 글을 같은 index를 줘서 사진에 맞는 글이 나오게끔 하는 작업 */

(() => {
    // 새가 x방향으로 윈도우 폭만큼 날라가게함, true면 실행하게하고 false면 새가 다시 원래위치로 돌아오게끔
    const actions = {
        birdFly(key) {
            if (key) {
                document.querySelector('[data-index="3"] .bird').style.transform = `translateX(${window.innerWidth}px)`;
            } else {
                document.querySelector('[data-index="3"] .bird').style.transform = `translateX(-100%)`;
            }
        },
        birdFly2(key) {
            if (key) {
                document.querySelector('[data-index="6"] .bird').style.transform = 
                `translate(${window.innerWidth}px, ${-window.innerHeight * 0.7}px)`;
            } else {
                document.querySelector('[data-index="6"] .bird').style.transform = `translateX(-100%)`;
            }
        }
    };

    const stepElems = document.querySelectorAll('.step');
    const graphicElems = document.querySelectorAll('.graphic-item');
    let currentItem = graphicElems[0]; // 현재 활성화되어 visible 클래스가 붙은걸 담을 변수, 0번 인덱스를 담는 이유는 화면에 첫 이미지는 나와야 하니까
    let ioIndex;

/* IntersectionObserver 객체가 말풍선이 사라지거나 나타날 때 그 시점마다 콜백함수가 실행이 됨*/
    const io = new IntersectionObserver((entries, observer) => {
        ioIndex = entries[0].target.dataset.index * 1;
    });

    for (let i = 0; i<stepElems.length; i++) {
        io.observe(stepElems[i]);
        stepElems[i].dataset.index = i;
        graphicElems[i].dataset.index = i;
    }

    function activate(action) {
        currentItem.classList.add('visible');
        if (action) {
            actions[action](true);
        }
    }

    function inactivate(action) {
        currentItem.classList.remove('visible');
        if (action) {
            actions[action](false);
        }
    }


    /* 스크롤로 내릴 때 처리되는거 작업처리, 스크롤할 때 텍스트가 보일때쯤 그에 맞는 그림이 visible로 되게끔 */
    /* visible된 이미지를 스크롤 내릴 때 다시 안보이게 하기 위해
    활성화된 것을 변수에 담아두고 그 변수에 들어있는 것의 visible을 없애고, 그 다음 활성화시킬 애를 visible 되게끔 */
    window.addEventListener('scroll', () => {
        let step;
        let boundingRect;
        /* 현재 인덱스의 앞뒤로 판단하게끔 */
        for (let i = ioIndex - 1; i < ioIndex + 2; i++) {
            step = stepElems[i];
            if (!step) continue;
            boundingRect = step.getBoundingClientRect();

            if (boundingRect.top > window.innerHeight * 0.1 && boundingRect.top < window.innerHeight * 0.8) {
                inactivate(currentItem.dataset.action);
                currentItem = graphicElems[step.dataset.index];
                activate(currentItem.dataset.action);
            }
        }
    });

    window.addEventListener('load', () => {
        setTimeout(() => scrollTo(0,0), 100); 
    }); // 새로고침하면 스크롤 맨처음으로 가게끔

    activate();

})();
