let path = [""];

const fileList = document.getElementById('fileList');

function fetchFiles(hash) {
    let strPath = hash.slice(1);   // removes leading #
    if (strPath == "/") strPath = "";
    path = strPath.split("/");
    fetch(`api/files?path=${strPath}`)
        .then(response => response.json())
        .then(renderFileList);
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

    document.getElementById("path").innerHTML = pathWay.join('\n');
    fileList.innerHTML = "";
    data.forEach(item => {
        const listItem = document.createElement('li');
        listItem.onclick = function () {
            switch (item.type) {
                case "file":
                    // opens the file or download it
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
