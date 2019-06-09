        function readysubmit() {

            $('select[selected_data] option').prop('selected', true);
        }

        function MoveElement(ths, target_id) {
            var $target_from_id = $(ths).parent().attr('id');
            var op = $('<option></option>');
            op.attr('ondblclick', 'MoveElement(this,"' + $target_from_id + '")');
            op[0].value = $(ths).val();
            op[0].text = $(ths).text();
            $('#' + target_id).append(op);
            $(ths).remove()
        }

        function MoveAllElements(from_id, target_id) {
            $('#' + from_id).children().each(function () {
                MoveElement($(this), target_id)
            })
        }

        function M2mSearch(ths) {
            var $searchText = $(ths).val().toUpperCase();
            $(ths).next().children().each(function () {
                var $matchText = $(this).text().toUpperCase().search($searchText);
                if ($matchText != -1) {
                    $(this).show()
                } else {
                    $(this).hide()
                }
            })


        }