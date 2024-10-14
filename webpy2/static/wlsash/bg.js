let totalBgs = 5;
function selectRandomBg() {
    let bgId = Math.ceil(Math.random() * totalBgs);
    let bgLink = `/static/wlsash/images/bg-${bgId}.jpg`;
    return bgLink;
}
console.log(selectRandomBg());