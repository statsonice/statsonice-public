// Set up autocomplete when document is ready
$(setup_autocomplete);

// Cache view_name -> url_name list
first_last_names = {};


// Set up an autocomplete
function setup_autocomplete(){
  var hth_type = $("#hth_type").val();
  if(hth_type == "full"){
    var names = ['#skater_name', '#matching_skater_name'];
  } else if(hth_type == "skater" || hth_type == "team"){
    var names = ['#matching_skater_name'];
  } else {
    return;
  }

  $.each(names, function(i, name) {
    var name = $(name);
    skater_autocomplete_closure(name);
    name.autocomplete({
      source: do_autocomplete,
      select: partner_autocomplete_event,
    });
  });
}

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
        partner_autocomplete(name, data.length);
      },
      'json'
    );
  }
}

function partner_autocomplete_event(event, ui){
  $(event.target).val(ui.item.value);
  partner_autocomplete($(event.target), 1);
}

// Update skater partner name dropdown
function partner_autocomplete(name, autocomplete_options){
  var partner = $('#'+name.attr('id')+'_partner');
  if(autocomplete_options != 1){
    partner.html('<option value="">Select A Skater</option>');
    partner.attr('disabled', true);
    return;
  }else{
    partner.attr('disabled', false);
  }
  // Populate skater partner names if only one skater found
  $.post(
    '/api/skater_team_search/',
    {skatername_query:name.val()},
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

// Feedback messages
function unknown_skater(){
  $("#search_error").text("Unknown skater name(s)");
  $("#search_error").show();
}
function incomplete_search(){
  $("#search_error").text("You must enter two skater names or two skater teams' names");
  $("#search_error").show();
}
function clear_errors(){
  $("#search_error").text("");
  $("#search_error").hide();
}

// Search for hth from the hth page
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
  clear_errors();

  // Display head to head
  var team = false;
  if(skater_name_partner!='') team = true;
  skater_name = first_last_names[skater_name].join('/');
  matching_skater_name = first_last_names[matching_skater_name].join('/');
  if(skater_name == undefined || matching_skater_name == undefined){
    unknown_skater();
    return;
  }
  if(team){
    // team hth
    skater_name_partner = first_last_names[skater_name_partner].join('/');
    matching_skater_name_partner = first_last_names[matching_skater_name_partner].join('/');
    if(skater_name_partner == undefined || matching_skater_name_partner == undefined){
      unknown_skater();
      return;
    }
    url = '/stats/hth/teams/'+skater_name+'/'+skater_name_partner+'/'+matching_skater_name+'/'+matching_skater_name_partner+'/';
    document.location = url;
  }else{
    // single skater hth
    url = '/stats/hth/singles/'+skater_name+'/'+matching_skater_name;
    document.location = url;
  }
}

// search for hth from the skater page
function skater_hth(){
  skater_name = JSON.parse($("#skater_name").val());
  skater_name = skater_name.join('/');
  matching_skater_name = $("#matching_skater_name").val();
  matching_skater_name = first_last_names[matching_skater_name].join('/');
  if(skater_name == undefined || matching_skater_name == undefined){
    unknown_skater();
    return;
  }
  url = '/stats/hth/singles/'+skater_name+'/'+matching_skater_name+'/';
  document.location = url;
}

// search for hth from the skaterteam page
function teams_hth(){
  skaterteam_names = JSON.parse($("#skaterteam_names").val());
  skaterteam_names = skaterteam_names.join('/');
  matching_skaterteam_name = $("#matching_skater_name").val();
  matching_skaterteam_name = first_last_names[matching_skaterteam_name].join('/');
  matching_skaterteam_name_partner = $("#matching_skater_name_partner").val();
  matching_skaterteam_name_partner = first_last_names[matching_skaterteam_name_partner].join('/');
  if(skaterteam_names == undefined || matching_skaterteam_name == undefined || matching_skaterteam_name_partner == undefined){
    unknown_skater();
    return;
  }
  matching_skaterteam_names = matching_skaterteam_name + '/' + matching_skaterteam_name_partner;
  url = '/stats/hth/teams/'+skaterteam_names+'/'+matching_skaterteam_names+'/';
  document.location = url;
}
