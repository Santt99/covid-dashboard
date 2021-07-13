// Load google charts
google.charts.load('current', { 'packages': ['corechart'] });
google.charts.setOnLoadCallback(drawChart);

// Draw the chart and set the chart values
function drawChart() {
    console.log(document.getElementById("json-info").value.slice(0, -2) + "}")
    var allData = JSON.parse(document.getElementById("json-info").value.slice(0, -2) + "}")
    document.write(allData["SEXO"])
    console.log(allData)
    console.log("Holaa")
    var ages = allData['EDAD'];
    var sex = allData['SEXO'];
    var region = allData['ENTIDAD_RES'];
    var paciente = allData['TIPO_PACIENTE'];

    ages.unshift(['Age', 'Quantity']);
    sex.unshift(['Category', 'Quantity'])
    region.unshift(['Region', 'Quantity']);
    paciente.unshift(['Category', 'Quantity']);

    var dataAge = google.visualization.arrayToDataTable(ages);
    var dataSex = google.visualization.arrayToDataTable(sex);
    var dataRegion = google.visualization.arrayToDataTable(region);
    var dataPaciente = google.visualization.arrayToDataTable(paciente);

    var optionsAge = { 'title': 'Age', 'width': 550, 'height': 400 };
    var optionsSex = { 'title': 'Sex', 'width': 550, 'height': 400, 'pieHole': 0.4 };
    var optionsRegion = { 'title': 'Region', 'width': 550, 'height': 400 };
    var optionsPaciente = { 'title': 'Pacient Type', 'width': 550, 'height': 400 };
    var chartAge = new google.visualization.ColumnChart(document.getElementById('ages'));
    chartAge.draw(dataAge, optionsAge);
    var chartSex = new google.visualization.PieChart(document.getElementById('sex'));
    chartSex.draw(dataSex, optionsSex);
    var chartRegion = new google.visualization.ColumnChart(document.getElementById('region'));
    chartRegion.draw(dataRegion, optionsRegion);
    var chartPaciente = new google.visualization.ColumnChart(document.getElementById('paciente'));
    chartPaciente.draw(dataPaciente, optionsPaciente);
}

function changeUI() {
    var ages = document.getElementById("agesCheck").value;
    var sex = document.getElementById("sexCheck").value;
    var region = document.getElementById("regionCheck").value;
    var paciente = document.getElementById("pacienteCheck").value;

    if (ages == 'on') {
        document.getElementById("ages").style.display = "";
    } else {
        document.getElementById("ages").style.display = "none";
    }
    if (sex == 'on') {
        document.getElementById("sex").style.display = "";
    } else {
        document.getElementById("sex").style.display = "none";
    }
    if (region == 'on') {
        document.getElementById("region").style.display = "";
    } else {
        document.getElementById("region").style.display = "none";
    }
    if (paciente == 'on') {
        document.getElementById("paciente").style.display = "";
    } else {
        document.getElementById("paciente").style.display = "none";
    }

}
