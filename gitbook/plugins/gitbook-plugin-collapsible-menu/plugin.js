require(["gitbook"], function(gitbook) {
    gitbook.events.bind("page.change", function() {
        $('ul.summary li li').hide();
        $('ul.summary li li.active').parents().children().show();
        $('ul.summary li.active > ul > li').slideDown('slow');
    });
});
