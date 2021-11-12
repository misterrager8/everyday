$(document).ready(function() {
    $('.grid').masonry({ itemSelector : '.card', transitionDuration : 0 });
});

function refreshDiv(divId) {
    $('#' + divId).load(
        location.href + ' #' + divId,
        function() {
            $('.grid').masonry({ itemSelector : '.card', transitionDuration : 0 });
        }
    );
}

function entryCreate() {
    $.post(
        'entry_create',
        { content : $('#content').val() },
        function(data) {
            refreshDiv('allEntries');
            $('#content').val('');
        }
    );
}

function entryUpdate(entryId) {
    $.post(
        'entry_update',
        { content : $('#contentUpdate' + entryId).val(), id_ : entryId },
        function(data) {
            refreshDiv('allEntries');
        }
    );
}

function entryDelete(entryId) {
    $.get(
        'entry_delete',
        { id_ : entryId },
        function(data) {
            refreshDiv('allEntries');
        }
    );
}