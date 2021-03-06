$( document ).ready(function() {
    // $(function() {
    //     var url = window.location.href;
    //     var page = url.match(/page=([^\?]+)/)[1];
    //     if (page=="reel") { runAccordion(1); }
    // });

    $('#home').on('click', function(){
        // reverse others
        $('.data-pane').css('display', 'none');
        $('.nav-link').removeClass('active');

        // display welcome
        $('#home-pane').css('display', 'block');
        // make basic data nav active
        $('#home').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('Charting Coronavirus in D.C.');

        $('#display-iframe').hide();
        // set iframe
        // $('#display-iframe').attr('src', './chart_htmls/nhood_diamond_pc.html');
        // $('#display-iframe').attr('height', '750');

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
        $('#display-iframe').attr('height', '575');

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

    // display tests graph on tab click
    $('#basic-positivity-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/positivity.html');

        // set graph note
        var graph_note = '<p style="text-align:center"> <em> Note: District-Wide positivity is based on the "Total Overall Number of Tests" variable released by D.C., and is different than the positivity data referenced in D.C.\'s ReOpening Metrics, which is an average of single-day positivity rates and adjusted for date of test. This 7-day positivity rate is a measure of what percent of tests were positive over the last 7-day period. </em> </p>'
        $('#graph-note').html(graph_note);
    });

    // display cumulative graph on tab click
    $('#basic-cumulative-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/herd_immunity.html');

        // set graph note
        var graph_note = 'Scientists generally agree that people who recover from COVID-19 attain at least some degree of immunity that lasts for several months after infection.';
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
        $('#neighborhood-data-total-positives-tab').addClass('active');
        // display iframe
        $('#display-iframe').show();
        // set iframe
        $('#display-iframe').attr('src', './chart_htmls/nhood_cases.html');
        $('#display-iframe').attr('height', '700');

        // set tab note
        var tab_note_html = '<p style="text-align:center">Select a neighborhood in the legend to activate it on the chart</p>';
        $('#tab-note').html(tab_note_html);

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display neighborhood total positives graph on tab click
    $('#neighborhood-data-total-positives-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/nhood_cases.html');
        $('#display-iframe').attr('height', '700');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display neighborhood positives per 10k graph on tab click
    $('#neighborhood-data-positives-per-10k-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/nhood_pc.html');
        $('#display-iframe').attr('height', '700');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display neighborhood positivity graph on tab click
    $('#neighborhood-data-positivity-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/nhood_positivity.html');
        $('#display-iframe').attr('height', '700');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    //display neighborhood tests graph on tab click
    $('#neighborhood-data-tests-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/nhood_tests.html');
        $('#display-iframe').attr('height', '700');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    //display neighborhood tests per 10k graph on tab click
    $('#neighborhood-data-tests-per-10k-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/nhood_tests_pc.html');
        $('#display-iframe').attr('height', '700');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });
    $('#neighborhood-data-vaccinations-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/nhood_vax.html');
        $('#display-iframe').attr('height', '700');

        // set graph note
        var graph_note = '<p style="text-align:center"> <em> Note: District-Wide doses are retroactively corrected for reporting delays, neighborhood data is not.</em> </p>'
        $('#graph-note').html(graph_note);
    });
    $('#neighborhood-data-vaccinations-65-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/nhood_vax_65.html');
        $('#display-iframe').attr('height', '700');

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
       $('#display-iframe').attr('height', '575');

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
        $('#display-iframe').attr('height', '575');

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

    // display cases by age graph on tab click
    $('#age-data-new-cases-census-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/ages_census.html');

        // set graph note
        var graph_note = '<pn style="text-align:center"><em>Because D.C. overwites its per capita age data, this data is a recreation from a crowdsourced archive of downloaded files from the D.C. Box site.<br>Do you have a downloaded copy of <a href="https://dcgov.app.box.com/v/DCHealthStatisticsData">this spreadsheet</a> from before November?<br><a href="mailto:ryan.stahlin@gmail.com">Send me an email!</a></em></p>';
        $('#graph-note').html(graph_note);
    });

    // display cases by age graph on tab click
    $('#age-data-new-cases-census-per-10k-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/ages_census_pc.html');

        // set graph note
        var graph_note = '<p style="text-align:center"><em>Because D.C. overwites its per capita age data, this data is a recreation from a crowdsourced archive of downloaded files from the D.C. Box site.<br>Do you have a downloaded copy of <a href="https://dcgov.app.box.com/v/DCHealthStatisticsData">this spreadsheet</a> from before November?<br><a href="mailto:ryan.stahlin@gmail.com">Send me an email!</a></em></p>';
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
        $('#display-iframe').attr('height', '575');

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
        var graph_note = '<p style="text-align:center"><em>Note: District-Wide positivity is based on the "Total Overall Number of Tests" variable released by D.C., and is different than the positivity data referenced in D.C.\'s ReOpening Metrics.</em></p>'
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    // $('#ward-data-test-breakdown-tab').click(function(){
    //     $('#display-iframe').attr('src', './chart_htmls/wards_tests_breakdown.html');

    //     // set graph note
    //     var graph_note = '<p style="text-align:center"><em>The data on this chart answers the question: "Over the last 7 days, what percent of tests have gone to each Ward?"</em></p>';
    //     $('#graph-note').html(graph_note);
    // });

    // display graph on tab click
    $('#ward-data-vaccinations-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/ward_vax.html');

        // set graph note
        var graph_note = '<p style="text-align:center"> <em> Note: District-Wide doses are retroactively corrected for reporting delays, Ward data is not.<br>Decreases in fully vaccinated rates are due to data corrections.</em> </p>'
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#ward-data-vaccinations-65-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/ward_vax_65.html');

        // set graph note
        var graph_note = '<p style="text-align:center"> <em> Note: Decreases in fully vaccinated rates are due to data corrections.</em> </p>'
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

    // // display graph on tab click
    // $('#ward-data-case-breakdown-tab').click(function(){
    //     $('#display-iframe').attr('src', './chart_htmls/wards_breakdown.html');
    //
    //     // set graph note
    //     var graph_note = '';
    //     $('#graph-note').html(graph_note);
    // });


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
        $('#display-iframe').attr('height', '575');

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
        $('#display-iframe').attr('height', '575');

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
        $('#display-iframe').attr('src', './chart_htmls/schools_map.html');
        $('#display-iframe').attr('height', '575');

        // set tab note
        var tab_note_html = '';
        $('#tab-note').html(tab_note_html);

        // set graph note
        var graph_note = '<div class="d-flex flex-column align-items-center justify-content-center"><p><em> Individual School data comes from <a href="https://dcpsreopenstrong.com/category/articles/">DCPS ReOpen Strong</a> and may not reflect the most recent changes.<br>Total number of students comes from OpenData and may not be up to date.</em></p></div>';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#dcps-cases-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/schools_cases.html');

        // set graph note
        var graph_note = '<div class="d-flex flex-column align-items-center justify-content-center"><p style="text-align:center"><em>DCPS case data is not released on weekends and holidays, so those days are hidden on the chart.</em></p></div>';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#dcps-map-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/schools_map.html');

        // set graph note
        var graph_note = '<div class="d-flex flex-column align-items-center justify-content-center"><p><em> Individual School data comes from <a href="https://dcpsreopenstrong.com/category/articles/">DCPS ReOpen Strong</a> and may not reflect the most recent changes.<br>Total number of students comes from OpenData and may not be up to date.</em></p></div>';
        $('#graph-note').html(graph_note);
    });

    $('#vaccination-data').on('click', function(){
        // ward others
        $('.data-pane').css('display', 'none');
        $('.nav-link').removeClass('active');

        // display neighborhood data
        $('#vaccination-data-pane').css('display', 'block');
        // make neightborhood nav active
        $('#vaccination-data').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('Vaccination Data');
        // set first tab to active
        $('#vaccination-data-daily-vaccinations-tab').addClass('active');
        // display iframe
        $('#display-iframe').show();
        // set iframe
        $('#display-iframe').attr('src', './chart_htmls/daily_vaccinations.html');
        $('#display-iframe').attr('height', '575');

        // set tab note
        var tab_note_html = '<div class="d-flex flex-column align-items-center justify-content-center"><p style="text-align:center">The most recent days\' daily vaccinations are likely an underestimate.</p></div>';
        $('#tab-note').html(tab_note_html);

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#vaccination-data-daily-vaccinations-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/daily_vaccinations.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#vaccination-data-vaccination-supply-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/all_vaccinations.html');

        // set graph note
        var graph_note = '<div class="d-flex flex-column align-items-center justify-content-center"><p style="text-align:center"><em>A large proportion of essential workers in D.C. reside in Virginia or Maryland.</em></p></div>';
        $('#graph-note').html(graph_note);
    });
    // display graph on tab click
    $('#vaccination-data-vaccination-breakdown-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/vaccinations_breakdown.html');

        // set graph note
        var graph_note = '<div class="d-flex flex-column align-items-center justify-content-center"><p style="text-align:center">How to interpret this data: What % of <em>new</em> doses over the last 7 days went to residents vs. non-residents?<br><em>A large proportion of essential workers in D.C. reside in Virginia or Maryland.</em></p></div>';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#vaccination-data-vaccination-breakdown-cumulative-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/vaccinations_breakdown_cumulative.html');

        // set graph note
        var graph_note = '<div class="d-flex flex-column align-items-center justify-content-center"><p style="text-align:center">How to interpret this data: What % of <em>all</em> doses have gone to residents vs. non-residents?<br><em>A large proportion of essential workers in D.C. reside in Virginia or Maryland.</em></p></div>';
        $('#graph-note').html(graph_note);
    });

     // display graph on tab click
    $('#vaccination-data-vaccination-map-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/vaccination_map_cumulative.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#vaccination-data-vaccination-map-65-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/vaccination_map_65_pc.html');

        // set graph note
        var graph_note = '<div class="d-flex flex-column align-items-center justify-content-center"><p style="text-align:center"><em>DC\'s dashboard\'s version of this does not show % of seniors vaccinated by neighborhood, but instead shows % of population who are vaccinated seniors.</em></p></div>';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#vaccination-data-vaccination-map-new-pc-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/vaccination_map_new_pc.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    $('#facility-data').on('click', function(){
        // ward others
        $('.data-pane').css('display', 'none');
        $('.nav-link').removeClass('active');

        // display neighborhood data
        $('#facility-data-pane').css('display', 'block');
        // make neightborhood nav active
        $('#facility-data').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('Nursing Facility and Assisted Living Data');
        // set first tab to active
        $('#facility-data-snf-cases-tab').addClass('active');
        // display iframe
        $('#display-iframe').show();
        // set iframe
        $('#display-iframe').attr('src', './chart_htmls/snf_cases.html');
        $('#display-iframe').attr('height', '575');

        // set tab note
        var tab_note_html = '<div class="d-flex flex-column align-items-center justify-content-center"><p style="text-align:center">Data is released weekly and is self reported by facilities and residences.</p></div>';
        $('#tab-note').html(tab_note_html);
        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#facility-data-snf-cases-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/snf_cases.html');

        // set graph note
        var graph_note = '';
        $('#graph-note').html(graph_note);
    });

    // display graph on tab click
    $('#facility-data-alr-cases-tab').click(function(){
        $('#display-iframe').attr('src', './chart_htmls/alr_cases.html');

        // set graph note
        var graph_note = '';
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
