function renderCSV(text) {
    let arr = text.split("\n");
    for (let line of arr) line.split(",");
    let thead = `<td>${line[0].join('</td><td>')}</td>`;
    arr.shift()
    let tbody = "";
    for (let line of arr) {
        tbody += `<tr><td>${line.join("</td><td>")}</td></tr>`;
    }
    let tableElem = document.createElement("table");
    tableElem.innerHTML = `
    <thead>${thead}</thead>
    <tbody>${tbody}</tbody>
    `
    return tableElem;
}
function renderMd(text) {
    let e = document.createElement("div");
    e.innerHTML = markdown.toHTML(text);
    return e;
}