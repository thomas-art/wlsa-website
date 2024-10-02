let path = [""];

const fileList = document.getElementById('fileList');

function fetchFiles(hash) {
    let strPath = hash.slice(1);   // removes leading #
    if (strPath == "/") strPath = "";
    path = strPath.split("/");
    fetch(`api/files?path=${strPath}&file=0`)
        .then(response => response.json())
        .then(renderFileList);
}

function fetchFile(path) {
    let ext = path.split(".").at(-1);
    let previewExts = {
        images: ["jpg", "jpeg", "png", "webp", "gif"],
        audio: ["mp3", "wav", "flac"],
        video: ["mp4", "mov", "avi"],
        document: ["pdf"],
        text: ["txt", "js", "py", "cpp", "c", "java", "html", "css"]
    }
    let fileType = "other";
    for (let type in previewExts) {
        if (previewExts[type].includes(ext)) {
            fileType = type;
            break;
        }
    }
    fetch(`api/files?path=${path}&file=1`)
    .then(response => response.blob())
    .then(result => {
        if (false /*fileType != "other"*/) {
            // opens the file in a separate page
            let newWindow = window.open("archives/preview", "_blank");
            newWindow.onload = () => newWindow.postMessage([result, fileType], "*");
        } else {
            // downloads the file
            let a = document.createElement("a");
            a.download = path.split("/").at(-1);
            a.href = URL.createObjectURL(result);
            a.click();
            URL.revokeObjectURL(a.href);
        }
    })
}

function joinPath() {
    return path.join("/");
}

// Function to render the folders and files
function renderFileList(data) {
    let pathWay = ["<a href='#/'>WLSA</a>"];
    let traversedPaths = [];
    for (let item of path) {
        traversedPaths.push(item);
        pathWay.push(` / <a href="#${traversedPaths.join('/')}">${decodeURIComponent(item)}</a>`)
    }

    data.sort((a, b) => {
        if (a.type == "folder" && b.type != "folder") return -1;
        else if (b.type == "folder" && a.type != "folder") return 1;
        else return a.name > b.name ? 1 : -1;
    })

    document.getElementById("path").innerHTML = pathWay.join('\n');
    fileList.innerHTML = "";
    data.forEach(item => {
        const listItem = document.createElement('li');
        listItem.onclick = function () {
            switch (item.type) {
                case "file":
                    fetchFile(path.join("/") + "/" + item.name);
                    break;
                case "folder":
                    if (window.location.hash.slice(1) == "/") window.location.hash = item.name;
                    else window.location.hash = path.join("/") + "/" + item.name;
                    break;
                case "link":
                    window.open(item.url, "_blank");
                    break;
                default:
                    alert("Unknown file type: " + item.type);
                    break;
            }
            
        };
        listItem.classList.add(item.type);
        listItem.innerHTML = `<img src="/static/common/images/icons8-${item.type}.svg"><span>${item.name}</span>`;
        fileList.appendChild(listItem);
    });
}

window.addEventListener("hashchange", () => fetchFiles(window.location.hash));

document.addEventListener('DOMContentLoaded', function () {
    if (window.location.hash == "") {
        window.location.hash = "/";
        // fetchFiles in the listener
    } else {
        fetchFiles(window.location.hash);
    }
});
