$( document ).ready(function() {

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
        // set iframe 
        $('#test-iframe').attr('src', './chart_htmls/cases.html');

    });

    // display cases graph on tab click
    $('#basic-cases-tab').click(function(){
        $('#test-iframe').attr('src', './chart_htmls/cases.html');
    });

    // display deaths graph on tab click
    $('#basic-deaths-tab').click(function(){
        $('#test-iframe').attr('src', './chart_htmls/deaths.html');
    });

    // display tests graph on tab click
    $('#basic-tests-tab').click(function(){
        $('#test-iframe').attr('src', './chart_htmls/tests.html');
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
        // set iframe 
        $('#test-iframe').attr('src', './chart_htmls/nhood_diamond_pc.html');

    });

    // display neighborhood overview graph on tab click
    $('#neighborhood-data-overview-tab').click(function(){
        $('#test-iframe').attr('src', './chart_htmls/nhood_diamond_pc.html');
    });

    // display neighborhood total positives graph on tab click
    $('#neighborhood-data-total-positives-tab').click(function(){
        $('#test-iframe').attr('src', './chart_htmls/nhood_cases.html');
    });

    // display neighborhood positives per 10k graph on tab click
    $('#neighborhood-data-positives-per-10k-tab').click(function(){
        $('#test-iframe').attr('src', './chart_htmls/nhood_pc.html');
    });

    // display neighborhood positivity graph on tab click
    $('#neighborhood-data-positivity-tab').click(function(){
        $('#test-iframe').attr('src', './chart_htmls/nhood_positivity.html');
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
    });
});