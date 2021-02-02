$( document ).ready(function() {

    $('#welcome').on('click', function(){
        // reverse others
        $('.data-pane').css('display', 'none');
        $('.nav-link').removeClass('active');

        // display welcome
        $('#home-pane').css('display', 'block');
        // make basic data nav active
        $('#home').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('Charting Coronavirus in D.C.');

        // hide iframe
        $('#display-iframe').hide();

        // set tab note
        var tab_note_html = '';
        $('#tab-note').html(tab_note_html);

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    $('#basic-data').on('click', function(){
        // reverse others
        $('.data-pane').css('display', 'none');
        $('.nav-link').removeClass('active');

        // display basic data
        $('#basic-data-pane').css('display', 'block');
        // make basic data nav active
        $('#basic-data').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('Basic Data');
        // set first tab to active
        $('#basic-cases-tab').addClass('active');
        // display iframe
        $('#display-iframe').show();
        // set iframe
        $('#display-iframe').attr('src', './chart_htmls/cases.html');

        // set tab note
        var tab_note_html = '';
        $('#tab-note').html(tab_note_html);

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display cases graph on tab click
    $('#basic-cases-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/cases.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display deaths graph on tab click
    $('#basic-deaths-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/deaths.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display tests graph on tab click
    $('#basic-tests-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/tests.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });


    $('#neighborhood-data').on('click', function(){
         // reverse others
         $('.data-pane').css('display', 'none');
         $('.nav-link').removeClass('active');

        // display neighborhood data
        $('#neighborhood-data-pane').css('display', 'block');
        // make neightborhood nav active
        $('#neighborhood-data').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('Neighborhood Data');
        // set first tab to active
        $('#neighborhood-data-overview-tab').addClass('active');
        // display iframe
        $('#display-iframe').show();
        // set iframe
        $('#display-iframe').attr('src', './chart_htmls/nhood_diamond_pc.html');

        // set tab note
        var tab_note_html = '';
        $('#tab-note').html(tab_note_html);

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display neighborhood overview graph on tab click
    $('#neighborhood-data-overview-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/nhood_diamond_pc.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display neighborhood total positives graph on tab click
    $('#neighborhood-data-total-positives-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/nhood_cases.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display neighborhood positives per 10k graph on tab click
    $('#neighborhood-data-positives-per-10k-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/nhood_pc.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display neighborhood positivity graph on tab click
    $('#neighborhood-data-positivity-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/nhood_positivity.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });


    $('#neighborhood-maps').on('click', function(){
        // reverse others
        $('.data-pane').css('display', 'none');
        $('.nav-link').removeClass('active');

       // display neighborhood data
       $('#neighborhood-maps-pane').css('display', 'block');
       // make neightborhood nav active
       $('#neighborhood-maps').addClass('active');
       // set dashboard header
       $('#dashboard-header').text('Neighborhood Maps');
       // set first tab to active
       $('#neighborhood-maps-weekly-positives-tab').addClass('active');
       // display iframe
       $('#display-iframe').show();
       // set iframe
       $('#display-iframe').attr('src', './chart_htmls/nhood_map_cases.html');

        // set tab note
        var tab_note_html = '';
        $('#tab-note').html(tab_note_html);

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display neighborhood maps weekly positives graph on tab click
    $('#neighborhood-maps-weekly-positives-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/nhood_map_cases.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display neighborhood map positives per 10k graph on tab click
    $('#neighborhood-maps-positives-10k-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/nhood_map_pc.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display neighborhood positivity graph on tab click
    $('#neighborhood-maps-positivity-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/nhood_map_positivity.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });



   $('#age-data').on('click', function(){
        // reverse others
        $('.data-pane').css('display', 'none');
        $('.nav-link').removeClass('active');

        // display neighborhood data
        $('#age-data-pane').css('display', 'block');
        // make neightborhood nav active
        $('#age-data').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('Age Data');
        // set internal first tab to active
        $('age-data-new-cases-tab').addClass('active');
        // set first tab to active
        $('#age-data-new-cases-tab').addClass('active');
        // display iframe
        $('#display-iframe').show();
        // set iframe
        $('#display-iframe').attr('src', './chart_htmls/ages.html');

        // set tab note
        var tab_note_html = '';
        $('#tab-note').html(tab_note_html);

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display cases by age graph on tab click
    $('#age-data-new-cases-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/ages.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display case breakdown by age graph on tab click
    $('#age-data-case-breakdown-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/ages_cases_pie.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display deaths by age graph on tab click
    $('#age-data-death-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/ages_deaths_pie.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });


    $('#ward-data').on('click', function(){
        // ward others
        $('.data-pane').css('display', 'none');
        $('.nav-link').removeClass('active');

        // display neighborhood data
        $('#ward-data-pane').css('display', 'block');
        // make neightborhood nav active
        $('#ward-data').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('Ward Data');
        // set first tab to active
        $('#ward-data-new-cases-tab').addClass('active');
        // display iframe
        $('#display-iframe').show();
        // set iframe
        $('#display-iframe').attr('src', './chart_htmls/wards.html');

        // set tab note
        var tab_note_html = '';
        $('#tab-note').html(tab_note_html);

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#ward-data-new-cases-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/wards.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#ward-data-new-cases-10k-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/wards_pc.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#ward-data-positivity-tab').click(function(){
        $('#display-iframe').attr('src', '../chart_htmls/wards_positivity.html');

        // set graph text
        var graph_note = 'p style="text-align:center"> <em> Note: District-Wide positivity is based on the "Total Overall Number of Tests" variable released by D.C., and is different than the positivity data referenced in D.C.\'s ReOpening Metrics. </em> </p>'
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#ward-data-case-breakdown-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/wards_breakdown.htm');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#ward-data-tests-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/wards_tests.html');

        // set graph note
        var graph_note = '<p style="text-align:center"> <em> Note: District-Wide tests are based on the "Total Overall Number of Tests" variable released by D.C., and is different than the testing data referenced in D.C.\'s ReOpening Metrics. </em> </p>'
        $('#graph-note').html(graph_note);
    });
        // display graph on tab click
    $('#ward-data-new-cases-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/wards.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#ward-data-new-cases-10k-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/wards_pc.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#ward-data-positivity-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/wards_positivity.html');

        // set graph note
        var graph_note = '<p style="text-align:center"> <em> Note: District-Wide positivity is based on the "Total Overall Number of Tests" variable released by D.C., and is different than the positivity data referenced in D.C.\'s ReOpening Metrics. </em> </p>'
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#ward-data-case-breakdown-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/wards_breakdown.htm');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });


    $('#hospitalization-data').on('click', function(){
        // ward others
        $('.data-pane').css('display', 'none');
        $('.nav-link').removeClass('active');

        // display neighborhood data
        $('#hospitalization-data-pane').css('display', 'block');
        // make neightborhood nav active
        $('#hospitalization-data').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('Hospitilization Data');
        // set first tab to active
        $('#hospitalization-data-patients-tab').addClass('active');
        // display iframe
        $('#display-iframe').show();
        // set iframe
        $('#display-iframe').attr('src', './chart_htmls/patients.html');

        // set tab note
        var tab_note_html = '';
        $('#tab-note').html(tab_note_html);

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#hospitalization-data-patients-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/patients.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#hospitalization-data-hospitalizations-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/patients_hospitalized.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#hospitalization-data-icu-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/patients_icu.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#hospitalization-data-ventilators-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/patients_ventilator.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });


    $('#race-and-ethnicity-data').on('click', function(){
        // ward others
        $('.data-pane').css('display', 'none');
        $('.nav-link').removeClass('active');

        // display neighborhood data
        $('#race-and-ethnicity-data-pane').css('display', 'block');
        // make neightborhood nav active
        $('#race-and-ethnicity-data').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('Race and Ethnicity Data');
        // set first tab to active
        $('#race-and-ethnicity-data-cases-tab').addClass('active');
        // display iframe
        $('#display-iframe').show();
        // set iframe
        $('#display-iframe').attr('src', './chart_htmls/races_cases_pie.html');

        // set tab note
        var tab_note_html = '<div class="d-flex flex-column align-items-center justify-content-center"><p><em> Note: DC releases separate Race and Ethnicity case data, but combines Race and Ethnicity in death data.</em></p></div>';
        $('#tab-note').html(tab_note_html);

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#race-and-ethnicity-data-cases-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/races_cases_pie.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#race-and-ethnicity-data-deaths-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/races_deaths_pie.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    $('#school-data').on('click', function(){
        // ward others
        $('.data-pane').css('display', 'none');
        $('.nav-link').removeClass('active');

        // display neighborhood data
        $('#school-data-pane').css('display', 'block');
        // make neightborhood nav active
        $('#school-data').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('DC Public Schools Data');
        // set first tab to active
        $('#dcps-map-tab').addClass('active');
        // display iframe
        $('#display-iframe').show();
        // set iframe
        $('#display-iframe').attr('src', './chart_htmls/schools_map.html.html');

        // set tab note
        var tab_note_html = '';
        $('#tab-note').html(tab_note_html);

        // set graph note
        var graph_note = '<div class="d-flex flex-column align-items-center justify-content-center"><p><em> Individual School data comes from <a href="https://dcpsreopenstrong.com/category/articles/">DCPS ReOpen Strong</a> and may not reflect the most recent changes.</em></p></div>';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#dcps-cases-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/schools_cases.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#dcps-map-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/schools_map.html');

        // set graph note
        var graph_note = '<div class="d-flex flex-column align-items-center justify-content-center"><p><em> Individual School data comes from <a href="https://dcpsreopenstrong.com/category/articles/">DCPS ReOpen Strong</a> and may not reflect the most recent changes.</em></p></div>';
        $('#graph-note').html(graph_note);
    });

    $('#about').on('click', function(){
        // reverse others
        $('.data-pane').css('display', 'none');
        $('.nav-link').removeClass('active');

        // display about
        $('#about-pane').css('display', 'block');
        // make basic data nav active
        $('#about').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('About');

        // hide iframe
        $('#display-iframe').hide();

        // set tab note
        var tab_note_html = '';
        $('#tab-note').html(tab_note_html);

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

});
