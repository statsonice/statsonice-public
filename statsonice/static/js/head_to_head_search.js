// Set up autocomplete when document is ready
$(setup_autocomplete);

first_last_names = {};

// Update skater name autocomplete
function skater_autocomplete_closure(name){
  do_autocomplete = function(request, response) {
    // Search for skater names matching input
    $.post(
      '/api/skater_name_search/',
      {skatername_query:request.term},
      function(data) {
        view_names = []
        $.each(data, function(i, url_name){
          view_name = url_name[0] + ' ' + url_name[1];
          view_names.push(view_name);
          first_last_names[view_name] = url_name;
        });
        response(view_names); // Display data from API call
        $(name).attr('data-autocomplete_length', data.length);
      },
      'json'
    );
  }
}

// Update skater partner name dropdown
function partner_autocomplete_closure(name, partner){
  partner_autocomplete = function(){
    var query = $(name).val();
    partner.html('<option value="">Select A Skater</option>');
    if($(name).attr('data-autocomplete_length') != 1){
      partner.attr('disabled', true);
      return;
    }else{
      partner.attr('disabled', false);
    }
    // Populate skater partner names if only one skater found
    $.post(
      '/api/skater_team_search/',
      {skatername_query:query},
      function(data) {
        partner.html('<option value="">None</option>');
        $.each(data, function(i, url_name) {
          view_name = url_name[0] + ' ' + url_name[1];
          partner.append('<option value="'+view_name+'">'+view_name+'</option>');
          first_last_names[view_name] = url_name;
        });
      },
      'json'
    );
  }
}

// Set up an autocomplete
function setup_autocomplete(){
  var names = ['#skater_name', '#matching_skater_name']
  $.each(names, function(i, name) {
    var partner = $(name+'_partner');
    skater_autocomplete_closure(name);
    partner_autocomplete_closure(name, partner);
    $(name).autocomplete({
      source: do_autocomplete,
    });
    $(name).focusout(partner_autocomplete);
  });
}


function unknown_skater(){
  $("#search_error").text("Unknown skater name(s)");
  $("#search_error").show();
}
function incomplete_search(){
  $("#search_error").text("You must enter two skater names or two skater teams' names");
  $("#search_error").show();
}
function clear_errors(){
  $("#search_error").hide();
}

function search(){
  // Get data
  skater_name = $('#skater_name').val();
  matching_skater_name = $('#matching_skater_name').val();
  skater_name_partner = $('#skater_name_partner').val();
  matching_skater_name_partner = $('#matching_skater_name_partner').val();

  // Check data
  if(skater_name_partner!='' && matching_skater_name_partner==''){
    incomplete_search();
    return;
  }
  if(skater_name_partner=='' && matching_skater_name_partner!=''){
    incomplete_search();
    return;
  }
  if(skater_name=='' || matching_skater_name==''){
    incomplete_search();
    return;
  }

  // Display head to head
  var team = false;
  if(skater_name_partner!='') team = true;
  skater_name = first_last_names[skater_name].join('/');
  matching_skater_name = first_last_names[matching_skater_name].join('/');
  if(team){
    // team hth
    skater_name_partner = first_last_names[skater_name_partner].join('/');
    matching_skater_name_partner = first_last_names[matching_skater_name_partner].join('/');
    url = '/stats/hth/teams/'+skater_name+'/'+skater_name_partner+'/'+matching_skater_name+'/'+matching_skater_name_partner+'/';
    clear_errors();
    document.location = url;
  }else{
    // single skater hth

    url = '/stats/hth/singles/'+skater_name+'/'+matching_skater_name;
    clear_errors();
    document.location = url;
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

function teams_skater(){
  skaterteam_names = teams_dict[$("#skaterteam_names").val()];
  matching_skaterteam_names = teams_dict[$("#matching_skaterteam_names").val()];
  if($('#skaterteam_names').val() != '' && $("#matching_skaterteam_names").val() != ''){
    url = '/stats/hth/teams/';
    url += skaterteam_names;
    url += '/';
    url += matching_skaterteam_names;
    if(skaterteam_names == undefined || matching_skaterteam_names == undefined){
      unknown_skater();
    }else{
	  clear_errors();
	  document.location = url;
	}
  }else{
    incomplete_search();
  }
}
