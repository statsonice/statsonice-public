var searchIds = [];
$(function() {
    $.each(
        $('.form-horizontal .control-label,.other-inputs'),
        function(index, element){
            input_id = "#"+$(element).attr('for');
            searchIds.push(input_id);
        }
    );
    search();
});

function search() {
    spinnerOn();
    var searchHash = {};
    $.each(
        searchIds,
        function(index, input_id){
            input_id = input_id.substr(1, input_id.length)
            searchHash[input_id] = $("#"+input_id).val();
        }
    );
    searchString = JSON.stringify(searchHash);
    // if($("#search_timer").data('old_search') == searchString){ spinnerOff(); return;}
    $("#search_timer").data("old_search", searchString);
    $.ajax({
        type: "POST",
        url: search_url,
        data: searchHash,
        complete: function(e, xhr, settings){
            if(e.status === 200){
                $("#search_results").html(e.responseText);
            } else {
                $("#search_results").html('<p class="center"><i>An error has occurred</i></p>');
            }
            spinnerOff();
        }
    });
}

function range_toggle(div_id){
    $("#"+div_id+"_toggle").hide();
    $("#"+div_id).show('blind', 'slow');
}
