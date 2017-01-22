$(document).ready(function() {
    function get_fname(row) {
        return $('input[name=fname_' + row + ']').val();
    }
    function get_year(row) {
        return $('input[name=year_' + row + ']').val();
    }
    $(".register").click(function()
    {
        var row=$(this).attr('id');
        $('input[name=year]').val(get_year(row));
        $('input[name=fname]').val(get_fname(row));
        $('#form').submit();
    });
});