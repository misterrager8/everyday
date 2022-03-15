function toggleDiv(divId) {
    $('#' + divId).fadeToggle(250);
}

function refreshPage() {
    $('#navContent').load(location.href + ' #navContent');
    $('#pageContent').load(location.href + ' #pageContent');
}

function formatText(cmd, val) {
    document.execCommand(cmd, false, val);
}

function createBook() {
    $('#spinner').show();
    $.post('create_book', {
        name: $('#name').val()
    }, function(data) {
        refreshPage();
    });
}

function editBook(bookId, event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        $('#spinner').show();
        $.post('edit_book', {
            id_: bookId,
            name: $('#name' + bookId).html()
        }, function(data) {
            refreshPage();
        });
    }
}

function deleteBook(bookId) {
    $('#spinner').show();
    $.get('delete_book', {
        id_: bookId
    }, function(data) {
        refreshPage();
    });
}

function editEntry(entryId) {
    $('#spinner').show();
    $.post('edit_entry', {
        id_: entryId,
        content: $('#content').html(),
        book: $('#book').val()
    }, function(data) {
        refreshPage();
    });
}

function deleteEntry(entryId) {
    $('#spinner').show();
    $.get('delete_entry', {
        id_: entryId
    }, function(data) {
        refreshPage();
    });
}