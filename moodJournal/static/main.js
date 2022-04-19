function refreshPage() {
    $('#pageContent').load(location.href + ' #pageContent');
}

function toggleDiv(divId) {
    $('#' + divId).toggle(150);
}

function entryAdd() {
    $('#spinner').show();
    $.post('entry_add', {
        content: $('#content').html(),
        mood: $('#mood').val()
    }, function(data) {
        refreshPage();
    });
}

function entryEdit(entryId) {
    $('#spinner').show();
    $.post('entry_edit', {
        id_: entryId,
        content: $('#content').val(),
        mood: $('#mood').val()
    }, function(data) {
        refreshPage();
    });
}

function entryDelete(entryId) {
    $('#spinner').show();
    $.get('entry_delete', {
        id_: entryId
    }, function(data) {
        refreshPage();
    });
}