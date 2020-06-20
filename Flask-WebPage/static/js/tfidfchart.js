var tfIDFchart
am4core.ready(function() {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    tfIDFchart = am4core.create("chartdiv", am4charts.XYChart);
    tfIDFchart.padding(40, 40, 40, 40);

    var categoryAxis = tfIDFchart.yAxes.push(new am4charts.CategoryAxis());
    categoryAxis.renderer.grid.template.location = 0;
    categoryAxis.dataFields.category = "word";
    categoryAxis.renderer.minGridDistance = 1;
    categoryAxis.renderer.inversed = true;
    categoryAxis.renderer.grid.template.disabled = true;

    var valueAxis = tfIDFchart.xAxes.push(new am4charts.ValueAxis());
    valueAxis.min = 0;

    var series = tfIDFchart.series.push(new am4charts.ColumnSeries());
    series.dataFields.categoryY = "word";
    series.dataFields.valueX = "tfidf";
    series.tooltipText = "{valueX.value}"
    series.columns.template.strokeOpacity = 0;
    series.columns.template.column.cornerRadiusBottomRight = 5;
    series.columns.template.column.cornerRadiusTopRight = 5;

    var labelBullet = series.bullets.push(new am4charts.LabelBullet())
    labelBullet.label.horizontalCenter = "left";
    labelBullet.label.dx = 10;
    labelBullet.label.text = "{values.valueX.workingValue}";
    labelBullet.locationX = 1;

    // as by default columns of the same series are of the same color, we add adapter which takes colors from chart.colors color set
    series.columns.template.adapter.add("fill", function(fill, target){
    return tfIDFchart.colors.getIndex(target.dataItem.index);
});

categoryAxis.sortBySeries = series;




}); // end am4core.ready()