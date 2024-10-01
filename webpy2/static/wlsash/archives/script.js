let path = ["WLSA", "School House", "Soilwater"];

const pathWay = path.map(pathName => ` / <a href="./archives/${pathName}">${pathName}</a>`);
//Array to a tag
document.getElementById("path").innerHTML = pathWay.join('\n');

document.addEventListener('DOMContentLoaded', function () {
    const fileList = document.getElementById('fileList');

    // Sample data representing folders and files
    const data = [
        { type: 'folder', name: 'SEO' },
        { type: 'folder', name: 'SEC' },
        { type: 'folder', name: 'Soilwateroilwateroilwateroilwateroilwateroilwateroilwateroilwateroilwateroilwateroilwateroilwateroilwateroilwateroilwateroilwateroilwateroilwateroilwateroilwateroilwateroilwateroilwater' },
        { type: 'folder', name: 'Ejiao' },
        { type: 'folder', name: 'SEO' },
        { type: 'folder', name: 'SEC' },
        { type: 'folder', name: 'Soilwater' },
        { type: 'folder', name: 'Ejiao' },
        { type: 'file', name: 'thing.pdf' },
        { type: 'file', name: 'thing.jpg' },
        { type: 'file', name: 'thing.mp3' },
        { type: 'file', name: 'thing.pdf' },
        { type: 'file', name: 'thing.jpg' },
        { type: 'file', name: 'thing.mp3' },
        { type: 'file', name: 'thing.pdf' },
        { type: 'file', name: 'thing.jpg' },
        { type: 'file', name: 'thing.mp3' },
    ];

    // Function to render the folders and files
    function renderFileList(data) {
        data.forEach(item => {
            const listItem = document.createElement('li');
            listItem.onclick = function () {
                window.open(`./archives/${item.name}`, '_blank');
            };
            listItem.classList.add(item.type);
            listItem.innerHTML = `<span>${item.name}</span>`;
            fileList.appendChild(listItem);
        });
    }

    // Render the file list on page load
    renderFileList(data);
});
