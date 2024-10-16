document.addEventListener('DOMContentLoaded', function () {
    var images = [
        document.getElementById('loadingImage1'),
        document.getElementById('loadingImage2'),
        document.getElementById('loadingImage3'),
        document.getElementById('loadingImage4')
    ];
    var progressText = document.getElementById('progressText');
    var loadingImage = document.getElementById('loadingImage');
    var image = selectRandomBg();
    var imageIndex = 0;
    var interval = setInterval(function () {
        images[imageIndex].style.display = 'none';
        imageIndex = (imageIndex + 1) % images.length;
        images[imageIndex].style.display = 'block';
    }, 500);

    function loadImageWithProgress(progressText, imageUrl) {
    fetch(imageUrl)
        .then(response => {
            const contentLength = response.headers.get('content-length');
            if (!contentLength) {
                progressText.textContent = 'connection failed';
                console.error('No Content-Length header');
                return;
            }
            const totalBytes = parseInt(contentLength, 10);
            let loadedBytes = 0;
            const reader = response.body.getReader();
            const stream = new ReadableStream({
                start(controller) {
                    function push() {
                        reader.read().then(({ done, value }) => {
                            if (done) {
                                controller.close();
                                return;
                            }
                            loadedBytes += value.length;
                            const percentComplete = (loadedBytes / totalBytes) * 100;
                            progressText.textContent = 'connecting... ' + percentComplete.toFixed(0) + '%';
                            controller.enqueue(value);
                            push();
                        });
                    }
                    push();
                }
            });
            return new Response(stream).blob();
        })
        .then(imageBlob => {
            let imageBlobUrl;
            try {
                imageBlobUrl = URL.createObjectURL(imageBlob);
            } catch (e) {
                console.error(e);
                imageBlobUrl = imageUrl;
            }
            const backgroundImage = document.getElementById('mainview');
            backgroundImage.src = imageBlobUrl;

            const mainBgImages = document.querySelectorAll('.mainbg');
            mainBgImages.forEach(img => {
                img.src = imageBlobUrl;
            });
            function isMobile() {
                return /Mobi|Android/i.test(navigator.userAgent);
            }
            if (isMobile()) {
                document.getElementById('customCursor').style.display = 'none';
                document.getElementById('catchIcon').style.display = 'none';
            }
            setTimeout(() => {
                clearInterval(interval);
                document.getElementById('loadingAnimation').remove();

                const animg = document.querySelectorAll('.ani');
                const mainbg = document.getElementById('mainview');

                mainbg.classList.remove('gradient-mv'); // 移除类以重置动画
                void mainbg.offsetWidth; // 强制重绘以重新触发动画
                mainbg.classList.add('gradient-mv'); // 重新添加类以触发动画

                animg.forEach(element => {
                    element.classList.remove('slide-in'); // 移除类以重置动画
                    void element.offsetWidth; // 强制重绘以重新触发动画
                    element.classList.add('slide-in'); // 重新添加类以触发动画
                });
            }, 200);
        });
    }
    loadImageWithProgress(progressText, image);
});
