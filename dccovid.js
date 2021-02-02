$( document ).ready(function() {
    $('#new-cases-toggle').click(function(){
        $('#iframe-test').attr('src', './chart_htmls/cases.html');
    });

    $('#new-tests-toggle').click(function(){
        $('#iframe-test').attr('src', './chart_htmls/tests.html');
    });
});