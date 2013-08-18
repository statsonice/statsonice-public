$(function() {
    $("#skater_name").keyup(function(){lock_pairs()});
    $("#matching_skater_name").keyup(function(){lock_pairs()});
    $("#skaterpair_names").keyup(function(){lock_singles()});
    $("#matching_skaterpair_names").keyup(function(){lock_singles()});

});
function lock_pairs(){
    $("#skaterpair_names").attr('disabled', true);
    $("#matching_skaterpair_names").attr('disabled', true);
}
function lock_singles(){
    $("#skater_name").attr('disabled', true);
    $("#matching_skater_name").attr('disabled', true);
}
function unknown_skater(){
    $("#search_error").text("Unknown skater name(s)");
    $("#search_error").show();
}
function incomplete_search(){
    $("#search_error").text("You must enter two skater names or two skater pairs' names");
    $("#search_error").show();
}
function clear_errors(){
    $("#search_error").hide();
}

function search(){
    skater_name = skaters_dict[$('#skater_name').val()];
    matching_skater_name = skaters_dict[$('#matching_skater_name').val()];
    skaterpair_names = pairs_dict[$('#skaterpair_names').val()];
    matching_skaterpair_names = pairs_dict[$('#matching_skaterpair_names').val()];
    if($('#skater_name').val() != '' && $('#matching_skater_name').val() != ''){
        url = '/stats/hth/singles/';
        url += skater_name;
        url += '/';
        url += matching_skater_name;
        if(skater_name == undefined || matching_skater_name == undefined){
            unknown_skater();
        }else{
            clear_errors();
            document.location = url;
        }
    }else if($('#skaterpair_names').val() != '' && $('#matching_skaterpair_names').val() != ''){
        url = '/stats/hth/teams/';
        url += skaterpair_names;
        url += '/';
        url += matching_skaterpair_names;
        if(skaterpair_name == undefined || matching_skaterpair_name == undefined){
            unknown_skater();
        }else{
            clear_errors();
            document.location = url;
        }
    }else{
        incomplete_search();
    }
}

function single_skater(){
    skater_name = skaters_dict[$("#skater_name").val()];
    matching_skater_name = skaters_dict[$("#matching_skater_name").val()];
    if($("#skater_name").val() != '' && $("#matching_skater_name").val() != ''){
        url = '/stats/hth/singles/';
        url += skater_name;
        url += '/';
        url += matching_skater_name;
        if(skater_name == undefined || matching_skater_name == undefined){
            unknown_skater();
        }else{
            clear_errors();
            document.location = url;
        }
    }else{
        incomplete_search();
    }
}

function pairs_skater(){
    skaterpair_names = pairs_dict[$("#skaterpair_names").val()];
    matching_skaterpair_names = pairs_dict[$("#matching_skaterpair_names").val()];
    if($('#skaterpair_names').val() != '' && $("#matching_skaterpair_names").val() != ''){
        url = '/stats/hth/teams/';
        url += skaterpair_names;
        url += '/';
        url += matching_skaterpair_names;
        console.log(skaterpair_names);
        console.log(matching_skaterpair_names);
        if(skaterpair_names == undefined || matching_skaterpair_names == undefined){
            unknown_skater();
        }else{
	    clear_errors();
	    document.location = url;
	}
    }else{
        incomplete_search();
    }
}
