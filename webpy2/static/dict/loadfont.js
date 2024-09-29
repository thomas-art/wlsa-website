document.addEventListener('DOMContentLoaded', function () {
    const fontUrl = '/static/font/FZLanTYK_Zhong.OTF';
    const progressText = document.getElementById('progressText');
    const loadingImage = document.getElementById('loadingAnimation');
    const content = document.getElementById('content');
    const images = [
        document.getElementById('loadingImage1'),
        document.getElementById('loadingImage2'),
        document.getElementById('loadingImage3'),
        document.getElementById('loadingImage4')
    ];

    let imageIndex = 0;
    const interval = setInterval(function () {
        images[imageIndex].style.display = 'none';
        imageIndex = (imageIndex + 1) % images.length;
        images[imageIndex].style.display = 'block';
    }, 500);

    function loadFontWithProgress(fontUrl) {
    fetch(fontUrl).then(response => {
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
                            console.log('font prepared');
                            controller.close();
                            return;
                        }
                        loadedBytes += value.length;
                        const percentComplete = ((loadedBytes / totalBytes) * 100).toFixed(0);
                        progressText.textContent = 'connecting... ' + percentComplete + '%';
                        controller.enqueue(value);
                        push();
                    });
                }
                push();
            }
        });
        return new Response(stream).blob();
    }).then(fontBlob => {
        const fontUrl = URL.createObjectURL(fontBlob); // 创建字体 URL
        const font = new FontFace('FZLanTYK_Zhong', `url(${fontUrl})`); // 使用 URL
        return font.load().then(loadedFont => {
            document.fonts.add(loadedFont);
            URL.revokeObjectURL(fontUrl);
            progressText.textContent = 'connecting... 100%';
            setTimeout(() => {
                loadingImage.style.display = 'none';
                content.removeAttribute('style');
            }, 200);
        });
    }).catch(error => {
        console.error('字体加载失败:', error);
        progressText.textContent = '加载失败，请重试';
    });
}
    loadFontWithProgress(fontUrl);
});

