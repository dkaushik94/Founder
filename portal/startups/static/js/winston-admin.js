/*function showMatchData() {
    if($('th[match]:visible, td[match]:visible').length != 0) return;
    $('th[setting], td[setting]').stop(true,true).hide();
    $('th[match], td[match]').stop(true,true).show();
}

function showSettingData() {
    if($('th[setting]:visible, td[setting]:visible').length != 0) return;
    $('th[match], td[match]').stop(true,true).hide();
    $('th[setting], td[setting]').stop(true,true).show();
}*/

function showUserDetails(btn) {
    var pane = $(btn).parent().parent().next();
    if ('none' == pane.css('display')) {
        pane.stop(true,true).fadeIn(800, 'swing');
    } else {
        pane.stop(true,true).fadeOut(400, 'swing');
    }
}

function deleteUser(id) {
    $.post('/ui/admin/delete-user', { id : id }, function(data) {
        console.log(data)
    })
}

function searchUsers() {
    keywords = $('input[type=text][name=keywords]').val();
    filter = $('select[name=filter]').val();

    href = window.location.href;

    var send_params = [ ];

    if (href.match(/\?/)) {
        params = href.replace(/^.*\?/, '').split('&');
        href = href.replace(/\?.*$/, '');
        for(var i = 0; i < params.length; ++i) {
            param = params[i];
            if(! param.match(/^filter/) && ! param.match(/^page_no/)) {
                send_params.push(param);
            }
        }
    }

    if('' != keywords) {
        send_params.push('filter=' + filter + ':' + keywords);
    }

    if(send_params.length) {
        window.location.assign(href + '?' + send_params.join('&'));
    } else {
        window.location.assign(href);
    }
}

function sortUsers() {
    sort_by = $('select[name=sort]').val();

    href = window.location.href;

    var send_params = [ ];

    if (href.match(/\?/)) {
        params = href.replace(/^.*\?/, '').split('&');
        href = href.replace(/\?.*$/, '');
        for(var i = 0; i < params.length; ++i) {
            param = params[i];
            if(! param.match(/^sort/) && ! param.match(/^page_no/)) {
                send_params.push(param);
            }
        }
    }

    send_params.push('sort=' + sort_by);

    if(send_params.length) {
        window.location.assign(href + '?' + send_params.join('&'));
    } else {
        window.location.assign(href);
    }
}
