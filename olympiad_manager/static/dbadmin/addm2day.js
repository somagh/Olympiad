
$(document).ready(function(){
    var dayNum=$('input[name=m2_day_count]').val();
    $("#add_m2_button").click(function () {
        $("#m2days").append('<div class="row">' +
                                '<label for="id_m2_'+dayNum+'_date" class="col-sm-1">تاریخ:</label>'+
                                '<input id="id_m2_'+dayNum+'_date" class="col-sm-3 form-control" name="m2_'+dayNum+'_date" type="text"/>' +
                                '<label for="id_m2_'+dayNum+'_darsad" class="col-sm-2">درصد تاثیر:</label>'+
                                '<input id="id_m2_'+dayNum+'_darsad" class="col-sm-3 form-control" name="m2_'+dayNum+'_darsad" type="number"/>' +
                            '</div>');
        dayNum++;
        $('input[name=m2_day_count]').val(dayNum);
    })
});
