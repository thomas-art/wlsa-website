let path = [""];

const fileList = document.getElementById('fileList');

function identifyFileType(fileName) {
    // Written by DingTalk AI
    var extension = fileName.substring(fileName.lastIndexOf('.') + 1).toLowerCase();
    switch (extension) {
        case 'jpg':
        case 'jpeg':
        case 'png':
        case 'png':
        case 'gif':
        case 'webp':
        case 'bmp':
        case 'tif':
        case 'tiff':
        case 'svg':
        case 'heic':
            return 'image';
        case 'txt':
        case 'html':
        case 'htm':
        case "css":
        case 'js':
        case 'cpp':
        case 'c':
        case 'h':
        case 'cs':
        case 'py':
        case 'php':
        case 'java':
        case 'json':
        case 'csv':
        case 'md':
        case 'bat':
        case 'cmd':
        case "sh":
        case 'vbs':
        case 'ps1':
        case 'psm1':
        case 'reg':
        case 'm':
        case 'r':
        case 'swift':
        case 'rb':
        case 'go':
        case 'rs':
        case 'lua':
        case 'kt':
        case 'asp':
        case 'aspx':
        case 'jsp':
        case 'bas':
        case 'rtf':
        case 'dbf':
        case 'wri':
        case 'kt':
        case 'prg':
            return 'text';
        case 'mp3':
        case 'wav':
        case 'aac':
        case 'flac':
        case 'aif':
        case 'aiff':
        case 'ape':
        case 'wma':
        case 'm4a':
            return 'audio';
        case 'mp4':
        case 'avi':
        case 'mov':
        case 'wmv':
        case 'm4v':
        case 'mkv':
        case 'flv':
        case '3gp':
        case 'ts':
            return 'video';
        default:
            return 'other';
    }
}

function updatePath() {
    let pathWay = ["<a href='#/'>WLSA</a>"];
    let traversedPaths = [];
    for (let item of path) {
        traversedPaths.push(item);
        pathWay.push(` / <a href="#${traversedPaths.join('/')}">${decodeURIComponent(item)}</a>`)
    }
    document.getElementById("path").innerHTML = pathWay.join('\n');
}

async function fetchFiles(hash) {
    let strPath = hash.slice(1);   // removes leading #
    if (strPath == "/") strPath = "";
    path = strPath.split("/");
    updatePath();

    fileList.innerHTML = "";

    let response = await fetch(`api/files?path=${strPath}`)
    if (response.headers.get("Is-File") == "True") {    // all thanks to Python
        let fileType = identifyFileType(strPath);
        let result = await response.blob();
        renderPreview(result, fileType);
    } else {
        let result = await response.json();
        renderFileList(result);
    }
}

function renderPreview(data, type) {
    let elem;
    switch (type) {
        case "text":
            elem = document.createElement("pre");
            data.text().then(res => elem.innerText = res);
            fileList.append(elem);
            break;
        case "image":
        case "audio":
            elem = new window[type[0].toUpperCase() + type.slice(1)];
            elem.src = URL.createObjectURL(data);
            fileList.append(elem);
            if (type == "audio") elem.controls = true;
            window.addEventListener("hashchange", function f() {
                elem.remove();
                URL.revokeObjectURL(elem.src);
                window.removeEventListener("hashchange", f);
            })
            break;
        case "video":
            elem = document.createElement("video");
            elem.src = URL.createObjectURL(data);
            fileList.append(elem);
            elem.controls = true;
            window.addEventListener("hashchange", function f() {
                elem.remove();
                URL.revokeObjectURL(elem.src);
                window.removeEventListener("hashchange", f);
            })
            break;
        default:
            // download
            let a = document.createElement("a");
            a.download = decodeURIComponent(path.at(-1));
            a.href = URL.createObjectURL(data);
            a.click();
            // moves to the previous folder
            path = path.slice(0, -1);
            window.location.hash = path.join("/");
            URL.revokeObjectURL(a.href);
            break;
    }
}

// Function to render the folders and files
function renderFileList(data) {
    data.sort((a, b) => {
        if (a.type == "folder" && b.type != "folder") return -1;
        else if (b.type == "folder" && a.type != "folder") return 1;
        else return a.name > b.name ? 1 : -1;
    })


    data.forEach(item => {
        const listItem = document.createElement('li');
        listItem.onclick = function () {
            switch (item.type) {
                case "file":
                /*fetchFile(path.join("/") + "/" + item.name);
                break;*/
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
