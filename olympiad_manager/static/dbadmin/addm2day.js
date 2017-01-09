
$(document).ready(function(){
    var dayNum=$('input[name=m2_day_count]').val();
    $("#add_m2_button").click(function () {
        $("#m2days").append('<div>' +
                                '<label for="id_m2_'+dayNum+'_date">تاریخ:</label>'+
                                '<input id="id_m2_'+dayNum+'_date" name="m2_'+dayNum+'_date" type="text"/>' +
                                '<label for="id_m2_'+dayNum+'_darsad">درصد تاثیر:</label>'+
                                '<input id="id_m2_'+dayNum+'_darsad" name="m2_'+dayNum+'_darsad" type="number"/>' +
                            '</div>');
        dayNum++;
        $('input[name=m2_day_count]').val(dayNum);
    })
});
