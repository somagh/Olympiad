var dayNum=0;
$(document).ready(function(){
    $("#add_m2_button").click(function () {
        $("#m2days").append('<div>' +
                                '<label for="m2_new_'+dayNum+'_date">تاریخ:</label>'+
                                '<input name="m2_new_'+dayNum+'_date" type="text"/>' +
                                '<label for="m2_new_'+dayNum+'_darsad">درصد تاثیر:</label>'+
                                '<input name="m2_new_'+dayNum+'_darsad" type="number"/>' +
                            '</div>');
        dayNum++;
    })
});
