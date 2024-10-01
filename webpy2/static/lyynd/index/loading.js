document.addEventListener('DOMContentLoaded', function () {
    const videoUrl = '/static/lyynd/videos/bg.mp4';
    var images = [
        document.getElementById('loadingImage1'),
        document.getElementById('loadingImage2'),
        document.getElementById('loadingImage3'),
        document.getElementById('loadingImage4')
    ];
    var backgroundVideo = document.getElementById('backgroundVideo');
    var progressText = document.getElementById('progressText');
    var loadingImage = document.getElementById('loadingImage');
    var image = '/static/lyynd/images/bg.jpg';
    var imageIndex = 0;
    var interval = setInterval(function () {
        images[imageIndex].style.display = 'none';
        imageIndex = (imageIndex + 1) % images.length;
        images[imageIndex].style.display = 'block';
    }, 500);

    function loadVideoWithProgress(videoElement, videoUrl, progressText) {
        fetch(videoUrl).then(response => {
            const contentLength = response.headers.get('Content-Length');
            if (!contentLength) {
                console.error('no Content-Length');
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
                                console.log('video prepared');
                                controller.close();
                                return;
                            }
                            loadedBytes += value.length;
                            const percentComplete = ((loadedBytes / totalBytes) * 50).toFixed(0);
                            progressText.textContent = 'connecting... ' + percentComplete + '%';
                            controller.enqueue(value);
                            push();
                        });
                    }
                    push();
                }
            });
            return new Response(stream).blob();
        }).then(videoBlob => {
            const videoBlobUrl = URL.createObjectURL(videoBlob);
            videoElement.src = videoBlobUrl;
            videoElement.play();
            loadBackgroundImageWithProgress(progressText, image);
        });
    }
    function loadBackgroundImageWithProgress(progressText, imageUrl) {
    fetch(imageUrl)
        .then(response => {
            const contentLength = response.headers.get('Content-Length');
            if (!contentLength) {
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
                            const percentComplete = 50 + ((loadedBytes / totalBytes) * 50);
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
            const imageBlobUrl = URL.createObjectURL(imageBlob);
            const backgroundImage = document.getElementById('backgroundImage');
            backgroundImage.src = imageBlobUrl;
            function isMobile() {
                return /Mobi|Android/i.test(navigator.userAgent);
            }
            if (isMobile()) {
                document.getElementById('backgroundVideo').style.display = 'none';
                document.getElementById('backgroundImage').style.display = 'block';
            } else {
                document.getElementById('backgroundVideo').play().catch(function (error) {
                    console.log("视频播放失败：", error);
                });
            }
            setTimeout(() => {
                document.getElementById('loadingAnimation').style.display = 'none';
            }, 200);
        });
    }
    loadVideoWithProgress(backgroundVideo, videoUrl, progressText);
});
