 function pop(url) {
        window.open(url,'PopName',"width=600,height=400,top=100,left=100")
    }

function get_data(pop_post_id,pk,obj) {
    var $option=$('<option>');
    $option.html(obj);
    $option.val(pk);
    $option.attr('selected','selected');
    $('#'+pop_post_id).append($option)
}