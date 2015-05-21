(function(){
    var URL = '/api/v1.0/img/',
        COUNT = 0,
        $more = null;

    var TEMPLATE = function(name, imgsrc, href) {
        return  '<div class="col-xs-6 col-md-3">' +
                    '<div href="#" class="thumbnail">' +
                        '<a href="' + href + '" class="img-wrap">' +
                            '<img src="' + imgsrc + '" title="' + name + '">' +
                        '</a>' +
                        '<div class="caption">' +
                            '<a href="' + href + '">' +
                                '<h3>' + name + '</h3>' +
                            '</a>' +
                        '</div>' +
                    '</div>' +
                '</div>';
    };

    function getList() {
        $more.addClass('spin');
        $.get(URL, function(response) {
            var markup = "";
            COUNT = response.count;
            URL = response.next;
            
            if (URL) {
                $more.attr('disabled', false);
            } else {
                $more.attr('disabled', true);
            }
            
            $.each(response.results, function(idx, img){
                markup += TEMPLATE(img.name, img.public_image, img.url);
            });

            $('#thumbs').append(markup);
            $more.removeClass('spin');
        });
    }

    $(function(){
        $more = $('#more');
        $more.click(getList);
        getList();
    });
})();