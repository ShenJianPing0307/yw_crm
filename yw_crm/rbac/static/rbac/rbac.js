(function (jq) {
    jq('.multi-menu .title').click(function () {
        $(this).next().toggleClass('hide');
        // $(this).next().removeClass('hide');
        // $(this).parent().siblings().find('.body').addClass('hide');
    });
})(jQuery);