document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('backgroundVideo');
    const soundToggle = document.getElementById('soundToggle');
    const soundIcon = document.getElementById('soundIcon');

    let isPlaying = false;

    soundToggle.addEventListener('mouseenter', function() {
        if (isPlaying) {
            soundIcon.src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACMAAAAjCAYAAAAe2bNZAAAACXBIWXMAAAsTAAALEwEAmpwYAAADD0lEQVRYhb2YzUsVURjGf3cctJKMzLSiKAnS2tgXtctS+1i3a5cQ/QW1011kiyCIdhFurUUtchdUBC0CQ60WmeCqklviTdOrpPa0mDM29zL3nJl71QcOc2fer+e+5z1z3jMZSaRAFdAOdAIngUPAdmAbMAPkgC/AEPASeA2sJPYuKclolNQnaVLpMGnsGpPEcSlUS+qRNJ+SRDHmJfUaf2WROSRpuEISxRiW1JKWTLuk3BoTCZEz/hOR6VDl0+JC3sQpiJ1R4WpqAd6Z1bHemAFOA2PhAy8irAEGNogIJs5jExcAPyK8ARwt0/EM8BOYMiML/DDXw8Be4AjQXGTXBtwEbgGr09QETABbHEEngMFIoCzwFRgH5krY7AIOGDKPYuQLhmQ2LJ7bCQvvSnHRpRhdFr99kvAIpqrbkZEQnlulJDIWWTfge8AZglQmQXUFZGxoAs55BJveRsB3yLt84EQKh7ZUh9gE7AMOAnsIlvA9YNZh1+YDrSnIhO3AcWPXSpDinUCDGeHvKJKQafEJ+pGkWDTX5wT/Oo2Na5rqPaAuBZlwmkq9U+KQtHur83CnLw5/UuhuNlcXqVmfoFVMmp2/CfU+AE8JaucCwRS5in/aBz4D+y1Kn4DfwCmgMQGR68DDyH2G4GVZ77Ab84H3wMUY4XfgKvDC3DfjLsK7RUQgmJ6VBLajYTMlSdORvWJO0m7LPvMxZn9ZkbTDYtPp2PfOe8Abgt03usTvA5OWfxFXjEvYF8OSRZYFXnnAMtBvHubN9a3FEOLPQtXY68JWb/3AcpjCJgV9aYhrjnZgqkSqH1hshkrY5E38goa8xwiXJX2TVFvC6SXH3PcW6ddLGrDo94S6UaMaSSNGYUHSoKQGSVsj45ikXw4ykjQu6YmkZ7IfeUZMXOfpYB6oddROJbCeDjCCywSb23oSWTRxxgqeKr4u2h3prQQ5pThRhqNV0ugaExkxflMf/MOi7lXhsi8HeeNntVjLIRN9D/VJyqYkkZV0x9g74xSvJheqgLNAB/+/XNUTtCCzwDQVfLn6B4IKNbeUtfxwAAAAAElFTkSuQmCC"; // 播放时悬停图像
        } else {
            soundIcon.src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACMAAAAjCAYAAAAe2bNZAAAACXBIWXMAAAsTAAALEwEAmpwYAAADi0lEQVRYhc2YTWgVVxTHfzN5JLGlpkaNtKGKlJiWEj9oaUqhRBITFMRFSwtCKXaTRSmIuy4SFyrGndR0025soQUVSjdCaRf9pDs1sXVhVErE0uRpSEwak1CN/y7uGd+8ybz5yFPpHy7Du/eec/5zz8ec+zxJ5EAN0AF0Aa8Am4BVQAMwDUwBV4BzwA/AT8BiZu2SsowmSQOSxpQPYybXlMVO2oZaSX2S7uQkEcUdSf2mb1lkNkkaqpJEFEOSWvOS6ZA09ZCJBJgy/ZnIdKp6t6RhzuyU2fZUnk0twHfAxjwptkxMA+3ASDDhhxbrgM3Aa8BXj4FMA3Da7AKUncxHwDjwuf3uBT4G6jMongZuARM2isBN4CpwzX6/AxyOke0HjoTJrAP+BJ4APgP2AwvAVuAMzn3YnrNmqGjjLzM6m0K4Dfg9Zn4eFxbFIHiORgJsSFKLrTVI+sbm90aDLsfYkRDQA7JsKii+sk5LetsUeZIOVEmmO4HMuKRCkMpJGJRUZwrXPiIyktTt4z56SfgQ+BlYjwvS5aKQsr6jALycQVE7cAHYBtxI2VsPPAc8DzyLS+HjwEyK3BZP0iiwIQMhgH3AF4AHyOQ+wGXbGhtr7RmGR+VsCjDq4/qRrFiw59dAM3Ad99ZPA28AL8YQCWTS3NToAytzkPHs+RIwBPTgCmU3rqDdj5HJ2r2t9En3ZRz+xbnjW+CQGTwI7GJpkK/ISGqmgGsVs55O9M19XDlvB94FvscF+RFgFOeyHpyLPJIxWQAukxzAl4B/gFeBpgp7enBu2wv8CrwfWvOMdGMKmREfOF9h8W8z0ga8Tqm9qIRmYHfMvHBNeVoAX6xUgWclPZNQTf+IkVmUtDpBpitLBf4F9/UN4wQwlvAWccF4l+RkuJ6wVgR+9IF7wMnI4m8JghB/F6olOS6u4XqaOMIngXvBEa6T60sDvJdw3EiaqHDUnyTIPGnPFpXfOubMfllD3hfaMJygdGeK7/sj+xslnZJ0RdJWm6uX9Knt7wv2hoXqjESAQbnG6qnQ2CbpdgoZSboq6YxcUzYVmp+X1BuyuUel9mTJVaU1o7Fq8aVKbnsw/EggjQBvUvq4PSq8hatf5Yiy0//sRhmMFyRdfMhEhk1vrM20vrVOLjvmlqjNhznT8yBYl0MmXIcGJBVzkihKOmbyqXaid+001ADbgU5K/1w14lqQGWCSKv65+g/qO7BOcUXwSgAAAABJRU5ErkJggg=="; // 静音时悬停图像
        }
    });

    soundToggle.addEventListener('click', function() {
        if (video.muted) {
            isPlaying = true;
            video.muted = false; // 取消静音
        } else {
            isPlaying = false;
            video.muted = true; // 静音
        }

        checkSoundicomouse();
    });
    soundToggle.addEventListener('mouseleave', checkSoundico);

    function checkSoundicomouse(){
        if (isPlaying) {
            soundIcon.src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACMAAAAjCAYAAAAe2bNZAAAACXBIWXMAAAsTAAALEwEAmpwYAAADD0lEQVRYhb2YzUsVURjGf3cctJKMzLSiKAnS2tgXtctS+1i3a5cQ/QW1011kiyCIdhFurUUtchdUBC0CQ60WmeCqklviTdOrpPa0mDM29zL3nJl71QcOc2fer+e+5z1z3jMZSaRAFdAOdAIngUPAdmAbMAPkgC/AEPASeA2sJPYuKclolNQnaVLpMGnsGpPEcSlUS+qRNJ+SRDHmJfUaf2WROSRpuEISxRiW1JKWTLuk3BoTCZEz/hOR6VDl0+JC3sQpiJ1R4WpqAd6Z1bHemAFOA2PhAy8irAEGNogIJs5jExcAPyK8ARwt0/EM8BOYMiML/DDXw8Be4AjQXGTXBtwEbgGr09QETABbHEEngMFIoCzwFRgH5krY7AIOGDKPYuQLhmQ2LJ7bCQvvSnHRpRhdFr99kvAIpqrbkZEQnlulJDIWWTfge8AZglQmQXUFZGxoAs55BJveRsB3yLt84EQKh7ZUh9gE7AMOAnsIlvA9YNZh1+YDrSnIhO3AcWPXSpDinUCDGeHvKJKQafEJ+pGkWDTX5wT/Oo2Na5rqPaAuBZlwmkq9U+KQtHur83CnLw5/UuhuNlcXqVmfoFVMmp2/CfU+AE8JaucCwRS5in/aBz4D+y1Kn4DfwCmgMQGR68DDyH2G4GVZ77Ab84H3wMUY4XfgKvDC3DfjLsK7RUQgmJ6VBLajYTMlSdORvWJO0m7LPvMxZn9ZkbTDYtPp2PfOe8Abgt03usTvA5OWfxFXjEvYF8OSRZYFXnnAMtBvHubN9a3FEOLPQtXY68JWb/3AcpjCJgV9aYhrjnZgqkSqH1hshkrY5E38goa8xwiXJX2TVFvC6SXH3PcW6ddLGrDo94S6UaMaSSNGYUHSoKQGSVsj45ikXw4ykjQu6YmkZ7IfeUZMXOfpYB6oddROJbCeDjCCywSb23oSWTRxxgqeKr4u2h3prQQ5pThRhqNV0ugaExkxflMf/MOi7lXhsi8HeeNntVjLIRN9D/VJyqYkkZV0x9g74xSvJheqgLNAB/+/XNUTtCCzwDQVfLn6B4IKNbeUtfxwAAAAAElFTkSuQmCC"; // 播放时悬停图像
        } else {
            soundIcon.src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACMAAAAjCAYAAAAe2bNZAAAACXBIWXMAAAsTAAALEwEAmpwYAAADi0lEQVRYhc2YTWgVVxTHfzN5JLGlpkaNtKGKlJiWEj9oaUqhRBITFMRFSwtCKXaTRSmIuy4SFyrGndR0025soQUVSjdCaRf9pDs1sXVhVErE0uRpSEwak1CN/y7uGd+8ybz5yFPpHy7Du/eec/5zz8ec+zxJ5EAN0AF0Aa8Am4BVQAMwDUwBV4BzwA/AT8BiZu2SsowmSQOSxpQPYybXlMVO2oZaSX2S7uQkEcUdSf2mb1lkNkkaqpJEFEOSWvOS6ZA09ZCJBJgy/ZnIdKp6t6RhzuyU2fZUnk0twHfAxjwptkxMA+3ASDDhhxbrgM3Aa8BXj4FMA3Da7AKUncxHwDjwuf3uBT4G6jMongZuARM2isBN4CpwzX6/AxyOke0HjoTJrAP+BJ4APgP2AwvAVuAMzn3YnrNmqGjjLzM6m0K4Dfg9Zn4eFxbFIHiORgJsSFKLrTVI+sbm90aDLsfYkRDQA7JsKii+sk5LetsUeZIOVEmmO4HMuKRCkMpJGJRUZwrXPiIyktTt4z56SfgQ+BlYjwvS5aKQsr6jALycQVE7cAHYBtxI2VsPPAc8DzyLS+HjwEyK3BZP0iiwIQMhgH3AF4AHyOQ+wGXbGhtr7RmGR+VsCjDq4/qRrFiw59dAM3Ad99ZPA28AL8YQCWTS3NToAytzkPHs+RIwBPTgCmU3rqDdj5HJ2r2t9En3ZRz+xbnjW+CQGTwI7GJpkK/ISGqmgGsVs55O9M19XDlvB94FvscF+RFgFOeyHpyLPJIxWQAukxzAl4B/gFeBpgp7enBu2wv8CrwfWvOMdGMKmREfOF9h8W8z0ga8Tqm9qIRmYHfMvHBNeVoAX6xUgWclPZNQTf+IkVmUtDpBpitLBf4F9/UN4wQwlvAWccF4l+RkuJ6wVgR+9IF7wMnI4m8JghB/F6olOS6u4XqaOMIngXvBEa6T60sDvJdw3EiaqHDUnyTIPGnPFpXfOubMfllD3hfaMJygdGeK7/sj+xslnZJ0RdJWm6uX9Knt7wv2hoXqjESAQbnG6qnQ2CbpdgoZSboq6YxcUzYVmp+X1BuyuUel9mTJVaU1o7Fq8aVKbnsw/EggjQBvUvq4PSq8hatf5Yiy0//sRhmMFyRdfMhEhk1vrM20vrVOLjvmlqjNhznT8yBYl0MmXIcGJBVzkihKOmbyqXaid+001ADbgU5K/1w14lqQGWCSKv65+g/qO7BOcUXwSgAAAABJRU5ErkJggg=="; // 静音时悬停图像
        }
    }

    function checkSoundico(){
        if (video.muted) {
            soundIcon.src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACcAAAAnCAYAAACMo1E1AAAACXBIWXMAAAsTAAALEwEAmpwYAAAEy0lEQVRYhbXYW4xeUxQH8N98RjXqlqhxzyBTFXpBXKMUqXbq9uIeFV4I0WBIPOEBT0KRoEjwoCFIihDGEHGpS5G0OurWeqAtopegBpkR42Gdk29/Z853m9F/8iXn22fvvf5nr7XX+u/dMTQ0ZByYijNxOo7E4dgDUzCE3/Et1uJdvI0t7RrpaJNcL67F2di5jXEjeA1L8cb/Te4UPIDj2iBUD5/hJnzQrGMzcrviflyNjsK7zzGAj4QLf8YwJmE/4eqTMR+zC2NH8Rhuxl/jIdeNVzAzaRvG03gQg42+qoCZuBFXZORzDOI8fN8OuSPFqhyYtA3geqxvg1QR0/CQWM0cm7L/XxY7V0om6BZBmxMbEcvfO0FisC6b52b8k7UdmNk7uNi5uHK7YiVmZP//xIV4fYKkynAunstsEi4+KbOJsSu3JCEGj+4gYvAqLhOeIeLyvrRDunJz8J6xu/JxEcx/t2BwT+wjkvRU7IsuEWs92f/ncXsypk8sCrGLT5WlmZTcp6p5bADLRW6bjNW4WMQMHCbc0pUZ3BcHZSR2a/IBg5iV/O9Av+om+RQnpOR6Vd03LFy7DkdnXzoNv+EqvIRnhEvGg7dwVqFtGr5QTTMLMJDH3HVJx2WqK7RarOYLwmXLVV0wXoyWtK3L7Oa4nli5vfGTaq2cjTUlEyzGvdgFm0VsjQdvqs1zOWaJqkN4b/8K5iXE1tQhRiTPufhhAsSo5rciUtuTMK8TpyUd+ptMvBLHYpWSpFnA39iA7/CjiNk+Ia3q4Q3VzTK3U23tXNnEIGwV+uxKET8dojY+ImJnS/bbbKyGa0bu4+T5qIrIPzm+boEckV7gAlEbuzPDv+J9fFVCLB9Tz61F+z0VtV/yS4vk8h23FseIvLifCPbbldfsYnIvQ2p/r4qQ1jlaqQIpJgn3LcQdGYE7Rc4sbppctzUiOZw8T+kUmj8nOBl/tECquDL/4i4Rs8tEqliF23CIcPGAcGlZnsuRar0/OsVhJCfXpf5BZAZ2xyfqu39AuPlZUSOfSt6NZh+xrQG5ruT5t4pajXZEyYADMqOD+FDsyAUNDGwSiqOIDuyk8YZI7a+vqJXbJxY6TxEHkrQWHipqYT1UcGuD950N3p2UPK+tCJmUo7fQ+Qbs32CysuDeWeNc1t3gXeqRdytCJeSCb5ZaOXNKg4kINxUxrHFc9QilU/yA1PYw3qqIjJ+q3RuT561NyG0oaRsVO7cehnCRCJej69jtx7Y8JSxNXixSjalG8qhfffIPlxDchkvFbl6d2fgI12TPiwrjGyrhXrEKi3G32ty2HmeIYt4IPRmZEbwjyhuRTx/MiBHC4ICER40SZuwZok/I9B2Jy/GE0IgUzhDpaqwQh5kc9+D8HUxuu9rU8pjkDqWVc+slypPqRNH2ufXPbNDGhOyLwsWtqIpW0JHN92JCbCPOSYmVkSOE4wJRhohlXyJ2Z09J/3YwLZtniao7N2X2xqSlMnLEpcoccVzLMV/otyfUqudWMBNPZvOlh5tBkejHXOIw8fu5N0Wu+sbY+7np4n7uLPXv525RcGU75HLMyUj+XzebfSI7NEQ9txaxAscLxfuyai1uFSPZuIXZPE2J0f6FdY7ibfp0IUTz2/TtwtUTuk3/DxwWSkf1S9ZlAAAAAElFTkSuQmCC"; // 静音图标
        } else {
            soundIcon.src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACcAAAAnCAYAAACMo1E1AAAACXBIWXMAAAsTAAALEwEAmpwYAAAD/ElEQVRYhc2Yz29VRRTHP+/ySghFIApFDAY1rRAQ2BiFUIUYfjySSoiJ8S9wYTBqxYUbN7hxBbpSCRIXhgUrd7SFmEBC+FFDYgkGBcOixPiDEkBQeDX9upiZ9LzLvXPvfW0N3+Tkzb1zZs537pmZd86pSaINLAJeATYDq4BngflAJ3AXuA38DFwETgDfAdcrW5FURRqSvpXUVDU0/bjtVeyVVdwoabgioTwM+/kK7dYUd+tcYD/wJlBL9f0ADAGnvQt/A5rAbOBx7+oNwDZgXdphwJfA+8A/7bh1uaSR1KrvSzooaU0V93j9g368xYi3U8mtqyRdS000KKm7Iqm09Ph5LK55e6XILZc0agY3JfVLqk2RWJCan2/c2BiV9GQRubmSLphBdyXtmCZSaenz8weMePu55L4wyvcl7ZwhYkF2qvVa+tz229PaC5w0p7If+DR2lDOwAFiMu6QXAUuALqAH6PbPR4CPzJh+YJ85xS8Bp4AWcsPA8749BDS8chaeAfq84SVelnkS8woWcAFYa55rwADuygk8XnBU3SdspNzZU+COw2ofxzLm61HrNbNNEoln+5ZZyTfA5YLVTxT0x5DljcvebsBugAR4DNhhOj4rYaDZNrV8WLsN4NEE2AJ0+JcjXmYS/+a8t7ZnA1vqwMtGYaCkgTJx1j1gFPgF+BW4hTuZ8yNjBpk8LJvqwBrTebYkuVn+9zxwycvvwJ+4uO26aVsUkTtj2qvruPsn4FJJcnP876u4r1JlTJ5b0/a7E1pX8kdJQ8GtRXeaRTrkyoK1vzDBhdYB9yoYA7dxyyLEbTGS9hborONi/kBwDnCnhKGkWAVwm/s13N4bwrk0dpjsYu/UcclIINdFfiLyHPAIcI5y7j+Ai6ADhLu8b0TGdJn2rTpwBVjqX6wEfkwNeAL4Gtjqn68S39QAH6SIgXPnrIKxK037SoL7Iw54MaXcCXxviAE8jfuDz0MCfBjpr0f61pv2xQQXJgU0UsrvMPlVs5C1uTuI32Udkb7tpn0iAY4D4/7FWlrDmY2RiWDyMrZoEt9XefvV2m4CxxNgDDhqlN417bECcqMZ7wR8HBnzSc57a3cAuFEUz62LxGVHC2K+vSn9MUlv5OhmxnNWwWb0g5rMtt6WdFPSbSPnJS0oIIdcKvm6pF2SFubo1NSaLp4LfVapV9KEUXqvhPHpkH5jc0KmVBHLvpr6f7Ivm7+2ZF9p5ay8tW+GiFXOW9GDGf+4HpKMP8hDWysJ8pRaXSy54/6V2qsyHVLFKtNU63PHcPW5n3iwPrcCV5/bSn59bg/wd671kivv1fRWNnvL2K26Z6ZaE25UsVfk1jykq+krcIFoqKb/5V09pWr6fxe8qJOuPHXyAAAAAElFTkSuQmCC"; // 开启声音图标，记得替换这个图标URL
        }
    }

    document.getElementById('uploadForm').onsubmit = function(event) {
        event.preventDefault();
        var fileInput = document.getElementById('myfile');
        var submitBtn = document.getElementById('submitBtn');
        var uploadStatus = document.getElementById('uploadStatus');
        var cancelBtn = document.getElementById('cancelBtn');
        var prepare = document.getElementById('preparing');

        var file = fileInput.files[0];
        if (!file) {
            window.location.href = '/disk/error/emptyfile';
            return;
        }

        submitBtn.style.display = 'none';
        cancelBtn.style.display = 'block';
        prepare.style.display = 'block';
        var fileSize = file.size;
        var formData = new FormData();
        formData.append('myfile', file);

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/disk/upload', true);

        xhr.setRequestHeader('X-File-Size', fileSize);

        uploadStatus.style.display = 'block';
        prepare.style.display = 'none';

        xhr.upload.onprogress = function(event) {
            if (event.lengthComputable) {
                var percentComplete = Math.round((event.loaded / event.total) * 100);
                var progressBar = document.getElementById('progressBar');
                progressBar.style.display = 'block';
                progressBar.value = percentComplete;
            }
        };

        xhr.onload = function() {
            document.open();  // 打开文档流
            document.write(xhr.responseText);  // 写入响应内容
            document.close();  // 关闭文档流
        };
        xhr.send(formData);

        document.getElementById('cancelBtn').onclick = function() {
            xhr.abort(); // 取消上传
            uploadStatus.style.display = 'none';
            prepare.style.display = 'none';
            progressBar.style.display = 'none';
            submitBtn.style.display = 'block';
            cancelBtn.style.display = 'none';
            showCustomCursor();
        };
    };

    function submitForm() {
        var filepath = document.getElementById('filepath').value;
        if (filepath) {
            window.location.href = '/disk/getfile/' + encodeURIComponent(filepath);
            return false; // 阻止表单提交，直接跳转
        } else {
            alert("请不要输入空路径");
            return false;
        }
    }
});
