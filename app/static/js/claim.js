$(document).ready(function(){
    // Counter to track service row index
    let serviceIndex = 0;
    function computeCosts() {
        var totalCost = 0;

        // Iterate through all service cost inputs
        $('.cost-of-service').each(function() {
            var cost = parseFloat($(this).val()) || 0;
            totalCost += cost;
        });
        var serviceResult = (10 / 100) * totalCost
        var finalCost = totalCost + serviceResult

        // Update total cost display
        $('#total-cost').val(parseInt(totalCost));
        $('#service-charge').val(parseInt(serviceResult));
        $('#final-cost').val(parseInt(finalCost));
    }
    computeCosts()

    $('#user-claim').change(function(){
        let userId = $(this).val();

        $.ajax({
            url: `/users/${userId}/details`,
            method: 'GET',
            success: function(response) {
                // set age value
                $('#user-age').val(response.age);
                $('#user-gender').val(response.gender);
                // set gender value
                $(`input[name="gender"][value="${response.gender}"]`).prop('checked', true);
            },
            error: function(error) {
                console.error("Error fetching user details: ", error);
            }
        });
    });

    $('#add-service').click(function() {
        // Increment service index
        serviceIndex++;
         // Clone the first service row
        var newServiceRow = $('.service-row:first').clone();

        // Clear input values
        newServiceRow.find('input, select').each(function() {
            var el = $(this)
            if (!['radio', 'hidden'].includes(el.attr('type'))) {
                el.val('')
            };
            let inputName = el.attr('name');
            if (inputName) {
                // Replace the index in the name attribute
                let newName = inputName.replace(/services-\d+/, `services-${serviceIndex}`);
                $(this).attr('name', newName);
                $(this).attr('id', newName);
            }
        });
         // Clear radio buttons
        newServiceRow.find('input[type="radio"]').each(function() {
            $(this).prop('checked', false)
            let inputName = $(this).attr('name');
            if (inputName) {
                // Replace the index in the name attribute
                let newName = inputName.replace(/services-\d+/, `services-${serviceIndex}`);
                $(this).attr('name', newName);
                $(this).attr('id', newName);
            }
        });
        newServiceRow.prepend(`
            <div class="row">
                <div class="form-group pull-right">
                    <button type="button" class="btn btn-link btn-remove-service">Remove</button>
                </div>
            </div>
        `);
        // Append to services container
        $('#servicesContainer').append(newServiceRow);
    })

    // Total cost calculation on any service cost input change
    $(document).on('keyup', '.cost-of-service', function() {
        computeCosts()
    });

    $(document).on('click', '.btn-remove-service', function() {
        // Prevent removal if only one service row exists
        if ($('.service-row').length > 1) {
            $(this).closest('.service-row').remove();
            computeCosts()
        }
    });
})