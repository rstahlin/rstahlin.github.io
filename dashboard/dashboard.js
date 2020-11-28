$( document ).ready(function() {

    console.log('logging on ready');

    $('#basic-data').on('click', function(){
         // reverse others
         $('.data-pane').hide();
         $('.nav-link').removeClass('active');

        // display basic data
        $('#basic-data-pane').show();
        // make basic data nac active
        $('#basic-data').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('Basic Data');


    });

    $('#neighborhood-data').on('click', function(){
         // reverse others
         $('.data-pane').hide();
         $('.nav-link').removeClass('active');

        // display neighborhood data 
        $('#neighborhood-data-pane').show();
        // make neightborhood nav active
        $('#neighborhood-data').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('Neighborhood Data');
    });

    $('#neighborhood-maps').on('click', function(){
        // reverse others
        $('.data-pane').hide();
        $('.nav-link').removeClass('active');

       // display neighborhood data 
       $('#neighborhood-maps-pane').show();
       // make neightborhood nav active
       $('#neighborhood-maps').addClass('active');
       // set dashboard header
       $('#dashboard-header').text('Neighborhood Maps');
   });

   $('#age-data').on('click', function(){
        // reverse others
        $('.data-pane').hide();
        $('.nav-link').removeClass('active');

        // display neighborhood data 
        $('#age-data-pane').show();
        // make neightborhood nav active
        $('#age-data').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('Age Data');
        // set internal first tab to active
        $('age-data-new-cases-tab').addClass('active');
    });

    $('#ward-data').on('click', function(){
        // ward others
        $('.data-pane').hide();
        $('.nav-link').removeClass('active');

        // display neighborhood data 
        $('#ward-data-pane').show();
        // make neightborhood nav active
        $('#ward-data').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('Ward Data');
    });

    $('#hospitalization-data').on('click', function(){
        // ward others
        $('.data-pane').hide();
        $('.nav-link').removeClass('active');

        // display neighborhood data 
        $('#hospitalization-data-pane').show();
        // make neightborhood nav active
        $('#hospitalization-data').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('Hospitilization Data');
    });

    $('#race-and-ethnicity-data').on('click', function(){
        // ward others
        $('.data-pane').hide();
        $('.nav-link').removeClass('active');

        // display neighborhood data 
        $('#race-and-ethnicity-data-pane').show();
        // make neightborhood nav active
        $('#race-and-ethnicity-data').addClass('active');
        // set dashboard header
        $('#dashboard-header').text('Race and Ethnicity Data');
    });
});