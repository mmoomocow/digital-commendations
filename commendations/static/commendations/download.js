saveCertAsPNG = function (querySelector = "#cert", filename = "commendation") {
    html2canvas(document.querySelector(querySelector)).then(canvas => {
        var link = document.createElement('a');
        link.download = `${filename}.png`;
        link.href = canvas.toDataURL();
        link.click();
    });
};