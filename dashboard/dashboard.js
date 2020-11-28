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
});