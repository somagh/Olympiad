$(document).ready(function(){
    function get_national_code(row){
        return $('input[name=grader_id_'+row+']').val();
    }
    var newGraderNum=0;
    $("#add_grader_button").click(function () {
        $("#newgraders").append('<div class="row">' +
                                '<label for="id_new_code_'+newGraderNum+'" class="col-sm-2">کد ملی:</label>'+
                                '<input id="id_new_code_'+newGraderNum+'" class="col-sm-4 form-control" name="new_code_'+newGraderNum+'" type="text"/>' +
                                '</div>');
        newGraderNum++;
        $('input[name=new_grader_count]').val(newGraderNum);
    });
    $(".delete").click(function()
        {
            var row=$(this).attr('id');
            var national_code=get_national_code(row);
            var url='/olympiad/'+$('input[name=fname]').val()+'/'+$('input[name=year]').val()+'/problem/'+$('input[name=eid]').val()+'/'+$('input[name=pnum]').val()+'/graders/delete/';
            $.ajax({
                    url: url,
                    method: 'POST',
                    data: {
                        national_code:national_code,
                        eid:$('input[name=eid]').val(),
                        pnum:$('input[name=pnum]').val()
                    },
                    success:function(data, status, xhttp) {
                        $('#grader_'+row).hide('slow');
                    }
                }
            );
        }
    );
});
